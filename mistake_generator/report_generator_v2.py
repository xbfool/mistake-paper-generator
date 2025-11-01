"""
学习报告生成器 v2.0
生成包含双维度分析的 HTML 报告
"""
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from .dual_analyzer import WeaknessAnalysis, ExamPerformance, KnowledgePointStatus


class ReportGeneratorV2:
    """学习报告生成器 v2"""

    def __init__(self):
        """初始化报告生成器"""
        pass

    def generate_html_report(
        self,
        student_name: str,
        subject: str,
        weakness_analysis: WeaknessAnalysis,
        exam_performances: List[ExamPerformance],
        learning_suggestions: str,
        output_path: Path
    ) -> None:
        """
        生成 HTML 学习报告

        Args:
            student_name: 学生姓名
            subject: 科目
            weakness_analysis: 薄弱点分析
            exam_performances: 考试表现列表
            learning_suggestions: 学习建议
            output_path: 输出路径
        """
        html_content = self._generate_html(
            student_name=student_name,
            subject=subject,
            weakness_analysis=weakness_analysis,
            exam_performances=exam_performances,
            learning_suggestions=learning_suggestions
        )

        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _generate_html(
        self,
        student_name: str,
        subject: str,
        weakness_analysis: WeaknessAnalysis,
        exam_performances: List[ExamPerformance],
        learning_suggestions: str
    ) -> str:
        """生成 HTML 内容"""

        # 计算总体统计
        total_exams = len(exam_performances)
        if total_exams > 0:
            avg_first_rate = sum(e.first_correct_rate for e in exam_performances) / total_exams
            avg_correction_rate = sum(e.correction_success_rate for e in exam_performances) / total_exams
        else:
            avg_first_rate = 0.0
            avg_correction_rate = 0.0

        # 生成考试表现部分
        exam_table_rows = self._generate_exam_table_rows(exam_performances)

        # 生成知识点分类部分
        weak_points_html = self._generate_knowledge_points_html(
            weakness_analysis.weak_points,
            "深度薄弱",
            "#ff4757"
        )
        consolidate_points_html = self._generate_knowledge_points_html(
            weakness_analysis.consolidate_points,
            "可巩固",
            "#ffa502"
        )
        mastered_points_html = self._generate_knowledge_points_html(
            weakness_analysis.mastered_points,
            "已掌握",
            "#2ed573"
        )

        # 转换 Markdown 学习建议为 HTML
        suggestions_html = self._markdown_to_html(learning_suggestions)

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{student_name} - {subject}学习分析报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 18px;
            opacity: 0.9;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 24px;
            color: #2d3436;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
        }}

        .section-title::before {{
            content: "📊";
            margin-right: 10px;
            font-size: 28px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .stat-value {{
            font-size: 42px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}

        .stat-label {{
            font-size: 14px;
            color: #636e72;
            text-transform: uppercase;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-radius: 10px;
            overflow: hidden;
        }}

        th, td {{
            padding: 15px;
            text-align: left;
        }}

        th {{
            background: #667eea;
            color: white;
            font-weight: 600;
        }}

        tr:nth-child(even) {{
            background: #f8f9fa;
        }}

        tr:hover {{
            background: #e9ecef;
        }}

        .knowledge-point-card {{
            background: white;
            border-left: 5px solid;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}

        .kp-name {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }}

        .kp-stats {{
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
        }}

        .kp-stat {{
            display: flex;
            flex-direction: column;
        }}

        .kp-stat-label {{
            font-size: 12px;
            color: #636e72;
            margin-bottom: 5px;
        }}

        .kp-stat-value {{
            font-size: 24px;
            font-weight: bold;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e9ecef;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 10px;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }}

        .suggestions {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            border-left: 5px solid #667eea;
        }}

        .suggestions h3 {{
            color: #2d3436;
            margin-bottom: 15px;
        }}

        .suggestions ul {{
            margin-left: 20px;
        }}

        .suggestions li {{
            margin: 10px 0;
            color: #2d3436;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #636e72;
            font-size: 14px;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            color: white;
        }}

        .badge-success {{ background: #2ed573; }}
        .badge-warning {{ background: #ffa502; }}
        .badge-danger {{ background: #ff4757; }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 学习分析报告</h1>
            <div class="subtitle">{student_name} · {subject} · {datetime.now().strftime('%Y年%m月%d日')}</div>
        </div>

        <div class="content">
            <!-- 总体统计 -->
            <div class="section">
                <h2 class="section-title">总体表现</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">考试次数</div>
                        <div class="stat-value">{total_exams}</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">平均卷面正确率</div>
                        <div class="stat-value">{avg_first_rate*100:.1f}%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">平均订正成功率</div>
                        <div class="stat-value">{avg_correction_rate*100:.1f}%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">深度薄弱知识点</div>
                        <div class="stat-value" style="color: #ff4757;">{len(weakness_analysis.weak_points)}</div>
                    </div>
                </div>
            </div>

            <!-- 考试表现 -->
            <div class="section">
                <h2 class="section-title">考试表现</h2>
                <table>
                    <thead>
                        <tr>
                            <th>考试</th>
                            <th>日期</th>
                            <th>卷面正确率</th>
                            <th>订正情况</th>
                            <th>主要错题类型</th>
                        </tr>
                    </thead>
                    <tbody>
                        {exam_table_rows}
                    </tbody>
                </table>
            </div>

            <!-- 知识点掌握情况 -->
            <div class="section">
                <h2 class="section-title">知识点掌握情况</h2>

                <!-- 深度薄弱 -->
                {weak_points_html}

                <!-- 可巩固 -->
                {consolidate_points_html}

                <!-- 已掌握 -->
                {mastered_points_html}
            </div>

            <!-- 学习建议 -->
            <div class="section">
                <h2 class="section-title">💡 本周学习建议</h2>
                <div class="suggestions">
                    {suggestions_html}
                </div>
            </div>
        </div>

        <div class="footer">
            <p>报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>智能学习系统 v3.0 | 基于 Claude AI 深度分析</p>
        </div>
    </div>
</body>
</html>"""

        return html

    def _generate_exam_table_rows(self, exams: List[ExamPerformance]) -> str:
        """生成考试表格行"""
        rows = []
        for exam in exams:
            # 主要错题类型
            if exam.mistake_distribution:
                top_mistakes = sorted(
                    exam.mistake_distribution.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:2]
                mistake_types = "、".join([f"{t}({c}题)" for t, c in top_mistakes])
            else:
                mistake_types = "无错题"

            # 订正情况
            if exam.corrected_count > 0:
                correction_info = f"{exam.correction_success}/{exam.corrected_count} ({exam.correction_success_rate*100:.0f}%)"
            else:
                correction_info = "未订正"

            rows.append(f"""
                <tr>
                    <td>{exam.title}</td>
                    <td>{exam.date or '未知'}</td>
                    <td><strong>{exam.first_correct_rate*100:.0f}%</strong> ({exam.first_correct}/{exam.total_questions})</td>
                    <td>{correction_info}</td>
                    <td>{mistake_types}</td>
                </tr>
            """)

        return "\n".join(rows)

    def _generate_knowledge_points_html(
        self,
        knowledge_points: List[KnowledgePointStatus],
        category: str,
        color: str
    ) -> str:
        """生成知识点分类 HTML"""
        if not knowledge_points:
            return f"""
                <div style="margin: 20px 0;">
                    <h3 style="color: {color};">🎯 {category}知识点</h3>
                    <p style="color: #636e72; padding: 20px;">暂无{category}的知识点</p>
                </div>
            """

        cards = []
        for kp in knowledge_points[:5]:  # 最多显示前5个
            cards.append(f"""
                <div class="knowledge-point-card" style="border-left-color: {color};">
                    <div class="kp-name" style="color: {color};">{kp.knowledge_point}</div>
                    <div class="kp-stats">
                        <div class="kp-stat">
                            <div class="kp-stat-label">首次正确率</div>
                            <div class="kp-stat-value" style="color: {color};">{kp.first_correct_rate*100:.0f}%</div>
                        </div>
                        <div class="kp-stat">
                            <div class="kp-stat-label">订正正确率</div>
                            <div class="kp-stat-value" style="color: {color};">{kp.correction_correct_rate*100:.0f}%</div>
                        </div>
                        <div class="kp-stat">
                            <div class="kp-stat-label">练习次数</div>
                            <div class="kp-stat-value" style="color: {color};">{kp.total_questions}题</div>
                        </div>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {kp.correction_correct_rate*100}%; background: {color};"></div>
                    </div>
                </div>
            """)

        return f"""
            <div style="margin: 30px 0;">
                <h3 style="color: {color}; margin-bottom: 15px;">
                    {'🔴' if category == '深度薄弱' else '⚠️' if category == '可巩固' else '✅'} {category}知识点 ({len(knowledge_points)}个)
                </h3>
                {''.join(cards)}
            </div>
        """

    def _markdown_to_html(self, markdown_text: str) -> str:
        """简单的 Markdown 转 HTML（支持基本格式）"""
        lines = markdown_text.split('\n')
        html_lines = []

        in_list = False

        for line in lines:
            line = line.strip()

            if not line:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append('<br>')
                continue

            # 标题
            if line.startswith('### '):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<h3>{line[4:]}</h3>')
            elif line.startswith('## '):
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                html_lines.append(f'<h2>{line[3:]}</h2>')
            # 列表
            elif line.startswith('- ') or line.startswith('* '):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                html_lines.append(f'<li>{line[2:]}</li>')
            elif line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
                # 数字列表
                content = line.split('. ', 1)[1] if '. ' in line else line
                if not in_list:
                    html_lines.append('<ol>')
                    in_list = True
                html_lines.append(f'<li>{content}</li>')
            # 粗体
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                # 处理粗体 **text**
                line = line.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                html_lines.append(f'<p>{line}</p>')

        if in_list:
            html_lines.append('</ul>')

        return '\n'.join(html_lines)
