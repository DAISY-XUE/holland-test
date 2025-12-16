import argparse
import io
import os
import sys
from typing import Optional, List, Tuple, Dict
import requests
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline
from flask import Flask, request, send_from_directory
import base64
import glob
import uuid


def _is_url(s: str) -> bool:
    return s.startswith("http://") or s.startswith("https://")


def _load_image(src: str) -> Image.Image:
    if _is_url(src):
        r = requests.get(src, timeout=20)
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    return Image.open(src).convert("RGB")


_CAPTION_PIPE = None
_ZH_PIPE = None


def _get_caption_pipe():
    global _CAPTION_PIPE
    if _CAPTION_PIPE is None:
        _CAPTION_PIPE = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
    return _CAPTION_PIPE


def _get_zh_pipe():
    global _ZH_PIPE
    if _ZH_PIPE is None:
        _ZH_PIPE = pipeline("translation_en_to_zh", model="Helsinki-NLP/opus-mt-en-zh")
    return _ZH_PIPE


def generate_caption(src: str, zh: bool = False) -> str:
    img = _load_image(src)
    cap_pipe = _get_caption_pipe()
    result = cap_pipe(img)
    text = result[0]["generated_text"]
    if zh:
        zh_pipe = _get_zh_pipe()
        zh_res = zh_pipe(text)
        return zh_res[0]["translation_text"]
    return text


def generate_caption_image(img: Image.Image, zh: bool = False) -> str:
    cap_pipe = _get_caption_pipe()
    result = cap_pipe(img)
    text = result[0]["generated_text"]
    if zh:
        zh_pipe = _get_zh_pipe()
        zh_res = zh_pipe(text)
        return zh_res[0]["translation_text"]
    return text


def _font_from_path(path: Optional[str], size: int) -> ImageFont.ImageFont:
    if path and os.path.isfile(path):
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


def _overlay_caption(img: Image.Image, text: str, font_path: Optional[str] = None) -> Image.Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    font = _font_from_path(font_path, max(16, int(h * 0.03)))
    padding = max(10, int(h * 0.02))
    text_w, text_h = draw.textbbox((0, 0), text, font=font)[2:4]
    box_h = text_h + padding * 2
    box_w = min(w, text_w + padding * 2)
    box_y0 = h - box_h - padding
    box_y1 = h - padding
    box_x0 = padding
    box_x1 = box_x0 + box_w
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([(box_x0, box_y0), (box_x1, box_y1)], fill=(0, 0, 0, 160))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    text_x = box_x0 + padding
    text_y = box_y0 + padding
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)
    return img.convert("RGB")


def _gather_images(directory: str) -> List[str]:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    result = []
    for root, _, files in os.walk(directory):
        for f in files:
            if os.path.splitext(f.lower())[1] in exts:
                result.append(os.path.join(root, f))
    return result


def _save_results(results: List[Tuple[str, str]], fmt: str, out_path: Optional[str]):
    if fmt == "json":
        import json
        data = [{"image": p, "caption": c} for p, c in results]
        path = out_path or "captions.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
    if fmt == "csv":
        import csv
        path = out_path or "captions.csv"
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["image", "caption"])
            for p, c in results:
                w.writerow([p, c])
        return path
    path = out_path or "captions.txt"
    with open(path, "w", encoding="utf-8") as f:
        for p, c in results:
            f.write(f"{p}\t{c}\n")
    return path


def _b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def _list_cn_fonts(font_dir: str) -> List[str]:
    exts = ["*.ttf", "*.ttc", "*.otf"]
    fonts: List[str] = []
    if os.path.isdir(font_dir):
        for pat in exts:
            fonts.extend(glob.glob(os.path.join(font_dir, pat)))
    return sorted(fonts)


def _choose_cn_font(font_dir: str) -> Optional[str]:
    prefer = [
        "msyh.ttc",
        "msyh.ttf",
        "msyhbd.ttc",
        "msyhbd.ttf",
        "simhei.ttf",
        "simhei.ttc",
        "simsun.ttf",
    ]
    for name in prefer:
        p = os.path.join(font_dir, name)
        if os.path.isfile(p):
            return p
    fonts = _list_cn_fonts(font_dir)
    return fonts[0] if fonts else None


