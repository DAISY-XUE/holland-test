#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试预览页面功能
验证120题测试是否正常工作
"""

import re
import sys
import io
from pathlib import Path

# 设置输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def test_html_structure():
    """测试HTML结构"""
    print("=" * 60)
    print("测试 HTML 结构")
    print("=" * 60)
    
    html_file = Path("holland_test_preview.html")
    if not html_file.exists():
        print("❌ holland_test_preview.html 文件不存在")
        return False
    
    content = html_file.read_text(encoding='utf-8')
    
    # 检查关键元素
    checks = [
        ("allQuestions 数组", "const allQuestions = [" in content),
        ("questionTypes 对象", 'const questionTypes = {' in content),
        ("totalQuestions", "const totalQuestions = allQuestions.length" in content),
        ("answers 对象", "let answers = {}" in content),
        ("updateQuestion 函数", "function updateQuestion()" in content),
        ("answerQuestion 函数", "function answerQuestion(answer)" in content),
        ("calculateScores 函数", "function calculateScores()" in content),
        ("showResults 函数", "function showResults()" in content),
        ("updateResultDisplay 函数", "function updateResultDisplay(result)" in content),
    ]
    
    all_ok = True
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
        if not result:
            all_ok = False
    
    return all_ok

def test_questions_count():
    """测试题目数量"""
    print("\n" + "=" * 60)
    print("测试题目数量")
    print("=" * 60)
    
    html_file = Path("holland_test_preview.html")
    content = html_file.read_text(encoding='utf-8')
    
    # 查找所有题目
    pattern = r'\{id: (\d+), text: "([^"]+)", type: "([RIASEC])"\}'
    matches = re.findall(pattern, content)
    
    print(f"找到题目数量: {len(matches)}")
    
    if len(matches) != 120:
        print(f"[ERROR] 题目数量不正确，应该是120题，实际找到{len(matches)}题")
        return False
    
    # 检查题目ID是否连续
    ids = [int(m[0]) for m in matches]
    expected_ids = list(range(1, 121))
    
    if ids != expected_ids:
        print(f"[ERROR] 题目ID不连续")
        return False
    
    # 检查每种类型的题目数量
    types = {}
    for match in matches:
        q_type = match[2]
        types[q_type] = types.get(q_type, 0) + 1
    
    print("\n各类型题目数量：")
    expected_count = 20
    all_ok = True
    for q_type in ['R', 'I', 'A', 'S', 'E', 'C']:
        count = types.get(q_type, 0)
        status = "[OK]" if count == expected_count else "[ERROR]"
        print(f"{status} {q_type}: {count}/20")
        if count != expected_count:
            all_ok = False
    
    return all_ok

def test_javascript_logic():
    """测试JavaScript逻辑"""
    print("\n" + "=" * 60)
    print("测试 JavaScript 逻辑")
    print("=" * 60)
    
    html_file = Path("holland_test_preview.html")
    content = html_file.read_text(encoding='utf-8')
    
    checks = [
        ("currentQuestion 初始化为 0", 'let currentQuestion = 0' in content),
        ("totalQuestions 使用 allQuestions.length", 'const totalQuestions = allQuestions.length' in content),
        ("答案检查逻辑", 'if (currentQuestion < totalQuestions)' in content),
        ("完成检查", 'if (currentQuestion >= totalQuestions)' in content),
        ("评分计算包含所有类型", 'scores = {R: 0, I: 0, A: 0, S: 0, E: 0, C: 0}' in content),
        ("百分比计算", 'percentages[type] = (scores[type] / 20) * 100' in content),
        ("类型排序", 'Object.entries(scores).sort((a, b) => b[1] - a[1])' in content),
    ]
    
    all_ok = True
    for name, result in checks:
        status = "[OK]" if result else "[ERROR]"
        print(f"{status} {name}")
        if not result:
            all_ok = False
    
    return all_ok

def test_result_display():
    """测试结果显示"""
    print("\n" + "=" * 60)
    print("测试结果显示")
    print("=" * 60)
    
    html_file = Path("holland_test_preview.html")
    content = html_file.read_text(encoding='utf-8')
    
    checks = [
        ("类型代码元素", 'id="type-code"' in content),
        ("结果卡片", 'class="result-card"' in content),
        ("类型徽章", 'class="type-badge"' in content),
        ("进度条", 'class="progress-bar"' in content),
        ("updateResultDisplay 函数", "function updateResultDisplay(result)" in content),
    ]
    
    all_ok = True
    for name, result in checks:
        status = "[OK]" if result else "[ERROR]"
        print(f"{status} {name}")
        if not result:
            all_ok = False
    
    return all_ok

def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("预览页面功能测试")
    print("=" * 60)
    print()
    
    results = {
        "HTML结构": test_html_structure(),
        "题目数量": test_questions_count(),
        "JavaScript逻辑": test_javascript_logic(),
        "结果显示": test_result_display(),
    }
    
    print("\n" + "=" * 60)
    print("测试结果总结")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for test_name, result in results.items():
        status = "[PASS] 通过" if result else "[FAIL] 失败"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] 所有测试通过！预览页面已准备好进行120题测试。")
        print("\n使用说明：")
        print("1. 在浏览器中打开 holland_test_preview.html")
        print("2. 点击'开始测试'按钮")
        print("3. 依次回答全部120道题目")
        print("4. 完成后会自动显示测试结果")
    else:
        print("⚠️  部分测试未通过，请检查代码。")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

