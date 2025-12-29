import os
from pathlib import Path


def get_default_watch_dir() -> Path:
    """
    默认监控目录：桌面下的“扫描文件夹”。
    如不存在则创建。
    """
    desktop = Path.home() / "Desktop"
    watch_dir = desktop / "扫描文件夹"
    watch_dir.mkdir(parents=True, exist_ok=True)
    return watch_dir


class Settings:
    """
    全局配置，可根据需要修改。
    """

    # 监控目录（默认：桌面/扫描文件夹）
    WATCH_DIR: Path = get_default_watch_dir()

    # 是否递归扫描子目录
    RECURSIVE: bool = False

    # 已处理文件移动到的子目录名（位于 WATCH_DIR 下），为空则不移动
    PROCESSED_SUBDIR: str = "_processed"

    # 日志文件路径
    LOG_FILE: Path = WATCH_DIR / "auto_renamer.log"


settings = Settings()











