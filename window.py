import random
import tkinter as tk

from tetris_shape import shapes_dict
from config import *


class Drawer(tk.Canvas):
    def __init__(self, master):
        # 初始化窗口
        super().__init__(master, width=COLUMN * CELL_SIZE, height=ROW * CELL_SIZE)
        self.pack()


class GameApp:
    def __init__(self):
        self.fps = FPS
        self.game_num = 1
        msg_width = 0  # 消息栏宽度
        msg_height = 0  # 消息栏高度
        width = self.game_num * (CELL_SIZE * COLUMN + msg_width)
        height = self.game_num * (CELL_SIZE * ROW + msg_height)
        self.win = tk.Tk()
        self.win.geometry("%sx%s+%s+%s" % (width, height, 200, 200))

        self.running = True  # 运行状态
        self.count = 0

    def generate_new_block(self):
        """生成新方块"""
        block_shape = random.choice(list(shapes_dict.keys()))

        # block出生位置
        block_x = random.randint(0, COLUMN - 1)
        block_location = [block_x, 0]

        new_block = {
            'kind': block_shape,
            'shape': shapes_dict[block_shape],
            'location': block_location,
        }

    def game_loop(self):
        if self.running:
            self.win.update()

            if self.count % GENSPEED:
                self.generate_new_block()

            self.count = (self.count + 1) % GENSPEED
            self.win.after(self.fps, self.game_loop)

    def __call__(self):
        self.game_loop()
        self.win.mainloop()


def main():
    game = GameApp()
    game()


if __name__ == '__main__':
    main()
