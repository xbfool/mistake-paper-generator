"""
TUI应用状态管理
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from pathlib import Path
from knowledge_system.knowledge_base import Subject
from knowledge_system.knowledge_graph import KnowledgeGraph
from mistake_generator.student_profile import StudentProfile


@dataclass
class AppState:
    """应用全局状态"""

    # 当前学生信息
    current_student: str = "琪琪"
    current_subject: Subject = Subject.MATH
    current_grade: int = 3

    # 数据对象
    student_profile: Optional[StudentProfile] = None
    knowledge_graph: Optional[KnowledgeGraph] = None

    # 选中的方案
    selected_plan: Optional[Dict[str, Any]] = None
    selected_plan_index: int = 0

    # 练习会话
    practice_session: Optional[Dict[str, Any]] = None
    current_question_index: int = 0

    # 路径配置
    profile_dir: Path = field(default_factory=lambda: Path("data/student_profiles"))
    knowledge_data_dir: Path = field(default_factory=lambda: Path("knowledge_data"))

    def load_student_profile(self):
        """加载学生档案"""
        if not self.student_profile or self.student_profile.student_name != self.current_student:
            self.student_profile = StudentProfile(self.current_student, self.profile_dir)

    def load_knowledge_graph(self):
        """加载知识图谱"""
        if not self.knowledge_graph:
            self.knowledge_graph = KnowledgeGraph(self.knowledge_data_dir)

    def switch_student(self, student_name: str):
        """切换学生"""
        self.current_student = student_name
        self.student_profile = None  # 清除缓存，重新加载
        self.selected_plan = None
        self.practice_session = None

    def reset_practice_session(self):
        """重置练习会话"""
        self.practice_session = None
        self.current_question_index = 0
