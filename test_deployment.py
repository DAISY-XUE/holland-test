#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel 部署测试脚本
用于验证部署配置和文件结构
"""

import os
import json
import sys
from pathlib import Path

# 设置输出编码为 UTF-8（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def check_file_exists(filepath):
    """检查文件是否存在"""
    path = Path(filepath)
    exists = path.exists()
    size = path.stat().st_size if exists else 0
    return exists, size

def validate_vercel_json():
    """验证 vercel.json 配置"""
    print("=" * 60)
    print("[验证] vercel.json 配置")
    print("=" * 60)
    
    if not check_file_exists("vercel.json")[0]:
        print("[ERROR] vercel.json 文件不存在！")
        return False
    
    try:
        with open("vercel.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        print("[OK] vercel.json 文件存在且格式正确")
        
        # 检查关键配置
        issues = []
        
        if "builds" in config:
            issues.append("[WARN] 发现 'builds' 配置（静态站点不需要）")
        
        if "routes" in config:
            issues.append("[ERROR] 发现 'routes' 配置（应使用 'rewrites'）")
        
        if "rewrites" not in config:
            issues.append("[ERROR] 缺少 'rewrites' 配置")
        else:
            print("[OK] 找到 'rewrites' 配置")
            for rewrite in config["rewrites"]:
                print(f"   - {rewrite.get('source')} -> {rewrite.get('destination')}")
        
        if "headers" in config:
            print("[OK] 找到 'headers' 配置")
        
        if issues:
            print("\n[WARN] 发现的问题：")
            for issue in issues:
                print(f"   {issue}")
            return False
        
        print("\n[OK] vercel.json 配置正确！")
        return True
        
    except json.JSONDecodeError as e:
        print(f"[ERROR] vercel.json JSON 格式错误: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] 读取 vercel.json 时出错: {e}")
        return False

def check_required_files():
    """检查必需的文件"""
    print("\n" + "=" * 60)
    print("[检查] 必需文件")
    print("=" * 60)
    
    required_files = [
        "holland_test_preview.html",
        "vercel.json"
    ]
    
    optional_files = [
        "index.html",
        "README.md"
    ]
    
    all_ok = True
    
    print("\n必需文件：")
    for file in required_files:
        exists, size = check_file_exists(file)
        if exists:
            print(f"[OK] {file} ({size:,} 字节)")
        else:
            print(f"[ERROR] {file} - 文件不存在！")
            all_ok = False
    
    print("\n可选文件：")
    for file in optional_files:
        exists, size = check_file_exists(file)
        if exists:
            print(f"[OK] {file} ({size:,} 字节)")
        else:
            print(f"[SKIP] {file} - 不存在（可选）")
    
    return all_ok

def check_html_content():
    """检查 HTML 文件内容"""
    print("\n" + "=" * 60)
    print("[检查] HTML 文件内容")
    print("=" * 60)
    
    html_file = "holland_test_preview.html"
    exists, size = check_file_exists(html_file)
    
    if not exists:
        print(f"[ERROR] {html_file} 不存在")
        return False
    
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        checks = [
            ("DOCTYPE 声明", "<!DOCTYPE html>" in content),
            ("HTML 标签", "<html" in content),
            ("Head 标签", "<head" in content),
            ("Body 标签", "<body" in content),
            ("字符编码", "UTF-8" in content or "utf-8" in content),
        ]
        
        print(f"\n文件大小: {size:,} 字节")
        print("\n内容检查：")
        all_ok = True
        for check_name, result in checks:
            status = "[OK]" if result else "[ERROR]"
            print(f"   {status} {check_name}")
            if not result:
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"[ERROR] 读取 {html_file} 时出错: {e}")
        return False

def check_git_status():
    """检查 Git 状态"""
    print("\n" + "=" * 60)
    print("[检查] Git 状态")
    print("=" * 60)
    
    git_dir = Path(".git")
    if not git_dir.exists():
        print("[WARN] 未检测到 .git 目录（可能不是 Git 仓库）")
        print("   提示：需要先初始化 Git 仓库才能部署到 Vercel")
        return False
    
    print("[OK] 检测到 Git 仓库")
    
    # 检查是否有未提交的更改
    try:
        import subprocess
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            if result.stdout.strip():
                print("[WARN] 有未提交的更改：")
                for line in result.stdout.strip().split("\n"):
                    print(f"   {line}")
                print("\n   建议：提交更改后再部署")
            else:
                print("[OK] 工作目录干净（无未提交更改）")
            
            # 检查远程仓库
            remote_result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if remote_result.returncode == 0 and remote_result.stdout.strip():
                print("[OK] 已配置远程仓库：")
                for line in remote_result.stdout.strip().split("\n"):
                    print(f"   {line}")
            else:
                print("[WARN] 未配置远程仓库")
        else:
            print("[WARN] 无法检查 Git 状态")
            
    except FileNotFoundError:
        print("[WARN] Git 未安装或不在 PATH 中")
    except Exception as e:
        print(f"[WARN] 检查 Git 状态时出错: {e}")
    
    return True

def generate_test_report():
    """生成测试报告"""
    print("\n" + "=" * 60)
    print("[报告] 部署测试结果")
    print("=" * 60)
    
    results = {
        "vercel_json": validate_vercel_json(),
        "required_files": check_required_files(),
        "html_content": check_html_content(),
        "git_status": check_git_status()
    }
    
    print("\n" + "=" * 60)
    print("[总结] 测试结果")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for test_name, result in results.items():
        status = "[PASS] 通过" if result else "[FAIL] 失败"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] 所有检查通过！可以部署到 Vercel")
        print("\n下一步：")
        print("1. 提交更改: git add . && git commit -m 'Fix Vercel deployment'")
        print("2. 推送到 GitHub: git push")
        print("3. Vercel 会自动部署（如果已连接 GitHub）")
        print("4. 或手动在 Vercel 控制台触发部署")
    else:
        print("[WARN] 部分检查未通过，请修复后再部署")
        print("\n需要修复的问题：")
        for test_name, result in results.items():
            if not result:
                print(f"   - {test_name}")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    try:
        generate_test_report()
    except KeyboardInterrupt:
        print("\n\n[INFO] 测试被用户中断")
    except Exception as e:
        print(f"\n[ERROR] 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

