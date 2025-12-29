"""专业报告生成器"""

from typing import Dict

from .analysis import (
    TYPE_COMBINATIONS,
    analyze_career_positioning,
    analyze_career_tendency,
    generate_career_guidance,
    get_career_suggestions,
    get_type_description,
)
from .questions import HOLLAND_TYPES
from .scorer import TestResult


def generate_professional_report(result: TestResult) -> str:
    """
    生成专业的测试报告
    
    Args:
        result: 测试结果
        
    Returns:
        完整的报告文本
    """
    report = []
    
    # 报告头部
    report.append("=" * 80)
    report.append("霍兰德职业兴趣测试 - 专业评估报告")
    report.append("Holland Career Interest Test - Professional Assessment Report")
    report.append("=" * 80)
    report.append("")
    
    # 一、测试概况
    report.append("一、测试概况")
    report.append("-" * 80)
    report.append(f"测试类型：霍兰德职业兴趣测试（RIASEC模型）")
    report.append(f"题目总数：120题")
    report.append(f"答题方式：是/否")
    report.append("")
    
    # 二、得分统计
    report.append("二、各类型得分统计")
    report.append("-" * 80)
    sorted_scores = sorted(result.scores.items(), key=lambda x: x[1], reverse=True)
    report.append(f"{'类型':<20} {'得分':<10} {'题目数':<10} {'百分比':<10} {'强度':<10}")
    report.append("-" * 80)
    for type_code, score in sorted_scores:
        type_name = HOLLAND_TYPES[type_code]
        total_questions = 20  # 每个类型20题
        percentage = result.percentages[type_code]
        
        # 强度等级
        if percentage >= 70:
            strength = "很强"
            bar = "█" * int(percentage / 5)
        elif percentage >= 50:
            strength = "较强"
            bar = "█" * int(percentage / 5)
        elif percentage >= 30:
            strength = "中等"
            bar = "█" * int(percentage / 5)
        else:
            strength = "较弱"
            bar = "█" * int(percentage / 5)
        
        report.append(f"{type_name:<20} {score:<10} {total_questions:<10} {percentage:>6.1f}%{'':<4} {strength:<10}")
        report.append(f"{'':<20} {bar}")
    
    report.append("")
    
    # 三、核心结果
    report.append("三、核心结果")
    report.append("-" * 80)
    primary_name = HOLLAND_TYPES[result.primary_type]
    secondary_name = HOLLAND_TYPES[result.secondary_type]
    tertiary_name = HOLLAND_TYPES[result.tertiary_type]
    
    report.append(f"主要类型：{primary_name} ({result.primary_type})")
    report.append(f"  得分：{result.scores[result.primary_type]}/20 ({result.percentages[result.primary_type]:.1f}%)")
    report.append("")
    report.append(f"次要类型：{secondary_name} ({result.secondary_type})")
    report.append(f"  得分：{result.scores[result.secondary_type]}/20 ({result.percentages[result.secondary_type]:.1f}%)")
    report.append("")
    report.append(f"第三类型：{tertiary_name} ({result.tertiary_type})")
    report.append(f"  得分：{result.scores[result.tertiary_type]}/20 ({result.percentages[result.tertiary_type]:.1f}%)")
    report.append("")
    report.append(f"类型代码：{result.type_combination}")
    report.append("")
    
    # 类型组合分析
    if result.type_combination in TYPE_COMBINATIONS:
        combo = TYPE_COMBINATIONS[result.type_combination]
        report.append(f"类型组合：{combo['name']}")
        report.append(f"组合特征：{combo['description']}")
        report.append(f"典型职业：{', '.join(combo['careers'][:5])}")
        report.append("")
    
    # 四、职业兴趣分析
    report.append("四、职业兴趣分析")
    report.append("-" * 80)
    primary_desc = get_type_description(result.primary_type)
    report.append(f"【{primary_desc['name']}】")
    report.append(f"核心特点：{primary_desc['characteristics']}")
    report.append(f"喜欢的工作：{primary_desc['likes']}")
    report.append(f"不喜欢的工作：{primary_desc['dislikes']}")
    report.append(f"适合的工作环境：{primary_desc['work_environment']}")
    report.append(f"核心能力：{primary_desc['skills']}")
    report.append(f"价值观：{primary_desc['values']}")
    report.append("")
    
    # 五、职业倾向分析
    report.append("五、职业倾向分析")
    report.append("-" * 80)
    tendency = analyze_career_tendency(result)
    report.append(f"主导倾向：{HOLLAND_TYPES[tendency['dominant_type']]}")
    report.append(f"辅助倾向：{', '.join([HOLLAND_TYPES[t] for t in tendency['supporting_types']])}")
    report.append("")
    report.append("各类型强度：")
    for type_code, level in tendency['strength_level'].items():
        report.append(f"  {HOLLAND_TYPES[type_code]}: {level} ({result.percentages[type_code]:.1f}%)")
    report.append("")
    report.append(f"工作风格：{tendency['work_style']}")
    report.append(f"团队偏好：{tendency['team_preference']}")
    report.append("")
    
    # 六、职业定位分析
    report.append("六、职业定位分析")
    report.append("-" * 80)
    positioning = analyze_career_positioning(result)
    report.append(f"主要定位：{positioning['primary_positioning']}")
    report.append("")
    report.append("适合的行业领域：")
    for i, industry in enumerate(positioning['suitable_industries'], 1):
        report.append(f"  {i}. {industry}")
    report.append("")
    report.append(f"职业层级建议：{positioning['career_level']}")
    report.append("")
    
    # 七、推荐职业方向
    report.append("七、推荐职业方向")
    report.append("-" * 80)
    all_careers = set()
    for type_code in [result.primary_type, result.secondary_type, result.tertiary_type]:
        careers = get_career_suggestions(type_code)
        all_careers.update(careers)
    
    # 按类型分组显示
    report.append(f"【{HOLLAND_TYPES[result.primary_type]}】相关职业：")
    primary_careers = get_career_suggestions(result.primary_type)
    for i, career in enumerate(primary_careers[:15], 1):
        report.append(f"  {i:2d}. {career}")
    report.append("")
    
    if result.secondary_type != result.primary_type:
        report.append(f"【{HOLLAND_TYPES[result.secondary_type]}】相关职业：")
        secondary_careers = get_career_suggestions(result.secondary_type)
        for i, career in enumerate(secondary_careers[:10], 1):
            report.append(f"  {i:2d}. {career}")
        report.append("")
    
    report.append("综合推荐职业（结合三个类型）：")
    combined_careers = sorted(all_careers)
    for i, career in enumerate(combined_careers[:20], 1):
        report.append(f"  {i:2d}. {career}")
    report.append("")
    
    # 八、职业指导建议
    report.append("八、职业指导建议")
    report.append("-" * 80)
    guidance = generate_career_guidance(result)
    
    report.append("【立即行动建议】")
    for i, action in enumerate(guidance['immediate_actions'], 1):
        report.append(f"  {i}. {action}")
    report.append("")
    
    report.append("【技能发展建议】")
    for i, skill in enumerate(guidance['skill_development'], 1):
        report.append(f"  {i}. {skill}")
    report.append("")
    
    report.append("【职业路径建议】")
    for i, path in enumerate(guidance['career_path'], 1):
        report.append(f"  {i}. {path}")
    report.append("")
    
    report.append("【工作环境建议】")
    for i, advice in enumerate(guidance['workplace_advice'], 1):
        report.append(f"  {i}. {advice}")
    report.append("")
    
    # 九、测试说明
    report.append("九、测试说明")
    report.append("-" * 80)
    report.append("1. 本测试基于霍兰德职业兴趣理论（RIASEC模型），是国际公认的职业兴趣评估工具。")
    report.append("2. 测试结果反映的是职业兴趣倾向，而非能力评估。")
    report.append("3. 职业选择应综合考虑兴趣、能力、价值观、市场需求等多方面因素。")
    report.append("4. 建议结合其他评估工具（如能力测试、性格测试等）进行综合评估。")
    report.append("5. 职业发展是一个动态过程，建议定期重新评估。")
    report.append("6. 本报告仅供参考，具体职业选择请结合个人实际情况和专业咨询。")
    report.append("")
    
    # 报告尾部
    report.append("=" * 80)
    report.append("报告生成时间：请填写实际时间")
    report.append("本报告基于您的测试结果生成，希望对您的职业规划有所帮助。")
    report.append("=" * 80)
    
    return "\n".join(report)


