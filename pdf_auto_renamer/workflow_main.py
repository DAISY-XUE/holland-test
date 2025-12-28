"""
工作流主入口：整合文件监控和Prefect工作流

使用方式：
    python -m pdf_auto_renamer.workflow_main
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

try:
    from prefect import flow, task
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError as e:
    print(f"❌ 缺少依赖：{e}")
    print("请运行：pip install -r requirements.txt")
    raise

from .config import settings
from .workflow_example import pdf_rename_workflow


logger = logging.getLogger(__name__)


class PdfWorkflowHandler(FileSystemEventHandler):
    """文件监控处理器，使用工作流处理新PDF文件"""

    def on_created(self, event):
        # event.src_path 可能是文件或目录
        path = Path(getattr(event, "src_path", ""))
        if not path.is_file() or path.suffix.lower() != ".pdf":
            return

        # 跳过临时文件
        if path.name.startswith("~$"):
            return

        # 稍等片刻，避免扫描仪/应用还没写完文件
        time.sleep(1.0)

        try:
            logger.info("=" * 60)
            logger.info("检测到新PDF文件，启动工作流处理：%s", path)
            logger.info("=" * 60)
            
            # 使用工作流处理文件
            result = pdf_rename_workflow(path)
            
            if result.get("success"):
                logger.info("✅ 工作流处理成功")
                logger.info("   原文件：%s", result.get("original_path"))
                logger.info("   新文件：%s", result.get("new_path"))
                logger.info("   文档类型：%s", result.get("doc_type"))
            else:
                logger.error("❌ 工作流处理失败：%s", result.get("error"))
                
        except Exception as e:
            logger.exception("工作流处理异常：%s", e)


@flow(
    name="启动PDF监控工作流",
    description="启动文件监控，使用工作流处理新PDF文件",
    log_prints=True,
)
def start_workflow_watch():
    """启动工作流监控"""
    watch_dir = settings.WATCH_DIR
    logger.info("=" * 60)
    logger.info("🚀 启动PDF工作流监控系统")
    logger.info("=" * 60)
    logger.info("监控目录：%s", watch_dir)
    logger.info("递归扫描：%s", settings.RECURSIVE)
    logger.info("已处理目录：%s", settings.PROCESSED_SUBDIR)
    logger.info("")
    logger.info("💡 提示：")
    logger.info("   - 将PDF文件放入监控目录即可自动处理")
    logger.info("   - 按 Ctrl+C 停止监控")
    logger.info("   - 查看Prefect UI：运行 'prefect server start' 后访问 http://localhost:4200")
    logger.info("=" * 60)

    event_handler = PdfWorkflowHandler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_dir), recursive=settings.RECURSIVE)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("")
        logger.info("=" * 60)
        logger.info("收到中断信号，停止监控...")
        logger.info("=" * 60)
    finally:
        observer.stop()
        observer.join()
        logger.info("监控已停止")


def setup_logging() -> None:
    """设置日志"""
    settings.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(settings.LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main() -> None:
    """主函数"""
    setup_logging()
    
    # 启动工作流监控
    start_workflow_watch()


if __name__ == "__main__":
    main()




