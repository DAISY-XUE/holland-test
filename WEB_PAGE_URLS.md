# Web页面访问地址

## 📍 本地访问

### 方式1：直接打开文件
双击以下文件即可在浏览器中打开：
```
holland_test_preview.html
```

### 方式2：使用文件路径
在浏览器地址栏输入：
```
file:///C:/Users/DELL/Desktop/AI编程类文件夹/holland_test_preview.html
```

### 方式3：使用PowerShell打开
```powershell
$file = (Resolve-Path "holland_test_preview.html").Path
Start-Process $file
```

## 🌐 GitHub在线访问

### GitHub仓库地址
- **仓库主页**：https://github.com/DAISY-XUE/holland-test
- **预览文件**：https://github.com/DAISY-XUE/holland-test/blob/main/holland_test_preview.html

### GitHub Pages（如果启用）
如果启用了GitHub Pages，可以通过以下地址访问：
- **Pages地址**：https://DAISY-XUE.github.io/holland-test/holland_test_preview.html

**启用GitHub Pages步骤**：
1. 访问：https://github.com/DAISY-XUE/holland-test/settings/pages
2. 在"Source"部分选择分支（通常是`main`）
3. 选择文件夹（通常是`/ (root)`）
4. 点击"Save"
5. 等待几分钟后即可通过Pages地址访问

## 🔧 本地服务器运行（推荐）

### 使用Python启动本地服务器

在项目目录下运行：

```bash
# Python 3
python -m http.server 8000

# 或者 Python 2
python -m SimpleHTTPServer 8000
```

然后在浏览器中访问：
```
http://localhost:8000/holland_test_preview.html
```

### 使用Node.js（如果已安装）

```bash
npx http-server -p 8000
```

访问：http://localhost:8000/holland_test_preview.html

## 📝 快速访问

**最简单的方式**：
1. 找到 `holland_test_preview.html` 文件
2. 双击打开
3. 即可在浏览器中查看

## ⚠️ 注意事项

1. **本地文件访问**：直接打开HTML文件即可，无需服务器
2. **GitHub访问**：需要先推送文件到GitHub仓库
3. **GitHub Pages**：需要手动启用，启用后可以通过网页访问

## 🎯 推荐方式

- **开发测试**：直接双击HTML文件打开
- **在线分享**：使用GitHub Pages或GitHub文件查看
- **本地演示**：使用Python HTTP服务器


