"""
学习报告生成器
生成可视化的HTML学习分析报告
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class ReportGenerator:
    """学习报告生成器"""

    def __init__(self, output_dir: Path):
        """
        初始化报告生成器

        Args:
            output_dir: 报告输出目录
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_learning_report(
        self,
        analysis_report: Dict[str, Any],
        output_filename: str = None
    ) -> Path:
        """
        生成学习分析报告

        Args:
            analysis_report: 分析报告数据
            output_filename: 输出文件名

        Returns:
            生成的HTML文件路径
        """
        if not output_filename:
            student_name = analysis_report['student_name']
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{student_name}_学习报告_{timestamp}.html"

        output_path = self.output_dir / output_filename

        print(f"\n正在生成学习报告: {output_filename}...", flush=True)

        # 构建HTML
        html_parts = []

        # HTML头部
        html_parts.append(self._generate_header())

        # 报告标题
        html_parts.append(f"""
    <div class="header">
        <h1>📊 学习分析报告</h1>
        <div class="student-info">
            <h2>{analysis_report['student_name']}</h2>
            <p class="report-date">报告生成时间：{datetime.now().strftime("%Y年%m月%d日 %H:%M")}</p>
        </div>
    </div>
""")

        # 总体概况
        html_parts.append(self._generate_overview_section(
            analysis_report['overall_stats'],
            analysis_report['learning_progress']
        ))

        # 知识点掌握情况
        html_parts.append(self._generate_knowledge_points_section(
            analysis_report['weak_points'],
            analysis_report['strong_points']
        ))

        # 题型分析
        html_parts.append(self._generate_question_types_section(
            analysis_report['question_type_analysis']
        ))

        # AI分析洞察
        if analysis_report.get('ai_insights'):
            html_parts.append(self._generate_ai_insights_section(
                analysis_report['ai_insights']
            ))

        # 学习建议
        html_parts.append(self._generate_recommendations_section(
            analysis_report['recommendations']
        ))

        # 学习趋势图（如果有多次数据）
        # 这里可以添加图表，暂时用文字描述

        # HTML尾部
        html_parts.append('</body>\n</html>')

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_parts))

        print(f"✓ 学习报告生成成功: {output_path}", flush=True)

        return output_path

    def _generate_header(self) -> str:
        """生成HTML头部"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>学习分析报告</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: "Microsoft YaHei", "SimSun", sans-serif;
            line-height: 1.8;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .student-info h2 {
            font-size: 24px;
            margin: 15px 0;
        }

        .report-date {
            opacity: 0.9;
            font-size: 14px;
        }

        .section {
            padding: 40px;
            border-bottom: 1px solid #f0f0f0;
        }

        .section:last-child {
            border-bottom: none;
        }

        .section-title {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }

        .section-title::before {
            content: "";
            width: 4px;
            height: 24px;
            background: #667eea;
            margin-right: 12px;
            border-radius: 2px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .stat-card {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            border: 2px solid #e8ebff;
            transition: transform 0.3s;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }

        .stat-value {
            font-size: 36px;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }

        .stat-label {
            color: #666;
            font-size: 14px;
        }

        .progress-bar {
            width: 100%;
            height: 30px;
            background: #f0f0f0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
            position: relative;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }

        .progress-fill.excellent {
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        }

        .progress-fill.good {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        }

        .progress-fill.average {
            background: linear-gradient(90deg, #fa709a 0%, #fee140 100%);
        }

        .progress-fill.weak {
            background: linear-gradient(90deg, #ff6b6b 0%, #feca57 100%);
        }

        .point-list {
            list-style: none;
        }

        .point-item {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .point-item.weak {
            border-left-color: #ff6b6b;
            background: #fff5f5;
        }

        .point-item.strong {
            border-left-color: #38ef7d;
            background: #f0fff4;
        }

        .point-name {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }

        .point-stats {
            color: #666;
            font-size: 14px;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 8px;
        }

        .badge.excellent {
            background: #38ef7d;
            color: white;
        }

        .badge.good {
            background: #4facfe;
            color: white;
        }

        .badge.average {
            background: #feca57;
            color: #333;
        }

        .badge.weak {
            background: #ff6b6b;
            color: white;
        }

        .insight-box {
            background: #fff9e6;
            border: 2px solid #ffe066;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 0;
            line-height: 2;
        }

        .recommendation-card {
            background: white;
            border: 2px solid #e8ebff;
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            transition: all 0.3s;
        }

        .recommendation-card:hover {
            border-color: #667eea;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
        }

        .recommendation-card.high-priority {
            border-color: #ff6b6b;
            background: #fff5f5;
        }

        .recommendation-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }

        .recommendation-description {
            color: #666;
            margin-bottom: 10px;
        }

        .recommendation-action {
            color: #667eea;
            font-weight: bold;
            font-size: 14px;
        }

        .priority-tag {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 10px;
        }

        .priority-high {
            background: #ff6b6b;
            color: white;
        }

        .priority-medium {
            background: #feca57;
            color: #333;
        }

        .priority-low {
            background: #4facfe;
            color: white;
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
<div class="container">
"""

    def _generate_overview_section(self, overall_stats: Dict, learning_progress: Dict) -> str:
        """生成总体概况部分"""
        accuracy = overall_stats['overall_accuracy']

        # 判断正确率等级
        if accuracy >= 90:
            progress_class = "excellent"
            status_text = "优秀"
        elif accuracy >= 75:
            progress_class = "good"
            status_text = "良好"
        elif accuracy >= 60:
            progress_class = "average"
            status_text = "一般"
        else:
            progress_class = "weak"
            status_text = "需加强"

        # 学习趋势图标
        trend = learning_progress.get('trend', 'stable')
        if trend == 'improving':
            trend_icon = "📈"
            trend_text = "进步中"
        elif trend == 'declining':
            trend_icon = "📉"
            trend_text = "需注意"
        else:
            trend_icon = "➡️"
            trend_text = "保持稳定"

        return f"""
    <div class="section">
        <h2 class="section-title">📊 总体概况</h2>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">测试次数</div>
                <div class="stat-value">{overall_stats['total_exams']}</div>
                <div class="stat-label">次</div>
            </div>

            <div class="stat-card">
                <div class="stat-label">累计题数</div>
                <div class="stat-value">{overall_stats['total_questions']}</div>
                <div class="stat-label">道</div>
            </div>

            <div class="stat-card">
                <div class="stat-label">错题数量</div>
                <div class="stat-value">{overall_stats['total_mistakes']}</div>
                <div class="stat-label">道</div>
            </div>

            <div class="stat-card">
                <div class="stat-label">学习趋势</div>
                <div class="stat-value">{trend_icon}</div>
                <div class="stat-label">{trend_text}</div>
            </div>
        </div>

        <div style="margin-top: 30px;">
            <h3 style="color: #333; margin-bottom: 15px;">总体正确率</h3>
            <div class="progress-bar">
                <div class="progress-fill {progress_class}" style="width: {accuracy}%;">
                    {accuracy}% - {status_text}
                </div>
            </div>
        </div>

        <div style="margin-top: 20px; color: #666;">
            <p>{learning_progress.get('message', '继续保持学习')}</p>
        </div>
    </div>
"""

    def _generate_knowledge_points_section(self, weak_points: list, strong_points: list) -> str:
        """生成知识点分析部分"""
        weak_html = []
        for idx, point in enumerate(weak_points[:5], 1):
            weak_html.append(f"""
            <li class="point-item weak">
                <div class="point-name">
                    {idx}. {point['knowledge_point']}
                    <span class="badge weak">需加强</span>
                </div>
                <div class="point-stats">
                    正确率：{point['accuracy_rate']}% |
                    做题数：{point['total']} |
                    错题：{point['mistakes']}
                </div>
                <div class="progress-bar" style="height: 8px; margin-top: 10px;">
                    <div class="progress-fill weak" style="width: {point['accuracy_rate']}%;"></div>
                </div>
            </li>
""")

        strong_html = []
        for idx, point in enumerate(strong_points[:5], 1):
            strong_html.append(f"""
            <li class="point-item strong">
                <div class="point-name">
                    {idx}. {point['knowledge_point']}
                    <span class="badge excellent">掌握良好</span>
                </div>
                <div class="point-stats">
                    正确率：{point['accuracy_rate']}% |
                    做题数：{point['total']} |
                    错题：{point['mistakes']}
                </div>
                <div class="progress-bar" style="height: 8px; margin-top: 10px;">
                    <div class="progress-fill excellent" style="width: {point['accuracy_rate']}%;"></div>
                </div>
            </li>
""")

        return f"""
    <div class="section">
        <h2 class="section-title">📚 知识点掌握情况</h2>

        <h3 style="color: #ff6b6b; margin: 20px 0 15px 0;">⚠️ 需要重点关注的知识点</h3>
        {'<ul class="point-list">' + ''.join(weak_html) + '</ul>' if weak_html else '<p style="color: #666;">暂无需要特别关注的知识点，继续保持！</p>'}

        <h3 style="color: #38ef7d; margin: 30px 0 15px 0;">✅ 掌握较好的知识点</h3>
        {'<ul class="point-list">' + ''.join(strong_html) + '</ul>' if strong_html else '<p style="color: #666;">暂无数据</p>'}
    </div>
"""

    def _generate_question_types_section(self, question_type_analysis: list) -> str:
        """生成题型分析部分"""
        type_html = []

        for type_data in question_type_analysis:
            accuracy = type_data['accuracy_rate']

            if accuracy >= 90:
                badge_class = "excellent"
            elif accuracy >= 75:
                badge_class = "good"
            elif accuracy >= 60:
                badge_class = "average"
            else:
                badge_class = "weak"

            type_html.append(f"""
            <li class="point-item">
                <div class="point-name">
                    {type_data['question_type']}
                    <span class="badge {badge_class}">{type_data['status']}</span>
                </div>
                <div class="point-stats">
                    做题数：{type_data['total']} |
                    错题：{type_data['mistakes']} |
                    正确率：{accuracy}%
                </div>
                <div class="progress-bar" style="height: 8px; margin-top: 10px;">
                    <div class="progress-fill {badge_class}" style="width: {accuracy}%;"></div>
                </div>
            </li>
""")

        return f"""
    <div class="section">
        <h2 class="section-title">📝 题型掌握情况</h2>
        <ul class="point-list">
            {''.join(type_html) if type_html else '<p style="color: #666;">暂无数据</p>'}
        </ul>
    </div>
"""

    def _generate_ai_insights_section(self, ai_insights: str) -> str:
        """生成AI分析洞察部分"""
        return f"""
    <div class="section">
        <h2 class="section-title">🤖 AI 智能分析</h2>
        <div class="insight-box">
            {ai_insights.replace(chr(10), '<br>')}
        </div>
    </div>
"""

    def _generate_recommendations_section(self, recommendations: list) -> str:
        """生成学习建议部分"""
        rec_html = []

        for rec in recommendations:
            priority = rec['priority']

            if priority == '高':
                priority_class = 'priority-high'
                card_class = 'high-priority'
            elif priority == '中':
                priority_class = 'priority-medium'
                card_class = ''
            else:
                priority_class = 'priority-low'
                card_class = ''

            rec_html.append(f"""
            <div class="recommendation-card {card_class}">
                <div class="recommendation-title">
                    <span class="priority-tag {priority_class}">{priority}优先级</span>
                    {rec['title']}
                </div>
                <div class="recommendation-description">
                    {rec['description']}
                </div>
                <div class="recommendation-action">
                    💡 建议行动：{rec['action']}
                </div>
            </div>
""")

        return f"""
    <div class="section">
        <h2 class="section-title">💡 学习建议</h2>
        {''.join(rec_html) if rec_html else '<p style="color: #666;">暂无建议</p>'}
    </div>
"""


