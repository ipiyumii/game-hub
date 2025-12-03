from EightQueensPuzzle.Solutions.sequential import solve_eight_queens_sequential

def test_solution_count():
    all_solutions = solve_eight_queens_sequential()
    assert len(all_solutions) == 92 

def test_solutions_are_valid():
    all_solutions = solve_eight_queens_sequential()

    n = 8
    for solution in all_solutions:
        assert len(solution) == n
        for r1 in range(n):
            for r2 in range(r1 + 1, n):
                # check same col
                assert solution[r1] != solution[r2]
                # check diagonal
                assert abs(r1 - r2) != abs(solution[r1] - solution[r2])

