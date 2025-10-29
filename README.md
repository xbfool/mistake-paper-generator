# 🎓 智能错题卷生成器 & 学生学习分析系统

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude](https://img.shields.io/badge/Powered%20by-Claude%20AI-orange.svg)](https://claude.ai)

> 基于 Claude AI 的智能教育辅助工具，自动识别试卷错题、生成练习题、分析学习情况

[English](#) | [中文文档](#)

---

## ✨ 核心功能

### 📷 1. 智能错题识别
- 🤖 **AI 图像识别** - 使用 Claude Vision API 自动识别试卷
- ✅ **精准识别** - 题目内容、题型、红笔标记一键识别
- 📊 **结构化存储** - 题库 JSON 格式，便于管理和查询

### 📝 2. 错题卷生成
- 🎨 **双格式输出** - HTML（推荐）/ PDF 格式
- 🔄 **AI 相似题** - 自动生成高质量相似练习题
- 📐 **几何图形** - 自动绘制带标注的几何图形
- 🎯 **按题型分类** - 计算题、应用题、几何题等

### 📊 3. 学生学习分析 ⭐
- 📚 **知识点体系** - 完整的小学三年级数学知识点（26个）
- 🔍 **薄弱点识别** - 智能识别学习薄弱环节
- 📈 **趋势追踪** - 追踪学习进度和变化趋势
- 🤖 **AI 深度分析** - 个性化学习建议
- 📊 **可视化报告** - 漂亮的 HTML 分析报告

---

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/xbfool/mistake-paper-generator.git
cd mistake-paper-generator

# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
cp .env.example .env
# 编辑 .env 文件，填入你的 Claude API 密钥
```

### 基础使用

```bash
# 1. 扫描试卷图片（放入 pictures/ 目录）
python main.py scan

# 2. 生成错题练习卷
python main.py generate

# 3. 添加学生档案
python main.py add-exam -s 学生名 --source "第一单元测试"

# 4. 生成学习分析报告
python main.py analyze -s 学生名
```

---

## 📚 详细文档

- 📖 [快速入门指南](快速入门.md)
- 📖 [学生学习分析指南](学生学习分析指南.md)
- 📖 [几何题生成指南](几何题生成指南.md)
- 📖 [项目总结](项目总结.md)

---

## 🎯 功能演示

### 错题识别
<img src="https://via.placeholder.com/800x400/667eea/ffffff?text=试卷图片识别演示" width="800"/>

系统自动识别：
- ✅ 62 道题目
- ✅ 32 道错题
- ✅ 7 种题型分类
- ✅ 知识点自动标注

### 学习分析报告
<img src="https://via.placeholder.com/800x400/764ba2/ffffff?text=学习分析报告演示" width="800"/>

报告包含：
- 📊 总体统计（正确率、测试次数）
- 🔴 薄弱知识点（自动排序）
- 🟢 优势知识点
- 📈 学习趋势分析
- 💡 AI 个性化建议

### 几何题绘图
<img src="https://via.placeholder.com/600x400/4facfe/ffffff?text=几何图形自动绘制" width="600"/>

自动生成：
- 正方形、长方形、圆形、三角形
- 自动标注尺寸
- SVG 矢量图，打印清晰

---

## 🏗️ 项目结构

```
mistake-paper-generator/
├── pictures/                    # 试卷图片目录
├── data/                        # 数据存储
│   ├── questions.json           # 题库
│   └── student_profiles/        # 学生档案
├── output/                      # 输出文件
│   ├── mistake_papers/          # 错题练习卷
│   └── reports/                 # 学习分析报告
├── mistake_generator/           # 核心模块
│   ├── image_analyzer.py        # 图像识别
│   ├── question_bank.py         # 题库管理
│   ├── question_generator.py    # 相似题生成
│   ├── html_generator.py        # HTML 生成
│   ├── geometry_drawer.py       # 几何图形绘制
│   ├── knowledge_points.py      # 知识点体系
│   ├── student_profile.py       # 学生档案
│   ├── learning_analyzer.py     # 学习分析
│   └── report_generator.py      # 报告生成
├── main.py                      # CLI 主程序
└── requirements.txt             # 依赖列表
```

---

## 💡 使用场景

### 家长场景
```bash
# 每周测试后
python main.py scan                              # 扫描试卷
python main.py add-exam -s 小明 --source "周测"   # 添加记录
python main.py analyze -s 小明                   # 查看分析报告
python main.py generate --type 应用题            # 生成专项练习
```

### 老师场景
```bash
# 批量管理多个学生
python main.py add-exam -s 学生A --source "月考"
python main.py add-exam -s 学生B --source "月考"
python main.py add-exam -s 学生C --source "月考"

# 分别生成分析报告
python main.py analyze -s 学生A
python main.py analyze -s 学生B
python main.py analyze -s 学生C
```

---

## 🎨 知识点体系

### 6 大类别，26 个细分知识点

| 类别 | 知识点 |
|------|--------|
| **计算能力** | 多位数加减法、乘法运算、除法运算、混合运算、估算 |
| **几何图形** | 周长、面积、图形认识、角的认识 |
| **应用能力** | 两步应用题、倍数问题、归一问题、归总问题、相遇问题 |
| **时间与测量** | 时间计算、长度单位、质量单位、单位换算 |
| **数的认识** | 万以内数、分数初步、小数初步、数的大小比较 |
| **逻辑思维** | 规律发现、简单推理、对应关系 |

---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3.10+** | 主要开发语言 |
| **Claude AI (Sonnet 4.5)** | 图像识别、相似题生成、学习分析 |
| **ReportLab** | PDF 生成 |
| **Click** | CLI 框架 |
| **Rich** | 终端美化 |
| **Pydantic** | 数据验证 |

---

## 📊 测试数据

已在实际环境中测试：
- ✅ **8 张试卷** 成功识别
- ✅ **62 道题目** 准确提取
- ✅ **32 道错题** 精准标记
- ✅ **学习报告** 生成成功
- ✅ **几何题** 自动画图

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发计划
- [ ] Web 界面
- [ ] 更多题型支持
- [ ] 多年级适配
- [ ] 错题本导出
- [ ] 微信小程序

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🙏 致谢

- [Claude AI](https://claude.ai) - 提供强大的 AI 能力
- [ReportLab](https://www.reportlab.com/) - PDF 生成库
- [Click](https://click.palletsprojects.com/) - CLI 框架

---

## 📞 联系方式

- GitHub: [@xbfool](https://github.com/xbfool)
- Issues: [提交问题](https://github.com/xbfool/mistake-paper-generator/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by Claude Code

</div>
