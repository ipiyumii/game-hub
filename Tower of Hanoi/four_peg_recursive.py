"""
4-Peg Tower of Hanoi Solver (Recursive - Frame-Stewart Algorithm)
Fixed version with proper state tracking.
"""

import math
import time

class FourPegRecursiveSolver:
    """
    Recursive solver for Tower of Hanoi with 4 pegs.
    Uses the Frame-Stewart algorithm which divides disks into groups.
    """
    
    def __init__(self, num_disks=3, pegs=['A', 'B', 'C', 'D']):
        """
        Initialize the 4-peg solver.
        
        Args:
            num_disks (int): Number of disks to solve
            pegs (list): List of 4 peg labels
        """
        if len(pegs) != 4:
            raise ValueError("Must provide exactly 4 pegs")
            
        self.num_disks = num_disks
        self.pegs = pegs
        self.moves = []
        self.move_count = 0
        self.memo = {}  # Memoization for optimization
        
    def solve(self):
        """
        Solve the 4-peg Tower of Hanoi problem using Frame-Stewart algorithm.
        
        Returns:
            list: List of moves as tuples (from_peg, to_peg)
        """
        self.moves = []
        self.move_count = 0
        self.memo = {}
        
        # Solve using Frame-Stewart algorithm
        self._frame_stewart(self.num_disks, 0, 3, 1, 2)
        return self.moves
    
    def _frame_stewart(self, n, source, target, aux1, aux2):
        """
        Frame-Stewart recursive algorithm for 4 pegs.
        
        Args:
            n (int): Number of disks to move
            source (int): Source peg index
            target (int): Target peg index
            aux1 (int): First auxiliary peg index
            aux2 (int): Second auxiliary peg index
        """
        if n == 0:
            return
        
        # Check memoization
        key = (n, source, target, aux1, aux2)
        if key in self.memo:
            self.moves.extend(self.memo[key])
            self.move_count += len(self.memo[key])
            return
        
        # Save starting position for memoization
        start_len = len(self.moves)
        
        if n == 1:
            # Base case: move single disk
            self._add_move(source, target)
            self.memo[key] = [(self.pegs[source], self.pegs[target])]
            return
        
        # Calculate optimal split
        k = self._optimal_split(n)
        
        # Step 1: Move k disks from source to aux1 using all 4 pegs
        self._frame_stewart(k, source, aux1, aux2, target)
        
        # Step 2: Move remaining n-k disks from source to target using 3 pegs
        # (aux1 is now occupied by k disks, so we can't use it)
        self._three_peg_solution(n - k, source, target, aux2)
        
        # Step 3: Move k disks from aux1 to target using all 4 pegs
        self._frame_stewart(k, aux1, target, source, aux2)
        
        # Memoize the result
        self.memo[key] = self.moves[start_len:].copy()
    
    def _optimal_split(self, n):
        """
        Calculate optimal k for splitting disks.
        Uses Frame-Stewart formula.
        
        Args:
            n (int): Total number of disks
            
        Returns:
            int: Optimal k (number of disks in first group)
        """
        if n == 1:
            return 0
        
        # Known optimal splits for small n
        optimal_splits = {
            2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3, 
            9: 4, 10: 4, 11: 5, 12: 5, 13: 6, 14: 6, 15: 7
        }
        
        if n in optimal_splits:
            return optimal_splits[n]
        
        # Approximation for larger n
        return n - int(math.sqrt(2 * n + 1)) + 1
    
    def _three_peg_solution(self, n, source, target, auxiliary):
        """
        Classic 3-peg Tower of Hanoi solution.
        
        Args:
            n (int): Number of disks
            source (int): Source peg index
            target (int): Target peg index
            auxiliary (int): Auxiliary peg index
        """
        if n == 0:
            return
        
        if n == 1:
            self._add_move(source, target)
            return
        
        # Move n-1 disks from source to auxiliary
        self._three_peg_solution(n - 1, source, auxiliary, target)
        
        # Move nth disk from source to target
        self._add_move(source, target)
        
        # Move n-1 disks from auxiliary to target
        self._three_peg_solution(n - 1, auxiliary, target, source)
    
    def _add_move(self, from_idx, to_idx):
        """
        Add a move to the sequence.
        
        Args:
            from_idx (int): Source peg index
            to_idx (int): Target peg index
        """
        move = (self.pegs[from_idx], self.pegs[to_idx])
        self.moves.append(move)
        self.move_count += 1
    
    def get_move_sequence(self):
        """
        Get the move sequence as a list of strings.
        
        Returns:
            list: List of moves as strings (e.g., ["AB", "AC", "BC"])
        """
        return [f"{move[0]}{move[1]}" for move in self.moves]
    
    def get_total_moves(self):
        """
        Get the total number of moves.
        
        Returns:
            int: Total number of moves
        """
        return self.move_count
    
    def verify_solution(self):
        """
        Verify that the solution is correct by simulating it.
        
        Returns:
            bool: True if solution is correct
        """
        # Initialize towers
        towers = {
            self.pegs[0]: list(range(self.num_disks, 0, -1)),
            self.pegs[1]: [],
            self.pegs[2]: [],
            self.pegs[3]: []
        }
        
        # Simulate each move
        for i, (from_peg, to_peg) in enumerate(self.moves, 1):
            if not towers[from_peg]:
                print(f"Move {i}: ERROR - Empty source peg {from_peg}")
                return False
            
            disk = towers[from_peg].pop()
            
            if towers[to_peg] and disk > towers[to_peg][-1]:
                print(f"Move {i}: ERROR - Illegal move disk {disk} onto {towers[to_peg][-1]}")
                return False
            
            towers[to_peg].append(disk)
        
        # Check final state
        final_correct = (
            towers[self.pegs[3]] == list(range(self.num_disks, 0, -1)) and
            towers[self.pegs[0]] == [] and
            towers[self.pegs[1]] == [] and
            towers[self.pegs[2]] == []
        )
        
        return final_correct
    
    def print_solution(self, max_display=20):
        """
        Print the solution.
        
        Args:
            max_display (int): Maximum moves to display
        """
        print(f"\n4-Peg Recursive Solution for {self.num_disks} disks:")
        print(f"Pegs: {', '.join(self.pegs)}")
        print(f"Total moves: {self.move_count}")
        
        if self.num_disks <= 6:
            print("\nMove sequence:")
            for i, move in enumerate(self.moves, 1):
                print(f"{i:3d}. {move[0]} -> {move[1]}")
        else:
            print(f"\nFirst {max_display} moves:")
            for i, move in enumerate(self.moves[:max_display], 1):
                print(f"{i:3d}. {move[0]} -> {move[1]}")
            if len(self.moves) > max_display:
                print(f"... and {len(self.moves) - max_display} more moves")


def solve_4peg_recursive(num_disks=3, pegs=['A', 'B', 'C', 'D']):
    """
    Convenience function to solve 4-peg Tower of Hanoi recursively.
    
    Args:
        num_disks (int): Number of disks
        pegs (list): List of 4 peg labels
        
    Returns:
        list: List of moves as strings
    """
    solver = FourPegRecursiveSolver(num_disks, pegs)
    solver.solve()
    return solver.get_move_sequence()


if __name__ == "__main__":
    # Example usage
    print("=== 4-Peg Tower of Hanoi Solver (Recursive) ===")
    
    # Test with 4 disks
    solver = FourPegRecursiveSolver(4, ['A', 'B', 'C', 'D'])
    solver.solve()
    solver.print_solution()
    
    print("\nVerification:", "PASS" if solver.verify_solution() else "FAIL")