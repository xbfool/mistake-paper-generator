"""
学习分析引擎
智能分析学生的学习情况并给出建议
"""
import os
from typing import Dict, List, Any
from anthropic import Anthropic
from .knowledge_points import KNOWLEDGE_POINTS, get_knowledge_point_info
from .student_profile import StudentProfile


class LearningAnalyzer:
    """学习分析器"""

    def __init__(self, api_key: str = None):
        """初始化分析器"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if self.api_key:
            self.client = Anthropic(api_key=self.api_key)
        else:
            self.client = None
            print("警告：未配置API密钥，AI分析功能将不可用")

    def analyze_student(self, student_profile: StudentProfile) -> Dict[str, Any]:
        """
        综合分析学生学习情况

        Args:
            student_profile: 学生档案

        Returns:
            分析报告
        """
        print(f"\n正在分析 {student_profile.student_name} 的学习情况...", flush=True)

        # 1. 基础统计
        overall_stats = student_profile.get_overall_stats()

        # 2. 薄弱知识点
        weak_points = student_profile.get_weak_knowledge_points(threshold=70.0, min_count=2)

        # 3. 优势知识点
        strong_points = student_profile.get_strong_knowledge_points(threshold=85.0, min_count=2)

        # 4. 学习趋势
        learning_progress = student_profile.get_learning_progress()

        # 5. 题型分析
        question_type_analysis = self._analyze_question_types(
            student_profile.data["question_type_stats"]
        )

        # 6. AI深度分析（如果可用）
        ai_insights = None
        if self.client:
            ai_insights = self._get_ai_insights(
                overall_stats,
                weak_points,
                strong_points,
                learning_progress
            )

        # 7. 生成学习建议
        recommendations = self._generate_recommendations(
            weak_points,
            learning_progress,
            question_type_analysis
        )

        return {
            "student_name": student_profile.student_name,
            "overall_stats": overall_stats,
            "weak_points": weak_points,
            "strong_points": strong_points,
            "learning_progress": learning_progress,
            "question_type_analysis": question_type_analysis,
            "ai_insights": ai_insights,
            "recommendations": recommendations,
            "analysis_date": overall_stats["last_updated"]
        }

    def _analyze_question_types(self, question_type_stats: Dict) -> List[Dict]:
        """分析各题型表现"""
        analysis = []

        for q_type, stats in question_type_stats.items():
            if stats["total"] > 0:
                analysis.append({
                    "question_type": q_type,
                    "total": stats["total"],
                    "mistakes": stats["mistakes"],
                    "accuracy_rate": stats["accuracy_rate"],
                    "status": self._get_performance_status(stats["accuracy_rate"])
                })

        # 按正确率排序
        analysis.sort(key=lambda x: x["accuracy_rate"])

        return analysis

    def _get_performance_status(self, accuracy_rate: float) -> str:
        """根据正确率判断掌握程度"""
        if accuracy_rate >= 90:
            return "优秀"
        elif accuracy_rate >= 75:
            return "良好"
        elif accuracy_rate >= 60:
            return "一般"
        else:
            return "需加强"

    def _get_ai_insights(
        self,
        overall_stats: Dict,
        weak_points: List,
        strong_points: List,
        learning_progress: Dict
    ) -> str:
        """使用AI进行深度分析"""
        print("  正在进行AI深度分析...", flush=True)

        # 构建分析提示词
        prompt = f"""你是一位经验丰富的小学数学老师，请分析这位三年级学生的学习情况：

学生姓名：{overall_stats['student_name']}
总体表现：
- 累计完成 {overall_stats['total_exams']} 次测试
- 共做 {overall_stats['total_questions']} 道题
- 错题 {overall_stats['total_mistakes']} 道
- 总体正确率：{overall_stats['overall_accuracy']}%

薄弱知识点（错误率高）：
{self._format_points_for_ai(weak_points)}

掌握较好的知识点：
{self._format_points_for_ai(strong_points)}

学习趋势：
{learning_progress.get('message', '数据不足')}

请提供：
1. 学生的主要优势（2-3点）
2. 需要重点改进的地方（2-3点）
3. 具体的学习建议（3-5点，要具体可操作）
4. 鼓励性评价（1-2句话）

