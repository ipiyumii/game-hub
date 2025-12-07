# game.py
import random
import time
from typing import Dict, Tuple

from boardgen import generate_board, BoardGenError

class GameError(Exception):
    pass

class GameState:
    def __init__(self, N: int):
        self.N = N
        self.max_cell = N * N
        self.cell_rc_map, self.num_to_rc, self.ladders, self.snakes = generate_board(N)
        self.position = 1
        self.history = []
        self.round_start_time = time.perf_counter()

    def roll_dice(self) -> int:
        return random.randint(1, 6)

    def apply_snake_or_ladder(self, cell: int) -> int:
        if cell in self.ladders:
            return self.ladders[cell]
        if cell in self.snakes:
            return self.snakes[cell]
        return cell

    def move_by_dice(self, dice_value: int) -> Tuple[int,int]:
        if dice_value < 1 or dice_value > 6:
            raise GameError("Dice must be 1..6")
        start = self.position
        target = start + dice_value
        if target > self.max_cell:
            # common rule: overshoot means stay in place
            target = start
        final = self.apply_snake_or_ladder(target)
        self.position = final
        self.history.append((dice_value, start, final))
        return start, final

    def is_win(self) -> bool:
        return self.position == self.max_cell

    def reset(self):
        self.cell_rc_map, self.num_to_rc, self.ladders, self.snakes = generate_board(self.N)
        self.position = 1
        self.history.clear()
        self.round_start_time = time.perf_counter()
