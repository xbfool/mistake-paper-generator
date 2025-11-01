# 📝 小学数学计算题生成器

灵活强大的计算题 PDF 生成工具，支持 1-4 位数的加减乘除运算

## ✨ 核心特性

- 🎯 **灵活位数配置** - 支持 1-4 位数的任意组合
- 📊 **四种题型** - 口算题、竖式计算、填空题、列竖式计算
- 🎨 **自动排版** - A4 纸张，适合打印
- 📄 **答案分页** - 题目和答案分别在不同页面
- 🔄 **批量生成** - 一次生成多份不重复的练习
- ⚙️ **高度可配置** - 精确控制进位、退位、余数等

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 生成练习

```bash
# 最简单的用法（生成默认30题）
python generate.py

# 查看帮助
python generate.py --help
```

### 3. 下载中文字体（可选）

下载 simhei.ttf 放到 `fonts/` 目录，以支持中文显示。

字体下载地址：
- https://github.com/StellarCN/scp_zh/raw/master/fonts/SimHei.ttf
- 或从 Windows 系统复制：`C:\Windows\Fonts\simhei.ttf`

---

## 💻 完整命令行参数

### 基础选项

```bash
--help              显示帮助信息
--output PATH       输出PDF文件路径
--count INTEGER     总题目数量 [默认: 30]
--difficulty LEVEL  难度预设 [easy|medium|hard]
```

### 运算配置

```bash
--add DIGITS        加法位数组合，如: "3x3,3x2"
--sub DIGITS        减法位数组合
--mul DIGITS        乘法位数组合
--div DIGITS        除法位数组合
```

**位数格式说明**：
- `AxB` 表示 A位数 运算 B位数
- 示例：`2x2` = 两位数 + 两位数，`3x1` = 三位数 × 一位数
- 多个用逗号分隔：`--add 2x2,3x2,3x3`

### 进位/退位控制

```bash
--force-carry       强制所有加法题都进位
--no-carry          强制所有加法题都不进位
--force-borrow      强制所有减法题都退位
--no-borrow         强制所有减法题都不退位
```

### 除法选项

```bash
--allow-remainder   允许除法有余数 [默认开启]
--no-remainder      只生成整除题
--force-remainder   强制必须有余数
```

### 题型配置

```bash
--oral INTEGER      口算题数量 [默认: 10]
--vertical INTEGER  竖式计算数量 [默认: 10]
--fill INTEGER      填空题数量 [默认: 5]
--list INTEGER      列竖式数量 [默认: 5]
```

### PDF 选项

```bash
--title TEXT        试卷标题 [默认: 数学计算练习]
--no-answers        不生成答案页
```

### 批量生成

```bash
--batch INTEGER     批量生成份数
--prefix TEXT       文件名前缀
```

---

## 📖 使用示例

### 场景1：快速生成三年级练习

```bash
# 使用难度预设
python generate.py --difficulty medium
```

### 场景2：四位数加法专项（50题）

```bash
python generate.py \
  --add 4x4,4x3,3x4 \
  --count 50 \
  --vertical 40 \
  --oral 10 \
  --output 四位数加法专项.pdf
```

### 场景3：除法专项（只整除）

```bash
python generate.py \
  --div 3x1,4x1,4x2 \
  --no-remainder \
  --vertical 25 \
  --fill 10 \
  --list 5 \
  --output 整除专项.pdf
```

### 场景4：口算专项（简单，不进位）

```bash
python generate.py \
  --oral 30 \
  --add 2x2,2x1 \
  --sub 2x2,2x1 \
  --no-carry \
  --no-borrow \
  --vertical 0 \
  --fill 0 \
  --list 0 \
  --output 口算专项_简单.pdf
```

### 场景5：综合混合运算

```bash
python generate.py \
  --add 3x3,4x2 \
  --sub 4x3,3x3 \
  --mul 3x2,2x3,4x1 \
  --div 4x2,3x1 \
  --allow-remainder \
  --oral 12 \
  --vertical 12 \
  --fill 6 \
  --output 综合练习.pdf
```

### 场景6：批量生成一周练习（5份）

```bash
python generate.py \
  --difficulty medium \
  --batch 5 \
  --prefix 本周练习
```

生成文件：
- `output/本周练习_第1期.pdf`
- `output/本周练习_第2期.pdf`
- ...
- `output/本周练习_第5期.pdf`

---

## 📊 难度预设说明

### Easy（一年级水平）
- 加法：1位+1位, 2位+1位, 2位+2位
- 减法：2位-1位, 2位-2位
- 乘法：1位×1位
- 除法：2位÷1位

### Medium（二三年级水平）
- 加法：2位+2位, 3位+2位, 3位+3位
- 减法：2位+2位, 3位+2位, 3位+3位
- 乘法：2位×1位, 2位×2位, 3位×1位
- 除法：2位÷1位, 3位÷1位

### Hard（高年级水平）
- 加法：3位+3位, 4位+3位, 4位+4位
- 减法：3位+3位, 4位+3位, 4位+4位
- 乘法：2位×2位, 3位×2位, 4位×1位
- 除法：3位÷1位, 4位÷1位, 4位÷2位

---

## 🎯 支持的位数组合

### 加法/减法
- 1x1 - 一位数 ± 一位数
- 2x1 - 两位数 ± 一位数
- 2x2 - 两位数 ± 两位数
- 3x2 - 三位数 ± 两位数
- 3x3 - 三位数 ± 三位数
- 4x3 - 四位数 ± 三位数
- 4x4 - 四位数 ± 四位数

