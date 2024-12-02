# 俄罗斯方块

1. Python内置Tkinter库简单使用；
2. Python俄罗斯方块游戏的逻辑介绍及运动控制效果实现；
3. Python俄罗斯方块游戏的数据结构；
4. Python俄罗斯方块游戏软件架构设计；
5. Python俄罗斯方块游戏碰撞检测；
6. Python俄罗斯方块游戏得分计算；
7. Python俄罗斯方块游戏暂停、数据文件保存；
8. Python俄罗斯方块游戏初始化加载、重新开始和简单特效；
9. Python俄罗斯方块游戏双人对战实现；

## 采用opencv图像坐标系

x, col
y, row

## 1. lesson-1 创建俄罗斯方块的形状

## 2. lesson-2 俄罗斯方块在界面的生成及运动

canvas中运动的block结构：
```python
block = {
    "type": block_type,
    "block": shapes_dict[block_type],
    'location': [loc_x, loc_y]
    }
```

## 3. lesson-3 俄罗斯方块的运动控制及碰撞检测

上下左右方向键及功能实现
形状碰撞检测
形状停靠
下落处理

## 4，lesson-4 行消除以及得分计算

行消除逻辑，计分栏更新

## 5. 暂停、保存数据文件

暂停，存档，读档

## 6. 重新开始和简单特效

## 7. 双人对战实现

