"""文件扫描器模块"""
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .config import settings

logger = logging.getLogger(__name__)


@dataclass
class FileInfo:
    """文件信息数据类"""
    path: Path
    name: str
    extension: str
    size: int
    created_time: datetime
    modified_time: datetime
    accessed_time: datetime
    is_file: bool = True

    @property
    def file_type(self) -> str:
        """获取文件类型（扩展名，不含点）"""
        return self.extension.lower().lstrip(".")

    @property
    def should_process(self) -> bool:
        """判断是否应该处理此文件"""
        # 检查扩展名
        if self.file_type in settings.EXCLUDE_EXTENSIONS:
            return False

        # 检查文件大小
        if settings.MAX_FILE_SIZE > 0 and self.size > settings.MAX_FILE_SIZE:
            return False
        if settings.MIN_FILE_SIZE > 0 and self.size < settings.MIN_FILE_SIZE:
            return False

        return True


def should_exclude_dir(dir_path: Path) -> bool:
    """判断目录是否应该被排除"""
    dir_name = dir_path.name

    # 检查排除列表
    for exclude in settings.EXCLUDE_DIRS:
        if exclude in dir_path.parts:
            return True

    # 排除隐藏目录（以点开头）
    if dir_name.startswith("."):
        return True

    return False


def scan_files(root_dir: Path, recursive: bool = True) -> List[FileInfo]:
    """
    扫描目录下的所有文件

    Args:
        root_dir: 根目录
        recursive: 是否递归扫描子目录

    Returns:
        文件信息列表
    """
    files: List[FileInfo] = []
    root_dir = Path(root_dir).resolve()

    if not root_dir.exists():
        logger.warning("扫描目录不存在: %s", root_dir)
        return files

    if not root_dir.is_dir():
        logger.warning("扫描路径不是目录: %s", root_dir)
        return files

    logger.info("开始扫描目录: %s (递归: %s)", root_dir, recursive)

    try:
        if recursive:
            iterator = root_dir.rglob("*")
        else:
            iterator = root_dir.glob("*")

        for item_path in iterator:
            try:
                # 跳过排除的目录
                if item_path.is_dir() and should_exclude_dir(item_path):
                    continue

                # 只处理文件
                if not item_path.is_file():
                    continue

                # 获取文件信息
                stat = item_path.stat()
                file_info = FileInfo(
                    path=item_path,
                    name=item_path.name,
                    extension=item_path.suffix,
                    size=stat.st_size,
                    created_time=datetime.fromtimestamp(stat.st_ctime),
                    modified_time=datetime.fromtimestamp(stat.st_mtime),
                    accessed_time=datetime.fromtimestamp(stat.st_atime),
                )

                # 检查是否应该处理
                if file_info.should_process:
                    files.append(file_info)

            except (OSError, PermissionError) as e:
                logger.warning("无法访问文件: %s (%s)", item_path, e)
                continue

    except Exception as e:
        logger.error("扫描目录时出错: %s", e, exc_info=True)

    logger.info("扫描完成，找到 %d 个文件", len(files))
    return files