if __name__ == "__main__":
    # 测试
    test_report = {
        "student_name": "小明",
        "overall_stats": {
            "total_exams": 3,
            "total_questions": 50,
            "total_mistakes": 12,
            "overall_accuracy": 76.0
        },
        "weak_points": [
            {"knowledge_point": "两步应用题", "accuracy_rate": 50.0, "total": 10, "mistakes": 5},
            {"knowledge_point": "周长", "accuracy_rate": 66.7, "total": 6, "mistakes": 2}
        ],
        "strong_points": [
            {"knowledge_point": "多位数加减法", "accuracy_rate": 95.0, "total": 20, "mistakes": 1}
        ],
        "learning_progress": {
            "trend": "improving",
            "message": "进步明显！准确率提升了 8.5%"
        },
        "question_type_analysis": [
            {"question_type": "应用题", "total": 15, "mistakes": 8, "accuracy_rate": 46.7, "status": "需加强"},
            {"question_type": "计算题", "total": 20, "mistakes": 2, "accuracy_rate": 90.0, "status": "优秀"}
        ],
        "ai_insights": "小明同学在计算题方面表现优秀，基础扎实。但在应用题，特别是两步应用题方面还需要加强。建议多练习理解题意，画图分析题目的能力。",
        "recommendations": [
            {
                "type": "重点突破",
                "priority": "高",
                "title": "加强「两步应用题」练习",
                "description": "当前正确率仅50.0%，建议每天专项练习5-10道题",
                "action": "生成两步应用题专项练习卷"
            }
        ]
    }

    from pathlib import Path

    gen = ReportGenerator(Path("output/reports"))
    gen.generate_learning_report(test_report)
