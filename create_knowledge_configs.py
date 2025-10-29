#!/usr/bin/env python3
"""
知识点配置文件批量生成器
使用 Claude AI 根据教学大纲生成完整的知识点配置
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()


class KnowledgeConfigGenerator:
    """知识点配置生成器"""

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.output_dir = Path("knowledge_data")

    def generate_math_grade(self, grade: int, point_count: int):
        """生成数学年级配置"""
        print(f"\n{'='*60}")
        print(f"正在生成：数学 {grade} 年级配置 ({point_count}个知识点)")
        print(f"{'='*60}\n")

        prompt = f"""请为小学{grade}年级数学创建完整的知识点配置文件（JSON格式）。

要求：
1. 总共约{point_count}个知识点
2. 按模块分类（如：数的认识、计算能力、几何图形、应用能力等）
3. 每个知识点必须包含：
   - id: 唯一标识，格式为 math_{grade}_xxx
   - category: 所属模块
   - name: 知识点名称
   - description: 详细描述
   - difficulty: 难度（1-5）
   - keywords: 关键词列表
   - prerequisites: 前置知识点ID列表（来自低年级）
   - next_points: 后续知识点ID列表
   - typical_questions: 典型题型列表
   - common_mistakes: 常见错误列表
   - learning_tips: 学习建议
   - importance: 重要性（1-5）
   - avg_learning_time: 平均学习时间（分钟）

4. 包含该年级的题型配置（口算、计算、填空、应用等）

请严格按照中国{grade}年级数学教学大纲，确保知识点完整、准确、符合实际教学内容。

返回格式：
{{
  "subject": "数学",
  "grade": {grade},
  "total_points": {point_count},
  "modules": {{
    "模块名": {{
      "description": "模块描述",
      "points": [...]
    }}
  }},
  "question_types": {{...}}
}}

请返回完整的JSON配置（不要省略）。"""

        try:
            print("调用 Claude API 生成配置...")

            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=16000,  # 大容量，确保完整输出
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # 提取JSON
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            # 解析JSON
            config = json.loads(response_text)

            # 保存文件
            output_file = self.output_dir / "math" / f"grade_{grade}.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            print(f"✓ 成功生成: {output_file}")
            print(f"  知识点数量: {len(self._count_points(config))}")

            return config

        except Exception as e:
            print(f"✗ 生成失败: {e}")
            return None

    def generate_chinese_grade(self, grade: int, point_count: int):
        """生成语文年级配置"""
        print(f"\n{'='*60}")
        print(f"正在生成：语文 {grade} 年级配置 ({point_count}个知识点)")
        print(f"{'='*60}\n")

        prompt = f"""请为小学{grade}年级语文创建完整的知识点配置文件（JSON格式）。

要求：
1. 总共约{point_count}个知识点
2. 按模块分类（如：拼音、识字写字、词语句子、阅读理解、古诗文、写作等）
3. 每个知识点包含完整字段（同数学）
4. 符合中国{grade}年级语文教学大纲

返回完整JSON配置。"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=16000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # 提取JSON
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            config = json.loads(response_text)

            # 保存文件
            output_file = self.output_dir / "chinese" / f"grade_{grade}.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            print(f"✓ 成功生成: {output_file}")
            print(f"  知识点数量: {len(self._count_points(config))}")

            return config

        except Exception as e:
            print(f"✗ 生成失败: {e}")
            return None

    def generate_english_grade(self, grade: int, point_count: int):
        """生成英语年级配置"""
        print(f"\n{'='*60}")
        print(f"正在生成：英语 {grade} 年级配置 ({point_count}个知识点)")
        print(f"{'='*60}\n")

        prompt = f"""请为小学{grade}年级英语创建完整的知识点配置文件（JSON格式）。

要求：
1. 总共约{point_count}个知识点
2. 按模块分类（如：字母、词汇、句型、语法、听力、阅读、写作等）
3. 每个知识点包含完整字段
4. 符合中国{grade}年级英语教学大纲

返回完整JSON配置。"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=16000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # 提取JSON
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            config = json.loads(response_text)

            # 保存文件
            output_file = self.output_dir / "english" / f"grade_{grade}.json"
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            print(f"✓ 成功生成: {output_file}")
            print(f"  知识点数量: {len(self._count_points(config))}")

            return config

        except Exception as e:
            print(f"✗ 生成失败: {e}")
            return None

    def _count_points(self, config: dict) -> list:
        """统计知识点数量"""
        points = []
        for module in config.get("modules", {}).values():
            points.extend(module.get("points", []))
        return points

    def generate_all(self):
        """生成所有配置文件"""
        print("\n" + "="*60)
        print("开始批量生成知识点配置文件")
        print("="*60)

        # 数学配置计划
        math_plan = [
            (4, 45),
            (5, 50),
            (6, 55)
        ]

        # 语文配置计划
        chinese_plan = [
            (1, 25),
            (2, 30),
            (3, 35),
            (4, 40),
            (5, 45),
            (6, 50)
        ]

        # 英语配置计划（从3年级开始）
        english_plan = [
            (3, 30),
            (4, 35),
            (5, 40),
            (6, 45)
        ]

        # 生成数学
        print("\n" + "="*60)
        print("第一部分：数学学科")
        print("="*60)
        for grade, count in math_plan:
            self.generate_math_grade(grade, count)

        # 生成语文
        print("\n" + "="*60)
        print("第二部分：语文学科")
        print("="*60)
        for grade, count in chinese_plan:
            self.generate_chinese_grade(grade, count)

        # 生成英语
        print("\n" + "="*60)
        print("第三部分：英语学科")
        print("="*60)
        for grade, count in english_plan:
            self.generate_english_grade(grade, count)

        print("\n" + "="*60)
        print("✓ 所有配置文件生成完成！")
        print("="*60)

        # 统计
        self.print_statistics()

    def print_statistics(self):
        """打印统计信息"""
        print("\n配置文件统计：")
        print("-"*60)

        total_files = 0
        total_points = 0

        for subject in ["math", "chinese", "english"]:
            subject_dir = self.output_dir / subject
            if not subject_dir.exists():
                continue

            subject_files = list(subject_dir.glob("grade_*.json"))
            subject_points = 0

            for file in subject_files:
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        points = self._count_points(config)
                        subject_points += len(points)
                except:
                    pass

            total_files += len(subject_files)
            total_points += subject_points

            print(f"{subject.upper():8s}: {len(subject_files):2d} 文件, {subject_points:3d} 知识点")

        print("-"*60)
        print(f"总计：{total_files} 个文件，{total_points} 个知识点")
        print("="*60)


if __name__ == "__main__":
    generator = KnowledgeConfigGenerator()

    print("知识点配置批量生成器")
    print("\n选项：")
    print("  1. 生成数学配置（4-6年级）")
    print("  2. 生成语文配置（1-6年级）")
    print("  3. 生成英语配置（3-6年级）")
    print("  4. 生成全部配置")
    print("  5. 查看统计信息")

    choice = input("\n请选择（1-5）：").strip()

    if choice == "1":
        for grade, count in [(4, 45), (5, 50), (6, 55)]:
            generator.generate_math_grade(grade, count)
    elif choice == "2":
        for grade, count in [(1, 25), (2, 30), (3, 35), (4, 40), (5, 45), (6, 50)]:
            generator.generate_chinese_grade(grade, count)
    elif choice == "3":
        for grade, count in [(3, 30), (4, 35), (5, 40), (6, 45)]:
            generator.generate_english_grade(grade, count)
    elif choice == "4":
        generator.generate_all()
    elif choice == "5":
        generator.print_statistics()
    else:
        print("无效选择")
