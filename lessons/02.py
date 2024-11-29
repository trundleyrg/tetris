import random
import tkinter as tk

from config import *
from tetris_shape import shapes_dict
from utils import draw_cells, draw_blank_board


def draw_block_move(canvas, block, direction=[0, 0]):
    """
    绘制向指定方向移动后的俄罗斯方块
    :param canvas: 画板
    :param block: 俄罗斯方块
    :param direction: 俄罗斯方块移动方向
    :return:
    """
    tetri = block["block"]
    raw_x, raw_y = block['location']  # 初始位置

    # 移动前，先清除原有位置绘制的俄罗斯方块，用背景色绘制原有的俄罗斯方块
    draw_cells(canvas, column=raw_x, row=raw_y,
               block={"shape": tetri["shape"], "color": BACKGROUND_COLOR})

    x, y = direction
    new_x, new_y = raw_x + x, raw_y + y  # 更新位置
    block['location'] = [new_x, new_y]
    # 在新位置绘制新的俄罗斯方块
    draw_cells(canvas, column=new_x, row=new_y, block=tetri)


def generate_new_block():
    """随机生成新的俄罗斯方块"""
    block_type = random.choice(list(shapes_dict.keys()))
    loc_x = COLUMN // 2
    loc_y = 0
    new_block = {
        "type": block_type,
        "block": shapes_dict[block_type],
        'location': [loc_x, loc_y]  # 对应横纵坐标，以左上角为原点，水平向右为横坐标轴正方向，竖直向下为纵坐标轴正方向
    }
    return new_block


def main():
    # 初始化
    win = tk.Tk()
    canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT)
    canvas.pack()

    draw_blank_board(canvas, column=COLUMN, row=ROW)

    # 生成一个俄罗斯方块
    new_block = generate_new_block()
    draw_block_move(canvas, new_block)
    win.update()

    def game_loop():
        win.update()

        down = [0, 1]
        draw_block_move(canvas, new_block, down)

        win.after(FPS, game_loop)

    win.after(FPS, game_loop)  # 在FPS 毫秒后调用 game_loop方法

    win.mainloop()


if __name__ == '__main__':
    main()
