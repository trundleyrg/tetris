import tkinter as tk


class Drawer(tk.Canvas):
    def __init__(self, master, c, r, cell_size):
        self.c = c
        self.r = r
        self.cell_size = cell_size
        height = r * cell_size
        width = c * cell_size
        super().__init__(master, width=width, height=height)
        self.pack()

    def init(self):
        for ri in range(self.r):
            for ci in range(self.c):
                self.draw_cell_by_cr(ci, ri, '')

    def draw_cell_by_cr(self, c, r, color, kind=None):
        x0 = c * cell_size
        y0 = r * cell_size
        x1 = c * cell_size + cell_size
        y1 = r * cell_size + cell_size
        # 三种类型
        # 没有俄罗斯方块，None
        # 失效的俄罗斯方块，dead
        # 俄罗斯方块，kind 代表第几个
        if kind is None:
            self.create_rectangle(x0, y0, x1, y1, fill="#CCCCCC", outline="white", width=2)
        elif kind == "dead":
            _tag = 'r%s' % r
            self.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2, tags=_tag)
        else:
            _tag = 'b%s' % kind
            self.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2, tags=_tag)

    def draw_block(self, block, kind):
        c, r = block['cr']
        shape_type = block['kind']
        cell_list = block['cell_list']
        for cell in cell_list:
            cell_c, cell_r = cell
            ci = cell_c + c
            ri = cell_r + r
            # 判断该位置方格在画板内部(画板外部的方格不再绘制)
            if 0 <= c < C and 0 <= r < R:
                self.draw_cell_by_cr(ci, ri, SHAPESCOLOR[shape_type], kind)

    def clean_by_block_id(self, block_id):
        _tag = 'b%s' % block_id
        self.delete(_tag)

    def clean_by_row(self, r):
        _tag = 'r%s' % r
        self.delete(_tag)
