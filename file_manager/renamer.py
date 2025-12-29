"""文件重命名模块"""
import logging
import re
import shutil
from pathlib import Path
from typing import Optional

from .config import settings
from .scanner import FileInfo

logger = logging.getLogger(__name__)


def safe_filename(name: str) -> str:
    """去除 Windows 不允许的文件名字符"""
    invalid_chars = '<>:"/\\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    # 去除首尾空格和点
    name = name.strip(" .")
    return name


def format_date(dt, format_str: str = "YYYY-MM-DD") -> str:
    """格式化日期"""
    if format_str == "YYYY-MM-DD":
        return dt.strftime("%Y-%m-%d")
    elif format_str == "YYYYMMDD":
        return dt.strftime("%Y%m%d")
    elif format_str == "YY-MM-DD":
        return dt.strftime("%y-%m-%d")
    else:
        # 默认格式
        return dt.strftime("%Y-%m-%d")


def extract_title_from_name(name: str) -> str:
    """从文件名中提取标题（去除日期、序号等）"""
    # 移除常见的日期格式
    patterns = [
        r"\d{4}[-_]\d{2}[-_]\d{2}",  # 2024-01-01 或 2024_01_01
        r"\d{4}\d{2}\d{2}",  # 20240101
        r"\d{2}[-_]\d{2}[-_]\d{2}",  # 24-01-01
        r"\(\d+\)",  # (1), (2) 等序号
        r"\[\d+\]",  # [1], [2] 等序号
        r"^\d+[-_]",  # 开头的数字和分隔符
        r"[-_]\d+$",  # 结尾的数字
    ]

    title = name
    for pattern in patterns:
        title = re.sub(pattern, "", title)

    # 清理多余的下划线和连字符
    title = re.sub(r"[-_]{2,}", "_", title)
    title = title.strip("-_ ")

    return title if title else name


def build_new_filename(file_info: FileInfo, use_modified_time: bool = True) -> Optional[str]:
    """
    根据文件信息生成新文件名

    Args:
        file_info: 文件信息
        use_modified_time: 是否使用修改时间（否则使用创建时间）

    Returns:
        新文件名（不含路径），如果不需要重命名则返回 None
    """
    original_name = file_info.name
    stem = file_info.path.stem
    extension = file_info.extension

    parts = []

    # 添加日期前缀
    if settings.RENAME_BY_DATE:
        dt = file_info.modified_time if use_modified_time else file_info.created_time
        date_str = format_date(dt, settings.DATE_FORMAT)
        parts.append(date_str)

    # 添加类型标识
    if settings.RENAME_BY_TYPE:
        type_map = {
            "pdf": "PDF",
            "doc": "DOC",
            "docx": "DOC",
            "xls": "XLS",
            "xlsx": "XLS",
            "ppt": "PPT",
            "pptx": "PPT",
            "jpg": "IMG",
            "jpeg": "IMG",
            "png": "IMG",
            "gif": "IMG",
            "mp4": "VID",
            "avi": "VID",
            "mov": "VID",
            "mp3": "AUD",
            "wav": "AUD",
            "zip": "ZIP",
            "rar": "ZIP",
            "txt": "TXT",
        }
        file_type = file_info.file_type
        type_label = type_map.get(file_type, file_type.upper())
        parts.append(type_label)

    # 提取并添加原始标题
    title = extract_title_from_name(stem)
    if title:
        parts.append(title)
    else:
        # 如果没有提取到标题，使用原始文件名（不含扩展名）
        parts.append(stem)

    # 组合新文件名
    new_stem = "_".join(parts)
    new_stem = safe_filename(new_stem)

    # 如果新文件名和原文件名相同，不重命名
    if new_stem == stem:
        return None

    new_filename = f"{new_stem}{extension}"
    return new_filename


def ensure_unique_path(target_dir: Path, base_name: str, extension: str) -> Path:
    """确保路径唯一，如果文件已存在则添加序号"""
    base_name = safe_filename(base_name)
    candidate = target_dir / f"{base_name}{extension}"
    idx = 1
    while candidate.exists():
        candidate = target_dir / f"{base_name}({idx}){extension}"
        idx += 1
    return candidate


def rename_file(file_info: FileInfo, target_dir: Optional[Path] = None) -> Optional[Path]:
    """
    重命名文件

    Args:
        file_info: 文件信息
        target_dir: 目标目录（如果为None则在原目录重命名）

    Returns:
        新文件路径，如果未重命名则返回 None
    """
    if not file_info.path.exists():
        logger.warning("文件不存在: %s", file_info.path)
        return None

    new_filename = build_new_filename(file_info)
    if not new_filename:
        logger.debug("文件无需重命名: %s", file_info.path)
        return None

    target_dir = target_dir or file_info.path.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    new_path = ensure_unique_path(target_dir, new_filename.rsplit(".", 1)[0], file_info.extension)

    if settings.DRY_RUN:
        logger.info("[预览] 将重命名: %s -> %s", file_info.path.name, new_path.name)
        return new_path

    try:
        file_info.path.rename(new_path)
        logger.info("已重命名: %s -> %s", file_info.path.name, new_path.name)
        return new_path
    except Exception as e:
        logger.error("重命名文件失败: %s (%s)", file_info.path, e)
        return None





