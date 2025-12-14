import math
import time
import pytest

from bfs_algorithm import BFSAlgorithm
from dijkstra_algorithm import DijkstraAlgorithm

class BoardStub:
    
    def __init__(self, total_cells, snakes=None, ladders=None):
        self.total_cells = total_cells
        self.snakes = snakes or {}
        self.ladders = ladders or {}

def baseline_min_moves(total_cells):
    
    if total_cells <= 1:
        return 0
    return math.ceil((total_cells - 1) / 6)

# TEST 1: both algorithms must match baseline

@pytest.mark.parametrize("total_cells", [2, 7, 10, 25, 100])
def test_algorithms_empty_board_min_moves(total_cells):
    board = BoardStub(total_cells)
    bfs = BFSAlgorithm(board)
    dijkstra = DijkstraAlgorithm(board)

    bfs_moves, bfs_time = bfs.find_minimum_moves()
    dij_moves, dij_time = dijkstra.find_minimum_moves()

    expected = baseline_min_moves(total_cells)

    assert bfs_moves == expected
    assert dij_moves == expected
    assert bfs_moves == dij_moves
    assert bfs_time >= 0.0
    assert dij_time >= 0.0


# TEST 2: LADDERS should reduce required moves

@pytest.fixture
def board_with_ladder():
    total_cells = 30
    ladders = {2: 28}  # major ladder
    return BoardStub(total_cells, ladders=ladders)

def test_ladder_reduces_moves(board_with_ladder):
    board = board_with_ladder
    bfs = BFSAlgorithm(board)
    dij = DijkstraAlgorithm(board)

    bfs_moves, _ = bfs.find_minimum_moves()
    dij_moves, _ = dij.find_minimum_moves()

    baseline = baseline_min_moves(board.total_cells)

    assert bfs_moves <= baseline
    assert dij_moves <= baseline
    assert bfs_moves == dij_moves


# TEST 3: SNAKES should increase or match baseline moves

@pytest.fixture
def board_with_snake():
    total_cells = 30
    snakes = {29: 5}  # snake near the end
    return BoardStub(total_cells, snakes=snakes)

def test_snake_increases_or_equals_moves(board_with_snake):
    board = board_with_snake
    bfs = BFSAlgorithm(board)
    dij = DijkstraAlgorithm(board)

    bfs_moves, _ = bfs.find_minimum_moves()
    dij_moves, _ = dij.find_minimum_moves()

    baseline = baseline_min_moves(board.total_cells)

    assert bfs_moves >= baseline
    assert dij_moves >= baseline
    assert bfs_moves == dij_moves


# TEST 4: Algorithm info returns expected keys

def test_get_algorithm_info_contains_expected_keys():
    board = BoardStub(10)
    bfs = BFSAlgorithm(board)
    dij = DijkstraAlgorithm(board)

    info_bfs = bfs.get_algorithm_info()
    info_dij = dij.get_algorithm_info()

    for info in (info_bfs, info_dij):
        assert isinstance(info, dict)
        for key in ('name', 'description', 'complexity', 'guarantees'):
            assert key in info

# TEST 5: Performance sanity check

def test_performance_small_board_runs_quickly():
    board = BoardStub(50)
    bfs = BFSAlgorithm(board)
    dij = DijkstraAlgorithm(board)

    start = time.time()
    bfs_moves, bfs_time = bfs.find_minimum_moves()
    elapsed_bfs = time.time() - start

    start = time.time()
    dij_moves, dij_time = dij.find_minimum_moves()
    elapsed_dij = time.time() - start

    assert bfs_time >= 0.0
    assert dij_time >= 0.0
    assert elapsed_bfs < 5.0
    assert elapsed_dij < 5.0
    assert bfs_moves == dij_moves
