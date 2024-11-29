import tkinter as tk

from config import CELL_SIZE
from tetris_shape import shapes_dict


def draw_cell_by_cr(canvas, c, r, color="#CCCCCC"):
    """
    :param canvas: 画板，用于绘制一个方块的Canvas对象
    :param c: 方块所在列
    :param r: 方块所在行
    :param color: 方块颜色，默认为#CCCCCC，轻灰色
    :return:
    """
    x0 = c * CELL_SIZE
    y0 = r * CELL_SIZE
    x1 = c * CELL_SIZE + CELL_SIZE
    y1 = r * CELL_SIZE + CELL_SIZE
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)


def draw_blank_board(canvas, column, row):
    # 绘制空白面板
    for r_i in range(row):
        for c_i in range(column):
            draw_cell_by_cr(canvas, c=c_i, r=r_i)


def draw_cells(canvas, column, row,  block: dict):
    """
    绘制指定形状指定颜色的俄罗斯方块
    :param canvas: 画板
    :param column: 该形状设定的原点所在的列
    :param row: 该形状设定的原点所在的行
    :param block: 形状类
    :return:
    """
    for x, y in block["shape"]:
        ci = y + column
        ri = x + row
        draw_cell_by_cr(canvas, c=ci, r=ri, color=block["color"])


def main():
    """绘制几种俄罗斯方块的形状"""
    win = tk.Tk()
    width_cell = 6  # 6个cell
    height_cell = 4 * len(shapes_dict.keys())  # N个格子
    canvas = tk.Canvas(win, width=6 * CELL_SIZE, height=4 * len(shapes_dict.keys()) * CELL_SIZE)
    canvas.pack()

    draw_blank_board(canvas, row=height_cell,  column=width_cell)

    for i, key in enumerate(shapes_dict.keys()):
        center_x = 3
        center_y = i * 4 + 2  # 每个方块展示位置占用4行
        print(key, center_x, center_y)
        draw_cells(canvas, row=center_y, column=center_x, block=shapes_dict[key])

    win.mainloop()


if __name__ == '__main__':
    main()
