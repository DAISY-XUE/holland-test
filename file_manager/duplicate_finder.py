"""重复文件检测模块"""
import hashlib
import logging
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple

from .config import settings
from .scanner import FileInfo

logger = logging.getLogger(__name__)


def calculate_file_hash(file_path: Path, chunk_size: int = 8192) -> Optional[str]:
    """
    计算文件的MD5哈希值

    Args:
        file_path: 文件路径
        chunk_size: 读取块大小

    Returns:
        MD5哈希值（十六进制字符串），如果出错则返回 None
    """
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logger.warning("计算文件哈希失败: %s (%s)", file_path, e)
        return None


def find_duplicates_by_size(files: List[FileInfo]) -> Dict[int, List[FileInfo]]:
    """按文件大小分组，找出可能重复的文件"""
    size_groups: Dict[int, List[FileInfo]] = defaultdict(list)

    for file_info in files:
        size_groups[file_info.size].append(file_info)

    # 只返回大小相同的文件组（可能有重复）
    return {size: file_list for size, file_list in size_groups.items() if len(file_list) > 1}


def find_duplicates_by_hash(files: List[FileInfo]) -> Dict[str, List[FileInfo]]:
    """
    通过文件哈希值找出重复文件

    Args:
        files: 文件信息列表

    Returns:
        以哈希值为键，文件列表为值的字典
    """
    hash_groups: Dict[str, List[FileInfo]] = defaultdict(list)
    total = len(files)
    processed = 0

    logger.info("开始计算文件哈希值，共 %d 个文件...", total)

    for file_info in files:
        processed += 1
        if processed % 100 == 0:
            logger.info("进度: %d/%d (%.1f%%)", processed, total, processed / total * 100)

        file_hash = calculate_file_hash(file_info.path)
        if file_hash:
            hash_groups[file_hash].append(file_info)

    # 只返回有重复的组
    duplicates = {h: file_list for h, file_list in hash_groups.items() if len(file_list) > 1}
    logger.info("找到 %d 组重复文件", len(duplicates))
    return duplicates


def organize_duplicates(duplicates: Dict[str, List[FileInfo]]) -> None:
    """
    整理重复文件到指定目录

    Args:
        duplicates: 重复文件字典（哈希值 -> 文件列表）
    """
    duplicates_dir = settings.DUPLICATES_DIR
    duplicates_dir.mkdir(parents=True, exist_ok=True)

    group_num = 0
    for file_hash, file_list in duplicates.items():
        if len(file_list) <= 1:
            continue

        group_num += 1
        group_dir = duplicates_dir / f"重复组_{group_num:04d}_{file_hash[:8]}"
        group_dir.mkdir(parents=True, exist_ok=True)

        # 按修改时间排序，保留最新的作为主文件
        sorted_files = sorted(file_list, key=lambda f: f.modified_time, reverse=True)

        for idx, file_info in enumerate(sorted_files):
            if idx == 0:
                # 主文件保持原名
                target_name = file_info.name
            else:
                # 其他文件添加序号
                stem = file_info.path.stem
                extension = file_info.extension
                target_name = f"{stem}_副本{idx}{extension}"

            target_path = group_dir / target_name

            if settings.DRY_RUN:
                logger.info("[预览] 将移动重复文件: %s -> %s", file_info.path, target_path)
            else:
                try:
                    import shutil
                    shutil.move(str(file_info.path), str(target_path))
                    logger.info("已移动重复文件: %s -> %s", file_info.path.name, target_path.name)
                except Exception as e:
                    logger.error("移动重复文件失败: %s (%s)", file_info.path, e)

        # 创建说明文件
        info_file = group_dir / "重复文件说明.txt"
        with open(info_file, "w", encoding="utf-8") as f:
            f.write(f"重复文件组 #{group_num}\n")
            f.write(f"文件哈希: {file_hash}\n")
            f.write(f"文件数量: {len(file_list)}\n")
            f.write(f"文件大小: {file_list[0].size:,} 字节\n\n")
            f.write("文件列表（按修改时间排序，最新的在前）:\n")
            for idx, file_info in enumerate(sorted_files, 1):
                f.write(f"{idx}. {file_info.path}\n")
                f.write(f"   修改时间: {file_info.modified_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"   创建时间: {file_info.created_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        logger.info("重复文件组 %d 已整理到: %s", group_num, group_dir)


def find_and_organize_duplicates(files: List[FileInfo], use_hash: bool = True) -> Dict[str, List[FileInfo]]:
    """
    查找并整理重复文件

    Args:
        files: 文件信息列表
        use_hash: 是否使用哈希值检测（更准确但较慢）

    Returns:
        重复文件字典
    """
    if use_hash:
        # 先按大小快速筛选
        size_groups = find_duplicates_by_size(files)
        candidate_files = []
        for file_list in size_groups.values():
            candidate_files.extend(file_list)

        if not candidate_files:
            logger.info("未找到可能重复的文件")
            return {}

        logger.info("找到 %d 个可能重复的文件，开始计算哈希值...", len(candidate_files))
        duplicates = find_duplicates_by_hash(candidate_files)
    else:
        # 仅按大小判断（不准确，但快速）
        size_groups = find_duplicates_by_size(files)
        duplicates = {}
        for size, file_list in size_groups.items():
            if len(file_list) > 1:
                # 使用大小作为"哈希"
                duplicates[str(size)] = file_list

    if duplicates:
        logger.info("找到 %d 组重复文件，开始整理...", len(duplicates))
        organize_duplicates(duplicates)
    else:
        logger.info("未找到重复文件")

    return duplicates


