# boardgen.py
import random
from typing import Dict, Tuple, Set

class BoardGenError(Exception):
    pass

def validate_board_size(N: int):
    if not isinstance(N, int):
        raise BoardGenError("Board size N must be an integer.")
    if N < 6 or N > 12:
        raise BoardGenError("Board size N must be between 6 and 12.")

def make_snaking_number_map(N: int) -> Dict[Tuple[int,int], int]:
    """
    (row, col) -> cell number using classic snake-ladder zigzag numbering.
    row 0 is top row, row N-1 bottom row. Cell 1 is bottom-left.
    """
    mapping = {}
    number = 1
    for r in range(N-1, -1, -1):              # bottom -> top
        row_index = (N - 1) - r
        if row_index % 2 == 0:
            cols = range(0, N)               # left -> right
        else:
            cols = range(N-1, -1, -1)        # right -> left
        for c in cols:
            mapping[(r, c)] = number
            number += 1
    return mapping

def invert_map_cell_to_rc(N: int) -> Dict[int, Tuple[int,int]]:
    m = make_snaking_number_map(N)
    return {num: rc for rc, num in m.items()}

def random_pairs_for_ladders_and_snakes(N: int, count: int):
    """
    Create `count` ladders and `count` snakes as dicts:
      ladders[bottom] = top  (bottom < top)
      snakes[head] = tail    (head > tail)
    Constraints:
      - no endpoints at 1 or N^2
      - no overlapping endpoints
    """
    max_cell = N * N
    forbidden = {1, max_cell}
    available = set(range(2, max_cell))
    if count * 2 > len(available):
        raise BoardGenError("Board too small for requested features.")

    ladders: Dict[int,int] = {}
    snakes: Dict[int,int] = {}
    used: Set[int] = set()

    # place ladders
    attempts = 0
    while len(ladders) < count and attempts < count * 200:
        bottom = random.choice(list(available - used))
        tops = [x for x in available - used if x > bottom]
        if not tops:
            attempts += 1
            continue
        top = random.choice(tops)
        if bottom in forbidden or top in forbidden:
            attempts += 1
            continue
        ladders[bottom] = top
        used.add(bottom); used.add(top)

    if len(ladders) < count:
        raise BoardGenError("Failed to place all ladders.")

    # place snakes
    attempts = 0
    while len(snakes) < count and attempts < count * 200:
        head = random.choice(list(available - used))
        tails = [x for x in available - used if x < head]
        if not tails:
            attempts += 1
            continue
        tail = random.choice(tails)
        if head in forbidden or tail in forbidden:
            attempts += 1
            continue
        snakes[head] = tail
        used.add(head); used.add(tail)

    if len(snakes) < count:
        raise BoardGenError("Failed to place all snakes.")

    return ladders, snakes

def generate_board(N: int):
    """
    Returns: (cell_rc_map, num_to_rc, ladders, snakes)
    - cell_rc_map: (row,col) -> cell number
    - num_to_rc: cell number -> (row,col)
    - ladders, snakes maps as described
    """
    validate_board_size(N)
    cell_rc_map = make_snaking_number_map(N)
    num_to_rc = invert_map_cell_to_rc(N)
    count = N - 2
    ladders, snakes = random_pairs_for_ladders_and_snakes(N, count)
    return cell_rc_map, num_to_rc, ladders, snakes
