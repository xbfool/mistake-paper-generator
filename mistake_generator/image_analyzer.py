"""
图像分析模块
使用 Claude Vision API 识别图片中的题目和错题标记
"""
import base64
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from anthropic import Anthropic
from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL, QUESTION_TYPES


class ImageAnalyzer:
    """图像分析器，用于识别试卷图片中的题目"""

    def __init__(self, api_key: str = None):
        """
        初始化图像分析器

        Args:
            api_key: Anthropic API密钥，如果不提供则从配置中读取
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("未找到 ANTHROPIC_API_KEY，请在 .env 文件中配置")
        self.client = Anthropic(api_key=self.api_key)

    def encode_image(self, image_path: Path) -> str:
        """
        将图片编码为base64

        Args:
            image_path: 图片路径

        Returns:
            base64编码的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.standard_b64encode(image_file.read()).decode("utf-8")

    def analyze_image(self, image_path: Path) -> Dict[str, Any]:
        """
        分析单张图片，识别其中的题目

        Args:
            image_path: 图片路径

        Returns:
            包含题目信息的字典
        """
        print(f"正在分析图片: {image_path.name}...", flush=True)

        # 读取并编码图片
        image_data = self.encode_image(image_path)
        print("  图片已加载，正在调用API识别...", flush=True)

        # 构建提示词
        prompt = f"""请仔细分析这张三年级数学试卷图片，提取所有题目信息。

要求：
1. 识别图片中的所有题目（包括题号、题目内容、学生的答案）
2. 识别哪些题目被红笔标记为错题（通常被红圈、红叉标记）
3. 对每道题目进行分类：{', '.join(QUESTION_TYPES.values())}
4. 提取题目的正确答案（如果能看到）

请以JSON格式返回结果，格式如下：
{{
    "page_info": {{
        "title": "试卷标题",
        "grade": "年级",
        "subject": "科目"
    }},
    "questions": [
        {{
            "question_number": "题号（如(1)、1、第1题等）",
            "question_type": "题目类型（从上述类型中选择对应的中文名称）",
            "question_content": "题目内容（完整的题目文本）",
            "student_answer": "学生的答案（如果有）",
            "correct_answer": "正确答案（如果能看到或推断出）",
            "is_mistake": true/false,  // 是否是错题
            "mistake_type": "错误类型描述（如果是错题）",
            "knowledge_points": ["知识点1", "知识点2"]  // 涉及的知识点
        }}
    ]
}}

注意：
- 请准确识别红笔标记
- 如果题目内容包含数学公式，请用文本形式表示（如：3×5=15）
- 如果无法确定某些字段，可以设为null
- 请确保返回的是有效的JSON格式"""

        # 调用Claude API
        try:
            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )

            # 解析响应
            response_text = message.content[0].text

            # 尝试从响应中提取JSON
            # Claude 可能会在JSON前后添加一些说明文字，需要提取出JSON部分
            response_text = response_text.strip()

            # 如果响应包含markdown代码块，提取其中的内容
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            # 解析JSON
            result = json.loads(response_text)
            result["image_path"] = str(image_path)

            print(f"  ✓ 识别到 {len(result.get('questions', []))} 道题目", flush=True)
            mistakes = sum(1 for q in result.get('questions', []) if q.get('is_mistake', False))
            print(f"  ✓ 其中错题 {mistakes} 道", flush=True)

            return result

        except Exception as e:
            print(f"  ✗ 分析失败: {str(e)}", flush=True)
            return {
                "image_path": str(image_path),
                "error": str(e),
                "page_info": {},
                "questions": []
            }

    def analyze_all_images(self, image_dir: Path) -> List[Dict[str, Any]]:
        """
        分析目录中的所有图片

        Args:
            image_dir: 图片目录路径

        Returns:
            所有图片的分析结果列表
        """
        # 获取所有图片文件
        image_files = sorted(
            [f for f in image_dir.glob("*.jpg") if f.is_file()] +
            [f for f in image_dir.glob("*.jpeg") if f.is_file()] +
            [f for f in image_dir.glob("*.png") if f.is_file()]
        )

        if not image_files:
            print(f"在 {image_dir} 中未找到图片文件", flush=True)
            return []

        print(f"\n找到 {len(image_files)} 张图片，开始分析...", flush=True)
        print("=" * 60, flush=True)

        results = []
        for idx, image_path in enumerate(image_files, 1):
            print(f"\n[{idx}/{len(image_files)}] ", end="", flush=True)
            result = self.analyze_image(image_path)
            results.append(result)

        print("\n" + "=" * 60, flush=True)
        print(f"分析完成！共处理 {len(results)} 张图片", flush=True)

        return results


if __name__ == "__main__":
    # 测试代码
    from .config import PICTURES_DIR

    analyzer = ImageAnalyzer()
    results = analyzer.analyze_all_images(PICTURES_DIR)

    # 打印统计信息
    total_questions = sum(len(r.get('questions', [])) for r in results)
    total_mistakes = sum(
        sum(1 for q in r.get('questions', []) if q.get('is_mistake', False))
        for r in results
    )

    print(f"\n总计识别题目: {total_questions} 道")
    print(f"总计错题: {total_mistakes} 道")
