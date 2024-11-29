import tkinter as tk

from config import *
from utils import *
from tetris_shape import shapes_dict


def check_move(block, block_list, direction=[0, 0]):
    """
    判断俄罗斯方块是否可以朝指定方向移动
    :param block: 俄罗斯方块对象
    :param block_list: 背景列表
    :param direction: 俄罗斯方块移动方向
    :return: boolean 是否可以朝指定方向移动
    """
    x, y = block['location']
    cell_list = block['block']["shape"]

    for cell in cell_list:
        cell_c, cell_r = cell
        cur_x = cell_c + x + direction[0]
        cur_y = cell_r + y + direction[1]

        # 边界检测
        # 判断该位置是否超出左右边界，以及下边界
        # 一般不判断上边界，因为俄罗斯方块生成的时候，可能有一部分在上边界之上还没有出来
        if cur_x >= COLUMN or cur_x < 0 or cur_y >= ROW:
            return False

        # 判断y不小于0，且该位置是否有方块
        if cur_y >= 0 and block_list[cur_x][cur_y]:
            return False

    return True


def save_block_to_list(block, block_list):
    """将当前方块放置位置同步到背景列表"""
    shape_type = block['type']
    x, y = block['location']
    cell_list = block["block"]["shape"]

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + x
        r = cell_r + y
        block_list[c][r] = shape_type  # block_list 在对应位置记下其类型


def horizontal_move_block(event, canvas, block_list, current_block):
    """
    左右水平移动俄罗斯方块
    """
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    if current_block is not None and check_move(current_block, block_list, direction=direction):
        draw_block_move(canvas, current_block, direction)


def rotate_block(canvas, current_block, event):
    """旋转block"""
    if current_block is None:
        return

    cell_list = current_block['shape']
    rotate_list = []
    for cell in cell_list:
        x, y = cell
        rotate_cell = [y, -x]
        rotate_list.append(rotate_cell)

    block_after_rotate = {
        "type": current_block['type'],
        "block": {"shape": rotate_list, "color": current_block['color']},  # 旋转后的shape
        "location": current_block['location'],
    }

    if check_move(block_after_rotate, block_list):
        raw_r, raw_c = current_block['location']
        draw_cells(canvas, row=raw_r, column=raw_c,
                   block={"type": current_block["type"], "shape": current_block["shape"],
                          "color": BACKGROUND_COLOR})  # 清除原来的形状
        draw_cells(canvas, row=raw_r, column=raw_c, block=block_after_rotate)
        return block_after_rotate


def land(event, canvas, block_list, current_block):
    if current_block is None:
        return

    cell_list = current_block['block']["shape"]
    x, y = current_block['location']
    min_height = ROW
    for cell in cell_list:
        cur_x, cur_y = x + cell[0], y + cell[1]
        if block_list[cur_x][cur_y]:
            return
        h = 0
        for yi in range(y + 1, ROW):
            if block_list[cur_x][yi]:
                break
            else:
                h += 1
        if h < min_height:
            min_height = h

    down = [0, min_height]
    if check_move(current_block, block_list, direction=down):
        draw_block_move(canvas, current_block, down)


def game_loop(canvas, win, current_block, block_list):
    if current_block is None:
        new_block = generate_new_block()
        draw_block_move(canvas, new_block)  # 绘制新生成的俄罗斯方块
        current_block = new_block
    else:
        if check_move(current_block, block_list, direction=[0, 1]):
            draw_block_move(canvas, current_block, [0, 1])
        else:
            # 无法移动，记入 block_list 中
            save_block_to_list(current_block, block_list)
            current_block = None

    win.after(FPS, game_loop, canvas, win, current_block, block_list)


def main():
    # 初始化
    win = tk.Tk()
    canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT)
    canvas.pack()

    draw_blank_board(canvas, row=ROW, column=COLUMN)

    # 初始化背景列表
    block_list = [['' for _ in range(ROW)] for _ in range(COLUMN)]

    canvas.focus_set()  # 聚焦到canvas画板对象上
    canvas.bind("<KeyPress-Left>", lambda e: horizontal_move_block(e, canvas, block_list, current_block))
    canvas.bind("<KeyPress-Right>", lambda e: horizontal_move_block(e, canvas, block_list, current_block))
    # canvas.bind("<KeyPress-Up>", rotate_block)
    canvas.bind("<KeyPress-Down>", lambda e: land(e, canvas, block_list, current_block))

    current_block = None

    win.update()
    win.after(FPS, game_loop, canvas, win, current_block, block_list)  # 在FPS 毫秒后调用 game_loop方法

    win.mainloop()


if __name__ == '__main__':
    main()
