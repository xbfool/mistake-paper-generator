#!/usr/bin/env python3
"""
生成带图形的几何题练习卷演示
"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from mistake_generator.geometry_drawer import GeometryDrawer

load_dotenv()


def generate_geometry_questions(count=5):
    """生成几何题"""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""请生成{count}道适合三年级学生的几何题，要求：

1. 包含不同类型的图形（正方形、长方形、圆形、三角形）
2. 涉及周长、面积等计算
3. 难度适中

请以JSON格式返回：
{{
  "questions": [
    {{
      "question": "题目内容",
      "shape_type": "图形类型（rectangle/square/circle/triangle）",
      "shape_params": {{图形参数}},
      "answer": "正确答案",
      "knowledge_points": ["知识点"]
    }}
  ]
}}"""

    print("正在生成几何题...", flush=True)

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()

    # 提取JSON
    if "```json" in response_text:
        start = response_text.find("```json") + 7
        end = response_text.find("```", start)
        response_text = response_text[start:end].strip()
    elif "```" in response_text:
        start = response_text.find("```") + 3
        end = response_text.find("```", start)
        response_text = response_text[start:end].strip()

    return json.loads(response_text)


def generate_html_with_shapes(questions_data, output_path="output/geometry_demo.html"):
    """生成带图形的HTML练习卷"""
    drawer = GeometryDrawer(grid_size=25)

    html_parts = []

    # HTML头部
    html_parts.append("""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>几何题练习卷</title>
    <style>
        @media print {
            .page-break { page-break-before: always; }
        }
        body {
            font-family: "Microsoft YaHei", "SimSun", sans-serif;
            line-height: 1.8;
            padding: 20mm;
            max-width: 210mm;
            margin: 0 auto;
            background: white;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }
        .info {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .question {
            margin-bottom: 40px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            background: #fafafa;
        }
        .question-number {
            font-size: 18px;
            font-weight: bold;
            color: #1976D2;
            margin-bottom: 10px;
        }
        .question-content {
            font-size: 15px;
            margin-bottom: 15px;
            line-height: 1.8;
        }
        .shape-container {
            text-align: center;
            margin: 20px 0;
            padding: 15px;
            background: white;
            border: 1px dashed #ccc;
            border-radius: 4px;
        }
        .answer-area {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            min-height: 60px;
        }
        .answer-label {
            color: #666;
            font-size: 14px;
            margin-bottom: 5px;
        }
        .answers-section {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 3px solid #333;
        }
        .answer-item {
            margin: 15px 0;
            padding: 10px;
            background: #f5f5f5;
            border-left: 4px solid #4CAF50;
        }
    </style>
</head>
<body>
    <h1>📐 几何题练习卷 📐</h1>
    <div class="info">
        生成时间：""" + datetime.now().strftime("%Y年%m月%d日") + """ |
        姓名：__________ |
        用时：____分钟
    </div>
""")

    # 生成题目
    questions = questions_data.get('questions', [])

    for idx, q in enumerate(questions, 1):
        html_parts.append(f'    <div class="question">')
        html_parts.append(f'        <div class="question-number">第 {idx} 题</div>')
        html_parts.append(f'        <div class="question-content">{q["question"]}</div>')

        # 插入图形
        if q.get('shape_type') and q.get('shape_params'):
            svg_code = drawer.draw_shape(
                q['shape_type'],
                q['shape_params'],
                width=500,
                height=350,
                show_grid=True,
                show_labels=True
            )
            html_parts.append(f'        <div class="shape-container">')
            html_parts.append(f'            {svg_code}')
            html_parts.append(f'        </div>')

        # 答题区
        html_parts.append(f'        <div class="answer-area">')
        html_parts.append(f'            <div class="answer-label">解答：</div>')
        html_parts.append(f'        </div>')
        html_parts.append(f'    </div>')

    # 答案页
    html_parts.append('    <div class="page-break"></div>')
    html_parts.append('    <div class="answers-section">')
    html_parts.append('        <h1>参考答案</h1>')

    for idx, q in enumerate(questions, 1):
        html_parts.append(f'        <div class="answer-item">')
        html_parts.append(f'            <strong>第 {idx} 题：</strong>{q.get("answer", "未提供答案")}')
        html_parts.append(f'        </div>')

    html_parts.append('    </div>')

    # HTML尾部
    html_parts.append('</body>')
    html_parts.append('</html>')

    # 保存文件
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))

    print(f"\n✅ HTML生成成功: {output_path}")
    print(f"共 {len(questions)} 道题目")
    print("\n提示：")
    print("  1. 在浏览器中打开该文件")
    print("  2. 使用浏览器的打印功能（Ctrl+P）保存为PDF")


if __name__ == "__main__":
    # 生成几何题
    questions_data = generate_geometry_questions(count=5)

    print(f"\n生成了 {len(questions_data['questions'])} 道几何题：")
    for idx, q in enumerate(questions_data['questions'], 1):
        print(f"  {idx}. {q['question'][:40]}...")

    # 生成HTML
    print("\n正在生成HTML练习卷...")
    generate_html_with_shapes(questions_data)

    print("\n🎉 完成！")
