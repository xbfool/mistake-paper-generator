"""
知识依赖图谱系统
管理知识点之间的依赖关系，支持前置检测和学习路径规划
"""
from typing import List, Dict, Set, Optional
from pathlib import Path
from .knowledge_base import KnowledgePoint, Subject
from .config_loader import KnowledgeConfigLoader


class KnowledgeGraph:
    """知识依赖图谱"""

    def __init__(self, config_dir: Path):
        """
        初始化知识图谱

        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = config_dir
        self.loader = KnowledgeConfigLoader(config_dir)
        self.knowledge_points: Dict[str, KnowledgePoint] = {}
        self._load_all_knowledge()

    def _load_all_knowledge(self):
        """加载所有知识点"""
        print("正在加载知识图谱...", flush=True)

        # 加载所有学科和年级
        for subject in Subject:
            for grade in range(1, 7):
                # 英语从3年级开始
                if subject == Subject.ENGLISH and grade < 3:
                    continue

                grade_knowledge = self.loader.load_grade_knowledge(subject, grade)
                if grade_knowledge:
                    for point in grade_knowledge.get_all_points():
                        self.knowledge_points[point.id] = point

        print(f"✓ 知识图谱加载完成：{len(self.knowledge_points)} 个知识点", flush=True)

    def get_point(self, point_id: str) -> Optional[KnowledgePoint]:
        """获取知识点"""
        return self.knowledge_points.get(point_id)

    def get_prerequisites(self, point_id: str) -> List[KnowledgePoint]:
        """
        获取某知识点的所有前置知识点

        Args:
            point_id: 知识点ID

        Returns:
            前置知识点列表
        """
        point = self.get_point(point_id)
        if not point:
            return []

        prerequisites = []
        for prereq_id in point.prerequisites:
            prereq_point = self.get_point(prereq_id)
            if prereq_point:
                prerequisites.append(prereq_point)

        return prerequisites

    def get_all_prerequisites_recursive(self, point_id: str) -> List[KnowledgePoint]:
        """
        递归获取所有前置知识点（包括前置的前置）

        Args:
            point_id: 知识点ID

        Returns:
            所有前置知识点列表（按依赖顺序）
        """
        visited = set()
        result = []

        def dfs(pid: str):
            if pid in visited:
                return
            visited.add(pid)

            point = self.get_point(pid)
            if not point:
                return

            # 先访问前置
            for prereq_id in point.prerequisites:
                dfs(prereq_id)

            # 再添加当前节点
            if pid != point_id:  # 不包含自己
                result.append(point)

        dfs(point_id)
        return result

    def check_readiness(
        self,
        point_id: str,
        mastered_points: Set[str]
    ) -> Dict[str, any]:
        """
        检查学生是否具备学习某知识点的条件

        Args:
            point_id: 目标知识点ID
            mastered_points: 学生已掌握的知识点ID集合

        Returns:
            检查结果字典
        """
        point = self.get_point(point_id)
        if not point:
            return {"ready": False, "reason": "知识点不存在"}

        # 检查所有前置知识点
        prerequisites = self.get_prerequisites(point_id)
        missing = []

        for prereq in prerequisites:
            if prereq.id not in mastered_points:
                missing.append(prereq)

        if not missing:
            return {
                "ready": True,
                "missing": [],
                "message": f"可以学习「{point.name}」"
            }
        else:
            return {
                "ready": False,
                "missing": missing,
                "message": f"需要先掌握 {len(missing)} 个前置知识点"
            }

    def get_learning_path(
        self,
        from_point_id: str,
        to_point_id: str
    ) -> List[KnowledgePoint]:
        """
        获取从一个知识点到另一个知识点的学习路径

        Args:
            from_point_id: 起始知识点
            to_point_id: 目标知识点

        Returns:
            学习路径（知识点列表）
        """
        # 获取目标的所有前置
        all_prereqs = self.get_all_prerequisites_recursive(to_point_id)

        # 找到起始点的位置
        path = []
        found_start = False

        for point in all_prereqs:
            if point.id == from_point_id:
                found_start = True

            if found_start:
                path.append(point)

        # 添加目标点
        target = self.get_point(to_point_id)
        if target:
            path.append(target)

        return path

    def find_weak_point_root_cause(
        self,
        weak_point_id: str,
        student_mastered: Set[str]
    ) -> Optional[KnowledgePoint]:
        """
        找到薄弱知识点的根本原因（最早的未掌握前置知识点）

        Args:
            weak_point_id: 薄弱知识点ID
            student_mastered: 学生已掌握的知识点集合

        Returns:
            根本原因知识点（需要优先补习的）
        """
        # 获取所有前置知识点
        all_prereqs = self.get_all_prerequisites_recursive(weak_point_id)

        # 找到第一个未掌握的
        for point in all_prereqs:
            if point.id not in student_mastered:
                return point

        # 如果所有前置都掌握了，那问题就在当前知识点本身
        return self.get_point(weak_point_id)

    def get_points_by_grade_subject(
        self,
        subject: Subject,
        grade: int
    ) -> List[KnowledgePoint]:
        """获取某学科某年级的所有知识点"""
        return [
            p for p in self.knowledge_points.values()
            if p.subject == subject and p.grade == grade
        ]

    def get_points_by_category(
        self,
        subject: Subject,
        grade: int,
        category: str
    ) -> List[KnowledgePoint]:
        """获取某学科某年级某类别的知识点"""
        return [
            p for p in self.knowledge_points.values()
            if p.subject == subject and p.grade == grade and p.category == category
        ]


if __name__ == "__main__":
    # 测试
    from pathlib import Path

    graph = KnowledgeGraph(Path("knowledge_data"))

    # 测试获取前置知识点
    prereqs = graph.get_prerequisites("math_3_rectangle_perimeter")
    print(f"\n长方形周长的前置知识点：")
    for p in prereqs:
        print(f"  - {p.name} ({p.grade}年级)")

    # 测试学习路径
    path = graph.get_learning_path("math_2_times_table_all", "math_3_mult_application")
    print(f"\n学习路径：")
    for p in path:
        print(f"  {p.grade}年级 - {p.name}")
