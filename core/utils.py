#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @FileName: utils.py
# @Time: 05/05/2025 11:40
# @Author: Amundsen Severus Rubeus Bjaaland


import random
import hashlib
from enum import Enum


class Position(object):
    def __init__(self, x: int, y: int):
        """位置类, 表示一个二维坐标位置
        注意: 对于计算机坐标系, y轴向下为正方向, x轴向右为正方向,
        也就是左上角为(0, 0), 右下角为(width, height)
        
        :param x: x坐标
        :type x: int
        :param y: y坐标
        :type y: int
        """
        self.__x = x
        self.__y = y
    
    def __repr__(self) -> str:
        return f"<Position x={self.__x} y={self.__y}>"
    
    def __hash__(self) -> int:
        pos = f"{self.__x}, {self.__y}".encode("UTF-8")
        
        sha256 = hashlib.sha256()
        sha256.update(pos)
        
        return int(sha256.hexdigest(), 16)
    
    def __eq__(self, other: "Position") -> bool:
        if not isinstance(other, Position):
            return False
        return self.__hash__() == other.__hash__()
    
    def __add__(self, other: "Position") -> "Position":
        if not isinstance(other, Position):
            raise TypeError("Position 只能与 Position 相加")
        return Position(self.__x + other.x, self.__y + other.y)
    
    def __sub__(self, other: "Position") -> "Position":
        if not isinstance(other, Position):
            raise TypeError("Position 只能与 Position 相减")
        return Position(self.__x - other.x, self.__y - other.y)
    
    @staticmethod
    def random(width: int, height: int) -> "Position":
        random_x = random.randint(0, width - 1)
        random_y = random.randint(0, height - 1)
        return Position(random_x, random_y)
    
    def on_the_left_of(self, other: "Position") -> bool:
        """判断当前坐标是否在另一个坐标的左侧"""
        return self.__x < other.x
    
    def on_the_right_of(self, other: "Position") -> bool:
        """判断当前坐标是否在另一个坐标的右侧"""
        return self.__x > other.x
    
    def on_the_top_of(self, other: "Position") -> bool:
        """判断当前坐标是否在另一个坐标的上方"""
        return self.__y < other.y
    
    def on_the_bottom_of(self, other: "Position") -> bool:
        """判断当前坐标是否在另一个坐标的下方"""
        return self.__y > other.y
    
    @property
    def x(self) -> int:
        return self.__x
    
    @property
    def y(self) -> int:
        return self.__y
    
    @property
    def xy(self) -> tuple[int, int]:
        return self.__x, self.__y
    
    @property
    def left(self) -> "Position":
        return Position(self.__x - 1, self.__y)
    
    @property
    def right(self) -> "Position":
        return Position(self.__x + 1, self.__y)
    
    @property
    def up(self) -> "Position":
        return Position(self.__x, self.__y - 1)
    
    @property
    def down(self) -> "Position":
        return Position(self.__x, self.__y + 1)


class Direction(Enum):
    """方向枚举类, 用于表示一个方向
    注意: 对于计算机坐标系, y轴向下为正方向, x轴向右为正方向,
    也就是左上角为(0, 0), 右下角为(width, height)
    """
    
    UP = (1, "up")
    DOWN = (2, "down")
    LEFT = (3, "left")
    RIGHT = (4, "right")
    
    def __int__(self):
        return self.value[0]
    
    def __str__(self):
        return self.value[1]
    
    @classmethod
    def from_int(cls, value: int) -> "Direction":
        """根据整数值获取方向枚举类
        注意: 若整数值不在1-4之间, 则返回上方向
        
        :param value: 整数值, 1表示上, 2表示下, 3表示左, 4表示右
        :type value: int
        """
        if value == 1:
            return cls.UP
        elif value == 2:
            return cls.DOWN
        elif value == 3:
            return cls.LEFT
        elif value == 4:
            return cls.RIGHT
        else:
            return cls.UP
    
    @classmethod
    def from_str(cls, value: str) -> "Direction":
        """根据字符串值获取方向枚举类
        注意: 若字符串值不在"up", "down", "left", "right"之间, 则返回上方向
        
        :param value: 字符串值, "up"表示上, "down"表示下, "left"表示左, "right"表示右
        :type value: str
        """
        if value == "up":
            return cls.UP
        elif value == "down":
            return cls.DOWN
        elif value == "left":
            return cls.LEFT
        elif value == "right":
            return cls.RIGHT
        else:
            return cls.UP