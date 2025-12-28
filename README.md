## PDF 自动命名器（合同/发票/审核报告等）

这是一个在 **Windows 桌面“扫描文件夹”** 自动运行的 PDF 重命名小工具：

- **自动监控**：当扫描仪或其它程序往桌面的 `扫描文件夹` 中放入新的 PDF 文件时，自动触发处理。
- **自动识别类型**（基于文本关键字）：
  - 合同
  - 发票
  - 审核报告
  - （后续可扩展：考勤表、收据等）
- **自动生成新文件名**：
  - 合同：`合同编号_项目名称.pdf`
  - 发票：`5月劳务费发票.pdf`（示例）
  - 审核报告：`(审核报告)项目名称.pdf`

> 默认监控目录：`C:\Users\你的用户名\Desktop\扫描文件夹`  
> 如该目录不存在，程序会自动创建。

---

### 1. 安装依赖

1. 打开 PowerShell，`cd` 到本项目所在目录，例如：

```powershell
cd "C:\Users\DELL\Desktop\AI编程类文件夹"
```

2. 安装依赖：

```powershell
pip install -r requirements.txt
```

---

### 2. 运行方式

#### 方式1：工作流版本（推荐，功能更强大）

```powershell
python -m pdf_auto_renamer.workflow_main
```

**工作流版本特点**：
- ✅ 自动任务重试机制
- ✅ 任务缓存（相同文件不重复处理）
- ✅ 可视化监控（可选，通过Prefect UI）
- ✅ 更详细的错误处理和日志

**启动Prefect UI监控（可选）**：
```powershell
# 在新的PowerShell窗口中运行
prefect server start
# 然后访问 http://localhost:4200 查看工作流执行情况
```

#### 方式2：原有版本（简单直接）

```powershell
python -m pdf_auto_renamer.main
```

**原有版本特点**：
- ✅ 轻量级，无需额外配置
- ✅ 适合简单使用场景

**两种版本都会**：

1. 先扫描一次桌面 `扫描文件夹` 中现有的 PDF，并尝试重命名。
2. 然后进入 **实时监控模式**：只要有新的 PDF 放入该文件夹，就会自动识别并重命名。

日志会输出在控制台，同时写入 `扫描文件夹\auto_renamer.log`。

> 💡 **提示**：两种版本功能相同，工作流版本提供更强大的监控和错误处理能力。建议使用工作流版本。

---

### 3. 命名规则说明

- **合同（包含“合同”“合同编号”等字样）**
  - 尝试从文本中匹配：
    - `合同编号：XXXX`
    - `项目名称：XXXX` 或 `工程名称：XXXX`
  - 命名规则：
    - 同时识别出两者：`合同编号_项目名称.pdf`
    - 只识别出编号：`合同编号_合同.pdf`
    - 只识别出项目：`合同_项目名称.pdf`

- **发票（包含“发票”“增值税发票”等字样）**
  - 尝试匹配：
    - 中文月份：如 `5月` `11月`
    - 费用关键字：`劳务费`、`服务费`、`咨询费`、`工程款`、`租金`、`材料费` 等
  - 命名规则：
    - 示例：`5月劳务费发票.pdf`
    - 若缺少月份，则可能为：`劳务费发票.pdf`
    - 若缺少费用类型，则为：`5月费用发票.pdf`

- **审核报告（包含“审核报告”“审查报告”等字样）**
  - 尝试从文本中匹配：`项目名称：XXXX` 或 `工程名称：XXXX`
  - 命名规则：
    - `(审核报告)项目名称.pdf`
    - 如未识别出项目名称：`(审核报告)未知项目.pdf`

---

### 4. 注意事项与扩展

- 本工具采用 **简单关键字 + 正则表达式** 规则识别，并不能保证 100% 正确，但对结构比较规范的合同/发票/报告文件通常效果较好。
- 如需支持：
  - 考勤表命名（例如：`2024年5月考勤表_项目名.pdf`）
  - 收据命名（例如：`2024-05-10_收据_某某公司.pdf`）
  - 其它自定义规则  
  可以在 `pdf_auto_renamer/classifier.py` 和 `pdf_auto_renamer/renamer.py` 中新增规则，我可以帮你继续完善。

# 图片字幕生成器（含网页端）

一个开箱即用的图片字幕生成器，支持：
- 单张/目录批量生成字幕（英文/中文）
- 将字幕叠加到图片底部
- 网页端上传/拖拽/粘贴图片，预览与下载
- 下载时可添加自定义水印
- 自动识别 `C:\Windows\Fonts` 并选择中文字体（可自定义字体路径）

## 快速开始

1) 安装依赖
```
python -m pip install --upgrade pip
python -m pip install transformers torch pillow requests flask
```

2) 命令行使用
```
python caption.py --image <图片路径或URL>
python caption.py --image <图片路径或URL> --zh
python caption.py --image <图片路径或URL> --zh --overlay --out_dir captioned --font C:\Windows\Fonts\msyh.ttc
```

3) 目录批量
```
python caption.py --dir <图片目录> --zh --format csv --out captions.csv
python caption.py --dir <图片目录> --zh --overlay --out_dir <图片目录>\captioned --font C:\Windows\Fonts\msyh.ttc
```

4) 启动网页端
```
python caption.py --serve --port 5000
# 浏览器打开 http://127.0.0.1:5000/
```

预览页（仅样式演示，无后端）：直接双击打开 `preview.html`。

## 网页端功能
- 图片输入：URL、文件上传、拖拽、粘贴
- 字幕：自动生成或在“字幕内容”文本框中手动输入覆盖
- 字幕叠加：勾选“叠加字幕到图片”即在页面展示效果
- 字体：自动选择中文字体，或下拉选择，可输入自定义字体路径
- 水印：勾选“为下载图片添加专属水印”，输入水印文本，下载即带水印

## 重要说明
- 首次运行会自动下载模型权重，耗时取决于网络环境
- 默认在 CPU 上运行，如需更快可安装支持 GPU 的 `torch`
- 生成的图片默认不推送到仓库（被 `.gitignore` 忽略），在 `web_captioned/` 或你指定的目录

## 项目结构
- `caption.py`：核心脚本与网页服务入口
- `preview.html`：静态预览页面
- `.gitignore`：忽略临时与生成文件

## 典型问题
- PowerShell 不支持 `&&`：请用分号 `;` 分隔命令
- 中文显示为方块：为网页端选择或输入中文字体，如 `C:\Windows\Fonts\msyh.ttc`

## 许可证
未指定许可证，默认保留权利。若需开源授权，请更新本节。 
