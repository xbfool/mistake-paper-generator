# 错题卷子生成器

智能识别试卷图片中的错题，并自动生成高质量的错题练习卷。

## 功能特点

- **智能识别** - 使用 Claude Vision AI 精准识别试卷图片中的题目和红笔标记的错题
- **题库管理** - 结构化存储题目数据，支持按题型分类查询
- **相似题生成** - AI 自动生成与错题相似的高质量练习题
- **专业PDF输出** - 生成格式规范的错题练习卷PDF文档

## 安装

### 1. 克隆或下载项目

```bash
cd work-qiqi
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥

复制 `.env.example` 为 `.env` 并填入你的 Claude API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
ANTHROPIC_API_KEY=your_api_key_here
```

获取 API 密钥：https://console.anthropic.com/

## 使用方法

### 基本流程

1. **准备图片**
   - 将试卷图片（jpg/png格式）放入 `pictures/` 目录

2. **扫描图片建立题库**
   ```bash
   python main.py scan
   ```
   这将：
   - 识别所有图片中的题目
   - 识别红笔标记的错题
   - 将数据保存到题库（`data/questions.json`）

3. **查看题库信息**
   ```bash
   python main.py view
   ```

4. **生成错题练习卷**
   ```bash
   python main.py generate
   ```
   生成的PDF将保存在 `output/mistake_papers/` 目录

### 命令详解

#### 1. scan - 扫描图片

```bash
# 扫描默认目录（pictures/）
python main.py scan

# 扫描指定目录
python main.py scan --dir /path/to/images
```

#### 2. view - 查看题库

```bash
# 查看题库统计
python main.py view

# 只查看错题
python main.py view --mistakes-only

# 查看指定题型
python main.py view --type 计算题
```

#### 3. generate - 生成练习卷

```bash
# 生成错题练习卷（默认每道错题生成2道相似题）
python main.py generate

# 指定输出文件名
python main.py generate --output 数学错题练习_第一周.pdf

# 每道错题生成3道相似题
python main.py generate --similar-count 3

# 不包含答案页
python main.py generate --no-answers

# 只生成指定题型的错题
python main.py generate --type 应用题

# 限制错题数量（只处理前5道错题）
python main.py generate --limit 5
```

#### 4. clear - 清空题库

```bash
python main.py clear
```

#### 5. info - 查看项目信息

```bash
python main.py info
```

## 项目结构

```
work-qiqi/
├── pictures/              # 试卷图片目录
├── data/                  # 数据目录
│   └── questions.json     # 题库文件
├── output/                # 输出目录
│   └── mistake_papers/    # 生成的错题卷PDF
├── mistake_generator/     # 核心模块
│   ├── config.py          # 配置文件
│   ├── image_analyzer.py  # 图像分析模块
│   ├── question_bank.py   # 题库管理模块
│   ├── question_generator.py  # 相似题生成模块
│   └── pdf_generator.py   # PDF生成模块
├── main.py               # CLI主程序
├── requirements.txt      # 依赖列表
├── .env.example         # 环境变量示例
└── README.md            # 使用说明
```

## 技术栈

- **Python 3.8+**
- **Claude AI** - 图像识别和题目生成
- **ReportLab** - PDF生成
- **Click** - CLI框架
- **Rich** - 终端美化

## 常见问题

### 1. 图片识别不准确？

- 确保图片清晰，光线充足
- 红笔标记要明显
- 可以手动编辑 `data/questions.json` 修正数据

### 2. PDF中文显示乱码？

- 确保系统安装了中文字体
- Windows: 宋体（simsun.ttc）
- Linux: Noto Sans CJK 或 Droid Sans Fallback
- macOS: PingFang

### 3. API调用失败？

- 检查 `.env` 文件中的 API 密钥是否正确
- 确认网络连接正常
- 检查 API 账户余额

## 示例工作流

```bash
# 1. 查看项目信息和配置
python main.py info

# 2. 扫描图片
python main.py scan

# 3. 查看题库统计
python main.py view

# 4. 查看所有错题
python main.py view --mistakes-only

# 5. 生成练习卷（包含答案）
python main.py generate --similar-count 2 --answers

# 6. 生成特定题型的练习卷
python main.py generate --type 应用题 --output 应用题专项练习.pdf
```

## 注意事项

- 首次使用前必须配置 Claude API 密钥
- 图片识别需要消耗 API 配额
- 题库数据保存在 `data/questions.json`，可以备份
- 生成的 PDF 保存在 `output/mistake_papers/`

## 许可证

MIT License

## 支持

如有问题或建议，欢迎提出 Issue。
