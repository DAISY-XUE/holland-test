"""文件管理工具配置模块"""
import os
from pathlib import Path
from typing import List


def get_default_scan_dir() -> Path:
    """默认扫描目录：用户主目录"""
    return Path.home()


class FileManagerSettings:
    """文件管理工具全局配置"""

    # 扫描目录（默认：用户主目录）
    SCAN_DIR: Path = get_default_scan_dir()

    # 是否递归扫描子目录
    RECURSIVE: bool = True

    # 排除的目录（相对路径或绝对路径）
    EXCLUDE_DIRS: List[str] = [
        "AppData",
        "Program Files",
        "Program Files (x86)",
        "Windows",
        "System Volume Information",
        "$Recycle.Bin",
        "node_modules",
        ".git",
        "__pycache__",
        ".venv",
        "venv",
    ]

    # 排除的文件扩展名（小写，不含点）
    EXCLUDE_EXTENSIONS: List[str] = [
        "lnk",  # 快捷方式
        "tmp",
        "temp",
    ]

    # 归档根目录（默认：扫描目录下的"归档"文件夹）
    ARCHIVE_ROOT: Path = SCAN_DIR / "文件归档"

    # 归档规则
    ARCHIVE_BY_DATE: bool = True  # 按日期归档
    ARCHIVE_BY_TYPE: bool = True  # 按文件类型归档
    ARCHIVE_BY_NAME: bool = False  # 按文件名首字母归档

    # 日期归档格式：year/month 或 year-month 或 year
    DATE_ARCHIVE_FORMAT: str = "year/month"  # year/month, year-month, year

    # 重复文件整理目录
    DUPLICATES_DIR: Path = SCAN_DIR / "重复文件整理"

    # 重命名规则
    RENAME_BY_DATE: bool = True  # 在文件名前添加日期
    RENAME_BY_TYPE: bool = False  # 在文件名前添加类型标识
    DATE_FORMAT: str = "YYYY-MM-DD"  # 日期格式

    # 日志文件路径
    LOG_FILE: Path = SCAN_DIR / "file_manager.log"

    # 是否执行实际操作（False时只显示预览）
    DRY_RUN: bool = False

    # 文件大小限制（字节），超过此大小的文件不处理（0表示无限制）
    MAX_FILE_SIZE: int = 0

    # 最小文件大小（字节），小于此大小的文件不处理（0表示无限制）
    MIN_FILE_SIZE: int = 0


settings = FileManagerSettings()




