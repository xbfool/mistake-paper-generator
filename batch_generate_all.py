#!/usr/bin/env python3
"""
批量生成所有知识点配置文件（非交互模式）
"""
import sys
sys.path.insert(0, '.')

from create_knowledge_configs import KnowledgeConfigGenerator

if __name__ == "__main__":
    generator = KnowledgeConfigGenerator()

    print("\n" + "="*60)
    print("开始批量生成所有知识点配置文件")
    print("="*60)
    print("\n这将生成：")
    print("  - 数学4-6年级（3个文件，150个知识点）")
    print("  - 语文1-6年级（6个文件，225个知识点）")
    print("  - 英语3-6年级（4个文件，150个知识点）")
    print("  - 总计：13个文件，525个知识点")
    print("\n预计需要5-10分钟...\n")

    generator.generate_all()

    print("\n✓ 全部完成！")
