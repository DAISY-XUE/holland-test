# 工作流使用指南

## 🚀 快速开始

### 1. 安装依赖

```powershell
pip install -r requirements.txt
```

这将安装：
- `pdfplumber` - PDF文本提取
- `watchdog` - 文件监控
- `prefect` - 工作流引擎

### 2. 运行工作流版本

#### 方式1：使用工作流监控（推荐）

```powershell
python -m pdf_auto_renamer.workflow_main
```

**功能特点**：
- ✅ 自动监控目录，新PDF文件自动触发工作流
- ✅ 完整的任务重试机制
- ✅ 可视化监控（可选）
- ✅ 详细的日志记录

#### 方式2：使用原有监控方式

```powershell
python -m pdf_auto_renamer.main
```

**功能特点**：
- ✅ 简单直接，无需额外依赖
- ✅ 适合轻量级使用

---

## 📊 工作流功能说明

### 工作流步骤

当检测到新PDF文件时，工作流会自动执行以下步骤：

```
1. 提取PDF文本
   ├─ 自动重试（失败时重试2次）
   ├─ 缓存机制（相同文件不重复处理）
   └─ 日志记录

2. 分析PDF内容
   ├─ 识别文档类型（合同/发票/审核报告等）
   ├─ 提取关键信息（合同编号、项目名称等）
   └─ 自动重试（失败时重试1次）

3. 重命名PDF文件
   ├─ 根据分析结果生成新文件名
   ├─ 避免文件名冲突（自动添加序号）
   └─ 可选移动到已处理目录

4. 发送处理通知
   └─ 记录处理结果到日志
```

### 工作流优势

相比原有方式，工作流版本提供：

1. **任务重试**：自动重试失败的任务，提高成功率
2. **任务缓存**：相同文件不重复处理，节省资源
3. **可视化监控**：通过Prefect UI查看任务执行情况
4. **更好的错误处理**：详细的错误信息和堆栈跟踪
5. **任务依赖管理**：清晰的步骤依赖关系

---

## 🖥️ Prefect UI 监控（可选）

### 启动Prefect服务器

在**新的PowerShell窗口**中运行：

```powershell
prefect server start
```

### 访问Web界面

打开浏览器访问：http://localhost:4200

### UI功能

- 📊 **Flow Runs**：查看所有工作流执行记录
- 📈 **Task Runs**：查看每个任务的执行详情
- 🔍 **Logs**：查看详细日志
- 📉 **Metrics**：查看性能指标

---

## 📝 使用示例

### 示例1：处理单个文件

```python
from pathlib import Path
from pdf_auto_renamer.workflow_example import pdf_rename_workflow

# 处理单个PDF文件
result = pdf_rename_workflow(Path("C:/Users/DELL/Desktop/扫描文件夹/test.pdf"))
print(result)
```

### 示例2：批量处理目录

```python
from pathlib import Path
from pdf_auto_renamer.workflow_example import batch_process_workflow

# 批量处理目录中的所有PDF
result = batch_process_workflow(Path("C:/Users/DELL/Desktop/扫描文件夹"))
print(f"总计：{result['total']}，成功：{result['success']}，失败：{result['failed']}")
```

### 示例3：定时批量处理

创建 `schedule_workflow.py`：

```python
from prefect import flow
from prefect.schedules import CronSchedule
from pdf_auto_renamer.workflow_example import batch_process_workflow

# 每天凌晨2点执行批量处理
@flow(
    name="定时批量处理PDF",
    schedule=CronSchedule(cron="0 2 * * *"),  # 每天2点
)
def scheduled_batch_process():
    batch_process_workflow()

if __name__ == "__main__":
    scheduled_batch_process()
```

运行：

```powershell
python schedule_workflow.py
```

---

## ⚙️ 配置说明

工作流使用与原有系统相同的配置，配置文件：`pdf_auto_renamer/config.py`

主要配置项：

```python
WATCH_DIR          # 监控目录（默认：桌面/扫描文件夹）
RECURSIVE          # 是否递归扫描子目录（默认：False）
PROCESSED_SUBDIR   # 已处理文件目录（默认：_processed）
LOG_FILE           # 日志文件路径
```

---

## 🔧 工作流任务配置

在 `workflow_example.py` 中可以自定义任务参数：

### 重试配置

```python
@task(
    retries=2,              # 重试次数
    retry_delay_seconds=5,  # 重试间隔（秒）
)
```

### 缓存配置

```python
@task(
    cache_key_fn=task_input_hash,      # 缓存键函数
    cache_expiration=timedelta(hours=24),  # 缓存过期时间
)
```

### 并发配置

```python
@task(
    task_run_name="处理文件-{pdf_path.name}",  # 任务运行名称
)
```

---

## 📋 日志说明

### 日志位置

- **控制台**：实时输出
- **文件日志**：`扫描文件夹/auto_renamer.log`

### 日志级别

- `INFO`：正常处理信息
- `WARNING`：警告信息（如未识别出文件名）
- `ERROR`：错误信息（处理失败）

### 日志格式

```
2024-01-01 10:00:00 [INFO] pdf_auto_renamer.workflow_example: 开始提取文本：test.pdf
2024-01-01 10:00:01 [INFO] pdf_auto_renamer.workflow_example: 文本提取完成，长度：1234 字符
2024-01-01 10:00:02 [INFO] pdf_auto_renamer.workflow_example: 分析完成，文档类型：contract
```

---

## ❓ 常见问题

### Q1: Prefect UI 无法访问？

**A**: 确保Prefect服务器正在运行：
```powershell
prefect server start
```

### Q2: 工作流处理速度慢？

**A**: 
- 检查是否有大量文件需要处理
- 考虑调整并发数量
- 检查系统资源使用情况

### Q3: 如何停止监控？

**A**: 在运行监控的终端按 `Ctrl+C`

### Q4: 工作流和原有方式有什么区别？

**A**: 
- **工作流版本**：功能更强大，支持重试、缓存、可视化监控
- **原有方式**：更简单直接，适合轻量级使用

### Q5: 可以同时运行两个版本吗？

**A**: 不建议，可能会造成文件冲突。选择一个版本使用即可。

---

## 🎯 下一步

1. **扩展功能**：
   - 添加邮件通知
   - 集成云存储备份
   - 数据库记录处理历史

2. **性能优化**：
   - 并行处理多个文件
   - 优化文本提取速度

3. **增强识别**：
   - 使用AI模型提高识别准确率
   - 支持更多文档类型

---

## 📞 需要帮助？

如果遇到问题，请检查：
1. 依赖是否安装完整：`pip list | findstr prefect`
2. 日志文件中的错误信息
3. Prefect UI中的任务执行详情






