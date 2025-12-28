import os
from typing import Optional

class CaptionGenerator:
    def __init__(self, model_name: Optional[str] = None, device: Optional[str] = None):
        self._pipeline = None
        self._backend = None
        self._model_name = model_name or "Salesforce/blip-image-captioning-large"
        self._device = device
        try:
            from transformers import pipeline
            kwargs = {}
            if self._device is not None:
                kwargs["device"] = 0 if self._device == "cuda" else -1
            self._pipeline = pipeline("image-to-text", model=self._model_name, **kwargs)
            self._backend = "blip"
        except Exception:
            self._backend = "fallback"

    def generate(self, image_path: str, max_new_tokens: int = 20, num_beams: int = 5) -> str:
        if self._backend == "blip":
            result = self._pipeline(image_path, max_new_tokens=max_new_tokens, num_beams=num_beams)
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"]
            return str(result)
        try:
            from PIL import Image, ImageStat
            img = Image.open(image_path).convert("RGB")
            stat = ImageStat.Stat(img)
            mean = stat.mean
            var = stat.var
            brightness = sum(mean) / 3
            colorfulness = max(mean) - min(mean)
            smooth = sum(var) / 3
            if smooth < 50:
                if colorfulness < 5:
                    if brightness > 200:
                        return "一张非常明亮的纯色背景图片"
                    if brightness < 55:
                        return "一张非常暗的纯色背景图片"
                    return "一张纯色背景图片"
                return "一张简单的纯色背景，带轻微色差的图片"
            if colorfulness > 40:
                if brightness > 170:
                    return "一张色彩丰富且偏亮的图片"
                if brightness < 80:
                    return "一张色彩浓郁且偏暗的图片"
                return "一张色彩丰富的图片"
            if brightness > 170:
                return "一张偏亮的图片"
            if brightness < 80:
                return "一张偏暗的图片"
            return "一张普通的图片"
        except Exception:
            return "一张图片"

