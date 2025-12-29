from __future__ import annotations

from pathlib import Path

import pdfplumber


def extract_text_from_pdf(path: Path) -> str:
    """使用 pdfplumber 提取 PDF 文本。"""
    texts = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            texts.append(t)
    return "\n".join(texts)












