import threading
import time

from EightQueensPuzzle.eightqueen_dbUtil import save_threaded_solutions_eight_queens

def solve_eight_queens_threaded(N=8):

    final_solutions = []
    lock = threading.Lock()

    def is_safe(current_solution, row, col):
        r = 0
        while r < row:
            c = current_solution[r]

            if c == col:
                return False

            dr = row - r
            dc1 = col - c         # diagonal  col - c
            dc2 = c - col         # diagonal  c - col

            if dr == dc1 or dr == dc2:
                return False

            r = r + 1

        return True

    def backtrack(current_solution, row):
        if row == N:
            return [current_solution]   # one full solution

        all_solutions = []
        col = 0
        while col < N:
            if is_safe(current_solution, row, col):
                new_solution = current_solution + [col]   # concat
                result = backtrack(new_solution, row + 1)

                i = 0
                while i < len(result):
                    all_solutions = all_solutions + [result[i]]
                    i = i + 1

            col = col + 1

        return all_solutions

    def worker(start_col):
        partial_solution = [start_col]
        sols = backtrack(partial_solution, 1)

        lock.acquire()
        try:
            i = 0
            while i < len(sols):
                final_solutions.append(sols[i])
                i = i + 1
        finally:
            lock.release()

    threads = []
    col = 0
    while col < N:
        t = threading.Thread(target=worker, args=(col,))
        threads.append(t)
        t.start()
        col = col + 1

    # Wait for threads to finish
    i = 0
    while i < len(threads):
        threads[i].join()
        i = i + 1

    return final_solutions

def findMaxSolutionsThreaded():
    start_time = time.time()
    all_solutions = solve_eight_queens_threaded()
    end_time = time.time() 
    timeTaken = end_time - start_time

    save_threaded_solutions_eight_queens(all_solutions, N=8, timeTaken=timeTaken)

    i = 0
    while i < 5 and i < len(all_solutions):
        print("Solution", i + 1, ":", all_solutions[i])
        i = i + 1 
