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
        return tuple(copy.deepcopy(self.__body))
    
    def die(self) -> None:
        self.__alive = False


class Food(object):
    pass


class Field(object):
    pass
