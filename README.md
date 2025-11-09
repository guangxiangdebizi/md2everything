# Markdown 万能转换工具 (md2everything)

一个强大的 Markdown 转换工具，支持转换为 HTML、Word (DOCX) 和 PDF 格式。

## ✨ 功能特性

- 📥 **HTML 导出** - 独立的 HTML 文件（可通过浏览器打印为 PDF）
- 📥 **Word 导出** - 生成标准 .docx 文档
- 📊 **表格支持** - 完美转换 Markdown 表格
- 💻 **代码高亮** - 保留代码块格式
- 🎨 **美观排版** - 专业的样式和布局
- 🌐 **Web 界面** - 友好的拖拽上传界面
- ⚡ **命令行工具** - 支持批量转换
- 🚀 **零依赖烦恼** - 无需安装复杂的系统库

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv

# Windows 激活
venv\Scripts\activate

# Linux/Mac 激活
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 启动 Web 服务

```bash
python server.py
```

然后访问 http://localhost:5000

### 3. 命令行使用

```bash
# 转换为 HTML
python converter.py input.md output.html

# 转换为 Word
python converter.py input.md output.docx
```

### 4. 导出 PDF

**方法：** 先转换为 HTML，再通过浏览器打印为 PDF

1. 生成 HTML：`python converter.py input.md output.html`
2. 用浏览器打开 `output.html`
3. 按 `Ctrl+P`（或点击页面按钮）
4. 在打印对话框选择"保存为 PDF"

**优点：** 完美支持中文、无需安装复杂依赖

## 📖 使用示例

### 转换示例文档

```bash
# 激活虚拟环境
venv\Scripts\activate

# 转换为 PDF
python converter.py 航空售票系统结构化分析实验报告.md 报告.pdf

# 转换为 Word
python converter.py 航空售票系统结构化分析实验报告.md 报告.docx

# 转换为 HTML  
python converter.py 航空售票系统结构化分析实验报告.md 报告.html
```

## 📁 项目结构

```
md2everything/
├── server.py                   # Web 服务（推荐）
├── converter.py                # 转换核心库 + 命令行工具
├── requirements.txt            # Python 依赖
├── index.html                  # 前端版本（纯浏览器）
├── venv/                       # 虚拟环境
└── 航空售票系统结构化分析实验报告.md  # 示例文档
```

## 🛠 技术栈

- **Python 3.8+**
- **Flask** - Web 框架
- **python-docx** - Word 文档生成
- **markdown** - Markdown 解析
- **BeautifulSoup4** - HTML 处理

**注：** PDF 导出通过浏览器打印实现，无需 WeasyPrint 等复杂依赖

## ❓ 常见问题

### 如何导出 PDF？

1. 先转换为 HTML
2. 用浏览器打开 HTML 文件
3. 按 `Ctrl+P` 打印，选择"保存为 PDF"

这种方式完美支持中文，无需额外安装库。

### Mermaid 图表如何显示？

- **前端版本** (`index.html`)：完整渲染 Mermaid 图表
- **Python 版本** (`server.py`)：显示占位符提示

**建议：** 需要 Mermaid 图表时使用 `index.html`

### 安装依赖失败？

确保使用虚拟环境，避免权限问题：

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 📝 许可证

MIT License

---

**提示：** 如需支持 Mermaid 图表渲染，请使用 `index.html` 的前端版本。
