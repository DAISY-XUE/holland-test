from __future__ import annotations

import logging
import time
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:  # 允许代码被静态检查，即使未安装 watchdog
    Observer = None  # type: ignore
    FileSystemEventHandler = object  # type: ignore

from .config import settings
from .pdf_reader import extract_text_from_pdf
from .classifier import analyze_pdf_text
from .renamer import rename_pdf_file


logger = logging.getLogger(__name__)


class PdfCreatedHandler(FileSystemEventHandler):  # type: ignore[misc]
    """监控新建 PDF 文件事件。"""

    def on_created(self, event):
        # event.src_path 可能是文件或目录
        path = Path(getattr(event, "src_path", ""))
        if not path.is_file() or path.suffix.lower() != ".pdf":
            return

        # 稍等片刻，避免扫描仪/应用还没写完文件
        time.sleep(1.0)

        try:
            logger.info("检测到新 PDF：%s", path)
            text = extract_text_from_pdf(path)
            info = analyze_pdf_text(text)
            rename_pdf_file(path, info)
        except Exception as e:  # noqa: BLE001
            logger.exception("处理新 PDF 失败：%s", e)


def start_watch():
    """启动目录监控，阻塞运行。"""
    if Observer is None:
        raise RuntimeError("未安装 watchdog，请先运行: pip install watchdog")

    watch_dir = settings.WATCH_DIR
    logger.info("开始监控目录：%s", watch_dir)

    event_handler = PdfCreatedHandler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=settings.RECURSIVE)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("收到中断信号，停止监控。")
    finally:
        observer.stop()
        observer.join()













