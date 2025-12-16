# 图片字幕生成器（含网页端）

一个开箱即用的图片字幕生成器，支持：
- 单张/目录批量生成字幕（英文/中文）
- 将字幕叠加到图片底部
- 网页端上传/拖拽/粘贴图片，预览与下载
- 下载时可添加自定义水印
- 自动识别 `C:\Windows\Fonts` 并选择中文字体（可自定义字体路径）

## 快速开始

1) 安装依赖
```
python -m pip install --upgrade pip
python -m pip install transformers torch pillow requests flask
```

2) 命令行使用
```
python caption.py --image <图片路径或URL>
python caption.py --image <图片路径或URL> --zh
python caption.py --image <图片路径或URL> --zh --overlay --out_dir captioned --font C:\Windows\Fonts\msyh.ttc
```

3) 目录批量
```
python caption.py --dir <图片目录> --zh --format csv --out captions.csv
python caption.py --dir <图片目录> --zh --overlay --out_dir <图片目录>\captioned --font C:\Windows\Fonts\msyh.ttc
```

4) 启动网页端
```
python caption.py --serve --port 5000
# 浏览器打开 http://127.0.0.1:5000/
```

预览页（仅样式演示，无后端）：直接双击打开 `preview.html`。

## 网页端功能
- 图片输入：URL、文件上传、拖拽、粘贴
- 字幕：自动生成或在“字幕内容”文本框中手动输入覆盖
- 字幕叠加：勾选“叠加字幕到图片”即在页面展示效果
- 字体：自动选择中文字体，或下拉选择，可输入自定义字体路径
- 水印：勾选“为下载图片添加专属水印”，输入水印文本，下载即带水印

## 重要说明
- 首次运行会自动下载模型权重，耗时取决于网络环境
- 默认在 CPU 上运行，如需更快可安装支持 GPU 的 `torch`
- 生成的图片默认不推送到仓库（被 `.gitignore` 忽略），在 `web_captioned/` 或你指定的目录

## 项目结构
- `caption.py`：核心脚本与网页服务入口
- `preview.html`：静态预览页面
- `.gitignore`：忽略临时与生成文件

## 典型问题
- PowerShell 不支持 `&&`：请用分号 `;` 分隔命令
- 中文显示为方块：为网页端选择或输入中文字体，如 `C:\Windows\Fonts\msyh.ttc`

## 许可证
未指定许可证，默认保留权利。若需开源授权，请更新本节。 
