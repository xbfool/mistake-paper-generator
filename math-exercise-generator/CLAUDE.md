# 开发环境配置

## Python 环境

本项目使用系统 Python 环境（非 conda）

## 依赖安装

```bash
pip install -r requirements.txt
```

## 依赖列表

- reportlab>=4.0.0 - PDF 生成（ReportLab方案）
- jinja2>=3.0.0 - LaTeX 模板引擎
- click>=8.0.0 - CLI 框架

## LaTeX 环境配置

### MiKTeX 安装

1. 下载并安装 MiKTeX：https://miktex.org/download
2. 安装时选择 "Always install missing packages on-the-fly"
3. 安装后需要**重启终端**使 PATH 生效

### 验证安装

```bash
pdflatex --version
```

应该显示 MiKTeX 版本信息。

### 常见路径

MiKTeX 通常安装在：
- `C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe`
- 或 `C:\Users\用户名\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe`

如果命令行找不到 pdflatex，需要将上述路径添加到系统 PATH 环境变量。

## 两种生成方式

### 方式1：ReportLab 生成（基础版）

```bash
python generate.py --difficulty medium --output test.pdf
```

特点：
- 快速生成
- 不依赖 LaTeX
- 格式相对简单

### 方式2：LaTeX 生成（专业版）✨

```bash
python generate_latex.py --difficulty medium --output test.pdf
```

特点：
- 专业的数学排版
- 使用 xlop 包生成标准竖式
- 格式完全符合教材标准
- **推荐使用**

## 测试

```bash
# 测试四则运算生成器
python test_operations.py

# 测试题型生成器
python test_question_types.py

# 测试 ReportLab PDF生成
python generate.py --count 10 --output output/test_reportlab.pdf

# 测试 LaTeX PDF生成（需要先安装 MiKTeX 并重启终端）
python generate_latex.py --count 10 --output output/test_latex.pdf
```

## 注意事项

1. Windows 系统下需要处理 UTF-8 编码问题
2. 中文字体文件：fonts/SimHei.ttf（已包含）
3. LaTeX 首次编译会自动下载缺失的包，需要联网
4. 使用 LaTeX 方案时，会在 output 目录生成 .tex 临时文件（自动清理）

## 字体文件

- **SimHei.ttf**（黑体，9.4MB）已放置在 fonts/ 目录
- 用于 ReportLab 方案的中文显示
- LaTeX 方案使用 ctex 包，会自动处理中文
