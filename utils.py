import random
from tetris_shape import shapes_dict
from config import CELL_SIZE, BACKGROUND_COLOR, COLUMN


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
        ci = x + column
        ri = y + row
        draw_cell_by_cr(canvas, c=ci, r=ri, color=block["color"])


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
    # block_type = "O"
    loc_x = COLUMN // 2
    loc_y = 0
    new_block = {
        "type": block_type,
        "block": shapes_dict[block_type],
        'location': [loc_x, loc_y]  # 对应横纵坐标，以左上角为原点，水平向右为横坐标轴正方向，竖直向下为纵坐标轴正方向
    }
    return new_block
