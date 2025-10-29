"""
配置文件
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 图片目录
PICTURES_DIR = ROOT_DIR / "pictures"

# 数据目录
DATA_DIR = ROOT_DIR / "data"
QUESTION_BANK_PATH = DATA_DIR / "questions.json"

# 输出目录
OUTPUT_DIR = ROOT_DIR / "output"
MISTAKE_PAPERS_DIR = OUTPUT_DIR / "mistake_papers"

# Claude API配置
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"  # 最新的Claude模型

# 题目类型
QUESTION_TYPES = {
    "calculation": "计算题",
    "application": "应用题",
    "fill_blank": "填空题",
    "choice": "选择题",
    "judge": "判断题",
    "column_calculation": "列竖式计算",
    "equation": "递等式计算",
}

# PDF配置
PDF_CONFIG = {
    "page_size": "A4",
    "font_name": "STSong",  # 宋体
    "font_size": 12,
    "title_font_size": 16,
    "margin": 50,
}

# 相似题生成配置
SIMILAR_QUESTIONS_COUNT = 2  # 每道错题生成的相似题数量
