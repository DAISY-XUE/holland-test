# 🚀 运行指南

## 方式一：工作流版本（推荐）

### 步骤1：安装依赖

打开 PowerShell，在项目目录下运行：

```powershell
pip install -r requirements.txt
```

如果遇到网络问题，可以使用国内镜像：

```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 步骤2：运行工作流

```powershell
python -m pdf_auto_renamer.workflow_main
```

### 步骤3：使用程序

1. 程序会自动监控：`C:\Users\你的用户名\Desktop\扫描文件夹`
2. 将PDF文件放入该文件夹
3. 程序会自动识别并重命名

### 步骤4（可选）：启动Prefect UI监控

在**新的PowerShell窗口**中运行：

```powershell
prefect server start
```

然后打开浏览器访问：http://localhost:4200 查看工作流执行情况

---

## 方式二：原有版本（简单直接）

如果不想使用工作流，可以使用原有版本：

```powershell
python -m pdf_auto_renamer.main
```

功能相同，但缺少工作流的重试、缓存等高级功能。

---

## 📋 运行前检查清单

- [ ] Python已安装（建议3.8+）
- [ ] 已安装依赖包（运行 `pip install -r requirements.txt`）
- [ ] 监控目录存在：`C:\Users\你的用户名\Desktop\扫描文件夹`（不存在会自动创建）

---

## ❓ 常见问题

### Q1: 提示"找不到模块"？

**解决**：确保已安装依赖
```powershell
pip install -r requirements.txt
```

### Q2: 提示"无法连接到代理"？

**解决**：使用国内镜像源
```powershell
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 程序运行但没有反应？

**解决**：
1. 检查监控目录是否存在
2. 确保有PDF文件放入监控目录
3. 查看日志文件：`扫描文件夹\auto_renamer.log`

### Q4: 如何停止程序？

**解决**：在运行程序的终端按 `Ctrl+C`

---

## 🎯 快速测试

1. 运行程序：
   ```powershell
   python -m pdf_auto_renamer.workflow_main
   ```

2. 在另一个窗口，将测试PDF文件复制到：
   ```
   C:\Users\你的用户名\Desktop\扫描文件夹
   ```

3. 观察程序输出，应该会看到处理日志

---

## 📝 运行示例输出

正常运行时，你会看到类似输出：

```
============================================================
🚀 启动PDF工作流监控系统
============================================================
监控目录：C:\Users\DELL\Desktop\扫描文件夹
递归扫描：False
已处理目录：_processed

💡 提示：
   - 将PDF文件放入监控目录即可自动处理
   - 按 Ctrl+C 停止监控
   - 查看Prefect UI：运行 'prefect server start' 后访问 http://localhost:4200
============================================================
2024-01-01 10:00:00 [INFO] 开始监控目录...
============================================================
检测到新PDF文件，启动工作流处理：test.pdf
============================================================
开始提取文本：test.pdf
文本提取完成，长度：1234 字符
开始分析PDF内容
分析完成，文档类型：contract
开始重命名：test.pdf
重命名成功：HT-2024-001_项目名称.pdf
✅ PDF处理成功：test.pdf
```

---

## 💡 提示

- 程序会持续运行，直到你按 `Ctrl+C` 停止
- 日志同时输出到控制台和文件
- 处理后的文件可能会移动到 `_processed` 子目录（如果配置了）

