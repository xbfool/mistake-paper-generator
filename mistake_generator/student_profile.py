"""
学生档案管理系统
追踪学生的学习进度和薄弱环节
"""
import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from collections import defaultdict


class StudentProfile:
    """学生学习档案"""

    def __init__(self, student_name: str, profile_dir: Path):
        """
        初始化学生档案

        Args:
            student_name: 学生姓名
            profile_dir: 档案存储目录
        """
        self.student_name = student_name
        self.profile_dir = profile_dir
        self.profile_dir.mkdir(parents=True, exist_ok=True)

        self.profile_path = self.profile_dir / f"{student_name}_profile.json"

        # 档案数据
        self.data = {
            "student_name": student_name,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_questions": 0,
            "total_mistakes": 0,
            "exams": [],  # 考试记录
            "knowledge_point_stats": {},  # 知识点统计
            "question_type_stats": {},  # 题型统计
            "difficulty_stats": {},  # 难度统计
            "learning_trend": []  # 学习趋势
        }

        # 加载已有档案
        self.load()

    def load(self):
        """从文件加载档案"""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"学生档案加载成功: {self.student_name}")
            except Exception as e:
                print(f"档案加载失败: {e}，将创建新档案")

    def save(self):
        """保存档案到文件"""
        self.data["last_updated"] = datetime.now().isoformat()

        with open(self.profile_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        print(f"学生档案已保存: {self.profile_path}")

    def add_exam(self, exam_data: Dict[str, Any]):
        """
        添加一次考试记录

        Args:
            exam_data: 考试数据，包含题目列表
        """
        exam_record = {
            "exam_id": len(self.data["exams"]) + 1,
            "date": datetime.now().isoformat(),
            "source": exam_data.get("source", "未知"),
            "total_questions": len(exam_data.get("questions", [])),
            "mistakes": 0,
            "correct": 0,
            "accuracy_rate": 0.0,
            "knowledge_points": {},
            "question_types": {}
        }

        # 分析题目
        for question in exam_data.get("questions", []):
            # 统计总数
            self.data["total_questions"] += 1

            # 统计错题
            is_mistake = question.get("is_mistake", False)
            if is_mistake:
                exam_record["mistakes"] += 1
                self.data["total_mistakes"] += 1
            else:
                exam_record["correct"] += 1

            # 统计题型
            q_type = question.get("question_type", "未分类")
            if q_type not in self.data["question_type_stats"]:
                self.data["question_type_stats"][q_type] = {
                    "total": 0,
                    "mistakes": 0,
                    "accuracy_rate": 0.0
                }
            if q_type not in exam_record["question_types"]:
                exam_record["question_types"][q_type] = {"total": 0, "mistakes": 0}

            self.data["question_type_stats"][q_type]["total"] += 1
            exam_record["question_types"][q_type]["total"] += 1

            if is_mistake:
                self.data["question_type_stats"][q_type]["mistakes"] += 1
                exam_record["question_types"][q_type]["mistakes"] += 1

            # 统计知识点
            for kp in question.get("knowledge_points", []):
                if kp not in self.data["knowledge_point_stats"]:
                    self.data["knowledge_point_stats"][kp] = {
                        "total": 0,
                        "mistakes": 0,
                        "accuracy_rate": 0.0,
                        "last_practice": None
                    }
                if kp not in exam_record["knowledge_points"]:
                    exam_record["knowledge_points"][kp] = {"total": 0, "mistakes": 0}

                self.data["knowledge_point_stats"][kp]["total"] += 1
                exam_record["knowledge_points"][kp]["total"] += 1
                self.data["knowledge_point_stats"][kp]["last_practice"] = datetime.now().isoformat()

                if is_mistake:
                    self.data["knowledge_point_stats"][kp]["mistakes"] += 1
                    exam_record["knowledge_points"][kp]["mistakes"] += 1

        # 计算准确率
        if exam_record["total_questions"] > 0:
            exam_record["accuracy_rate"] = round(
                exam_record["correct"] / exam_record["total_questions"] * 100, 2
            )

        # 更新各项统计的准确率
        for q_type, stats in self.data["question_type_stats"].items():
            if stats["total"] > 0:
                stats["accuracy_rate"] = round(
                    (stats["total"] - stats["mistakes"]) / stats["total"] * 100, 2
                )

        for kp, stats in self.data["knowledge_point_stats"].items():
            if stats["total"] > 0:
                stats["accuracy_rate"] = round(
                    (stats["total"] - stats["mistakes"]) / stats["total"] * 100, 2
                )

        # 添加考试记录
        self.data["exams"].append(exam_record)

        # 更新学习趋势
        self._update_learning_trend(exam_record)

        # 保存
        self.save()

        return exam_record

    def _update_learning_trend(self, exam_record):
        """更新学习趋势"""
        self.data["learning_trend"].append({
            "date": exam_record["date"],
            "exam_id": exam_record["exam_id"],
            "accuracy_rate": exam_record["accuracy_rate"],
            "total_questions": exam_record["total_questions"],
            "mistakes": exam_record["mistakes"]
        })

    def get_weak_knowledge_points(self, threshold=60.0, min_count=3):
        """
        获取薄弱知识点

        Args:
            threshold: 正确率阈值（低于此值视为薄弱）
            min_count: 最小题目数（至少做过这么多题才纳入统计）

        Returns:
            薄弱知识点列表
        """
        weak_points = []

        for kp, stats in self.data["knowledge_point_stats"].items():
            if stats["total"] >= min_count and stats["accuracy_rate"] < threshold:
                weak_points.append({
                    "knowledge_point": kp,
                    "accuracy_rate": stats["accuracy_rate"],
                    "total": stats["total"],
                    "mistakes": stats["mistakes"],
                    "last_practice": stats["last_practice"]
                })

        # 按正确率排序（从低到高）
        weak_points.sort(key=lambda x: x["accuracy_rate"])

        return weak_points

    def get_strong_knowledge_points(self, threshold=90.0, min_count=3):
        """获取掌握较好的知识点"""
        strong_points = []

        for kp, stats in self.data["knowledge_point_stats"].items():
            if stats["total"] >= min_count and stats["accuracy_rate"] >= threshold:
                strong_points.append({
                    "knowledge_point": kp,
                    "accuracy_rate": stats["accuracy_rate"],
                    "total": stats["total"],
                    "mistakes": stats["mistakes"]
                })

        # 按正确率排序（从高到低）
        strong_points.sort(key=lambda x: x["accuracy_rate"], reverse=True)

        return strong_points

    def get_overall_stats(self):
        """获取总体统计数据"""
        if self.data["total_questions"] == 0:
            overall_accuracy = 0.0
        else:
            overall_accuracy = round(
                (self.data["total_questions"] - self.data["total_mistakes"]) /
                self.data["total_questions"] * 100, 2
            )

        return {
            "student_name": self.student_name,
            "total_exams": len(self.data["exams"]),
            "total_questions": self.data["total_questions"],
            "total_mistakes": self.data["total_mistakes"],
            "overall_accuracy": overall_accuracy,
            "created_at": self.data["created_at"],
            "last_updated": self.data["last_updated"]
        }

    def get_learning_progress(self):
        """获取学习进度趋势"""
        if len(self.data["learning_trend"]) < 2:
            return {
                "trend": "insufficient_data",
                "improvement": 0,
                "message": "数据不足，需要至少2次测试"
            }

        # 计算最近几次的准确率趋势
        recent_trends = self.data["learning_trend"][-5:]  # 最近5次

        if len(recent_trends) < 2:
            return {"trend": "insufficient_data", "improvement": 0}

        # 简单线性趋势分析
        first_accuracy = recent_trends[0]["accuracy_rate"]
        last_accuracy = recent_trends[-1]["accuracy_rate"]
        improvement = last_accuracy - first_accuracy

        if improvement > 5:
            trend = "improving"
            message = f"进步明显！准确率提升了 {improvement:.1f}%"
        elif improvement < -5:
            trend = "declining"
            message = f"需要注意，准确率下降了 {abs(improvement):.1f}%"
        else:
            trend = "stable"
            message = "保持稳定"

        return {
            "trend": trend,
            "improvement": round(improvement, 2),
            "message": message,
            "recent_accuracy": [t["accuracy_rate"] for t in recent_trends]
        }


if __name__ == "__main__":
    # 测试
    from pathlib import Path

    profile_dir = Path("data/student_profiles")

    # 创建学生档案
    student = StudentProfile("小明", profile_dir)

    print(student.get_overall_stats())
