#!/usr/bin/env python3
"""
智能学习系统 - TUI终端界面入口

使用方法：
  python3 tui_app.py

快捷键：
  Q - 退出
  H - 帮助
  1-7 - 快速导航
  Ctrl+S - 切换学生
  Ctrl+R - 刷新数据
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from ui.tui.app import LearningSystemApp


def main():
    """主函数"""
    print("正在启动智能学习系统TUI...")
    print("提示：按 Q 退出，按 H 查看帮助\n")

    app = LearningSystemApp()

    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"\n\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
