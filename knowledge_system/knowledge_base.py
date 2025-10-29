"""
知识点体系基础类
定义知识点的数据结构和基本操作
"""
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class Subject(Enum):
    """学科枚举"""
    MATH = "数学"
    CHINESE = "语文"
    ENGLISH = "英语"


class Difficulty(Enum):
    """难度等级"""
    VERY_EASY = 1    # 非常简单
    EASY = 2         # 简单
    MEDIUM = 3       # 中等
    HARD = 4         # 困难
    VERY_HARD = 5    # 非常困难


@dataclass
class KnowledgePoint:
    """知识点数据类"""

    # 基本信息
    id: str                          # 唯一标识，如: math_1_number_20
    subject: Subject                 # 学科
    grade: int                       # 年级 (1-6)
    category: str                    # 分类，如: 数的认识
    name: str                        # 名称，如: 20以内数的认识
    description: str                 # 详细描述

    # 难度和关键词
    difficulty: Difficulty           # 难度等级
    keywords: List[str] = field(default_factory=list)  # 关键词

    # 依赖关系
    prerequisites: List[str] = field(default_factory=list)  # 前置知识点ID
    next_points: List[str] = field(default_factory=list)    # 后续知识点ID

    # 学习指导
    typical_questions: List[str] = field(default_factory=list)  # 典型题型
    common_mistakes: List[str] = field(default_factory=list)    # 常见错误
    learning_tips: str = ""          # 学习建议

    # 元数据
    importance: int = 3              # 重要性 (1-5)
    avg_learning_time: int = 30      # 平均学习时间（分钟）

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "subject": self.subject.value,
            "grade": self.grade,
            "category": self.category,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty.value,
            "keywords": self.keywords,
            "prerequisites": self.prerequisites,
            "next_points": self.next_points,
            "typical_questions": self.typical_questions,
            "common_mistakes": self.common_mistakes,
            "learning_tips": self.learning_tips,
            "importance": self.importance,
            "avg_learning_time": self.avg_learning_time
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KnowledgePoint':
        """从字典创建"""
        return cls(
            id=data["id"],
            subject=Subject(data["subject"]),
            grade=data["grade"],
            category=data["category"],
            name=data["name"],
            description=data["description"],
            difficulty=Difficulty(data["difficulty"]),
            keywords=data.get("keywords", []),
            prerequisites=data.get("prerequisites", []),
            next_points=data.get("next_points", []),
            typical_questions=data.get("typical_questions", []),
            common_mistakes=data.get("common_mistakes", []),
            learning_tips=data.get("learning_tips", ""),
            importance=data.get("importance", 3),
            avg_learning_time=data.get("avg_learning_time", 30)
        )


@dataclass
class QuestionType:
    """题型配置"""
    name: str                        # 题型名称
    weight: float                    # 权重（用于随机选题）
    time_per_question: int           # 每题平均时间（秒）
    difficulty_range: tuple          # 难度范围
    description: str = ""            # 描述


class KnowledgeModule:
    """知识点模块（一组相关知识点）"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.points: Dict[str, KnowledgePoint] = {}

    def add_point(self, point: KnowledgePoint):
        """添加知识点"""
        self.points[point.id] = point

    def get_point(self, point_id: str) -> Optional[KnowledgePoint]:
        """获取知识点"""
        return self.points.get(point_id)

    def get_all_points(self) -> List[KnowledgePoint]:
        """获取所有知识点"""
        return list(self.points.values())

    def get_points_by_difficulty(self, difficulty: Difficulty) -> List[KnowledgePoint]:
        """按难度获取知识点"""
        return [p for p in self.points.values() if p.difficulty == difficulty]


class GradeKnowledge:
    """年级知识体系"""

    def __init__(self, grade: int, subject: Subject):
        self.grade = grade
        self.subject = subject
        self.modules: Dict[str, KnowledgeModule] = {}
        self.question_types: Dict[str, QuestionType] = {}

    def add_module(self, module: KnowledgeModule):
        """添加知识模块"""
        self.modules[module.name] = module

    def get_module(self, name: str) -> Optional[KnowledgeModule]:
        """获取知识模块"""
        return self.modules.get(name)

    def get_all_points(self) -> List[KnowledgePoint]:
        """获取所有知识点"""
        points = []
        for module in self.modules.values():
            points.extend(module.get_all_points())
        return points

    def get_point_by_id(self, point_id: str) -> Optional[KnowledgePoint]:
        """根据ID获取知识点"""
        for module in self.modules.values():
            point = module.get_point(point_id)
            if point:
                return point
        return None

    def get_points_by_category(self, category: str) -> List[KnowledgePoint]:
        """按分类获取知识点"""
        return [p for p in self.get_all_points() if p.category == category]

    def add_question_type(self, q_type: QuestionType):
        """添加题型"""
        self.question_types[q_type.name] = q_type

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "grade": self.grade,
            "subject": self.subject.value,
            "total_points": len(self.get_all_points()),
            "modules": {
                name: {
                    "description": module.description,
                    "points": {p.id: p.to_dict() for p in module.get_all_points()}
                }
                for name, module in self.modules.items()
            },
            "question_types": {
                name: {
                    "weight": qt.weight,
                    "time_per_question": qt.time_per_question,
                    "difficulty_range": qt.difficulty_range,
                    "description": qt.description
                }
                for name, qt in self.question_types.items()
            }
        }


if __name__ == "__main__":
    # 测试
    kp = KnowledgePoint(
        id="math_1_number_20",
        subject=Subject.MATH,
        grade=1,
        category="数的认识",
        name="20以内数的认识",
        description="认识、读、写20以内的数",
        difficulty=Difficulty.EASY,
        keywords=["数数", "20以内", "读数", "写数"],
        typical_questions=["数数题", "读数题", "写数题"]
    )

    print(kp.to_dict())
