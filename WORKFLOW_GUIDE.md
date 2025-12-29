# 工作流搭建指南

## 📋 准备工作清单

### 1. 确定工作流需求

在开始之前，请明确以下信息：

#### ✅ 触发方式
- [ ] **文件监控**：当新PDF文件出现时自动触发（当前已实现）
- [ ] **定时任务**：每天/每周固定时间批量处理
- [ ] **手动触发**：通过命令行或API手动启动
- [ ] **事件触发**：通过Webhook、消息队列等外部事件触发

#### ✅ 处理步骤
- [ ] **基础流程**：提取文本 → 分析内容 → 重命名（当前已实现）
- [ ] **扩展步骤**：
  - [ ] 文件备份到云存储
  - [ ] 发送邮件/通知
  - [ ] 写入数据库记录
  - [ ] 生成处理报告
  - [ ] 调用其他系统API

#### ✅ 错误处理
- [ ] **重试策略**：失败后重试几次？间隔多久？
- [ ] **告警机制**：失败时如何通知（邮件/短信/企业微信）？
- [ ] **日志记录**：需要记录哪些信息？

#### ✅ 性能要求
- [ ] **并发处理**：同时处理几个文件？
- [ ] **资源限制**：CPU/内存使用限制？
- [ ] **处理速度**：每小时需要处理多少文件？

---

## 🛠️ 工具选择

### 方案1：Prefect（推荐 - 轻量级）

**适用场景**：中小型项目，需要可视化监控

**优点**：
- ✅ 轻量级，易于上手
- ✅ 内置Web UI，可视化监控
- ✅ 支持任务重试、缓存、调度
- ✅ Python原生，与现有代码集成简单

**安装**：
```powershell
pip install prefect
```

**使用**：
```powershell
# 启动Prefect UI（可选）
prefect server start

# 运行工作流
python -m pdf_auto_renamer.workflow_example
```

**需要准备**：
- Python 3.8+
- 网络连接（首次运行会下载依赖）

---

### 方案2：APScheduler（简单定时任务）

**适用场景**：只需要定时执行，不需要复杂工作流

**优点**：
- ✅ 极轻量，无额外服务
- ✅ 适合简单的定时任务
- ✅ 无需额外配置

**安装**：
```powershell
pip install apscheduler
```

**使用示例**：
```python
from apscheduler.schedulers.blocking import BlockingScheduler
from pdf_auto_renamer.main import process_existing_pdfs

scheduler = BlockingScheduler()

# 每天凌晨2点执行
scheduler.add_job(process_existing_pdfs, 'cron', hour=2, minute=0)

scheduler.start()
```

**需要准备**：
- Python 3.6+
- 无其他依赖

---

### 方案3：Windows任务计划程序

**适用场景**：只需要定时执行，不想安装额外工具

**优点**：
- ✅ 系统自带，无需安装
- ✅ 图形界面，易于配置
- ✅ 系统级调度，稳定可靠

**配置步骤**：
1. 打开"任务计划程序"（taskschd.msc）
2. 创建基本任务
3. 触发器：选择"每天"或"当特定事件发生时"
4. 操作：启动程序
   - 程序：`python`
   - 参数：`-m pdf_auto_renamer.main`
   - 起始于：项目目录路径

**需要准备**：
- Windows系统
- Python已添加到PATH

---

### 方案4：Apache Airflow（企业级）

**适用场景**：大型项目，需要复杂工作流编排

**优点**：
- ✅ 功能强大，支持复杂工作流
- ✅ 丰富的插件生态
- ✅ 企业级监控和调度

**缺点**：
- ❌ 配置复杂，需要数据库
- ❌ 资源占用较大

**需要准备**：
- Python 3.8+
- PostgreSQL/MySQL数据库
- 较多系统资源

---

## 📦 依赖安装

根据选择的方案，更新 `requirements.txt`：

### Prefect方案
```txt
pdfplumber>=0.11.0
watchdog>=4.0.0
prefect>=2.0.0
```

### APScheduler方案
```txt
pdfplumber>=0.11.0
watchdog>=4.0.0
apscheduler>=3.10.0
```

---

## 🔧 配置信息

### 必须配置

1. **监控目录**
   - 位置：`pdf_auto_renamer/config.py`
   - 默认：`C:\Users\你的用户名\Desktop\扫描文件夹`

2. **日志路径**
   - 位置：`pdf_auto_renamer/config.py`
   - 默认：监控目录下的 `auto_renamer.log`

### 可选配置

3. **已处理文件目录**
   - 位置：`pdf_auto_renamer/config.py`
   - 配置项：`PROCESSED_SUBDIR`
   - 默认：`_processed`

4. **是否递归扫描**
   - 位置：`pdf_auto_renamer/config.py`
   - 配置项：`RECURSIVE`
   - 默认：`False`

---

## 📝 工作流设计示例

### 简单工作流（3步）
```
1. 提取PDF文本
   ↓
2. 分析并识别类型
   ↓
3. 重命名文件
```

### 完整工作流（6步）
```
1. 提取PDF文本
   ↓
2. 分析并识别类型
   ↓
3. 重命名文件
   ↓
4. 备份到云存储（可选）
   ↓
5. 写入数据库记录（可选）
   ↓
6. 发送处理通知（可选）
```

---

## 🚀 快速开始

### 步骤1：选择工具
根据你的需求选择上述方案之一（推荐Prefect）

### 步骤2：安装依赖
```powershell
pip install -r requirements.txt
```

### 步骤3：配置参数
编辑 `pdf_auto_renamer/config.py`，设置监控目录等参数

### 步骤4：运行工作流
```powershell
# Prefect方案
python -m pdf_auto_renamer.workflow_example

# 或使用原有监控方式
python -m pdf_auto_renamer.main
```

---

## 📊 监控和日志

### 日志位置
- 控制台输出：实时查看
- 文件日志：`扫描文件夹/auto_renamer.log`

### Prefect UI监控
```powershell
prefect server start
# 访问 http://localhost:4200 查看工作流执行情况
```

---

## ❓ 常见问题

### Q1: 工作流和现有监控功能有什么区别？
**A**: 工作流提供了更强大的功能：
- 任务重试机制
- 可视化监控
- 任务依赖管理
- 更好的错误处理

### Q2: 需要数据库吗？
**A**: 
- Prefect：不需要（可选，用于持久化任务状态）
- APScheduler：不需要
- Airflow：需要

### Q3: 可以同时使用文件监控和工作流吗？
**A**: 可以！文件监控触发 → 调用工作流处理，两者可以结合使用。

---

## 📚 下一步

1. **扩展功能**：
   - 添加邮件通知
   - 集成云存储备份
   - 数据库记录处理历史

2. **优化性能**：
   - 并行处理多个文件
   - 缓存已处理文件
   - 优化文本提取速度

3. **增强识别**：
   - 使用AI模型提高识别准确率
   - 支持更多文档类型
   - 自定义命名规则

---

## 💡 建议

对于你的PDF自动重命名项目，我建议：

1. **短期**：使用 **Prefect** 或 **APScheduler**，快速搭建工作流
2. **中期**：添加通知、备份等扩展功能
3. **长期**：如果需要更复杂的编排，考虑迁移到 Airflow

需要我帮你实现具体的工作流吗？告诉我你的选择，我可以帮你配置！





