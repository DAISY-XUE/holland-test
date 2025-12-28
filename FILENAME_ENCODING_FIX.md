# 文件名乱码问题修复说明

## 🔍 问题原因

GitHub仓库中显示乱码文件名（如 `\345\246\202\344\275\225...`）的原因是：

1. **中文文件名编码问题**：Git在存储中文文件名时，会使用UTF-8编码，但在某些情况下会显示为八进制转义序列
2. **Git配置问题**：Git的`core.quotepath`设置可能导致中文路径显示为转义序列
3. **终端编码问题**：Windows PowerShell的编码设置可能与Git不匹配

## ✅ 解决方案

### 已修复的文件

以下中文文件名已重命名为英文：

| 原文件名（中文） | 新文件名（英文） |
|----------------|-----------------|
| `如何查看仓库URL.md` | `HOW_TO_VIEW_REPO_URL.md` |
| `运行指南.md` | `RUNNING_GUIDE.md` |

### 如何查看正确的文件名

在GitHub上，这些文件现在会显示为：
- `HOW_TO_VIEW_REPO_URL.md` - 如何查看仓库URL的指南
- `RUNNING_GUIDE.md` - 运行指南

## 🔧 防止未来出现乱码的方法

### 方法1：使用英文文件名（推荐）

创建新文件时，使用英文文件名：
- ✅ `README.md`
- ✅ `HOW_TO_USE.md`
- ✅ `INSTALLATION.md`
- ❌ `使用说明.md`
- ❌ `安装指南.md`

### 方法2：配置Git编码

设置Git使用UTF-8编码：

```bash
git config --global core.quotepath false
git config --global gui.encoding utf-8
git config --global i18n.commitencoding utf-8
git config --global i18n.logoutputencoding utf-8
```

### 方法3：设置PowerShell编码

在PowerShell中设置UTF-8编码：

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
```

## 📝 当前状态

- ✅ 已创建英文版本的文件
- ✅ 已提交到Git仓库
- ⚠️ 旧的中文文件名可能仍在Git历史中，但不影响使用

## 🎯 建议

1. **使用英文文件名**：避免跨平台和跨工具的编码问题
2. **文件内容可以用中文**：文件名用英文，但文件内容可以用中文
3. **使用描述性的英文名**：如 `HOW_TO_VIEW_REPO_URL.md` 比 `URL.md` 更清晰

## 📚 相关文件

- `HOW_TO_VIEW_REPO_URL.md` - 如何查看仓库URL
- `RUNNING_GUIDE.md` - 运行指南
- `README.md` - 项目说明（已使用英文名）

