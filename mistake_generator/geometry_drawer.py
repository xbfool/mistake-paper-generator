"""
几何图形绘制模块
自动生成几何题目的图形（SVG格式）
"""
import math
from typing import Dict, Any, List, Tuple


class GeometryDrawer:
    """几何图形绘制器"""

    def __init__(self, grid_size: int = 20):
        """
        初始化绘图器

        Args:
            grid_size: 网格大小（像素）
        """
        self.grid_size = grid_size

    def draw_shape(
        self,
        shape_type: str,
        shape_params: Dict[str, Any],
        width: int = 400,
        height: int = 300,
        show_grid: bool = True,
        show_labels: bool = True
    ) -> str:
        """
        绘制几何图形（返回SVG代码）

        Args:
            shape_type: 图形类型 (rectangle/square/circle/triangle)
            shape_params: 图形参数
            width: SVG画布宽度
            height: SVG画布高度
            show_grid: 是否显示网格
            show_labels: 是否显示标注

        Returns:
            SVG代码字符串
        """
        svg_parts = []

        # SVG头部
        svg_parts.append(f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">')

        # 背景
        svg_parts.append(f'  <rect width="{width}" height="{height}" fill="white" stroke="#ddd" stroke-width="1"/>')

        # 网格（可选）
        if show_grid:
            svg_parts.append(self._draw_grid(width, height))

        # 根据类型绘制图形
        if shape_type == "rectangle":
            svg_parts.append(self._draw_rectangle(shape_params, width, height, show_labels))
        elif shape_type == "square":
            svg_parts.append(self._draw_square(shape_params, width, height, show_labels))
        elif shape_type == "circle":
            svg_parts.append(self._draw_circle(shape_params, width, height, show_labels))
        elif shape_type == "triangle":
            svg_parts.append(self._draw_triangle(shape_params, width, height, show_labels))

        # SVG尾部
        svg_parts.append('</svg>')

        return '\n'.join(svg_parts)

    def _draw_grid(self, width: int, height: int) -> str:
        """绘制网格"""
        grid_svg = []
        grid_svg.append('  <g class="grid" stroke="#f0f0f0" stroke-width="0.5">')

        # 垂直线
        for x in range(0, width + 1, self.grid_size):
            grid_svg.append(f'    <line x1="{x}" y1="0" x2="{x}" y2="{height}"/>')

        # 水平线
        for y in range(0, height + 1, self.grid_size):
            grid_svg.append(f'    <line x1="0" y1="{y}" x2="{width}" y2="{y}"/>')

        grid_svg.append('  </g>')
        return '\n'.join(grid_svg)

    def _draw_rectangle(
        self,
        params: Dict[str, Any],
        canvas_width: int,
        canvas_height: int,
        show_labels: bool
    ) -> str:
        """绘制长方形"""
        length = params.get('length', params.get('width', 8))
        width = params.get('width', params.get('height', 5))

        # 计算实际像素大小（每个单位用grid_size表示）
        rect_width = length * self.grid_size
        rect_height = width * self.grid_size

        # 居中
        x = (canvas_width - rect_width) // 2
        y = (canvas_height - rect_height) // 2

        svg = []
        svg.append('  <g class="shape">')

        # 长方形
        svg.append(f'    <rect x="{x}" y="{y}" width="{rect_width}" height="{rect_height}" ')
        svg.append('          fill="none" stroke="#2196F3" stroke-width="2"/>')

        # 标注
        if show_labels:
            # 长度标注（上方）
            svg.append(f'    <line x1="{x}" y1="{y-10}" x2="{x+rect_width}" y2="{y-10}" ')
            svg.append('          stroke="#666" stroke-width="1" marker-start="url(#arrowstart)" marker-end="url(#arrowend)"/>')
            svg.append(f'    <text x="{x+rect_width//2}" y="{y-15}" text-anchor="middle" ')
            svg.append(f'          font-size="14" fill="#333">{length}cm</text>')

            # 宽度标注（右侧）
            svg.append(f'    <line x1="{x+rect_width+10}" y1="{y}" x2="{x+rect_width+10}" y2="{y+rect_height}" ')
            svg.append('          stroke="#666" stroke-width="1" marker-start="url(#arrowstart)" marker-end="url(#arrowend)"/>')
            svg.append(f'    <text x="{x+rect_width+15}" y="{y+rect_height//2}" ')
            svg.append(f'          font-size="14" fill="#333">{width}cm</text>')

        svg.append('  </g>')

        # 添加箭头定义
        if show_labels:
            svg.insert(0, self._get_arrow_markers())

        return '\n'.join(svg)

    def _draw_square(
        self,
        params: Dict[str, Any],
        canvas_width: int,
        canvas_height: int,
        show_labels: bool
    ) -> str:
        """绘制正方形"""
        side = params.get('side', 6)

        # 计算实际像素大小
        square_size = side * self.grid_size

        # 居中
        x = (canvas_width - square_size) // 2
        y = (canvas_height - square_size) // 2

        svg = []
        svg.append('  <g class="shape">')

        # 正方形
        svg.append(f'    <rect x="{x}" y="{y}" width="{square_size}" height="{square_size}" ')
        svg.append('          fill="none" stroke="#4CAF50" stroke-width="2"/>')

        # 标注
        if show_labels:
            # 边长标注
            svg.append(f'    <line x1="{x}" y1="{y-10}" x2="{x+square_size}" y2="{y-10}" ')
            svg.append('          stroke="#666" stroke-width="1" marker-start="url(#arrowstart)" marker-end="url(#arrowend)"/>')
            svg.append(f'    <text x="{x+square_size//2}" y="{y-15}" text-anchor="middle" ')
            svg.append(f'          font-size="14" fill="#333">{side}米</text>')

        svg.append('  </g>')

        if show_labels:
            svg.insert(0, self._get_arrow_markers())

        return '\n'.join(svg)

    def _draw_circle(
        self,
        params: Dict[str, Any],
        canvas_width: int,
        canvas_height: int,
        show_labels: bool
    ) -> str:
        """绘制圆形"""
        radius = params.get('radius', 4)

        # 计算实际像素大小
        r = radius * self.grid_size

        # 居中
        cx = canvas_width // 2
        cy = canvas_height // 2

        svg = []
        svg.append('  <g class="shape">')

        # 圆形
        svg.append(f'    <circle cx="{cx}" cy="{cy}" r="{r}" ')
        svg.append('          fill="none" stroke="#FF9800" stroke-width="2"/>')

        # 标注
        if show_labels:
            # 半径标注
            svg.append(f'    <line x1="{cx}" y1="{cy}" x2="{cx+r}" y2="{cy}" ')
            svg.append('          stroke="#666" stroke-width="1" stroke-dasharray="5,5"/>')
            svg.append(f'    <text x="{cx+r//2}" y="{cy-5}" text-anchor="middle" ')
            svg.append(f'          font-size="14" fill="#333">r={radius}cm</text>')

            # 圆心
            svg.append(f'    <circle cx="{cx}" cy="{cy}" r="3" fill="#666"/>')

        svg.append('  </g>')

        return '\n'.join(svg)

    def _draw_triangle(
        self,
        params: Dict[str, Any],
        canvas_width: int,
        canvas_height: int,
        show_labels: bool
    ) -> str:
        """绘制三角形"""
        base = params.get('base', 8)
        height = params.get('height', 6)

        # 计算实际像素大小
        base_px = base * self.grid_size
        height_px = height * self.grid_size

        # 居中
        x1 = (canvas_width - base_px) // 2
        y1 = (canvas_height + height_px) // 2
        x2 = x1 + base_px
        y2 = y1
        x3 = (x1 + x2) // 2
        y3 = y1 - height_px

        svg = []
        svg.append('  <g class="shape">')

        # 三角形
        svg.append(f'    <polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" ')
        svg.append('          fill="none" stroke="#E91E63" stroke-width="2"/>')

        # 标注
        if show_labels:
            # 底边标注
            svg.append(f'    <line x1="{x1}" y1="{y1+10}" x2="{x2}" y2="{y1+10}" ')
            svg.append('          stroke="#666" stroke-width="1" marker-start="url(#arrowstart)" marker-end="url(#arrowend)"/>')
            svg.append(f'    <text x="{(x1+x2)//2}" y="{y1+25}" text-anchor="middle" ')
            svg.append(f'          font-size="14" fill="#333">底={base}cm</text>')

            # 高标注
            svg.append(f'    <line x1="{x3}" y1="{y3}" x2="{x3}" y2="{y1}" ')
            svg.append('          stroke="#666" stroke-width="1" stroke-dasharray="5,5"/>')
            svg.append(f'    <text x="{x3+20}" y="{(y3+y1)//2}" ')
            svg.append(f'          font-size="14" fill="#333">高={height}cm</text>')

        svg.append('  </g>')

        if show_labels:
            svg.insert(0, self._get_arrow_markers())

        return '\n'.join(svg)

    def _get_arrow_markers(self) -> str:
        """获取箭头标记定义"""
        return """  <defs>
    <marker id="arrowstart" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="5,0 10,5 5,10" fill="#666"/>
    </marker>
    <marker id="arrowend" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
      <polygon points="0,5 5,0 5,10" fill="#666"/>
    </marker>
  </defs>"""


if __name__ == "__main__":
    # 测试代码
    drawer = GeometryDrawer(grid_size=20)

    # 测试长方形
    print("生成长方形...")
    rect_svg = drawer.draw_shape("rectangle", {"length": 8, "width": 5})
    with open("test_rectangle.svg", "w", encoding="utf-8") as f:
        f.write(rect_svg)

    # 测试正方形
    print("生成正方形...")
    square_svg = drawer.draw_shape("square", {"side": 6})
    with open("test_square.svg", "w", encoding="utf-8") as f:
        f.write(square_svg)

    # 测试圆形
    print("生成圆形...")
    circle_svg = drawer.draw_shape("circle", {"radius": 4})
    with open("test_circle.svg", "w", encoding="utf-8") as f:
        f.write(circle_svg)

    print("测试完成！")
