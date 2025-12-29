"""文件归档模块"""
import logging
import shutil
from pathlib import Path
from typing import Optional

from .config import settings
from .scanner import FileInfo

logger = logging.getLogger(__name__)


def get_date_archive_path(file_info: FileInfo, format_str: str = "year/month") -> Path:
    """根据日期归档格式生成归档路径"""
    dt = file_info.modified_time

    if format_str == "year/month":
        date_path = f"{dt.year}/{dt.month:02d}月"
    elif format_str == "year-month":
        date_path = f"{dt.year}-{dt.month:02d}"
    elif format_str == "year":
        date_path = str(dt.year)
    else:
        date_path = f"{dt.year}/{dt.month:02d}月"

    return Path(date_path)


def get_type_archive_path(file_info: FileInfo) -> Path:
    """根据文件类型生成归档路径"""
    file_type = file_info.file_type

    # 类型分类
    type_categories = {
        "文档": ["pdf", "doc", "docx", "txt", "rtf", "odt"],
        "表格": ["xls", "xlsx", "csv", "ods"],
        "演示": ["ppt", "pptx", "odp"],
        "图片": ["jpg", "jpeg", "png", "gif", "bmp", "webp", "svg", "ico"],
        "视频": ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"],
        "音频": ["mp3", "wav", "flac", "aac", "ogg", "m4a"],
        "压缩": ["zip", "rar", "7z", "tar", "gz", "bz2"],
        "程序": ["exe", "msi", "dmg", "deb", "rpm"],
        "代码": ["py", "js", "java", "cpp", "c", "h", "html", "css", "xml", "json"],
    }

    category = "其他"
    for cat, exts in type_categories.items():
        if file_type in exts:
            category = cat
            break

    return Path(category)


def get_name_archive_path(file_info: FileInfo) -> Path:
    """根据文件名首字母生成归档路径"""
    name = file_info.name
    if not name:
        return Path("其他")

    first_char = name[0].upper()
    if first_char.isalpha():
        return Path(first_char)
    elif first_char.isdigit():
        return Path("0-9")
    else:
        return Path("其他")


def get_archive_path(file_info: FileInfo) -> Path:
    """生成完整的归档路径"""
    parts = []

    if settings.ARCHIVE_BY_DATE:
        parts.append(get_date_archive_path(file_info, settings.DATE_ARCHIVE_FORMAT))

    if settings.ARCHIVE_BY_TYPE:
        parts.append(get_type_archive_path(file_info))

    if settings.ARCHIVE_BY_NAME:
        parts.append(get_name_archive_path(file_info))

    # 如果没有设置任何归档规则，使用默认的"未分类"
    if not parts:
        parts.append(Path("未分类"))

    # 组合路径
    archive_path = Path(*parts)
    return archive_path


def archive_file(file_info: FileInfo, rename: bool = True) -> Optional[Path]:
    """
    归档文件

    Args:
        file_info: 文件信息
        rename: 是否同时重命名文件

    Returns:
        归档后的文件路径，如果归档失败则返回 None
    """
    if not file_info.path.exists():
        logger.warning("文件不存在: %s", file_info.path)
        return None

    # 生成归档路径
    relative_archive_path = get_archive_path(file_info)
    archive_dir = settings.ARCHIVE_ROOT / relative_archive_path
    archive_dir.mkdir(parents=True, exist_ok=True)

    # 确定目标文件名
    if rename:
        from .renamer import build_new_filename
        new_filename = build_new_filename(file_info)
        if new_filename:
            target_name = new_filename
        else:
            target_name = file_info.name
    else:
        target_name = file_info.name

    # 确保目标文件名唯一
    from .renamer import ensure_unique_path
    target_path = ensure_unique_path(archive_dir, target_name.rsplit(".", 1)[0], file_info.extension)

    if settings.DRY_RUN:
        logger.info("[预览] 将归档: %s -> %s", file_info.path, target_path)
        return target_path

    try:
        # 移动文件
        shutil.move(str(file_info.path), str(target_path))
        logger.info("已归档: %s -> %s", file_info.path.name, target_path)
        return target_path
    except Exception as e:
        logger.error("归档文件失败: %s (%s)", file_info.path, e)
        return None





