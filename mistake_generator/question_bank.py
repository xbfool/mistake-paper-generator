"""
题库管理模块
用于存储、查询和管理题目数据
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Question(BaseModel):
    """题目数据模型"""
    id: str = Field(default="", description="题目唯一ID")
    question_number: str = Field(description="题号")
    question_type: str = Field(description="题目类型")
    question_content: str = Field(description="题目内容")
    student_answer: Optional[str] = Field(default=None, description="学生答案")
    correct_answer: Optional[str] = Field(default=None, description="正确答案")
    is_mistake: bool = Field(default=False, description="是否是错题")
    mistake_type: Optional[str] = Field(default=None, description="错误类型")
    knowledge_points: List[str] = Field(default_factory=list, description="知识点")
    source_image: Optional[str] = Field(default=None, description="来源图片")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="创建时间")

    def __init__(self, **data):
        super().__init__(**data)
        if not self.id:
            # 生成唯一ID：时间戳 + 题号
            self.id = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{self.question_number.replace(' ', '_')}"


class QuestionBank:
    """题库管理器"""

    def __init__(self, db_path: Path):
        """
        初始化题库

        Args:
            db_path: 题库JSON文件路径
        """
        self.db_path = db_path
        self.questions: List[Question] = []
        self.metadata: Dict[str, Any] = {
            "total_count": 0,
            "mistake_count": 0,
            "last_updated": None,
            "question_types": {}
        }
        self.load()

    def load(self):
        """从文件加载题库"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.questions = [Question(**q) for q in data.get('questions', [])]
                    self.metadata = data.get('metadata', self.metadata)
                print(f"题库加载成功：{len(self.questions)} 道题目")
            except Exception as e:
                print(f"题库加载失败: {e}")
                self.questions = []
        else:
            print("题库文件不存在，将创建新题库")

    def save(self):
        """保存题库到文件"""
        # 更新元数据
        self.metadata['total_count'] = len(self.questions)
        self.metadata['mistake_count'] = sum(1 for q in self.questions if q.is_mistake)
        self.metadata['last_updated'] = datetime.now().isoformat()

        # 统计各类型题目数量
        type_counts = {}
        for q in self.questions:
            type_counts[q.question_type] = type_counts.get(q.question_type, 0) + 1
        self.metadata['question_types'] = type_counts

        # 保存到文件
        data = {
            'metadata': self.metadata,
            'questions': [q.model_dump() for q in self.questions]
        }

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"题库已保存：{len(self.questions)} 道题目")

    def add_question(self, question: Question):
        """添加题目"""
        self.questions.append(question)

    def add_questions(self, questions: List[Question]):
        """批量添加题目"""
        self.questions.extend(questions)

    def get_all_questions(self) -> List[Question]:
        """获取所有题目"""
        return self.questions

    def get_mistakes(self) -> List[Question]:
        """获取所有错题"""
        return [q for q in self.questions if q.is_mistake]

    def get_by_type(self, question_type: str) -> List[Question]:
        """根据类型获取题目"""
        return [q for q in self.questions if q.question_type == question_type]

    def get_mistakes_by_type(self, question_type: str) -> List[Question]:
        """根据类型获取错题"""
        return [q for q in self.questions if q.is_mistake and q.question_type == question_type]

    def import_from_analysis_results(self, analysis_results: List[Dict[str, Any]]):
        """
        从图像分析结果导入题目

        Args:
            analysis_results: 图像分析结果列表
        """
        imported_count = 0
        for result in analysis_results:
            source_image = result.get('image_path', '')
            for q_data in result.get('questions', []):
                # 创建Question对象
                question = Question(
                    question_number=q_data.get('question_number', ''),
                    question_type=q_data.get('question_type', '未分类'),
                    question_content=q_data.get('question_content', ''),
                    student_answer=q_data.get('student_answer'),
                    correct_answer=q_data.get('correct_answer'),
                    is_mistake=q_data.get('is_mistake', False),
                    mistake_type=q_data.get('mistake_type'),
                    knowledge_points=q_data.get('knowledge_points', []),
                    source_image=source_image
                )
                self.add_question(question)
                imported_count += 1

        print(f"成功导入 {imported_count} 道题目")
        self.save()

    def print_statistics(self):
        """打印题库统计信息"""
        print("\n" + "=" * 60)
        print("题库统计信息")
        print("=" * 60)
        print(f"总题目数: {self.metadata['total_count']}")
        print(f"错题数: {self.metadata['mistake_count']}")
        print(f"正确题数: {self.metadata['total_count'] - self.metadata['mistake_count']}")
        print(f"最后更新: {self.metadata['last_updated']}")
        print("\n各类型题目统计:")
        for q_type, count in self.metadata['question_types'].items():
            mistakes = len(self.get_mistakes_by_type(q_type))
            print(f"  {q_type}: {count} 道 (错题: {mistakes})")
        print("=" * 60)

    def clear(self):
        """清空题库"""
        self.questions = []
        self.save()
        print("题库已清空")


if __name__ == "__main__":
    # 测试代码
    from .config import QUESTION_BANK_PATH

    bank = QuestionBank(QUESTION_BANK_PATH)
    bank.print_statistics()