要求：
- 语气温和，鼓励为主
- 建议要具体、可操作
- 适合家长和学生阅读
- 200字左右
"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            insights = message.content[0].text.strip()
            print("  ✓ AI分析完成", flush=True)
            return insights

        except Exception as e:
            print(f"  ✗ AI分析失败: {e}", flush=True)
            return None

    def _format_points_for_ai(self, points: List) -> str:
        """格式化知识点用于AI分析"""
        if not points:
            return "暂无"

        formatted = []
        for p in points[:5]:  # 只取前5个
            formatted.append(
                f"- {p['knowledge_point']}: 正确率{p['accuracy_rate']}% "
                f"({p['mistakes']}/{p['total']}道错题)"
            )

        return "\n".join(formatted)

    def _generate_recommendations(
        self,
        weak_points: List,
        learning_progress: Dict,
        question_type_analysis: List
    ) -> List[Dict]:
        """生成学习建议"""
        recommendations = []

        # 1. 针对薄弱知识点的建议
        if weak_points:
            top_weak = weak_points[0]
            kp_info = get_knowledge_point_info(top_weak["knowledge_point"])

            recommendations.append({
                "type": "重点突破",
                "priority": "高",
                "title": f"加强「{top_weak['knowledge_point']}」练习",
                "description": f"当前正确率仅{top_weak['accuracy_rate']}%，建议每天专项练习5-10道题",
                "action": f"生成{top_weak['knowledge_point']}专项练习卷"
            })

        # 2. 针对题型的建议
        if question_type_analysis:
            weak_type = question_type_analysis[0]
            if weak_type["accuracy_rate"] < 70:
                recommendations.append({
                    "type": "题型强化",
                    "priority": "中",
                    "title": f"提升「{weak_type['question_type']}」能力",
                    "description": f"该题型正确率{weak_type['accuracy_rate']}%，需要加强练习",
                    "action": f"生成{weak_type['question_type']}专项练习"
                })

        # 3. 针对学习趋势的建议
        if learning_progress.get("trend") == "declining":
            recommendations.append({
                "type": "状态调整",
                "priority": "高",
                "title": "注意学习状态",
                "description": "最近准确率有所下降，建议调整学习节奏，注意劳逸结合",
                "action": "适当减少题量，提高质量"
            })
        elif learning_progress.get("trend") == "improving":
            recommendations.append({
                "type": "保持进步",
                "priority": "低",
                "title": "保持良好势头",
                "description": f"准确率持续提升，继续保持！",
                "action": "可适当增加难度"
            })

        # 4. 综合学习建议
        recommendations.append({
            "type": "日常学习",
            "priority": "中",
            "title": "养成良好学习习惯",
            "description": "建议每天定时练习，及时订正错题，总结解题方法",
            "action": "制定每日学习计划"
        })

        return recommendations


if __name__ == "__main__":
    # 测试
    from pathlib import Path
    from .config import QUESTION_BANK_PATH

    profile_dir = Path("data/student_profiles")
    student = StudentProfile("小明", profile_dir)

    # 如果有题库数据，添加一次测试记录
    if QUESTION_BANK_PATH.exists():
        from .question_bank import QuestionBank

        bank = QuestionBank(QUESTION_BANK_PATH)
        exam_data = {
            "source": "测试卷1",
            "questions": [q.model_dump() for q in bank.get_all_questions()[:20]]
        }
        student.add_exam(exam_data)

    # 分析
    analyzer = LearningAnalyzer()
    report = analyzer.analyze_student(student)

    print("\n" + "=" * 60)
    print(f"学习分析报告 - {report['student_name']}")
    print("=" * 60)
    print(f"\n总体统计：")
    print(f"  测试次数：{report['overall_stats']['total_exams']}")
    print(f"  总题数：{report['overall_stats']['total_questions']}")
    print(f"  正确率：{report['overall_stats']['overall_accuracy']}%")

    print(f"\n薄弱知识点：")
    for p in report['weak_points'][:3]:
        print(f"  • {p['knowledge_point']}: {p['accuracy_rate']}%")

    print(f"\n学习建议：")
    for r in report['recommendations']:
        print(f"  【{r['priority']}】{r['title']}")
