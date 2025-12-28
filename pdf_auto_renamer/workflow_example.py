"""
工作流示例：展示如何将 PDF 自动重命名功能整合到工作流中

使用 Prefect 作为工作流引擎（轻量级、易用）
安装：pip install prefect
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

from .config import settings
from .pdf_reader import extract_text_from_pdf
from .classifier import analyze_pdf_text
from .renamer import rename_pdf_file


logger = logging.getLogger(__name__)


# ==================== 任务定义 ====================

@task(
    name="提取PDF文本",
    description="从PDF文件中提取文本内容",
    retries=2,  # 失败重试2次
    retry_delay_seconds=5,  # 重试间隔5秒
    cache_key_fn=task_input_hash,  # 相同文件不重复处理
    cache_expiration=timedelta(hours=24),  # 缓存24小时
)
def extract_text_task(pdf_path: Path) -> str:
    """任务1：提取PDF文本"""
    logger.info(f"开始提取文本：{pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    logger.info(f"文本提取完成，长度：{len(text)} 字符")
    return text


@task(
    name="分析PDF内容",
    description="识别PDF类型并提取关键信息",
    retries=1,
)
def analyze_pdf_task(text: str) -> dict:
    """任务2：分析PDF内容"""
    logger.info("开始分析PDF内容")
    info = analyze_pdf_text(text)
    # 转换为字典以便在工作流中传递
    result = {
        "doc_type": info.doc_type,
        "contract_number": info.contract_number,
        "project_name": info.project_name,
        "month_text": info.month_text,
        "invoice_keyword": info.invoice_keyword,
        "year_text": info.year_text,
        "labor_fee_doc_type": info.labor_fee_doc_type,
        "receipt_item": info.receipt_item,
        "receipt_year": info.receipt_year,
        "receipt_month_range": info.receipt_month_range,
        "raw_text": info.raw_text[:1000],  # 只保存前1000字符，避免过大
    }
    logger.info(f"分析完成，文档类型：{info.doc_type}")
    return result


@task(
    name="重命名PDF文件",
    description="根据分析结果重命名PDF文件",
    retries=1,
)
def rename_pdf_task(pdf_path: Path, pdf_info: dict) -> Optional[Path]:
    """任务3：重命名PDF文件"""
    logger.info(f"开始重命名：{pdf_path}")
    # 将字典转换回 PdfInfo 对象
    from .classifier import PdfInfo
    info = PdfInfo(
        raw_text=pdf_info.get("raw_text", ""),
        doc_type=pdf_info["doc_type"],
        contract_number=pdf_info.get("contract_number"),
        project_name=pdf_info.get("project_name"),
        month_text=pdf_info.get("month_text"),
        invoice_keyword=pdf_info.get("invoice_keyword"),
        year_text=pdf_info.get("year_text"),
        labor_fee_doc_type=pdf_info.get("labor_fee_doc_type"),
        receipt_item=pdf_info.get("receipt_item"),
        receipt_year=pdf_info.get("receipt_year"),
        receipt_month_range=pdf_info.get("receipt_month_range"),
    )
    new_path = rename_pdf_file(pdf_path, info)
    if new_path:
        logger.info(f"重命名成功：{new_path}")
    return new_path


@task(
    name="发送通知",
    description="处理完成后发送通知（可选）",
)
def send_notification_task(pdf_path: Path, success: bool, message: str = ""):
    """任务4：发送通知（示例）"""
    if success:
        logger.info(f"✅ PDF处理成功：{pdf_path.name}")
        # 这里可以集成：
        # - 邮件通知
        # - 企业微信/钉钉通知
        # - 数据库记录
        # - 等等
    else:
        logger.warning(f"❌ PDF处理失败：{pdf_path.name} - {message}")


# ==================== 工作流定义 ====================

@flow(
    name="PDF自动重命名工作流",
    description="完整的PDF处理工作流：提取文本 -> 分析内容 -> 重命名 -> 通知",
    log_prints=True,
)
def pdf_rename_workflow(pdf_path: Path) -> dict:
    """
    主工作流：处理单个PDF文件
    
    工作流步骤：
    1. 提取PDF文本
    2. 分析PDF内容（识别类型、提取信息）
    3. 重命名PDF文件
    4. 发送处理结果通知
    
    返回：
        dict: 包含处理结果的字典
    """
    try:
        # 步骤1：提取文本
        text = extract_text_task(pdf_path)
        
        # 步骤2：分析内容
        pdf_info = analyze_pdf_task(text)
        
        # 步骤3：重命名
        new_path = rename_pdf_task(pdf_path, pdf_info)
        
        # 步骤4：发送通知
        success = new_path is not None
        send_notification_task(pdf_path, success, "处理完成")
        
        return {
            "success": success,
            "original_path": str(pdf_path),
            "new_path": str(new_path) if new_path else None,
            "doc_type": pdf_info["doc_type"],
        }
    except Exception as e:
        logger.exception(f"工作流执行失败：{e}")
        send_notification_task(pdf_path, False, str(e))
        return {
            "success": False,
            "error": str(e),
            "original_path": str(pdf_path),
        }


@flow(
    name="批量处理PDF工作流",
    description="批量处理目录中的所有PDF文件",
)
def batch_process_workflow(watch_dir: Optional[Path] = None) -> dict:
    """
    批量处理工作流：扫描目录并处理所有PDF文件
    
    参数：
        watch_dir: 要处理的目录（默认使用配置中的WATCH_DIR）
    
    返回：
        dict: 包含处理统计的字典
    """
    if watch_dir is None:
        watch_dir = settings.WATCH_DIR
    
    logger.info(f"开始批量处理：{watch_dir}")
    
    # 查找所有PDF文件
    if settings.RECURSIVE:
        pdf_files = list(watch_dir.rglob("*.pdf"))
    else:
        pdf_files = list(watch_dir.glob("*.pdf"))
    
    # 过滤临时文件
    pdf_files = [f for f in pdf_files if not f.name.startswith("~$")]
    
    logger.info(f"找到 {len(pdf_files)} 个PDF文件")
    
    results = []
    success_count = 0
    fail_count = 0
    
    # 并行处理（Prefect会自动管理并发）
    for pdf_path in pdf_files:
        result = pdf_rename_workflow(pdf_path)
        results.append(result)
        if result.get("success"):
            success_count += 1
        else:
            fail_count += 1
    
    summary = {
        "total": len(pdf_files),
        "success": success_count,
        "failed": fail_count,
        "results": results,
    }
    
    logger.info(f"批量处理完成：成功 {success_count}，失败 {fail_count}")
    return summary


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 示例1：处理单个文件
    # pdf_rename_workflow(Path("C:/Users/DELL/Desktop/扫描文件夹/test.pdf"))
    
    # 示例2：批量处理
    # batch_process_workflow()
    
    # 示例3：启动Prefect UI查看工作流执行情况
    # 运行：prefect server start
    # 然后访问：http://localhost:4200
    pass

