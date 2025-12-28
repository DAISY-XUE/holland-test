from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class PdfInfo:
    """PDF 文本解析后的关键信息。"""

    raw_text: str
    doc_type: str  # "contract" | "invoice" | "attendance" | "audit_report" | "receipt" | "labor_fee" | "unknown"
    contract_number: Optional[str] = None
    project_name: Optional[str] = None
    month_text: Optional[str] = None  # 如 "5月"
    invoice_keyword: Optional[str] = None  # 如 "劳务费"
    year_text: Optional[str] = None  # 如 "2025年"
    labor_fee_doc_type: Optional[str] = None  # "审批材料" | "付款申请单" | "发票"
    receipt_item: Optional[str] = None  # 收据中的收款项目
    receipt_year: Optional[str] = None  # 收据年份，如 "2025年"
    receipt_month_range: Optional[str] = None  # 公共维护基金等使用的月份范围，如 "4-6月"


CONTRACT_KEYWORDS = ["合同", "合同编号", "发包人", "承包人"]
INVOICE_KEYWORDS = ["发票", "增值税发票", "普通发票"]
ATTENDANCE_KEYWORDS = ["考勤表", "出勤", "出勤表"]
AUDIT_REPORT_KEYWORDS = ["审核报告", "审查报告", "评审报告", "结算审核报告"]
RECEIPT_KEYWORDS = ["收据", "收条", "收款凭证"]
# 劳务费相关关键字，兼容“劳务费”和“劳务费用”等写法
LABOR_FEE_KEYWORDS = ["劳务费", "劳务费用"]


def detect_doc_type(text: str) -> str:
    """根据关键字粗略识别文档类型。"""
    t = text[:4000]  # 只看前 4000 字符，够用且速度快
    # 劳务费类优先识别（因为既可能包含“发票”也可能不是发票）
    if any(k in t for k in LABOR_FEE_KEYWORDS):
        return "labor_fee"
    if any(k in t for k in CONTRACT_KEYWORDS):
        return "contract"
    if any(k in t for k in INVOICE_KEYWORDS):
        return "invoice"
    if any(k in t for k in ATTENDANCE_KEYWORDS):
        return "attendance"
    if any(k in t for k in AUDIT_REPORT_KEYWORDS):
        return "audit_report"
    if any(k in t for k in RECEIPT_KEYWORDS):
        return "receipt"
    return "unknown"


def extract_contract_info(text: str) -> tuple[Optional[str], Optional[str]]:
    """
    提取合同编号和项目名称（尽量，不保证 100% 命中）。
    常见格式示例：
      合同编号：HT-2024-001
      项目名称：XXX工程项目
    """
    # 合同编号
    m_no = re.search(r"(合同编号|合同号)\s*[:：]?\s*([A-Za-z0-9\-_/]{4,})", text)
    contract_number = m_no.group(2).strip() if m_no else None

    # 项目名称
    m_proj = re.search(r"(项目名称|工程名称)\s*[:：]?\s*([^\n\r]{4,60})", text)
    project_name: Optional[str] = m_proj.group(2).strip() if m_proj else None

    # 如果没有显式“项目名称/工程名称”，尝试从前几行标题中获取
    if project_name is None:
        head_lines = text.splitlines()[:15]
        for line in head_lines:
            s = line.strip()
            if len(s) < 4:
                continue
            # 典型合同主标题：以“合同”结尾，但不包含“编号”
            if "合同" in s and "编号" not in s and "合同号" not in s:
                project_name = s
                break

    return contract_number, project_name


def extract_invoice_info(text: str) -> tuple[Optional[str], Optional[str]]:
    """
    提取发票中的月份和费用类型（如“劳务费”、“服务费”等）。
    最终用于命名为：5月劳务费发票.pdf
    """
    # 月份（中文格式）
    m_month = re.search(r"([1-9]|1[0-2])\s*月", text)
    month_text = f"{m_month.group(1)}月" if m_month else None

    # 费用类型简单匹配
    fee_keywords = ["劳务费", "服务费", "咨询费", "工程款", "租金", "房租", "材料费", "建筑服务", "工程服务"]
    fee_hit = None
    for k in fee_keywords:
        if k in text:
            fee_hit = k
            break

    return month_text, fee_hit


def extract_year_month(text: str) -> tuple[Optional[str], Optional[str]]:
    """
    提取“服务期间所在的年月”，优先顺序：
      1）中文形式：2025年3月
      2）数字形式：2025.03 或 2025-03
      3）区间形式：2025.03.01-2025.03.31（取前半段的年月）
    返回 (year_text, month_text) 例如 ("2025年", "3月")
    """
    # 1) 直接的“2025年3月”
    m = re.search(r"(20\d{2})\s*年\s*([1-9]|1[0-2])\s*月", text)
    if m:
        year = f"{m.group(1)}年"
        month = f"{m.group(2)}月"
        return year, month

    # 2) 区间形式：2025.03.01-2025.03.31 或 2025-03-01~2025-03-31
    m = re.search(r"(20\d{2})[.\-/](\d{1,2})[.\-/]\d{1,2}\s*[-~～]\s*(20\d{2})?[.\-/](\d{1,2})[.\-/]\d{1,2}", text)
    if m:
        year_num = m.group(1)
        month_num = m.group(2)
        year = f"{year_num}年"
        month = f"{int(month_num)}月"
        return year, month

    # 3) 单个数字年月：2025.03 或 2025-03
    m = re.search(r"(20\d{2})[.\-/](\d{1,2})", text)
    if m:
        year_num = m.group(1)
        month_num = m.group(2)
        year = f"{year_num}年"
        month = f"{int(month_num)}月"
        return year, month

    return None, None


