# 开发环境配置

## Python 环境

本项目使用系统 Python 环境（非 conda）

## 依赖安装

```bash
pip install -r requirements.txt
```

## 依赖列表

- reportlab>=4.0.0 - PDF 生成
- click>=8.0.0 - CLI 框架

## 测试

```bash
# 测试四则运算生成器
python test_operations.py

# 测试题型生成器
python test_question_types.py

# 生成PDF测试
python generate.py --count 10 --output test.pdf
```

## 注意事项

1. Windows 系统下需要处理 UTF-8 编码问题
2. 中文字体文件需要放在 fonts/simhei.ttf（可选）
3. 如果没有中文字体，PDF 将使用英文字体显示数字和符号
