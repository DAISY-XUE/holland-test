import argparse
import os
import sys
from pathlib import Path
from caption_generator import CaptionGenerator

def ensure_demo_image(path: Path) -> Path:
    return path

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", "-i", type=str, required=False)
    parser.add_argument("--model", "-m", type=str, required=False)
    parser.add_argument("--device", "-d", type=str, choices=["cpu", "cuda"], required=False)
    parser.add_argument("--max_tokens", type=int, default=20)
    parser.add_argument("--beams", type=int, default=5)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo and not args.image:
        args.image = "demo.jpg"
    if not args.image:
        print("请提供图片路径，例如: python main.py --image ./xxx.jpg 或使用 --demo")
        sys.exit(1)
    if not os.path.isfile(args.image) and not args.demo:
        print("未找到图片文件: " + args.image)
        sys.exit(1)
    generator = CaptionGenerator(model_name=args.model, device=args.device)
    caption = generator.generate(args.image, max_new_tokens=args.max_tokens, num_beams=args.beams)
    print(caption)

if __name__ == "__main__":
    run()
