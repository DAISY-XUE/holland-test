#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动本地HTTP服务器来打开测试页面
这样可以避免浏览器直接打开文件时的限制
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

# 尝试的端口列表（如果8000被占用，会自动尝试其他端口）
PORTS = [8000, 8080, 8888, 3000, 5000]

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    # 切换到脚本所在目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 检查文件是否存在
    html_file = script_dir / "holland_test_preview.html"
    if not html_file.exists():
        print(f"❌ 错误：找不到文件 {html_file}")
        print(f"   请确保 holland_test_preview.html 文件在当前目录下")
        input("\n按回车键退出...")
        return
    
    # 尝试找到一个可用的端口
    port = None
    for test_port in PORTS:
        try:
            test_server = socketserver.TCPServer(("", test_port), MyHTTPRequestHandler)
            test_server.server_close()
            port = test_port
            break
        except OSError:
            continue
    
    if port is None:
        print("❌ 错误：所有常用端口都被占用")
        print("   请关闭其他使用以下端口的程序：")
        for p in PORTS:
            print(f"   - 端口 {p}")
        input("\n按回车键退出...")
        return
    
    if port != PORTS[0]:
        print(f"⚠️  端口 {PORTS[0]} 被占用，使用端口 {port} 代替")
    
    print("=" * 60)
    print("启动本地HTTP服务器")
    print("=" * 60)
    print(f"\n服务器地址: http://localhost:{port}")
    print(f"测试页面: http://localhost:{port}/holland_test_preview.html")
    print("\n正在启动服务器...")
    print("提示：按 Ctrl+C 可以停止服务器\n")
    
    try:
        with socketserver.TCPServer(("", port), MyHTTPRequestHandler) as httpd:
            # 自动打开浏览器
            url = f"http://localhost:{port}/holland_test_preview.html"
            print(f"正在打开浏览器: {url}")
            webbrowser.open(url)
            
            print("\n✅ 服务器已启动！")
            print("浏览器应该已经自动打开测试页面")
            print("\n如果浏览器没有自动打开，请手动访问：")
            print(f"   {url}")
            print("\n按 Ctrl+C 停止服务器\n")
            
            # 保持服务器运行
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
    except OSError as e:
        print(f"\n❌ 启动服务器时出错: {e}")
        print("   这不应该发生，因为已经检查了端口可用性")
        input("\n按回车键退出...")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()

