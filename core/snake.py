#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @FileName: snake.py
# @Time: 07/05/2025 13:40
# @Author: Amundsen Severus Rubeus Bjaaland


import copy
import time
import threading
from multiprocessing import Queue
from typing import Iterable, List, Tuple

from .objects import Snake, Food, Field
from .utils import Position, Direction


class Events(object):
    @staticmethod
    def eat(
        snake: Snake, direction: Direction, food_list: Iterable[Food]
    ) -> List[Food]:
        """吃到食物"""
        buffer = []
        for i in food_list:
            if i.pos != snake.head_next(direction):
                buffer.append(i)
        return buffer
    
    @staticmethod
    def all_pos(snakes: Iterable[Snake]) -> List[Position]:
        """获取所有蛇的身体位置"""
        buffer = []
        for i in snakes:
            buffer.extend(i.body)
        return buffer


class SnakeGame(object):
    def __init__(
        self, width: int, height: int, players_id: Iterable[str]
    ):
        self.__field = Field(width, height)
        self.__snakes = {
            i: Snake(
                Position(int(width * 0.2), int(height * 0.2)) + \
                Position.random(int(width * 0.6), int(height * 0.6))
            )
            for i in players_id
        }
        self.__food = []
        
        self.__stop_flag = False
        self.__lock = threading.Lock()
        
        self.__time_queue = Queue()
        self.__control_queue = Queue()
    
    def get_snake(self, player_id: str) -> Snake | None:
        with self.__lock:
            return self.__snakes.get(player_id, None)
    
    @property
    def foods(self) -> Tuple[Food]:
        buffer = []
        with self.__lock:
            for i in self.__food: buffer.append(copy.deepcopy(i))
        return tuple(buffer)
    
    def __update_player(
        self, player_id: str, direction: Direction
    ) -> None:
        snake: Snake = self.get_snake(player_id)
        if snake is None:
            return 
        head_next = snake.head_next(direction)
        if not self.__field.in_bounds(head_next):
            snake.die()
        if head_next in Events.all_pos(self.__snakes.values()):
            snake.die()
        buffer = Events.eat(snake, direction, self.__food)
        if len(buffer) == len(self.__food):
            snake.step(direction)
        else:
            self.__food = buffer
            snake.step(direction, True)
    
    def time(self) -> None:
        while not self.__stop_flag:
            time.sleep(0.5)
            self.__time_queue.put(time.time())
    
    def run(self) -> None:
        while not self.__stop_flag:
            if not self.__control_queue.empty():
                data = self.__control_queue.get()
            for player_id, direction in data.items():
                self.__update_player(player_id, direction)
                    
                
    
    