### 乘法
- 1x1 - 一位数 × 一位数（九九乘法表）
- 2x1 - 两位数 × 一位数
- 2x2 - 两位数 × 两位数
- 3x1 - 三位数 × 一位数
- 3x2 - 三位数 × 两位数
- 4x1 - 四位数 × 一位数
- 4x2 - 四位数 × 两位数

### 除法
- 2x1 - 两位数 ÷ 一位数
- 3x1 - 三位数 ÷ 一位数
- 4x1 - 四位数 ÷ 一位数
- 3x2 - 三位数 ÷ 两位数
- 4x2 - 四位数 ÷ 两位数
- 4x3 - 四位数 ÷ 三位数

---

## 📁 项目结构

```
math-exercise-generator/
├── math_generator/
│   ├── number_gen.py           # 数字生成器
│   ├── operations/             # 四则运算生成器
│   │   ├── addition.py
│   │   ├── subtraction.py
│   │   ├── multiplication.py
│   │   └── division.py
│   ├── question_types/         # 题型生成器
│   │   ├── oral.py
│   │   ├── vertical.py
│   │   ├── fill_blank.py
│   │   └── list_vertical.py
│   └── pdf/                    # PDF 生成
│       ├── builder.py
│       └── fonts.py
├── fonts/
│   └── simhei.ttf              # 中文字体（需下载）
├── output/                     # 生成的 PDF
├── generate.py                 # 主程序
├── test_operations.py          # 运算测试
├── test_question_types.py      # 题型测试
├── requirements.txt
├── CLAUDE.md                   # 开发环境说明
└── README.md                   # 本文档
```

---

## 🧪 测试

```bash
# 测试四则运算生成器
python test_operations.py

# 测试题型生成器
python test_question_types.py

# 生成测试 PDF
python generate.py --count 10 --output output/test.pdf
```

---

## 💡 使用技巧

### 1. 针对性练习

```bash
# 只练习加法
python generate.py --add 3x3 --sub 0x0 --mul 0x0 --div 0x0 --vertical 30

# 只练习乘法
python generate.py --mul 2x2,3x1 --add 0x0 --sub 0x0 --div 0x0 --vertical 30
```

### 2. 控制难度

```bash
# 简单加法（不进位）
python generate.py --add 2x2 --no-carry --oral 20

# 困难减法（必须退位）
python generate.py --sub 3x3,4x3 --force-borrow --vertical 30
```

### 3. 每日练习

```bash
# 每天生成不同的练习
python generate.py --output "练习_$(date +%Y%m%d).pdf"
```

### 4. 寒暑假作业

```bash
# 生成20份不重复的练习
python generate.py --batch 20 --prefix 寒假作业
```

---

## 📊 PDF 输出格式

### 题目页

```
数学计算练习（第1期）
姓名:__________  班级:__________  日期:2025年01月01日  成绩:__________
────────────────────────────────────────────────────────────────

一、口算题（每题3分，共30分）

1. 234 + 567 = ___        6. 48 × 12 = ___
2. 1234 - 567 = ___       7. 156 ÷ 12 = ___
3. 456 + 789 = ___        8. 234 × 3 = ___
...

二、竖式计算（每题5分，共50分）
（请在下方列竖式计算）

11. 1234 + 567            13. 2345 - 678
...

三、填空题（每题4分，共20分）

21. (      ) + 567 = 1234
22. 2345 - (      ) = 678
...

四、列竖式计算（每题5分，共25分）
（请在下方空白处列竖式计算）

26. 2345 + 678 = ___

27. 3456 - 789 = ___
...
```

### 答案页

```
参考答案
────────────────────────────────────────────────────────────────

一、口算题
1. 801   2. 667   3. 1245  4. 1667  5. 492
6. 576   7. 13    8. 702   9. 48    10. 4245

二、竖式计算
11. 1801  12. 4245  13. 1667  14. 3676  ...

三、填空题
21. 667   22. 1667  23. 60   24. 24   25. 5

四、列竖式计算
26. 3023  27. 2667  28. 13104  29. 3669  30. 288
```

---

## ❓ 常见问题

### Q1: PDF 中的中文无法显示？
**A**: 请下载 simhei.ttf 字体文件放到 `fonts/` 目录。

### Q2: 如何控制题目难度？
**A**:
- 使用 `--difficulty easy/medium/hard` 预设
- 或精确指定位数：`--add 2x2 --no-carry`

### Q3: 如何生成特定类型的题目？
**A**: 将不需要的题型数量设为 0，例如：
```bash
python generate.py --oral 30 --vertical 0 --fill 0 --list 0
```

### Q4: 批量生成的题目会重复吗？
**A**: 不会。每次运行都是随机生成，题目不会重复。

### Q5: 支持哪些年级？
**A**: 支持 1-6 年级，通过位数和难度配置适配不同年级。

---

## 🔧 技术栈

- **Python 3.10+** - 核心开发语言
- **ReportLab** - PDF 生成库
- **Click** - CLI 框架

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [ReportLab](https://www.reportlab.com/) - 强大的 PDF 生成库
- [Click](https://click.palletsprojects.com/) - 优秀的 CLI 框架

---

<div align="center">

**⭐ 如果这个工具对你有帮助，请给个 Star！**

Made with ❤️ by Claude Code

</div>
