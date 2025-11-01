"""
三维度薄弱点分析系统
分析维度：
1. 卷面表现（首次答题）
2. 订正效果
3. 知识点掌握程度分类
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from .question_parser_v2 import QuestionV2


@dataclass
class KnowledgePointStatus:
    """知识点掌握状态"""
    knowledge_point: str
    category: str  # "已掌握", "可巩固", "深度薄弱", "未测试"
    first_correct_rate: float  # 首次正确率
    correction_correct_rate: float  # 订正正确率
    total_questions: int
    first_correct_count: int
    correction_correct_count: int
    need_practice: bool


@dataclass
class ExamPerformance:
    """考试表现分析"""
    exam_id: str
    subject: str
    title: str
    date: Optional[str]

    # 卷面表现
    total_questions: int
    first_correct: int
    first_wrong: int
    first_correct_rate: float

    # 订正情况
    corrected_count: int
    correction_success: int
    correction_failed: int
    correction_success_rate: float

    # 错题分布
    mistake_distribution: Dict[str, int]  # 题型 -> 错题数


@dataclass
class WeaknessAnalysis:
    """薄弱点分析结果"""
    subject: str

    # 知识点分类
    mastered_points: List[KnowledgePointStatus] = field(default_factory=list)  # 已掌握
    consolidate_points: List[KnowledgePointStatus] = field(default_factory=list)  # 可巩固
    weak_points: List[KnowledgePointStatus] = field(default_factory=list)  # 深度薄弱
    untested_points: List[KnowledgePointStatus] = field(default_factory=list)  # 未测试

    # 考试表现列表
    exam_performances: List[ExamPerformance] = field(default_factory=list)


class DualAnalyzer:
    """双维度分析器"""

    def __init__(self):
        """初始化分析器"""
        pass

    def analyze_exam(
        self,
        exam_id: str,
        subject: str,
        title: str,
        questions: List[QuestionV2],
        date: Optional[str] = None
    ) -> ExamPerformance:
        """
        分析单次考试的表现

        Args:
            exam_id: 考试ID
            subject: 科目
            title: 考试标题
            questions: 题目列表
            date: 考试日期

        Returns:
            考试表现分析
        """
        total = len(questions)
        first_correct = sum(1 for q in questions if q.first_attempt.is_correct)
        first_wrong = total - first_correct

        # 统计订正情况
        corrected_questions = [q for q in questions if q.correction.has_corrected]
        corrected_count = len(corrected_questions)
        correction_success = sum(1 for q in corrected_questions if q.correction.is_correct)
        correction_failed = corrected_count - correction_success

        # 错题分布
        mistake_dist = defaultdict(int)
        for q in questions:
            if not q.first_attempt.is_correct and q.question_type:
                mistake_dist[q.question_type] += 1

        return ExamPerformance(
            exam_id=exam_id,
            subject=subject,
            title=title,
            date=date,
            total_questions=total,
            first_correct=first_correct,
            first_wrong=first_wrong,
            first_correct_rate=first_correct / total if total > 0 else 0.0,
            corrected_count=corrected_count,
            correction_success=correction_success,
            correction_failed=correction_failed,
            correction_success_rate=correction_success / corrected_count if corrected_count > 0 else 0.0,
            mistake_distribution=dict(mistake_dist)
        )

    def analyze_knowledge_points(
        self,
        questions: List[QuestionV2],
        all_knowledge_points: Optional[List[str]] = None
    ) -> Dict[str, KnowledgePointStatus]:
        """
        分析知识点掌握情况

        Args:
            questions: 题目列表
            all_knowledge_points: 所有知识点列表（用于识别未测试的知识点）

        Returns:
            知识点状态字典
        """
        # 统计每个知识点的情况
        kp_stats = defaultdict(lambda: {
            "total": 0,
            "first_correct": 0,
            "has_correction": 0,
            "correction_correct": 0,
            "need_practice": False
        })

        for question in questions:
            for kp in question.knowledge_points:
                kp_stats[kp]["total"] += 1

                if question.first_attempt.is_correct:
                    kp_stats[kp]["first_correct"] += 1

                if question.correction.has_corrected:
                    kp_stats[kp]["has_correction"] += 1
                    if question.correction.is_correct:
                        kp_stats[kp]["correction_correct"] += 1

                if question.error_analysis.suggest_practice:
                    kp_stats[kp]["need_practice"] = True

        # 转换为 KnowledgePointStatus 对象
        kp_statuses = {}
        for kp, stats in kp_stats.items():
            total = stats["total"]
            first_correct = stats["first_correct"]
            correction_correct = stats["correction_correct"]
            has_correction = stats["has_correction"]

            first_rate = first_correct / total if total > 0 else 0.0
            correction_rate = correction_correct / has_correction if has_correction > 0 else 0.0

            # 分类知识点
            category = self._classify_knowledge_point(
                first_rate,
                correction_rate,
                has_correction > 0
            )

            kp_statuses[kp] = KnowledgePointStatus(
                knowledge_point=kp,
                category=category,
                first_correct_rate=first_rate,
                correction_correct_rate=correction_rate,
                total_questions=total,
                first_correct_count=first_correct,
                correction_correct_count=correction_correct,
                need_practice=stats["need_practice"]
            )

        return kp_statuses

    def _classify_knowledge_point(
        self,
        first_rate: float,
        correction_rate: float,
        has_correction: bool
    ) -> str:
        """
        分类知识点掌握程度

        Args:
            first_rate: 首次正确率
            correction_rate: 订正正确率
            has_correction: 是否有订正

        Returns:
            分类：已掌握、可巩固、深度薄弱、未测试
        """
        # 已掌握：首次正确率 >= 80%
        if first_rate >= 0.8:
            return "已掌握"

        # 如果没有订正记录
        if not has_correction:
            if first_rate >= 0.6:
                return "已掌握"
            else:
                return "可巩固"

        # 深度薄弱：首次错误，订正后仍错
        if first_rate < 0.5 and correction_rate < 0.5:
            return "深度薄弱"

        # 可巩固：首次错误，订正后正确
        if first_rate < 0.8 and correction_rate >= 0.8:
            return "可巩固"

        # 默认可巩固
        return "可巩固"

    def generate_weakness_analysis(
        self,
        subject: str,
        all_questions: List[QuestionV2],
        all_knowledge_points: Optional[List[str]] = None
    ) -> WeaknessAnalysis:
        """
        生成薄弱点分析报告

        Args:
            subject: 科目
            all_questions: 所有题目列表
            all_knowledge_points: 所有知识点列表

        Returns:
            薄弱点分析结果
        """
        # 分析知识点
        kp_statuses = self.analyze_knowledge_points(all_questions, all_knowledge_points)

        # 分类知识点
        analysis = WeaknessAnalysis(subject=subject)

        for kp_status in kp_statuses.values():
            if kp_status.category == "已掌握":
                analysis.mastered_points.append(kp_status)
            elif kp_status.category == "可巩固":
                analysis.consolidate_points.append(kp_status)
            elif kp_status.category == "深度薄弱":
                analysis.weak_points.append(kp_status)

        # 按优先级排序
        analysis.weak_points.sort(key=lambda x: x.first_correct_rate)  # 深度薄弱按正确率升序
        analysis.consolidate_points.sort(key=lambda x: x.correction_correct_rate, reverse=True)  # 可巩固按订正正确率降序
        analysis.mastered_points.sort(key=lambda x: x.first_correct_rate, reverse=True)  # 已掌握按正确率降序

        return analysis

    def generate_learning_suggestions(
        self,
        weakness_analysis: WeaknessAnalysis,
        ai_provider
    ) -> str:
        """
        生成学习建议

        Args:
            weakness_analysis: 薄弱点分析结果
            ai_provider: AI 提供者

        Returns:
            学习建议（Markdown 格式）
        """
        # 构建提示词
        weak_points_str = "\n".join([
            f"- {kp.knowledge_point}（首次{kp.first_correct_rate*100:.0f}%，订正{kp.correction_correct_rate*100:.0f}%）"
            for kp in weakness_analysis.weak_points[:3]  # 最多3个
        ])

        consolidate_points_str = "\n".join([
            f"- {kp.knowledge_point}（首次{kp.first_correct_rate*100:.0f}%，订正{kp.correction_correct_rate*100:.0f}%）"
            for kp in weakness_analysis.consolidate_points[:3]  # 最多3个
        ])

        prompt = f"""请为这个{weakness_analysis.subject}学生生成本周学习建议。

### 深度薄弱知识点（需家长辅导）：
{weak_points_str if weak_points_str else "无"}

### 可巩固知识点（可自主练习）：
{consolidate_points_str if consolidate_points_str else "无"}

请生成结构化的学习建议，包括：
1. **优先级1：深度薄弱点** - 需要重点关注，给出具体的学习方法
2. **优先级2：可巩固知识点** - 需要反复练习，给出练习建议
3. **优先级3：保持练习** - 已掌握的知识点也要保持练习

请用 Markdown 格式返回，语气要鼓励性，建议要具体可操作。"""

        try:
            suggestions = ai_provider.text_completion(
                prompt=prompt,
                temperature=0.7
            )
            return suggestions
        except Exception as e:
            print(f"警告：生成学习建议失败: {e}")
            return "（暂时无法生成学习建议）"
