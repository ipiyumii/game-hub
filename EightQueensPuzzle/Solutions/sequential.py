def solve_eight_queens_sequential(N=8):
    solutions = []

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
            # found a solution
            solutions = [current_solution]  # store as list
            return [current_solution]  # return solution 

        all_solutions = []
        # try each column
        col_list = [0,1,2,3,4,5,6,7]
        for col in col_list:
            if is_safe(current_solution, row, col):
                # Use list concatenation instead of append
                new_solution = current_solution + [col]
                # recurse for next row
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


def findMaxSolutionsSequantial():

    all_solutions = solve_eight_queens_sequential()
    print("Total number of solutions:", len(all_solutions))

    i = 0
    while i < 92 and i < len(all_solutions):
        print("Solution", i+1, ":", all_solutions[i])
        i = i + 1

