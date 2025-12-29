#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成包含所有题目的JavaScript代码
用于更新预览页面
"""

from holland_test.questions import QUESTIONS

def generate_questions_js():
    """生成JavaScript题目数组"""
    js_code = "        const allQuestions = [\n"
    
    for q in QUESTIONS:
        # 转义JavaScript字符串中的特殊字符
        text = q.text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        js_code += f'            {{id: {q.id}, text: "{text}", type: "{q.type}"}},\n'
    
    js_code += "        ];\n"
    
    return js_code

if __name__ == "__main__":
    print("// 自动生成的题目数据 - 共120题")
    print(generate_questions_js())
    print("\n// 题目类型映射")
    print("        const questionTypes = {")
    print('            "R": "现实型 (Realistic)",')
    print('            "I": "研究型 (Investigative)",')
    print('            "A": "艺术型 (Artistic)",')
    print('            "S": "社会型 (Social)",')
    print('            "E": "企业型 (Enterprising)",')
    print('            "C": "常规型 (Conventional)"')
    print("        };")

