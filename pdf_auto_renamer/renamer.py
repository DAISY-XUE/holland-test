from __future__ import annotations

import logging
import re
import shutil
from pathlib import Path
from typing import Optional

from .classifier import PdfInfo
from .config import settings


logger = logging.getLogger(__name__)


def safe_filename(name: str) -> str:
    """去除 Windows 不允许的文件名字符。"""
    invalid_chars = '<>:"/\\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    return name.strip()


def build_new_name(info: PdfInfo, original_name: str) -> Optional[str]:
    """
    根据识别结果生成新的文件名（不含后缀）。
    返回 None 表示不重命名。
    """
    # 合同：合同编号+项目名称
    if info.doc_type == "contract":
        if info.contract_number and info.project_name:
            return f"{info.contract_number}_{info.project_name}"
        elif info.contract_number:
            return f"{info.contract_number}_合同"
        elif info.project_name:
            return f"合同_{info.project_name}"
        else:
            return None

    # 发票：
    #   - 劳务费类会在 labor_fee 分支里处理
    #   - 其他工程/建筑服务发票：命名为 “(发票)+项目名称”
    if info.doc_type == "invoice":
        # 如果已经识别出工程项目名称，则按照 “(发票)项目名称” 命名
        if info.project_name:
            return f"(发票){info.project_name}"

        # 否则退回到简单的 “月份+费用类型发票”
        month = info.month_text or ""
        fee = info.invoice_keyword or "费用"
        base = f"{month}{fee}发票".lstrip()
        return base or None

    # 劳务费类（审批材料 / 付款申请单 / 发票）
    if info.doc_type == "labor_fee":
        year = info.year_text or ""
        month = info.month_text or ""
        prefix = f"{year}{month}".lstrip()

        if not prefix:
            prefix = "劳务费"
        else:
            prefix = f"{prefix}劳务费"

        doc_type = info.labor_fee_doc_type or ""

        # 统一成：YYYY年M月劳务费审批材料 / 付款申请单 / 发票
        if doc_type:
            return f"{prefix}{doc_type}"
        return prefix

    # 收据 / 资金往来统一票据
    if info.doc_type == "receipt":
        # 公共维护基金类：尽量命名为 “2025年4-6月_5号楼_公共维护基金收据”
        item = info.receipt_item or ""
        year = info.receipt_year or ""
        month_range = info.receipt_month_range or ""

        # 是否公共维护基金
        is_maint_fund = "公共维护基金" in item

        parts: list[str] = []
        if year:
            if month_range:
                parts.append(f"{year}{month_range}")
            else:
                parts.append(year)

        # 简单从项目中提取“X号楼”
        building = None
        if "号楼" in item:
            m = re.search(r"(\d+号楼)", item)
            if m:
                building = m.group(1)
        if building:
            parts.append(building)

        # 描述部分
        if is_maint_fund:
            parts.append("公共维护基金收据")
        elif item:
            # 例如“施工押金” → “施工押金收据”
            clean_item = item.replace("收款项目", "").strip()
            parts.append(f"{clean_item}收据")
        else:
            parts.append("收据")

        base = "_".join(p for p in parts if p)
        return base or "收据"

    # 审核报告：（审核报告）+项目名称
    if info.doc_type == "audit_report":
        if info.project_name:
            # 如果正文中出现“结算审核报告”等字样，文件名前缀也使用“结算审核报告”
            prefix = "审核报告"
            if "简易立项表" in info.raw_text:
                prefix = "简易立项表"
            elif "结算审核报告" in info.raw_text:
                prefix = "结算审核报告"
            return f"({prefix}){info.project_name}"
        return "(审核报告)未知项目"

    # 其他类型暂时不自动命名
    return None


def ensure_unique_path(target_dir: Path, base_name: str, suffix: str) -> Path:
    """避免重名，必要时在后面加 (1)、(2)..."""
    base_name = safe_filename(base_name)
    candidate = target_dir / f"{base_name}{suffix}"
    idx = 1
    while candidate.exists():
        candidate = target_dir / f"{base_name}({idx}){suffix}"
        idx += 1
    return candidate


def move_to_processed(src: Path) -> None:
    """将原文件移动到已处理目录（可选）。"""
    subdir = settings.PROCESSED_SUBDIR
    if not subdir:
        return
    processed_dir = settings.WATCH_DIR / subdir
    processed_dir.mkdir(parents=True, exist_ok=True)
    dst = ensure_unique_path(processed_dir, src.stem, src.suffix)
    shutil.move(str(src), str(dst))
    logger.info("已移动到已处理目录: %s", dst)


def rename_pdf_file(path: Path, info: PdfInfo) -> Optional[Path]:
    """根据 PdfInfo 对单个 PDF 进行重命名并可选移动。"""
    if not path.exists() or path.suffix.lower() != ".pdf":
        return None

    new_base_name = build_new_name(info, path.stem)
    if not new_base_name:
        logger.info("未生成新文件名，跳过：%s", path)
        return None

    target_dir = path.parent
    new_path = ensure_unique_path(target_dir, new_base_name, path.suffix)

    # 先重命名
    path.rename(new_path)
    logger.info("已重命名：%s -> %s", path.name, new_path.name)

    # 再移动到已处理子目录（如果配置了）
    move_to_processed(new_path)

    return new_path


