# 🎓 智能学习系统 v3.0

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Claude%20%7C%20OpenAI-orange.svg)](#)
[![Version](https://img.shields.io/badge/Version-3.0-brightgreen.svg)](#)

> **基于双 AI 引擎的智能学习分析平台**
> 照片驱动 + 双维度分析 + 个性化诊断

## 🆕 v3.0 核心升级

### ✨ 全新功能
- 🤖 **双 AI 支持** - Claude 和 OpenAI 灵活切换
- 📷 **照片智能分组** - 自动识别试卷类型（原卷/批阅/订正）
- 📊 **双维度分析** - 卷面表现 + 订正效果深度分析
- 🎯 **三类知识点** - 精准分类：已掌握/可巩固/深度薄弱
- 📈 **学习轨迹** - 追踪首次→订正的完整进步曲线

### 🌟 技术亮点
- 支持语数英三科
- 基于知识图谱的依赖分析
- AI 生成个性化学习建议
- 精美的 HTML 可视化报告

---

## 📋 系统架构

```
智能学习系统 v3.0
├── 双 AI 引擎 (Claude Sonnet 4.5 + OpenAI GPT-4o)
├── 照片智能处理流程
│   ├── 自动识别页面类型
│   ├── 提取试卷元信息
│   └── 智能分组考试
├── 双状态题目追踪
│   ├── 首次答题状态（批阅卷）
│   ├── 订正状态（订正页）
│   └── 知识点自动映射
└── 三维度学习分析
    ├── 卷面表现维度
    ├── 订正效果维度
    └── 知识点掌握维度
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone https://github.com/xbfool/mistake-paper-generator.git
cd mistake-paper-generator

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置 API 密钥

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 文件，配置 API 密钥
```

**.env 配置示例：**
```bash
# Claude API（推荐用于图像识别）
CLAUDE_API_KEY=sk-ant-xxxxx
CLAUDE_MODEL=claude-sonnet-4.5-20250929

# OpenAI API（备选）
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4o

# 默认使用的 AI（claude 或 openai）
DEFAULT_AI_PROVIDER=claude
```

### 3. 准备照片

将拍摄的试卷照片放入 `pictures/inbox/` 目录：
- 批阅后的试卷（有红笔批改）
- 订正页（学生重新答题）
- 按拍照顺序命名（如 001.jpg, 002.jpg...）

---

## 💻 命令行使用指南

### 📷 步骤1：智能分组照片

```bash
python main.py group-photos
```

**功能：**
- 自动识别试卷类型（原卷/批阅卷/订正页）
- 提取试卷元信息（科目、标题、章节、日期）
- 智能分组为考试

**可选参数：**
```bash
# 指定照片目录
python main.py group-photos --dir /path/to/photos

# 使用 OpenAI 模型
python main.py group-photos --ai openai
```

**输出示例：**
```
✓ 分组完成！共识别 3 个考试

考试 1: 数学第三单元测试卷
  科目: 数学
  类型: 单元测试
  照片: 3张 (批阅2张, 订正1张)

考试 2: 语文第二单元测试卷
  科目: 语文
  类型: 单元测试
  照片: 2张 (批阅2张)
```

---

### 📝 步骤2：解析考试试卷

```bash
python main.py parse-exam
```

**功能：**
- 从批阅卷提取题目和首次答题状态
- 从订正页提取订正答案
- 建立完整的双状态题目数据

**可选参数：**
```bash
# 只解析特定分组
python main.py parse-exam --group-id 1

# 使用 Claude 模型
python main.py parse-exam --ai claude
```

**输出示例：**
```
解析: 数学第三单元测试卷 (数学)
  解析批阅卷... (2张)
  提取到 20 道题目
  解析订正页... (1张)
  ✓ 保存到: data/exams/xxx_questions.json
```

---

### 📊 步骤3：生成学习分析报告

```bash
python main.py analyze-v2 -s 学生姓名 --subject 数学
```

**功能：**
- 三维度薄弱点分析
- 考试表现时间线
- AI 生成个性化学习建议
- 生成精美的 HTML 报告

**参数说明：**
```bash
-s, --student   学生姓名（必填）
--subject       科目：数学/语文/英语（必填）
--ai            指定 AI 模型：claude/openai（可选）
```

**示例：**
```bash
# 生成数学分析报告
python main.py analyze-v2 -s 琪琪 --subject 数学

# 使用 OpenAI 生成语文报告
python main.py analyze-v2 -s 琪琪 --subject 语文 --ai openai
```

**输出示例：**
```
✓ 分析完成！

📊 分析摘要
  考试次数: 3
  总题数: 60
  已掌握: 5 个知识点
  可巩固: 3 个知识点
  深度薄弱: 2 个知识点

报告已生成: output/reports/琪琪_数学_分析报告.html
```

---

## 📖 完整使用流程示例

### 场景：分析琪琪的数学学习情况

```bash
# 1. 将照片放入 pictures/inbox/ 目录
#    - math_unit3_page1_graded.jpg（批阅卷第1页）
#    - math_unit3_page2_graded.jpg（批阅卷第2页）
#    - math_unit3_correction.jpg（订正页）

# 2. 智能分组照片
python main.py group-photos

# 3. 解析试卷
python main.py parse-exam

# 4. 生成分析报告
python main.py analyze-v2 -s 琪琪 --subject 数学

# 5. 用浏览器打开生成的 HTML 报告
# output/reports/琪琪_数学_分析报告.html
```

---

## 📊 分析报告内容

生成的 HTML 报告包含：

### 1. 总体表现
- 📈 考试次数
- 📊 平均卷面正确率
- ✅ 平均订正成功率
- ⚠️ 深度薄弱知识点数量

### 2. 考试表现详情
- 每次考试的日期和成绩
- 卷面正确率
- 订正情况
- 主要错题类型分布

### 3. 知识点掌握分类

#### 🔴 深度薄弱（需重点关注）
- 首次错误，订正后仍错
- 需要家长深度辅导
- 示例：两步应用题（首次0%，订正0%）

#### ⚠️ 可巩固（需反复练习）
- 首次错误，订正正确
- 可以自主练习巩固
- 示例：乘法口诀（首次67%，订正100%）

#### ✅ 已掌握（保持练习）
- 首次正确率 ≥ 80%
- 继续保持即可

### 4. 💡 AI 个性化学习建议
- 优先级1：深度薄弱点（具体方法）
- 优先级2：可巩固知识点（练习建议）
- 优先级3：保持练习计划

---

## 🎯 核心优势

### 1. 双维度分析
```
首次答题（卷面） → 识别薄弱点
      ↓
订正答题 → 评估理解程度
      ↓
三类分类 → 精准学习路径
```

### 2. 知识点精准分类

| 分类 | 特征 | 学习策略 |
|------|------|----------|
| **已掌握** | 首次正确率≥80% | 保持练习，防止遗忘 |
| **可巩固** | 首次错误，订正正确 | 反复练习，加强记忆 |
| **深度薄弱** | 首次错误，订正仍错 | 系统讲解，专项训练 |

### 3. 学习轨迹追踪
```
第一次考试 → 识别薄弱点
     ↓
  订正练习
     ↓
第二次考试 → 查看进步
     ↓
持续优化学习路径
```

---

## 🛠️ 技术栈

| 技术 | 用途 | 版本 |
|------|------|------|
| **Python** | 核心开发语言 | 3.10+ |
| **Claude AI** | 图像识别、深度分析 | Sonnet 4.5 |
| **OpenAI** | 备选 AI 引擎 | GPT-4o |
| **Click** | CLI 框架 | 8.0+ |
| **Rich** | 终端美化 | 13.0+ |
| **Pydantic** | 数据验证 | 2.0+ |

---

## 📁 项目结构

```
mistake-paper-generator/
├── pictures/
│   └── inbox/              # 待处理照片
├── data/
│   ├── photo_groups.json   # 照片分组结果
│   ├── exams/              # 解析的考试数据
│   └── student_profiles/   # 学生档案（待实现）
├── output/
│   └── reports/            # 生成的分析报告
├── knowledge_data/         # 知识点体系
│   ├── math/              # 数学（1-3年级）
│   ├── chinese/           # 语文
│   └── english/           # 英语
├── mistake_generator/     # 核心模块
│   ├── ai_provider.py      # AI 抽象层
│   ├── claude_provider.py  # Claude 实现
│   ├── openai_provider.py  # OpenAI 实现
│   ├── photo_grouper.py    # 照片分组
│   ├── question_parser_v2.py # 双状态题目解析
│   ├── dual_analyzer.py    # 三维度分析
│   └── report_generator_v2.py # 报告生成
├── main.py                # CLI 主程序
├── requirements.txt       # 依赖列表
└── README.md             # 本文档
```

---

## ❓ 常见问题

### Q1: 照片应该如何命名？
**A:** 按拍照顺序命名即可（如 001.jpg, 002.jpg），系统会自动识别并分组。

### Q2: 必须要有订正页吗？
**A:** 不是必须的。如果只有批阅卷，系统仍可分析卷面表现和识别薄弱点。

### Q3: 支持哪些科目？
**A:** 目前支持小学语文、数学、英语三科，重点优化三年级内容。

### Q4: Claude 和 OpenAI 如何选择？
**A:**
- **Claude**: 图像识别更精准，推荐用于照片分组和试卷解析
- **OpenAI**: 成本更低，可用于文本分析任务
- 可在 `.env` 设置默认模型，也可通过 `--ai` 参数临时切换

### Q5: 报告中的"深度薄弱"是什么意思？
**A:** 首次答错且订正后仍然答错的知识点，说明学生对该知识点理解不深，需要系统讲解。

---

## 🔮 未来规划

- [ ] 支持更多年级（4-6年级）
- [ ] 增加错题自动出题功能
- [ ] 支持多学生管理
- [ ] 导出 PDF 格式报告
- [ ] 移动端支持

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🙏 致谢

- [Claude AI](https://claude.ai) - 强大的多模态 AI 能力
- [OpenAI](https://openai.com) - GPT-4o 模型支持
- [Click](https://click.palletsprojects.com/) - 优秀的 CLI 框架

---

## 📞 联系方式

- GitHub: [@xbfool](https://github.com/xbfool)
- Issues: [提交问题](https://github.com/xbfool/mistake-paper-generator/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by Claude Code

</div>
