"""霍兰德职业兴趣测试主程序 - 专业版"""

from datetime import datetime
from typing import Dict, Optional

from .questions import get_all_questions
from .report_generator import generate_professional_report, generate_summary_report
from .scorer import score_test


def print_welcome():
    """打印欢迎信息"""
    print("=" * 80)
    print("欢迎参加霍兰德职业兴趣测试")
    print("Holland Career Interest Test")
    print("=" * 80)
    print()
    print("【测试简介】")
    print("霍兰德职业兴趣测试（Holland Career Interest Test）")
    print("是基于RIASEC模型的国际权威职业兴趣评估工具，")
    print("被广泛应用于企业招聘、职业规划、教育咨询等领域。")
    print()
    print("【测试说明】")
    print("• 测试共有120道题目，每个职业兴趣类型20题")
    print("• 请根据您的真实想法和感受，回答\"是\"或\"否\"")
    print("• 请诚实回答，这将帮助您获得更准确的结果")
    print("• 建议在安静、不受干扰的环境下完成测试")
    print("• 预计完成时间：15-20分钟")
    print()
    print("【答题方式】")
    print("• 输入 Y 或 y 或 1 或 是 表示\"是\"")
    print("• 输入 N 或 n 或 0 或 否 表示\"否\"")
    print("• 输入 Q 或 q 可以随时退出测试")
    print()
    print("=" * 80)
    print()


def parse_answer(answer: str) -> Optional[bool]:
    """
    解析用户答案
    
    Returns:
        True表示"是"，False表示"否"，None表示无效输入或退出
    """
    answer = answer.strip().lower()
    
    # 退出命令
    if answer in ['q', 'quit', 'exit', '退出']:
        return None
    
    # 表示"是"的输入
    if answer in ['y', 'yes', '1', '是', 'true', 't']:
        return True
    
    # 表示"否"的输入
    if answer in ['n', 'no', '0', '否', 'false', 'f']:
        return False
    
    # 无效输入
    return None


def get_answer(question_num: int, total: int) -> Optional[bool]:
    """获取用户答案，确保输入有效"""
    while True:
        answer_input = input(f"[{question_num}/{total}] 请输入您的答案 (Y/N 或 Q退出): ").strip()
        parsed = parse_answer(answer_input)
        
        if parsed is None:
            if answer_input.lower() in ['q', 'quit', 'exit', '退出']:
                return None  # 用户要求退出
            print("无效输入！请输入 Y(是) 或 N(否) 或 Q(退出)")
            continue
        
        return parsed


def conduct_test() -> Optional[Dict[int, bool]]:
    """进行测试，收集答案"""
    answers = {}
    questions = get_all_questions()
    total = len(questions)
    
    print("\n" + "=" * 80)
    print("开始测试...")
    print("=" * 80)
    print()
    print("请根据您的真实想法回答以下问题。")
    print("注意：请回答\"是\"或\"否\"，不要过度思考，第一反应往往更准确。")
    print()
    print("-" * 80)
    print()
    
    for i, question in enumerate(questions, 1):
        print(f"题目 {i}/{total}")
        print(f"{question.text}")
        print()
        
        answer = get_answer(i, total)
        
        if answer is None:  # 用户要求退出
            confirm = input("确定要退出测试吗？未完成的进度将丢失 (Y/N): ").strip().lower()
            if confirm in ['y', 'yes', '是']:
                return None
            continue
        
        answers[question.id] = answer
        
        # 每10题显示一次进度
        if i % 10 == 0:
            print(f"\n已完成 {i}/{total} 题 ({i/total*100:.1f}%)，继续加油！\n")
    
    return answers


def save_result(report: str, filename: str = None):
    """保存测试结果到文件"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"holland_test_result_{timestamp}.txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n✓ 结果已保存到文件: {filename}")
        return filename
    except Exception as e:
        print(f"\n✗ 保存文件失败: {e}")
        return None


def main():
    """主函数"""
    print_welcome()
    
    # 询问是否开始测试
    start = input("按回车键开始测试，或输入'q'退出: ").strip().lower()
    if start == 'q':
        print("测试已取消。")
        return
    
    # 进行测试
    answers = conduct_test()
    
    if answers is None:
        print("\n测试已中断。")
        return
    
    if len(answers) == 0:
        print("\n未完成任何题目，测试已取消。")
        return
    
    print("\n" + "=" * 80)
    print("测试完成！正在生成报告...")
    print("=" * 80)
    print()
    
    # 计算结果
    result = score_test(answers)
    
    # 生成专业报告
    report = generate_professional_report(result)
    
    # 替换报告中的时间戳
    timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    report = report.replace("报告生成时间：请填写实际时间", f"报告生成时间：{timestamp}")
    
    # 显示报告
    print(report)
    
    # 询问是否保存
    print("\n" + "=" * 80)
    save_choice = input("是否保存详细报告到文件？(Y/N): ").strip().lower()
    if save_choice in ['y', 'yes', '是', '1']:
        saved_file = save_result(report)
        if saved_file:
            print(f"您可以使用文本编辑器打开文件查看完整报告。")
    
    # 询问是否生成简要报告
    summary_choice = input("\n是否生成简要报告并保存？(Y/N): ").strip().lower()
    if summary_choice in ['y', 'yes', '是', '1']:
        summary_report = generate_summary_report(result)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_filename = f"holland_test_summary_{timestamp}.txt"
        save_result(summary_report, summary_filename)
    
    print("\n" + "=" * 80)
    print("感谢您参加霍兰德职业兴趣测试！")
    print("祝您职业发展顺利！")
    print("=" * 80)


if __name__ == "__main__":
    main()
