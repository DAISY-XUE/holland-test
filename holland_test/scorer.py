"""霍兰德职业兴趣测试评分系统"""

from dataclasses import dataclass
from typing import Dict, Tuple

from .questions import HOLLAND_TYPES


@dataclass
class TestResult:
    """测试结果"""
    scores: Dict[str, int]  # 每种类型的得分
    percentages: Dict[str, float]  # 每种类型的百分比
    primary_type: str  # 主要类型
    secondary_type: str  # 次要类型
    tertiary_type: str  # 第三类型
    type_combination: str  # 类型组合代码


def calculate_scores(answers: Dict[int, bool]) -> Dict[str, int]:
    """
    计算各类型得分
    
    Args:
        answers: 题目ID到答案的映射，True表示"是"，False表示"否"
        
    Returns:
        每种类型的得分（答"是"的题目数量）
    """
    from .questions import QUESTIONS
    
    scores = {type_code: 0 for type_code in HOLLAND_TYPES.keys()}
    type_counts = {type_code: 0 for type_code in HOLLAND_TYPES.keys()}
    
    # 计算每个类型的总题目数和得分
    for question in QUESTIONS:
        type_counts[question.type] += 1
        if answers.get(question.id, False):
            scores[question.type] += 1
    
    return scores


def calculate_percentages(scores: Dict[str, int], type_counts: Dict[str, int]) -> Dict[str, float]:
    """
    计算各类型的百分比
    
    Args:
        scores: 各类型得分
        type_counts: 各类型题目总数
        
    Returns:
        各类型的百分比
    """
    percentages = {}
    for type_code in HOLLAND_TYPES.keys():
        count = type_counts.get(type_code, 1)
        score = scores.get(type_code, 0)
        percentages[type_code] = (score / count * 100) if count > 0 else 0.0
    return percentages


def determine_types(scores: Dict[str, int]) -> Tuple[str, str, str]:
    """
    确定主要、次要和第三类型
    
    Args:
        scores: 各类型得分
        
    Returns:
        (主要类型, 次要类型, 第三类型)
    """
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_types[0][0]
    secondary = sorted_types[1][0] if len(sorted_types) > 1 else primary
    tertiary = sorted_types[2][0] if len(sorted_types) > 2 else secondary
    
    return primary, secondary, tertiary


def score_test(answers: Dict[int, bool]) -> TestResult:
    """
    计算测试结果
    
    Args:
        answers: 题目ID到答案的映射（True/False）
        
    Returns:
        测试结果对象
    """
    from .questions import get_question_count_by_type
    
    scores = calculate_scores(answers)
    type_counts = get_question_count_by_type()
    percentages = calculate_percentages(scores, type_counts)
    primary, secondary, tertiary = determine_types(scores)
    type_combination = primary + secondary + tertiary
    
    return TestResult(
        scores=scores,
        percentages=percentages,
        primary_type=primary,
        secondary_type=secondary,
        tertiary_type=tertiary,
        type_combination=type_combination,
    )
