"""
知识点配置加载器
从JSON配置文件加载知识点数据
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from .knowledge_base import (
    KnowledgePoint, Subject, Difficulty,
    QuestionType, KnowledgeModule, GradeKnowledge
)


class KnowledgeConfigLoader:
    """知识点配置加载器"""

    def __init__(self, config_dir: Path):
        """
        初始化加载器

        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def load_grade_knowledge(
        self,
        subject: Subject,
        grade: int
    ) -> Optional[GradeKnowledge]:
        """
        加载某个年级的知识点配置

        Args:
            subject: 学科
            grade: 年级

        Returns:
            GradeKnowledge对象
        """
        # 确定配置文件路径
        subject_dir = self.config_dir / subject.name.lower()
        config_file = subject_dir / f"grade_{grade}.json"

        if not config_file.exists():
            print(f"配置文件不存在: {config_file}")
            return None

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)

            return self._parse_grade_config(config_data, subject, grade)

        except Exception as e:
            print(f"加载配置文件失败 {config_file}: {e}")
            return None

    def _parse_grade_config(
        self,
        config_data: Dict,
        subject: Subject,
        grade: int
    ) -> GradeKnowledge:
        """解析年级配置数据"""
        grade_knowledge = GradeKnowledge(grade, subject)

        # 加载知识模块
        for module_name, module_data in config_data.get("modules", {}).items():
            module = KnowledgeModule(
                name=module_name,
                description=module_data.get("description", "")
            )

            # 加载知识点
            for point_data in module_data.get("points", []):
                point = self._parse_knowledge_point(point_data, subject, grade)
                if point:
                    module.add_point(point)

            grade_knowledge.add_module(module)

        # 加载题型配置
        for type_name, type_data in config_data.get("question_types", {}).items():
            q_type = QuestionType(
                name=type_name,
                weight=type_data.get("weight", 1.0),
                time_per_question=type_data.get("time_per_question", 30),
                difficulty_range=tuple(type_data.get("difficulty_range", [1, 5])),
                description=type_data.get("description", "")
            )
            grade_knowledge.add_question_type(q_type)

        return grade_knowledge

    def _parse_knowledge_point(
        self,
        point_data: Dict,
        subject: Subject,
        grade: int
    ) -> Optional[KnowledgePoint]:
        """解析知识点数据"""
        try:
            return KnowledgePoint(
                id=point_data["id"],
                subject=subject,
                grade=grade,
                category=point_data["category"],
                name=point_data["name"],
                description=point_data.get("description", ""),
                difficulty=Difficulty(point_data.get("difficulty", 3)),
                keywords=point_data.get("keywords", []),
                prerequisites=point_data.get("prerequisites", []),
                next_points=point_data.get("next_points", []),
                typical_questions=point_data.get("typical_questions", []),
                common_mistakes=point_data.get("common_mistakes", []),
                learning_tips=point_data.get("learning_tips", ""),
                importance=point_data.get("importance", 3),
                avg_learning_time=point_data.get("avg_learning_time", 30)
            )
        except Exception as e:
            print(f"解析知识点失败: {e}")
            return None

    def load_all_subjects(self, grade: int) -> Dict[str, GradeKnowledge]:
        """加载某个年级的所有学科"""
        result = {}

        for subject in Subject:
            knowledge = self.load_grade_knowledge(subject, grade)
            if knowledge:
                result[subject.value] = knowledge

        return result

    def save_grade_knowledge(
        self,
        grade_knowledge: GradeKnowledge,
        overwrite: bool = False
    ):
        """
        保存年级知识点配置

        Args:
            grade_knowledge: 年级知识对象
            overwrite: 是否覆盖已有文件
        """
        subject = grade_knowledge.subject
        grade = grade_knowledge.grade

        # 确定保存路径
        subject_dir = self.config_dir / subject.name.lower()
        subject_dir.mkdir(parents=True, exist_ok=True)

        config_file = subject_dir / f"grade_{grade}.json"

        if config_file.exists() and not overwrite:
            print(f"配置文件已存在: {config_file}，使用 overwrite=True 覆盖")
            return

        # 转换为字典并保存
        config_data = self._grade_to_config(grade_knowledge)

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)

        print(f"配置已保存: {config_file}")

    def _grade_to_config(self, grade_knowledge: GradeKnowledge) -> Dict:
        """将年级知识转换为配置格式"""
        config = {
            "subject": grade_knowledge.subject.value,
            "grade": grade_knowledge.grade,
            "total_points": len(grade_knowledge.get_all_points()),
            "modules": {},
            "question_types": {}
        }

        # 转换知识模块
        for module_name, module in grade_knowledge.modules.items():
            config["modules"][module_name] = {
                "description": module.description,
                "points": [
                    {
                        "id": p.id,
                        "category": p.category,
                        "name": p.name,
                        "description": p.description,
                        "difficulty": p.difficulty.value,
                        "keywords": p.keywords,
                        "prerequisites": p.prerequisites,
                        "next_points": p.next_points,
                        "typical_questions": p.typical_questions,
                        "common_mistakes": p.common_mistakes,
                        "learning_tips": p.learning_tips,
                        "importance": p.importance,
                        "avg_learning_time": p.avg_learning_time
                    }
                    for p in module.get_all_points()
                ]
            }

        # 转换题型
        for type_name, q_type in grade_knowledge.question_types.items():
            config["question_types"][type_name] = {
                "weight": q_type.weight,
                "time_per_question": q_type.time_per_question,
                "difficulty_range": list(q_type.difficulty_range),
                "description": q_type.description
            }

        return config


if __name__ == "__main__":
    # 测试
    from pathlib import Path

    loader = KnowledgeConfigLoader(Path("knowledge_data"))

    # 测试加载
    math_grade_1 = loader.load_grade_knowledge(Subject.MATH, 1)
    if math_grade_1:
        print(f"加载成功: {math_grade_1.subject.value} {math_grade_1.grade}年级")
        print(f"知识点数量: {len(math_grade_1.get_all_points())}")
