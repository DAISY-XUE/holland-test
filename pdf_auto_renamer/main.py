from __future__ import annotations

import logging

from .config import settings
from .pdf_reader import extract_text_from_pdf
from .classifier import analyze_pdf_text
from .renamer import rename_pdf_file
from .watcher import start_watch


def setup_logging() -> None:
    settings.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(settings.LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def process_existing_pdfs() -> None:
    """一次性处理监控目录下已存在的 PDF 文件。"""
    root = settings.WATCH_DIR
    if settings.RECURSIVE:
        files = root.rglob("*.pdf")
    else:
        files = root.glob("*.pdf")

    for path in files:
        if path.name.startswith("~$"):  # 临时文件跳过
            continue
        try:
            text = extract_text_from_pdf(path)
            info = analyze_pdf_text(text)
            rename_pdf_file(path, info)
        except Exception as e:  # noqa: BLE001
            logging.getLogger(__name__).exception("处理已存在 PDF 失败：%s (%s)", path, e)


def main() -> None:
    setup_logging()
    logging.info("监控目录：%s", settings.WATCH_DIR)

    # 先处理一下监控目录下已经存在的 PDF
    process_existing_pdfs()

    # 再启动持续监控
    start_watch()


if __name__ == "__main__":
    main()




