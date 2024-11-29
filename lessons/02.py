import random
import tkinter as tk

from config import *
from tetris_shape import shapes_dict


def draw_cell_by_cr(canvas, r, c, color="#CCCCCC"):
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


def draw_blank_board(canvas, row, column):
    # 绘制空白面板
    for r_i in range(row):
        for c_i in range(column):
            draw_cell_by_cr(canvas, r_i, c_i)


def draw_cells(canvas, row, column, block: dict):
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


def draw_block_move(canvas, block, direction=[0, 0]):
    """
    绘制向指定方向移动后的俄罗斯方块
    :param canvas: 画板
    :param block: 俄罗斯方块对象
    :param direction: 俄罗斯方块移动方向
    :return:
    """
    tetri = block["block"]
    raw_r, raw_c = block['location']  # 初始位置

    # 移动前，先清除原有位置绘制的俄罗斯方块，用背景色绘制原有的俄罗斯方块
    draw_cells(canvas, raw_r, raw_c, {"shape": tetri["shape"], "color": BACKGROUND_COLOR})

    dc, dr = direction
    new_r, new_c = raw_r + dr, raw_c + dc  # 更新位置
    block['location'] = [new_r, new_c]
    # 在新位置绘制新的俄罗斯方块
    draw_cells(canvas, new_r, new_c, tetri)


def main():
    # 初始化
    win = tk.Tk()
    canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT)
    canvas.pack()

    draw_blank_board(canvas, row=ROW, column=COLUMN)

    # 生成一个俄罗斯方块
    block_type = random.choice(list(shapes_dict.keys()))
    loc_x = COLUMN // 2
    loc_y = 0
    new_block = {
        "type": block_type,
        "block": shapes_dict[block_type],
        'location': [loc_x, loc_y]  # 对应横纵坐标，以左上角为原点，水平向右为横坐标轴正方向，竖直向下为纵坐标轴正方向
    }
    draw_block_move(canvas, new_block)
    win.update()

    def game_loop():
        win.update()

        down = [1, 0]
        draw_block_move(canvas, new_block, down)

        win.after(FPS, game_loop)

    win.after(FPS, game_loop)  # 在FPS 毫秒后调用 game_loop方法

    win.mainloop()


if __name__ == '__main__':
    main()
