"""
诊断测试系统
检测学生的实际知识掌握水平，找出薄弱的前置知识点
"""
import os
from typing import Dict, List, Set, Tuple
from pathlib import Path
from anthropic import Anthropic
from knowledge_system.knowledge_base import Subject, KnowledgePoint
from knowledge_system.knowledge_graph import KnowledgeGraph
from mistake_generator.student_profile import StudentProfile


class DiagnosisSystem:
    """诊断测试系统"""

    def __init__(self, knowledge_graph: KnowledgeGraph):
        """
        初始化诊断系统

        Args:
            knowledge_graph: 知识图谱
        """
        self.graph = knowledge_graph
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def diagnose_student(
        self,
        student_profile: StudentProfile,
        subject: Subject,
        target_grade: int = None
    ) -> Dict:
        """
        诊断学生在某学科的掌握情况

        Args:
            student_profile: 学生档案
            subject: 学科
            target_grade: 目标年级（默认使用学生当前年级）

        Returns:
            诊断报告
        """
        if target_grade is None:
            target_grade = 3  # 默认三年级

        print(f"\n开始诊断：{student_profile.student_name} - {subject.value} {target_grade}年级")
        print("="*60)

        # 1. 获取该年级所有知识点
        target_points = self.graph.get_points_by_grade_subject(subject, target_grade)

        if not target_points:
            return {
                "error": f"未找到{subject.value}{target_grade}年级的知识点配置"
            }

        print(f"目标知识点: {len(target_points)} 个")

        # 2. 从学生档案中分析已掌握的知识点
        mastered_points = self._analyze_mastered_points(student_profile, subject)
        print(f"已掌握知识点: {len(mastered_points)} 个")

        # 3. 找出薄弱知识点
        weak_points = self._find_weak_points(student_profile, subject, target_grade)
        print(f"薄弱知识点: {len(weak_points)} 个")

        # 4. 回溯检查前置知识点
        root_causes = []
        for weak_point in weak_points:
            root_cause = self.graph.find_weak_point_root_cause(
                weak_point.id,
                mastered_points
            )
            if root_cause and root_cause.id not in [r.id for r in root_causes]:
                root_causes.append(root_cause)

        print(f"需要补习的前置知识点: {len(root_causes)} 个")

        # 5. 评估实际掌握水平
        actual_grade_level = self._estimate_grade_level(
            mastered_points,
            subject,
            target_grade
        )

        print(f"实际掌握水平: {actual_grade_level} 年级")

        # 6. 生成诊断报告
        report = {
            "student_name": student_profile.student_name,
            "subject": subject.value,
            "target_grade": target_grade,
            "actual_grade_level": actual_grade_level,
            "mastered_count": len(mastered_points),
            "weak_count": len(weak_points),
            "root_causes": [
                {
                    "id": p.id,
                    "name": p.name,
                    "grade": p.grade,
                    "category": p.category,
                    "importance": p.importance
                }
                for p in root_causes[:10]  # 最多10个
            ],
            "weak_points": [
                {
                    "id": p.id,
                    "name": p.name,
                    "grade": p.grade,
                    "accuracy_rate": self._get_point_accuracy(student_profile, p.id)
                }
                for p in weak_points[:10]
            ],
            "recommendations": self._generate_diagnosis_recommendations(
                root_causes,
                weak_points,
                actual_grade_level,
                target_grade
            )
        }

        print("="*60)
        print("✓ 诊断完成")

        return report

    def _analyze_mastered_points(
        self,
        student_profile: StudentProfile,
        subject: Subject
    ) -> Set[str]:
        """分析学生已掌握的知识点"""
        mastered = set()

        # 从学生档案的知识点统计中获取
        for kp_name, stats in student_profile.data.get("knowledge_point_stats", {}).items():
            # 正确率>=80% 视为掌握
            if stats.get("accuracy_rate", 0) >= 80.0 and stats.get("total", 0) >= 3:
                # 找到对应的知识点ID
                for point in self.graph.knowledge_points.values():
                    if point.name == kp_name and point.subject == subject:
                        mastered.add(point.id)
                        break

        return mastered

    def _find_weak_points(
        self,
        student_profile: StudentProfile,
        subject: Subject,
        grade: int
    ) -> List[KnowledgePoint]:
        """找出薄弱知识点"""
        weak_points = []

        # 从学生档案中找薄弱点
        for kp_name, stats in student_profile.data.get("knowledge_point_stats", {}).items():
            # 正确率<60% 且至少做过3题
            if stats.get("accuracy_rate", 100) < 60.0 and stats.get("total", 0) >= 3:
                # 找到对应的知识点
                for point in self.graph.knowledge_points.values():
                    if point.name == kp_name and point.subject == subject and point.grade <= grade:
                        weak_points.append(point)
                        break

        # 按正确率排序
        weak_points.sort(key=lambda p: self._get_point_accuracy(student_profile, p.id))

        return weak_points

    def _get_point_accuracy(self, student_profile: StudentProfile, point_id: str) -> float:
        """获取某知识点的正确率"""
        point = self.graph.get_point(point_id)
        if not point:
            return 100.0

        stats = student_profile.data.get("knowledge_point_stats", {}).get(point.name)
        if stats:
            return stats.get("accuracy_rate", 100.0)

        return 100.0

    def _estimate_grade_level(
        self,
        mastered_points: Set[str],
        subject: Subject,
        target_grade: int
    ) -> float:
        """估算学生的实际年级水平"""
        # 统计各年级的掌握情况
        grade_stats = {}

        for grade in range(1, target_grade + 1):
            grade_points = self.graph.get_points_by_grade_subject(subject, grade)
            if not grade_points:
                continue

            mastered_count = sum(1 for p in grade_points if p.id in mastered_points)
            total_count = len(grade_points)

            if total_count > 0:
                mastery_rate = mastered_count / total_count
                grade_stats[grade] = {
                    "mastery_rate": mastery_rate,
                    "mastered": mastered_count,
                    "total": total_count
                }

        # 估算实际水平
        actual_level = 0.0

        for grade, stats in sorted(grade_stats.items()):
            if stats["mastery_rate"] >= 0.8:
                # 掌握80%以上，达到该年级水平
                actual_level = grade
            elif stats["mastery_rate"] >= 0.5:
                # 掌握50-80%，部分达到
                actual_level = grade - 0.5
            else:
                # 掌握不足50%，未达到该年级
                break

        return round(actual_level, 1)

    def _generate_diagnosis_recommendations(
        self,
        root_causes: List[KnowledgePoint],
        weak_points: List[KnowledgePoint],
        actual_level: float,
        target_grade: int
    ) -> List[Dict]:
        """生成诊断建议"""
        recommendations = []

        # 1. 如果有需要补习的前置知识点
        if root_causes:
            root_cause = root_causes[0]  # 最重要的
            recommendations.append({
                "priority": "高",
                "type": "基础补习",
                "title": f"优先补习：{root_cause.grade}年级 - {root_cause.name}",
                "description": f"这是当前薄弱环节的根本原因，建议从这里开始补习",
                "knowledge_point": root_cause.name,
                "grade": root_cause.grade,
                "action": f"生成「{root_cause.name}」专项练习"
            })

        # 2. 如果实际水平低于目标年级
        if actual_level < target_grade - 0.5:
            recommendations.append({
                "priority": "高",
                "type": "年级回溯",
                "title": f"建议从{int(actual_level + 1)}年级内容开始系统学习",
                "description": f"当前实际掌握水平为{actual_level}年级，低于目标{target_grade}年级",
                "action": "制定系统补习计划"
            })

        # 3. 针对薄弱知识点的建议
        if weak_points:
            weak_point = weak_points[0]
            recommendations.append({
                "priority": "中",
                "type": "专项突破",
                "title": f"重点突破：{weak_point.name}",
                "description": "该知识点掌握不牢，需要重点练习",
                "knowledge_point": weak_point.name,
                "action": f"每天练习5-10道相关题目"
            })

        return recommendations

    def generate_diagnosis_test(
        self,
        subject: Subject,
        grade: int,
        point_count: int = 10
    ) -> List[Dict]:
        """
        生成诊断测试题

        Args:
            subject: 学科
            grade: 年级
            point_count: 要测试的知识点数量

        Returns:
            测试题列表
        """
        print(f"\n生成诊断测试：{subject.value} {grade}年级")

        # 获取该年级的核心知识点
        all_points = self.graph.get_points_by_grade_subject(subject, grade)

        # 按重要性排序，选择最重要的知识点
        important_points = sorted(all_points, key=lambda p: p.importance, reverse=True)
        selected_points = important_points[:point_count]

        print(f"选择 {len(selected_points)} 个核心知识点进行测试")

        # 为每个知识点生成1-2道测试题
        test_questions = []

        for point in selected_points:
            questions = self._generate_test_questions_for_point(point, count=2)
            test_questions.extend(questions)

        return test_questions

    def _generate_test_questions_for_point(
        self,
        point: KnowledgePoint,
        count: int = 2
    ) -> List[Dict]:
        """为某个知识点生成测试题"""
        print(f"  为「{point.name}」生成测试题...", end="", flush=True)

        prompt = f"""请为小学{point.grade}年级{point.subject.value}知识点「{point.name}」生成{count}道测试题。

知识点信息：
- 描述：{point.description}
- 难度：{point.difficulty.value}/5
- 典型题型：{', '.join(point.typical_questions)}
- 关键词：{', '.join(point.keywords)}

要求：
1. 题目要准确考查该知识点
2. 难度适中，适合{point.grade}年级学生
3. 每道题包含：题目内容、正确答案、解析

返回JSON格式：
{{
  "questions": [
    {{
      "question": "题目内容",
      "answer": "正确答案",
      "explanation": "解析",
      "difficulty": {point.difficulty.value}
    }}
  ]
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # 提取JSON
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            import json
            result = json.loads(response_text)

            questions = result.get("questions", [])

            # 添加知识点信息
            for q in questions:
                q["knowledge_point_id"] = point.id
                q["knowledge_point_name"] = point.name
                q["grade"] = point.grade

            print(f" ✓ {len(questions)}题")

            return questions

        except Exception as e:
            print(f" ✗ 失败: {e}")
            return []


if __name__ == "__main__":
    # 测试
    from pathlib import Path

    graph = KnowledgeGraph(Path("knowledge_data"))
    diagnosis = DiagnosisSystem(graph)

    # 生成诊断测试
    test = diagnosis.generate_diagnosis_test(Subject.MATH, 3, point_count=5)

    print(f"\n生成了 {len(test)} 道诊断测试题")
    for idx, q in enumerate(test[:3], 1):
        print(f"\n{idx}. {q['question'][:50]}...")
        print(f"   知识点：{q['knowledge_point_name']}")
