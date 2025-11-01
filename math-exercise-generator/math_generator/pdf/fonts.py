"""
字体管理
"""
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping


class FontManager:
    """字体管理器"""

    _initialized = False

    @staticmethod
    def initialize():
        """初始化字体（只需调用一次）"""
        if FontManager._initialized:
            return

        # 尝试注册中文字体（支持大小写文件名）
        fonts_dir = Path(__file__).parent.parent.parent / "fonts"
        font_path = None

        for filename in ["simhei.ttf", "SimHei.ttf", "SIMHEI.TTF"]:
            test_path = fonts_dir / filename
            if test_path.exists():
                font_path = test_path
                break

        if font_path and font_path.exists():
            try:
                # 注册黑体
                pdfmetrics.registerFont(TTFont('SimHei', str(font_path)))
                # 添加字体映射
                addMapping('SimHei', 0, 0, 'SimHei')
                FontManager._initialized = True
                print(f"成功加载字体: {font_path}")
            except Exception as e:
                print(f"警告: 加载字体失败: {e}")
                print("将使用系统默认字体（可能无法显示中文）")
        else:
            print(f"警告: 未找到字体文件 {font_path}")
            print("将使用系统默认字体（可能无法显示中文）")

        FontManager._initialized = True

    @staticmethod
    def get_font_name() -> str:
        """获取可用的中文字体名称"""
        fonts_dir = Path(__file__).parent.parent.parent / "fonts"

        for filename in ["simhei.ttf", "SimHei.ttf", "SIMHEI.TTF"]:
            if (fonts_dir / filename).exists():
                return 'SimHei'

        # 使用 Helvetica（英文字体）
        return 'Helvetica'