def _add_watermark(img: Image.Image, text: str, font_path: Optional[str] = None) -> Image.Image:
    w, h = img.size
    font = _font_from_path(font_path, max(14, int(h * 0.025)))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    tb = od.textbbox((0, 0), text, font=font)
    tw, th = tb[2] - tb[0], tb[3] - tb[1]
    pad = max(10, int(h * 0.02))
    x = w - tw - pad
    y = h - th - pad
    od.text((x + 1, y + 1), text, fill=(0, 0, 0, 160), font=font)
    od.text((x, y), text, fill=(255, 255, 255, 230), font=font)
    out = Image.alpha_composite(img.convert("RGBA"), overlay)
    return out.convert("RGB")


def create_app() -> Flask:
    _get_caption_pipe()
    app = Flask(__name__)
    font_dir = "C:\\Windows\\Fonts" if os.name == "nt" else ""
    fonts = _list_cn_fonts(font_dir) if font_dir else []
    default_font = _choose_cn_font(font_dir) if font_dir else None
    download_dir = os.path.join(os.getcwd(), "web_captioned")
    os.makedirs(download_dir, exist_ok=True)
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
        "<rect width='64' height='64' rx='12' fill='#2563eb'/>"
        "<rect x='14' y='16' width='36' height='10' rx='5' fill='#1e40af'/>"
        "<circle cx='32' cy='36' r='14' fill='#ffffff'/>"
        "<circle cx='32' cy='36' r='7' fill='#2563eb'/>"
        "<rect x='22' y='22' width='20' height='4' rx='2' fill='#93c5fd'/>"
        "</svg>"
    )
    icon_b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")

    @app.get("/")
    def index():
        opts = "".join(
            f"<option value='{f}' {'selected' if f==default_font else ''}>{os.path.basename(f)}</option>"
            for f in fonts
        )
        return (
            "<!doctype html><html><head><meta charset='utf-8'><title>图片字幕生成器</title>"
            f"<link rel='icon' href='data:image/svg+xml;base64,{icon_b64}'>"
            "<style>"
            "body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Microsoft YaHei',sans-serif;background:#f6f7fb;margin:0}"
            ".wrap{max-width:900px;margin:40px auto;padding:0 20px}"
            ".card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;box-shadow:0 6px 20px rgba(0,0,0,.06);overflow:hidden}"
            ".header{padding:18px 20px;border-bottom:1px solid #eee;font-weight:600}"
            ".title{display:flex;align-items:center;gap:10px}"
            ".title img{width:28px;height:28px}"
            ".body{padding:20px}"
            ".row{margin-bottom:14px}"
            ".input{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #d1d5db;border-radius:8px}"
            ".btn{background:#2563eb;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-weight:600;cursor:pointer}"
            ".btn:hover{background:#1e40af}"
            ".chk{margin-right:8px}"
            ".drop{border:2px dashed #9ca3af;border-radius:12px;padding:24px;text-align:center;color:#6b7280;background:#fafafa}"
            ".drop.drag{background:#eef2ff;border-color:#6366f1;color:#4338ca}"
            "#preview{max-width:100%;height:auto;margin-top:12px;border-radius:8px;border:1px solid #e5e7eb}"
            "</style>"
            "</head><body><div class='wrap'>"
            "<div class='card'>"
            f"<div class='header'><div class='title'><img src='data:image/svg+xml;base64,{icon_b64}' alt='icon'>图片字幕生成器</div></div>"
            "<div class='body'>"
            "<form id='form' method='post' action='/caption' enctype='multipart/form-data'>"
            "<div class='row'><label>图片URL</label><input id='url' class='input' type='url' name='url' placeholder='https://...'></div>"
            "<div class='row'>"
            "<div id='drop' class='drop'>拖拽图片到此处或点击下方选择文件</div>"
            "<input id='file' class='input' type='file' name='file' accept='image/*'>"
            "<img id='preview' style='display:none'>"
            "</div>"
            "<div class='row'><label>字幕内容</label><textarea class='input' name='manual_caption' rows='3' placeholder='在此输入或修改生成的字幕内容'></textarea></div>"
            "<div class='row'><label><input class='chk' type='checkbox' name='zh'>输出中文字幕</label></div>"
            "<div class='row'><label><input class='chk' type='checkbox' name='overlay'>叠加字幕到图片</label></div>"
            "<div class='row'><label><input class='chk' type='checkbox' name='watermark'>为下载图片添加专属水印</label></div>"
            "<div class='row'><input class='input' type='text' name='wm_text' placeholder='例如：© 我的水印'></div>"
            "<div class='row'>"
            f"<div>中文字体目录：{font_dir or '未检测到'}</div>"
            "<div style='display:flex;gap:8px;align-items:center'>"
            "<label><input class='chk' type='checkbox' name='auto_font' checked>自动选择中文字体</label>"
            f"<select class='input' name='font_sel'>{opts or '<option value=\"\">无可用字体</option>'}</select>"
            "</div>"
            "<div class='row'><input class='input' type='text' name='font' placeholder='自定义字体文件完整路径'></div>"
            "</div>"
            "<div class='row'><button class='btn' type='submit'>生成</button></div>"
            "</form>"
            "</div></div>"
            "</div>"
            "<script>"
            "const drop=document.getElementById('drop');"
            "const file=document.getElementById('file');"
            "const url=document.getElementById('url');"
            "const preview=document.getElementById('preview');"
            "function showPreviewFromFile(f){const o=URL.createObjectURL(f);preview.src=o;preview.style.display='block';}"
            "function showPreviewFromUrl(u){preview.src=u;preview.style.display='block';}"
            "drop.addEventListener('dragover',e=>{e.preventDefault();drop.classList.add('drag');});"
            "drop.addEventListener('dragleave',e=>{e.preventDefault();drop.classList.remove('drag');});"
            "drop.addEventListener('drop',e=>{e.preventDefault();drop.classList.remove('drag');"
            "if(e.dataTransfer.files&&e.dataTransfer.files.length){file.files=e.dataTransfer.files;showPreviewFromFile(file.files[0]);}"
            "else{const t=e.dataTransfer.getData('text');if(t){url.value=t;showPreviewFromUrl(t);}}});"
            "document.addEventListener('paste',e=>{if(e.clipboardData.files&&e.clipboardData.files.length){file.files=e.clipboardData.files;showPreviewFromFile(file.files[0]);}});"
            "file.addEventListener('change',()=>{if(file.files&&file.files[0])showPreviewFromFile(file.files[0]);});"
            "url.addEventListener('change',()=>{if(url.value)showPreviewFromUrl(url.value);});"
            "</script>"
            "</body></html>"
        )

    @app.get("/file/<name>")
    def file_route(name: str):
        safe_name = os.path.basename(name)
        path = os.path.join(download_dir, safe_name)
        if not os.path.isfile(path):
            return "文件不存在", 404
        return send_from_directory(download_dir, safe_name, as_attachment=True)

    @app.post("/caption")
    def caption_route():
        url = request.form.get("url") or ""
        zh = bool(request.form.get("zh"))
        overlay = bool(request.form.get("overlay"))
        font = request.form.get("font") or ""
        auto_font = bool(request.form.get("auto_font"))
        font_sel = request.form.get("font_sel") or ""
        watermark = bool(request.form.get("watermark"))
        wm_text = (request.form.get("wm_text") or "").strip()
        manual_caption = (request.form.get("manual_caption") or "").strip()
        try:
            if url.strip():
                img = _load_image(url.strip())
            else:
                f = request.files.get("file")
                if not f:
                    return "缺少图片输入", 400
                img = Image.open(f.stream).convert("RGB")
            text = manual_caption if manual_caption else generate_caption_image(img, zh=zh)
            img_el = ""
            download_el = ""
            if overlay:
                fp = None
                if font.strip():
                    fp = font.strip()
                elif font_sel.strip():
                    fp = font_sel.strip()
                elif auto_font and font_dir:
                    fp = _choose_cn_font(font_dir)
                over = _overlay_caption(img, text, font_path=fp)
                b64 = _b64(over)
                img_el = (
                    "<div style='margin-top:16px'>"
                    f"<img src='data:image/jpeg;base64,{b64}'/>"
                    "</div>"
                )
                fname = f"caption_{uuid.uuid4().hex}.jpg"
                save_path = os.path.join(download_dir, fname)
                try:
                    to_save = over
                    if watermark:
                        wm_font = fp
                        wm_txt = wm_text or "© Caption"
                        to_save = _add_watermark(to_save, wm_txt, font_path=wm_font)
                    to_save.save(save_path, quality=90)
                    download_el = (
                        "<div style='margin-top:12px'>"
                        f"<a class='btn' href='/file/{fname}' download>下载图片</a>"
                        "</div>"
                    )
                except Exception:
                    pass
            return (
                "<!doctype html><html><head><meta charset='utf-8'><title>结果</title>"
                f"<link rel='icon' href='data:image/svg+xml;base64,{icon_b64}'>"
                "<style>body{font-family:sans-serif;margin:24px} .box{max-width:720px;margin:auto} img{max-width:100%;height:auto}</style>"
                "</head><body><div class='box'>"
                f"<h3>字幕</h3><div style='padding:12px;background:#f5f5f5;border:1px solid #ddd'>{text}</div>"
                f"{img_el}{download_el}"
                "<div style='margin-top:16px'><a href='/'>返回</a></div>"
                "</div></body></html>"
            )
        except Exception as e:
            return f"错误：{e}", 500

    return app


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(prog="caption", description="Image caption generator")
    grp = parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--image", "-i", help="Image path or URL")
    grp.add_argument("--dir", "-d", help="Directory of images")
    grp.add_argument("--serve", action="store_true", help="Start web server")
    parser.add_argument("--zh", action="store_true", help="Translate caption to Chinese")
    parser.add_argument("--format", choices=["csv", "json", "txt"], default="csv")
    parser.add_argument("--out", help="Output file path for captions")
    parser.add_argument("--overlay", action="store_true", help="Save images with overlaid captions")
    parser.add_argument("--out_dir", help="Directory to save overlaid images")
    parser.add_argument("--font", help="Font file path for overlay text")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args(argv)
    try:
        if args.serve:
            app = create_app()
            app.run(host="127.0.0.1", port=args.port, debug=False)
            return 0
        if args.image:
            caption = generate_caption(args.image, zh=args.zh)
            print(caption)
            if args.overlay:
                img = _load_image(args.image)
                out_dir = args.out_dir or "captioned"
                os.makedirs(out_dir, exist_ok=True)
                base = os.path.basename(args.image) if not _is_url(args.image) else os.path.basename(args.image.split("?")[0])
                name, _ = os.path.splitext(base)
                out_path = os.path.join(out_dir, f"{name}_captioned.jpg")
                over = _overlay_caption(img, caption, font_path=args.font)
                over.save(out_path, quality=90)
            return 0
        if args.dir:
            imgs = _gather_images(args.dir)
            results: List[Tuple[str, str]] = []
            for p in imgs:
                try:
                    cap = generate_caption(p, zh=args.zh)
                    results.append((p, cap))
                except Exception:
                    continue
            saved = _save_results(results, args.format, args.out)
            if args.overlay:
                out_dir = args.out_dir or os.path.join(args.dir, "captioned")
                os.makedirs(out_dir, exist_ok=True)
                for p, c in results:
                    try:
                        img = _load_image(p)
                        over = _overlay_caption(img, c, font_path=args.font)
                        base = os.path.basename(p)
                        name, _ = os.path.splitext(base)
                        out_path = os.path.join(out_dir, f"{name}_captioned.jpg")
                        over.save(out_path, quality=90)
                    except Exception:
                        continue
            print(saved)
            return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