def generate_summary_report(result: TestResult) -> str:
    """
    生成简要报告（适合快速查看）
    
    Args:
        result: 测试结果
        
    Returns:
        简要报告文本
    """
    report = []
    report.append("=" * 60)
    report.append("霍兰德职业兴趣测试 - 简要报告")
    report.append("=" * 60)
    report.append("")
    
    primary_name = HOLLAND_TYPES[result.primary_type]
    report.append(f"主要类型：{primary_name} ({result.primary_type})")
    report.append(f"类型组合：{result.type_combination}")
    report.append("")
    
    report.append("各类型得分：")
    sorted_scores = sorted(result.scores.items(), key=lambda x: x[1], reverse=True)
    for type_code, score in sorted_scores:
        type_name = HOLLAND_TYPES[type_code]
        percentage = result.percentages[type_code]
        report.append(f"  {type_name}: {score}/20 ({percentage:.1f}%)")
    report.append("")
    
    report.append("推荐职业方向（前10项）：")
    all_careers = set()
    for type_code in [result.primary_type, result.secondary_type]:
        careers = get_career_suggestions(type_code)
        all_careers.update(careers)
    
    for i, career in enumerate(sorted(all_careers)[:10], 1):
        report.append(f"  {i:2d}. {career}")
    
    report.append("")
    report.append("=" * 60)
    
    return "\n".join(report)


