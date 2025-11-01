"""
照片智能分组模块
自动识别并分组试卷照片
"""
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from .ai_provider import get_ai_provider


@dataclass
class PhotoMetadata:
    """照片元数据"""
    filename: str
    page_type: str  # "original", "graded", "corrected", "unknown"
    subject: Optional[str] = None  # "数学", "语文", "英语"
    title: Optional[str] = None  # "第三单元测试卷"
    exam_type: Optional[str] = None  # "单元测试", "月考", "期中考试"
    chapter: Optional[str] = None  # "第三单元"
    page_number: Optional[int] = None  # 页码
    total_pages: Optional[int] = None  # 总页数
    date: Optional[str] = None  # 考试日期
    score: Optional[str] = None  # 分数（批阅卷）
    confidence: float = 0.0  # AI 识别置信度


@dataclass
class ExamGroup:
    """考试分组"""
    exam_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    images: Dict[str, List[str]] = field(default_factory=lambda: {
        "original": [],
        "graded": [],
        "corrected": []
    })
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    confirmed: bool = False  # 是否已人工确认


class PhotoGrouper:
    """照片智能分组器"""

    def __init__(self, ai_provider_name: Optional[str] = None):
        """
        初始化照片分组器

        Args:
            ai_provider_name: AI 提供者名称（'claude' 或 'openai'）
        """
        self.ai_provider = get_ai_provider(ai_provider_name)

    def analyze_photo(self, image_path: Path) -> PhotoMetadata:
        """
        分析单张照片，提取元数据

        Args:
            image_path: 图片路径

        Returns:
            照片元数据
        """
        prompt = """请分析这张照片，识别以下信息：

1. **页面类型**：
   - original: 原始试卷（无批改标记）
   - graded: 批阅后的试卷（有红笔批改、分数等）
   - corrected: 订正页（学生重新答题）
   - unknown: 无法确定

2. **试卷信息**（如果是试卷）：
   - subject: 科目（数学/语文/英语）
   - title: 试卷标题（如"第三单元测试卷"）
   - exam_type: 考试类型（单元测试/月考/期中考试/期末考试）
   - chapter: 章节/单元（如"第三单元"）
   - page_number: 页码（如果有标注）
   - total_pages: 总页数（如果有标注）
   - date: 考试日期（如果有标注）
   - score: 分数（仅批阅卷，如"85/100"）

3. **置信度**：
   - confidence: 0.0-1.0，表示识别的置信度

请以 JSON 格式返回，格式如下：
{
  "page_type": "graded",
  "subject": "数学",
  "title": "第三单元测试卷",
  "exam_type": "单元测试",
  "chapter": "第三单元",
  "page_number": 1,
  "total_pages": 2,
  "date": "2025-01-15",
  "score": "85/100",
  "confidence": 0.95
}

如果某个字段无法识别，请设为 null。"""

        try:
            # 使用 AI 分析图像
            result = self.ai_provider.structured_output(
                prompt=prompt,
                response_format={
                    "page_type": "graded",
                    "subject": "数学",
                    "title": "第三单元测试卷",
                    "exam_type": "单元测试",
                    "chapter": "第三单元",
                    "page_number": 1,
                    "total_pages": 2,
                    "date": "2025-01-15",
                    "score": "85/100",
                    "confidence": 0.95
                }
            )

            # 注意：对于图像分析，需要使用 analyze_image 而不是 structured_output
            # 先用 analyze_image 获取文本响应
            response_text = self.ai_provider.analyze_image(
                image_path=image_path,
                prompt=prompt
            )

            # 尝试解析 JSON
            # 清理可能的 markdown 代码块
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            result = json.loads(response_text)

            return PhotoMetadata(
                filename=image_path.name,
                page_type=result.get("page_type", "unknown"),
                subject=result.get("subject"),
                title=result.get("title"),
                exam_type=result.get("exam_type"),
                chapter=result.get("chapter"),
                page_number=result.get("page_number"),
                total_pages=result.get("total_pages"),
                date=result.get("date"),
                score=result.get("score"),
                confidence=result.get("confidence", 0.0)
            )

        except Exception as e:
            print(f"警告：分析照片 {image_path.name} 时出错: {e}")
            # 返回未知类型
            return PhotoMetadata(
                filename=image_path.name,
                page_type="unknown",
                confidence=0.0
            )

    def group_photos(
        self,
        photo_dir: Path,
        photo_metadata_list: Optional[List[PhotoMetadata]] = None
    ) -> List[ExamGroup]:
        """
        将照片分组为考试

        Args:
            photo_dir: 照片目录
            photo_metadata_list: 照片元数据列表（如果已分析）

        Returns:
            考试分组列表
        """
        # 如果没有提供元数据，先分析所有照片
        if photo_metadata_list is None:
            image_files = sorted(
                [f for f in photo_dir.iterdir()
                 if f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp']],
                key=lambda x: x.name
            )
            photo_metadata_list = [
                self.analyze_photo(img) for img in image_files
            ]

        # 分组策略
        groups: List[ExamGroup] = []
        current_group: Optional[ExamGroup] = None

        for meta in photo_metadata_list:
            # 如果有明确的试卷标题，创建新分组
            if meta.title and meta.confidence > 0.6:
                # 检查是否与当前分组匹配
                if current_group and self._matches_group(current_group, meta):
                    # 添加到当前分组
                    self._add_to_group(current_group, meta)
                else:
                    # 创建新分组
                    current_group = self._create_new_group(meta)
                    groups.append(current_group)
            elif current_group and meta.page_type != "unknown":
                # 尝试归入当前分组
                self._add_to_group(current_group, meta)
            else:
                # 无法分组，创建独立分组
                current_group = self._create_new_group(meta)
                groups.append(current_group)

        return groups

    def _matches_group(self, group: ExamGroup, meta: PhotoMetadata) -> bool:
        """
        判断照片是否属于当前分组

        Args:
            group: 考试分组
            meta: 照片元数据

        Returns:
            是否匹配
        """
        # 比较科目和标题
        if group.metadata.get("subject") == meta.subject and \
           group.metadata.get("title") == meta.title:
            return True
        return False

    def _create_new_group(self, meta: PhotoMetadata) -> ExamGroup:
        """
        创建新的考试分组

        Args:
            meta: 照片元数据

        Returns:
            新的考试分组
        """
        group = ExamGroup()

        # 设置元数据
        group.metadata = {
            "subject": meta.subject,
            "title": meta.title or "未命名考试",
            "exam_type": meta.exam_type,
            "chapter": meta.chapter,
            "date": meta.date,
            "total_pages": meta.total_pages
        }

        # 添加第一张照片
        self._add_to_group(group, meta)

        return group

    def _add_to_group(self, group: ExamGroup, meta: PhotoMetadata) -> None:
        """
        将照片添加到分组

        Args:
            group: 考试分组
            meta: 照片元数据
        """
        page_type = meta.page_type
        if page_type in group.images:
            group.images[page_type].append(meta.filename)
        else:
            group.images["original"].append(meta.filename)

        # 更新分数（如果是批阅卷）
        if meta.score and not group.metadata.get("score"):
            group.metadata["score"] = meta.score

    def save_groups(self, groups: List[ExamGroup], output_file: Path) -> None:
        """
        保存分组结果

        Args:
            groups: 考试分组列表
            output_file: 输出文件路径
        """
        data = {
            "total_groups": len(groups),
            "created_at": datetime.now().isoformat(),
            "groups": [asdict(g) for g in groups]
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_groups(self, input_file: Path) -> List[ExamGroup]:
        """
        加载分组结果

        Args:
            input_file: 输入文件路径

        Returns:
            考试分组列表
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        groups = []
        for g_data in data["groups"]:
            group = ExamGroup(**g_data)
            groups.append(group)

        return groups
