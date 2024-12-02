import json
import tkinter as tk
from tkinter import messagebox

from config import *
from utils import *

scores = 0  # 记录分数
current_block = None  # 当前方块
background_list = [['' for _ in range(ROW)] for _ in range(COLUMN)]  # 初始化背景列表
pause = False


def check_move(block, direction=[0, 0]):
    """
    判断俄罗斯方块是否可以朝指定方向移动
    :param block: 俄罗斯方块对象
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
        if cur_y >= 0 and background_list[cur_x][cur_y]:
            return False

    return True


def save_block_to_list(block):
    """将当前方块放置位置同步到背景列表"""
    global background_list
    shape_type = block['type']
    x, y = block['location']
    cell_list = block["block"]["shape"]

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + x
        r = cell_r + y
        background_list[c][r] = shape_type  # block_list 在对应位置记下其类型


def horizontal_move_block(event, canvas):
    """
    左右水平移动俄罗斯方块
    """
    global current_block
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    if current_block is not None and check_move(current_block, direction=direction):
        draw_block_move(canvas, current_block, direction)


def rotate_block(event, canvas):
    """旋转block"""
    global current_block
    if current_block is None:
        return

    cell_list = current_block['block']["shape"]
    rotate_list = []
    for cell in cell_list:
        x, y = cell
        rotate_cell = [y, -x]
        rotate_list.append(rotate_cell)

    block_after_rotate = {
        "type": current_block['type'],
        "block": {"shape": rotate_list,
                  "color": current_block["block"]['color']},  # 旋转后的shape
        "location": current_block['location'],  # 以原点为中心旋转，原点位置不变
    }

    if check_move(block_after_rotate):
        raw_x, raw_y = current_block['location']
        draw_cells(canvas, column=raw_x, row=raw_y,
                   block={"type": current_block["type"],
                          "shape": current_block["block"]["shape"],
                          "color": BACKGROUND_COLOR})  # 清除原来的形状
        current_block = block_after_rotate  # 旋转有效时，替换全局变量
        draw_cells(canvas, column=raw_x, row=raw_y, block=current_block["block"])


def land(event, canvas):
    global current_block
    if current_block is None:
        return

    cell_list = current_block['block']["shape"]
    x, y = current_block['location']
    min_height = ROW
    for cell in cell_list:
        cur_x, cur_y = x + cell[0], y + cell[1]
        if background_list[cur_x][cur_y]:
            return
        h = 0
        for yi in range(y + 1, ROW):
            if background_list[cur_x][yi]:
                break
            else:
                h += 1
        if h - cell[1] < min_height:  # 以原点为中心估算下落高度
            min_height = h - cell[1]

    down = [0, min_height]
    if check_move(current_block, direction=down):
        draw_block_move(canvas, current_block, down)


def draw_board(canvas):
    """按照更新后的block_list绘制界面"""
    for column_index in range(len(background_list)):
        for row_index in range(len(background_list[0])):
            cell_type = background_list[column_index][row_index]
            if cell_type == "":
                draw_cell_by_cr(canvas, c=column_index, r=row_index, color=BACKGROUND_COLOR)  # 设置为背景色
            else:
                draw_cell_by_cr(canvas, c=column_index, r=row_index, color=shapes_dict[cell_type]["color"])


def check_and_clear(canvas, score_label):
    """检查block_list中是否有满行，有则消除"""
    global scores, background_list

    def check_row_complete(row):
        """检查一行是否已满"""
        return all(cell != '' for cell in row)

    # 转置数组，方便计算
    block_list_copy = [[row[i] for row in background_list] for i in range(len(background_list[0]))]

    has_complete_row = False
    for row_index in range(len(block_list_copy)):
        if check_row_complete(block_list_copy[row_index]):
            has_complete_row = True
            # 当前行可消除
            if row_index > 0:
                # 非最下面的行，将上面的行整体下移
                for cur_ri in range(row_index, 0, -1):
                    block_list_copy[cur_ri] = block_list_copy[cur_ri - 1][:]
            # 对于最上面那一行，直接置空
            block_list_copy[0] = ['' for _ in range(len(block_list_copy[0]))]
            scores += 10  # 消除一行加十分

    if has_complete_row:
        # 转置回原数组
        # print("clear line!")
        background_list = [[row[i] for row in block_list_copy] for i in range(len(block_list_copy[0]))]
        draw_board(canvas)  # 绘制消除后的背景
        score_label.config(text="Scores: {}".format(scores))


def pause_action():
    """暂停标志位变更"""
    global pause
    pause = not pause


def save_record():
    with open("record.json", "w") as f:
        json.dump(background_list, f)


def load_record(canvas):
    global background_list
    with open("record.json", "r") as f:
        background_list = json.load(f)
    # 重新更新界面
    for c_i in range(len(background_list)):
        for r_i in range(len(background_list[0])):
            if background_list[c_i][r_i] != "":
                draw_cell_by_cr(canvas, c=c_i, r=r_i, color=shapes_dict[background_list[c_i][r_i]]["color"])
            else:
                draw_cell_by_cr(canvas, c=c_i, r=r_i, color=BACKGROUND_COLOR)


def game_loop(canvas, win, score_label):
    win.update()
    global current_block, pause
    if not pause:
        if current_block is None:
            new_block = generate_new_block()
            draw_block_move(canvas, new_block)  # 绘制新生成的俄罗斯方块
            current_block = new_block
            if not check_move(current_block, direction=[0, 0]):  # 检查是否游戏结束
                messagebox.showinfo("Game Over", "Game Over")
                win.destroy()
                return
        else:
            if check_move(current_block, direction=[0, 1]):
                draw_block_move(canvas, current_block, [0, 1])
            else:
                # 无法移动，记入 block_list 中
                save_block_to_list(current_block)
                current_block = None
                check_and_clear(canvas, score_label)  # 检查同行消除

    win.after(FPS, game_loop, canvas, win, score_label)


def main():
    # 初始化
    win = tk.Tk()
    canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT)
    canvas.pack()

    draw_blank_board(canvas, row=ROW, column=COLUMN)

    canvas.focus_set()  # 聚焦到canvas画板对象上
    canvas.bind("<KeyPress-Left>", lambda e: horizontal_move_block(e, canvas))
    canvas.bind("<KeyPress-Right>", lambda e: horizontal_move_block(e, canvas))
    canvas.bind("<KeyPress-Up>", lambda e: rotate_block(e, canvas))
    canvas.bind("<KeyPress-Down>", lambda e: land(e, canvas))

    current_block = None

    # 底部补充计分栏
    score_label = tk.Label(win, text="Scores: {}".format(scores))
    score_label.pack(side=tk.BOTTOM)

    # 存档、读档
    save_button = tk.Button(win, text="存档", command=save_record)
    save_button.pack(side=tk.TOP)
    load_button = tk.Button(win, text="读档", command=lambda: load_record(canvas))
    load_button.pack(side=tk.TOP)

    # 增加暂停按钮
    pause_button = tk.Button(win, text="暂停/继续", command=pause_action)
    pause_button.pack(side=tk.TOP)

    win.update()
    win.after(FPS, game_loop, canvas, win, score_label)  # 在FPS 毫秒后调用 game_loop方法

    win.mainloop()


if __name__ == '__main__':
    main()