def detect_labor_fee_doc_type(text: str) -> Optional[str]:
    """
    劳务费相关文档中区分具体类型：
      - 审批材料
      - 付款申请单
      - 发票
    """
    if "审批材料" in text or "审批表" in text:
        return "审批材料"
    if "付款申请单" in text or "付款申请表" in text or "支付申请单" in text:
        return "付款申请单"
    if "发票" in text:
        return "发票"
    return None


def extract_receipt_info(text: str) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    提取收据（资金往来统一票据等）的关键信息：
      - receipt_item: 收款项目（如“5号楼及2025年4-6月份公共维护基金”、“施工押金”）
      - receipt_year: 年份（如“2025年”）
      - receipt_month_range: 月份范围字符串（如“4-6月”），主要用于公共维护基金
    """
    # 简单从“收款项目”行附近提取一整行
    item = None
    lines = text.splitlines()
    for line in lines:
        if "收款项目" in line or "收 款 项 目" in line:
            # 下一行通常就是具体项目
            idx = lines.index(line)
            if idx + 1 < len(lines):
                candidate = lines[idx + 1].strip()
                if len(candidate) >= 2:
                    item = candidate
            break

    # 如果上面没取到，退而求其次：找包含“公共维护基金”或“押金”的行
    if item is None:
        for line in lines:
            s = line.strip()
            if "公共维护基金" in s or "押金" in s:
                item = s
                break

    # 年份：优先从票据抬头日期区域获取“2025年”
    m_year = re.search(r"(20\d{2})\s*年", text)
    receipt_year = f"{m_year.group(1)}年" if m_year else None

    # 月份范围：例如“2025年4-6月份公共维护基金”
    m_range = re.search(r"(\d{1,2})\s*[-~～]\s*(\d{1,2})\s*月", text)
    receipt_month_range = None
    if m_range:
        start_m = int(m_range.group(1))
        end_m = int(m_range.group(2))
        receipt_month_range = f"{start_m}-{end_m}月"

    return item, receipt_year, receipt_month_range


def extract_audit_report_info(text: str) -> Optional[str]:
    """
    提取审核报告里的项目名称，用于命名：
      - (审核报告)+项目名称.pdf
      - 或 (结算审核报告)+项目名称.pdf

    优先从“项目名称 / 工程名称”字段中取；
    如无，则从开头几行中尝试找到包含“工程”的那一行作为项目名。
    """
    # 1) 结构化字段：项目名称 / 工程名称
    m_proj = re.search(r"(项目名称|工程名称)\s*[:：]?\s*([^\n\r]{4,60})", text)
    if m_proj:
        return m_proj.group(2).strip()

    # 2) 从前几行文本里找一行“工程”标题
    head = text.splitlines()[:15]  # 只看前 15 行
    for line in head:
        s = line.strip()
        if len(s) < 4:
            continue
        # 典型封面标题包含“工程”，例如“象屿保税区二期对外道路交通改善工程BD匝道...”
        if "工程" in s and "报告" not in s:
            return s

    return None


def analyze_pdf_text(text: str) -> PdfInfo:
    """综合识别类型并提取关键信息。"""
    doc_type = detect_doc_type(text)

    info = PdfInfo(raw_text=text, doc_type=doc_type)

    if doc_type == "contract":
        info.contract_number, info.project_name = extract_contract_info(text)
    elif doc_type == "invoice":
        # 非劳务费发票：可能是建筑服务、工程服务等，后面用于“(发票)+项目名称”
        info.month_text, info.invoice_keyword = extract_invoice_info(text)
        # 复用审核报告的项目名称提取逻辑，尝试从正文中取工程项目名
        if info.project_name is None:
            info.project_name = extract_audit_report_info(text)
    elif doc_type == "audit_report":
        info.project_name = extract_audit_report_info(text)
    elif doc_type == "labor_fee":
        # 劳务费类：提取“YYYY年M月”和类型（审批材料/付款申请单/发票）
        info.year_text, info.month_text = extract_year_month(text)
        info.labor_fee_doc_type = detect_labor_fee_doc_type(text)
        info.invoice_keyword = "劳务费"
    elif doc_type == "receipt":
        info.receipt_item, info.receipt_year, info.receipt_month_range = extract_receipt_info(text)

    return info


