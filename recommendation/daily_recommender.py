"""
每日推荐引擎
根据学生学习情况，智能推荐每日练习方案
"""
import os
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from anthropic import Anthropic
from knowledge_system.knowledge_base import Subject, KnowledgePoint
from knowledge_system.knowledge_graph import KnowledgeGraph
from mistake_generator.student_profile import StudentProfile


class DailyRecommender:
    """每日推荐引擎"""

    def __init__(self, knowledge_graph: KnowledgeGraph):
        """
        初始化推荐引擎

        Args:
            knowledge_graph: 知识图谱
        """
        self.graph = knowledge_graph
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def recommend_daily_practice(
        self,
        student_profile: StudentProfile,
        subject: Subject = Subject.MATH,
        grade: int = 3
    ) -> List[Dict]:
        """
        推荐每日练习方案

        Args:
            student_profile: 学生档案
            subject: 学科
            grade: 年级

        Returns:
            推荐方案列表
        """
        print(f"\n为 {student_profile.student_name} 生成今日推荐...")
        print("="*60)

        # 1. 分析学生情况
        weak_points = self._get_weak_points(student_profile, subject, grade)
        not_practiced_recently = self._get_not_practiced_recently(student_profile, subject, grade)
        needs_review = self._get_needs_review(student_profile, subject, grade)

        print(f"薄弱知识点: {len(weak_points)}")
        print(f"近期未练习: {len(not_practiced_recently)}")
        print(f"需要复习: {len(needs_review)}")

        # 2. 生成推荐方案
        recommendations = []

        # 方案1：薄弱点突破
        if weak_points:
            recommendations.append(self._create_weakness_plan(weak_points, student_profile))

        # 方案2：全面复习
        recommendations.append(self._create_comprehensive_plan(student_profile, subject, grade))

        # 方案3：快速练习
        recommendations.append(self._create_quick_practice_plan(student_profile, subject, grade))

        # 方案4：系统补习（如果有前置知识薄弱）
        root_causes = self._find_root_causes(weak_points, student_profile)
        if root_causes:
            recommendations.append(self._create_remedial_plan(root_causes, student_profile))

        print(f"✓ 生成了 {len(recommendations)} 个推荐方案")

        return recommendations

    def _get_weak_points(
        self,
        student_profile: StudentProfile,
        subject: Subject,
        grade: int,
        threshold: float = 60.0
    ) -> List[Tuple[KnowledgePoint, float]]:
        """获取薄弱知识点"""
        weak_points = []

        for kp_name, stats in student_profile.data.get("knowledge_point_stats", {}).items():
            if stats.get("accuracy_rate", 100) < threshold and stats.get("total", 0) >= 2:
                # 找到对应的知识点
                for point in self.graph.knowledge_points.values():
                    if (point.name == kp_name and
                        point.subject == subject and
                        point.grade <= grade):
                        weak_points.append((point, stats["accuracy_rate"]))
                        break

        # 按正确率排序（从低到高）
        weak_points.sort(key=lambda x: x[1])

        return weak_points

    def _get_not_practiced_recently(
        self,
        student_profile: StudentProfile,
        subject: Subject,
        grade: int,
        days: int = 7
    ) -> List[KnowledgePoint]:
        """获取最近N天未练习的知识点"""
        cutoff_date = datetime.now() - timedelta(days=days)
        not_practiced = []

        for kp_name, stats in student_profile.data.get("knowledge_point_stats", {}).items():
            last_practice = stats.get("last_practice")
            if last_practice:
                last_date = datetime.fromisoformat(last_practice)
                if last_date < cutoff_date:
                    # 找到对应的知识点
                    for point in self.graph.knowledge_points.values():
                        if (point.name == kp_name and
                            point.subject == subject and
                            point.grade <= grade):
                            not_practiced.append(point)
                            break

        return not_practiced

    def _get_needs_review(
        self,
        student_profile: StudentProfile,
        subject: Subject,
        grade: int
    ) -> List[KnowledgePoint]:
        """根据遗忘曲线，获取需要复习的知识点"""
        # 简化的遗忘曲线模型：7天、15天、30天需要复习
        review_days = [7, 15, 30]
        needs_review = []

        current_date = datetime.now()

        for kp_name, stats in student_profile.data.get("knowledge_point_stats", {}).items():
            last_practice = stats.get("last_practice")
            if not last_practice:
                continue

            last_date = datetime.fromisoformat(last_practice)
            days_passed = (current_date - last_date).days

            # 检查是否接近复习时间点（±1天）
            for review_day in review_days:
                if abs(days_passed - review_day) <= 1:
                    # 找到对应的知识点
                    for point in self.graph.knowledge_points.values():
                        if (point.name == kp_name and
                            point.subject == subject and
                            point.grade <= grade):
                            needs_review.append(point)
                            break

        return needs_review

    def _find_root_causes(
        self,
        weak_points: List[Tuple[KnowledgePoint, float]],
        student_profile: StudentProfile
    ) -> List[KnowledgePoint]:
        """找到薄弱点的根本原因"""
        root_causes = []

        # 从学生档案获取已掌握的知识点
        mastered = set()
        for kp_name, stats in student_profile.data.get("knowledge_point_stats", {}).items():
            if stats.get("accuracy_rate", 0) >= 80:
                for point in self.graph.knowledge_points.values():
                    if point.name == kp_name:
                        mastered.add(point.id)

        # 为每个薄弱点找根本原因
        for weak_point, _ in weak_points[:5]:  # 最多检查5个
            root_cause = self.graph.find_weak_point_root_cause(weak_point.id, mastered)
            if root_cause and root_cause.id not in [r.id for r in root_causes]:
                root_causes.append(root_cause)

        return root_causes

    def _create_weakness_plan(
        self,
        weak_points: List[Tuple[KnowledgePoint, float]],
        student_profile: StudentProfile
    ) -> Dict:
        """创建薄弱点突破方案"""
        # 选择前3个最薄弱的知识点
        selected_points = [p for p, _ in weak_points[:3]]

        total_questions = 15
        estimated_time = 20  # 分钟

        return {
            "plan_id": "weakness_breakthrough",
            "name": "薄弱点突破",
            "emoji": "🎯",
            "description": f"重点练习{len(selected_points)}个薄弱知识点，每个5道题",
            "knowledge_points": [
                {
                    "id": p.id,
                    "name": p.name,
                    "grade": p.grade,
                    "current_accuracy": weak_points[[pt for pt, _ in weak_points].index(p)][1],
                    "questions_count": 5
                }
                for p in selected_points
            ],
            "total_questions": total_questions,
            "estimated_time": estimated_time,
            "difficulty": "简单→中等",
            "goal": "巩固薄弱环节，提高正确率",
            "priority": "高"
        }

    def _create_comprehensive_plan(
        self,
        student_profile: StudentProfile,
        subject: Subject,
        grade: int
    ) -> Dict:
        """创建全面复习方案"""
        # 获取该年级所有已学知识点
        all_points = self.graph.get_points_by_grade_subject(subject, grade)

        # 根据正确率分配题量
        total_questions = 20
        estimated_time = 30

        return {
            "plan_id": "comprehensive_review",
            "name": "全面复习",
            "emoji": "📚",
            "description": f"覆盖{grade}年级主要知识点，全面巩固",
            "knowledge_points_count": min(len(all_points), 10),
            "total_questions": total_questions,
            "estimated_time": estimated_time,
            "difficulty": "中等",
            "goal": "全面复习，查漏补缺",
            "priority": "中"
        }

    def _create_quick_practice_plan(
        self,
        student_profile: StudentProfile,
        subject: Subject,
        grade: int
    ) -> Dict:
        """创建快速练习方案"""
        total_questions = 10
        estimated_time = 10

        return {
            "plan_id": "quick_practice",
            "name": "快速练习",
            "emoji": "⚡",
            "description": "10道精选题目，快速练手",
            "total_questions": total_questions,
            "estimated_time": estimated_time,
            "difficulty": "简单",
            "goal": "保持手感，每日一练",
            "priority": "低"
        }

    def _create_remedial_plan(
        self,
        root_causes: List[KnowledgePoint],
        student_profile: StudentProfile
    ) -> Dict:
        """创建系统补习方案"""
        # 选择最重要的前置知识点
        root_cause = root_causes[0] if root_causes else None

        if not root_cause:
            return None

        total_questions = 15
        estimated_time = 20

        return {
            "plan_id": "remedial_study",
            "name": "基础补习",
            "emoji": "🔧",
            "description": f"回溯到{root_cause.grade}年级，补习「{root_cause.name}」",
            "knowledge_points": [
                {
                    "id": root_cause.id,
                    "name": root_cause.name,
                    "grade": root_cause.grade,
                    "questions_count": total_questions
                }
            ],
            "total_questions": total_questions,
            "estimated_time": estimated_time,
            "difficulty": "简单",
            "goal": "打牢基础，为后续学习做准备",
            "priority": "高",
            "is_remedial": True
        }


if __name__ == "__main__":
    # 测试
    from pathlib import Path
    from mistake_generator.student_profile import StudentProfile

    graph = KnowledgeGraph(Path("knowledge_data"))
    recommender = DailyRecommender(graph)

    # 加载学生档案
    profile_dir = Path("data/student_profiles")
    student = StudentProfile("琪琪", profile_dir)

    # 生成推荐
    plans = recommender.recommend_daily_practice(student, Subject.MATH, 3)

    print(f"\n今日推荐方案：")
    for idx, plan in enumerate(plans, 1):
        print(f"\n{idx}. {plan['emoji']} {plan['name']}")
        print(f"   {plan['description']}")
        print(f"   题量：{plan['total_questions']}道 | 时间：{plan['estimated_time']}分钟")
