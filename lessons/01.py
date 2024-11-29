import tkinter as tk

from config import *
from tetris_shape import *


def draw_cell_by_cr(canvas, c, r, color="#CCCCCC"):
    x0 = c * cell_size
    y0 = r * cell_size
    x1 = c * cell_size + cell_size
    y1 = r * cell_size + cell_size
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)


def draw_blank_board(canvas, column, row):
    for r_i in range(row):
        for c_i in range(column):
            draw_cell_by_cr(canvas, c_i, r_i)


def draw_cells(canvas, row, column, block:dict):
    """
    绘制指定形状指定颜色的俄罗斯方块
    :param canvas: 画板
    :param row: 该形状设定的原点所在的行
    :param column: 该形状设定的原点所在的列
    :param block: 形状类
    :return:
    """
    for x, y in block["shape"]:
        ci = y + column
        ri = x + row
        draw_cell_by_cr(canvas, ci, ri, block["color"])


def main():
    win = tk.Tk()
    width_cell = 6  # 6个cell
    height_cell = 5 * len(shapes_dict.keys())  # N个格子
    canvas = tk.Canvas(win, width=6 * cell_size, height=4 * len(shapes_dict.keys()) * cell_size)
    canvas.pack()

    draw_blank_board(canvas, width_cell, height_cell)

    for i, key in enumerate(shapes_dict.keys()):
        center_x = 3
        center_y = i * 4 + 2  # 每个方块展示位置占用4行
        print(key, center_x, center_y)
        draw_cells(canvas, row=center_y, column=center_x, block=shapes_dict[key])

    win.mainloop()


if __name__ == '__main__':
    main()
