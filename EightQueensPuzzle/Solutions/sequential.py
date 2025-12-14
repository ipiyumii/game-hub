import time
from EightQueensPuzzle.eightqueen_dbUtil import save_program_solutions

def solve_eight_queens_sequential(N=8):

    def is_safe(current_solution, row, col):
        r = 0
        while r < row:
            c = current_solution[r]
            if c == col:
                return False
          
            delta_row = row - r
            delta_col1 = col - c
            delta_col2 = c - col
            if delta_row == delta_col1 or delta_row == delta_col2:
                return False
            r = r + 1
        return True

    # recursive function
    def checkQueenPosition(current_solution, row):
        if row == N:
            return [current_solution]

        all_solutions = []

        for col in range(N):
            if is_safe(current_solution, row, col):
                new_solution = current_solution + [col]
                result = checkQueenPosition(new_solution, row + 1)
                # add results to allsolution
                temp_index = 0
                while temp_index < len(result):
                    all_solutions = all_solutions + [result[temp_index]]
                    temp_index = temp_index + 1

        return all_solutions

    ##starting point
    solutions = checkQueenPosition([], 0)
    return solutions

def find_max_solutions_sequantial(player_name=None):
    start_time = time.time()
    all_solutions = solve_eight_queens_sequential()
    end_time = time.time()
    time_taken = end_time - start_time

    try:
        save_program_solutions(all_solutions, N=8, program_type = "sequential", time_took = time_taken, player_name = player_name)
    except Exception as e:
        print(f"Error saving solutions to database: {e}")

    print("Total number of solutions:", len(all_solutions))

    i = 0
    while i < 92 and i < len(all_solutions):
        print("Solution", i+1, ":", all_solutions[i])
        i = i + 1