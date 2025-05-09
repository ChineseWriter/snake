#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @FileName: objects.py
# @Time: 05/05/2025 11:43
# @Author: Amundsen Severus Rubeus Bjaaland


import copy
import hashlib
from typing import List, Tuple

from .utils import Position, Direction


class Snake(object):
    def __init__(self, init_pos: Position):
        self.__body: List[Position] = [init_pos, init_pos.down]
        self.__alive = True
        
    def __len__(self) -> int:
        return len(self.__body)
    
    def __hash__(self):
        body = [f"{i.x}, {i.y}" for i in self.__body]
        body = "; ".join(body).encode("UTF-8")
        
        sha256 = hashlib.sha256()
        sha256.update(body)
        
        return int(sha256.hexdigest(), 16)
    
    def __eq__(self, other: "Snake"):
        if not isinstance(other, Snake):
            return False
        return self.__hash__() == other.__hash__()
    
    def __repr__(self) -> str:
        return f"<Snake head={self.__body[0].xy} len={len(self)}>"
    
    @property
    def alive(self) -> bool:
        return self.__alive
    
    @property
    def body(self) -> Tuple[Position]:
        buffer = []
        for i in self.__body:
            buffer.append(copy.deepcopy(i))
        return tuple(buffer)
    
    @property
    def head(self) -> Position:
        return copy.deepcopy(self.__body[0])
    
    @property
    def direction(self) -> Direction:
        if self.__body[0].on_the_left_of(self.__body[1]):
            return Direction.LEFT
        elif self.__body[0].on_the_right_of(self.__body[1]):
            return Direction.RIGHT
        elif self.__body[0].on_the_top_of(self.__body[1]):
            return Direction.UP
        else:
            return Direction.DOWN
    
    def die(self) -> None:
        self.__alive = False
    
    def head_next(self, direction: Direction) -> Position:
        head = self.__body[0]
        match direction:
            case Direction.UP: return head.up
            case Direction.DOWN: return head.down
            case Direction.LEFT: return head.left
            case Direction.RIGHT: return head.right
    
    def step(
        self, direction: Direction | None, grow: bool = False
    ) -> None:
        if not self.__alive:
            return
        
        if direction is None:
            direction = self.direction
        
        # 移动蛇头
        head = self.__body[0]
        match direction:
            case Direction.UP: new_head = head.up
            case Direction.DOWN: new_head = head.down
            case Direction.LEFT: new_head = head.left
            case Direction.RIGHT: new_head = head.right
        
        match self.direction:
            case Direction.UP:
                if direction == Direction.DOWN:
                    new_head = head.up
            case Direction.DOWN:
                if direction == Direction.UP:
                    new_head = head.down
            case Direction.LEFT:
                if direction == Direction.RIGHT:
                    new_head = head.left
            case Direction.RIGHT:
                if direction == Direction.LEFT:
                    new_head = head.right
        
        # 更新蛇身
        self.__body.insert(0, new_head)
        if not grow: self.__body.pop()


class Food(object):
    def __init__(self, init_pos: Position):
        self.__position = init_pos
    
    def __hash__(self):
        pos = str(self.__position.xy).encode("UTF-8")
        
        sha256 = hashlib.sha256()
        sha256.update(pos)
        
        return int(sha256.hexdigest(), 16)
    
    def __eq__(self, other: "Food"):
        if not isinstance(other, Food):
            return False
        return self.__hash__() == other.__hash__()
    
    def __repr__(self) -> str:
        return f"<Food pos={self.__position.xy}>"
    
    @property
    def pos(self) -> Position:
        return copy.deepcopy(self.__position)


class Field(object):
    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height
    
    def __repr__(self) -> str:
        return f"<Field width={self.__width} height={self.__height}>"
    
    @property
    def width(self) -> int:
        return self.__width
    
    @property
    def height(self) -> int:
        return self.__height
    
    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.__width and 0 <= pos.y < self.__height