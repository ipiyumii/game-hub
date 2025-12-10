"""
Iterative Tower of Hanoi Solver
This module provides an iterative solution to the Tower of Hanoi problem.
The solution uses mathematical patterns based on disk parity.
"""

class IterativeSolver:
    """
    Iterative solver for Tower of Hanoi with 3 pegs.
    Uses pattern-based approach that works for any number of disks.
    """
    
    def __init__(self, num_disks=3, source='A', target='C', auxiliary='B'):
        """
        Initialize the iterative solver.
        
        Args:
            num_disks (int): Number of disks to solve
            source (str): Source peg label
            target (str): Target peg label
            auxiliary (str): Auxiliary peg label
        """
        self.num_disks = num_disks
        self.source = source
        self.target = target
        self.auxiliary = auxiliary
        self.moves = []
        self.total_moves = 0
        
    def solve(self):
        """
        Solve the Tower of Hanoi problem iteratively.
        Always produces optimal solution with 2^n - 1 moves.
        
        Returns:
            list: List of moves as tuples (from_peg, to_peg)
        """
        self.moves = []
        
        # No disks, no moves needed
        if self.num_disks == 0:
            self.total_moves = 0
            return self.moves
        
        # Initialize towers (disks numbered from largest to smallest)
        towers = {
            self.source: list(range(self.num_disks, 0, -1)),
            self.auxiliary: [],
            self.target: []
        }
        
        # Total moves needed (2^n - 1)
        total_moves_needed = (1 << self.num_disks) - 1
        
        # Determine move pattern based on parity of number of disks
        if self.num_disks % 2 == 1:
            # Odd number of disks: pattern is source->target, source->auxiliary, target->auxiliary
            move_patterns = [
                (self.source, self.target),      # Move 1: source -> target
                (self.source, self.auxiliary),   # Move 2: source -> auxiliary
                (self.target, self.auxiliary)    # Move 3: target -> auxiliary
            ]
        else:
            # Even number of disks: pattern is source->auxiliary, source->target, auxiliary->target
            move_patterns = [
                (self.source, self.auxiliary),   # Move 1: source -> auxiliary
                (self.source, self.target),      # Move 2: source -> target
                (self.auxiliary, self.target)    # Move 3: auxiliary -> target
            ]
        
        move_count = 0
        
        # Keep making moves until all disks are on target peg
        while len(towers[self.target]) < self.num_disks:
            # Get the next move pattern (cycles through the 3 patterns)
            from_peg, to_peg = move_patterns[move_count % 3]
            
            # Check if forward move is legal
            if towers[from_peg] and (not towers[to_peg] or towers[from_peg][-1] < towers[to_peg][-1]):
                # Forward move is legal: from_peg -> to_peg
                disk = towers[from_peg].pop()
                towers[to_peg].append(disk)
                self.moves.append((from_peg, to_peg))
            else:
                # Forward move not legal, try reverse move
                if towers[to_peg] and (not towers[from_peg] or towers[to_peg][-1] < towers[from_peg][-1]):
                    # Reverse move is legal: to_peg -> from_peg
                    disk = towers[to_peg].pop()
                    towers[from_peg].append(disk)
                    self.moves.append((to_peg, from_peg))
                else:
                    # This should never happen with correct algorithm
                    print(f"Warning: No legal move found at step {move_count}")
                    # Skip this pattern and try next one
                    move_count += 1
                    continue
            
            move_count += 1
        
        self.total_moves = len(self.moves)
        return self.moves
    
    def get_move_sequence(self):
        """
        Get the move sequence as a list of strings.
        
        Returns:
            list: List of moves as strings (e.g., ["AB", "AC", "BC"])
        """
        return [f"{move[0]}{move[1]}" for move in self.moves]
    
    def get_total_moves(self):
        """
        Get the total number of moves required.
        
        Returns:
            int: Total number of moves (should be 2^n - 1)
        """
        return self.total_moves
    
    def print_solution(self):
        """Print the solution in a readable format."""
        print(f"\nIterative Solution for {self.num_disks} disks:")
        print(f"Source: {self.source}, Target: {self.target}, Auxiliary: {self.auxiliary}")
        print(f"Total moves required: {self.total_moves} (2^{self.num_disks} - 1 = {(1 << self.num_disks) - 1})")
        print("\nMove sequence:")
        for i, move in enumerate(self.moves, 1):
            print(f"{i:3d}. {move[0]} -> {move[1]}")
    
    def verify_solution(self):
        """
        Verify that the solution is correct by simulating it.
        
        Returns:
            bool: True if solution is correct, False otherwise
        """
        if self.num_disks == 0:
            return len(self.moves) == 0
        
        # Initialize towers
        towers = {
            self.source: list(range(self.num_disks, 0, -1)),
            self.auxiliary: [],
            self.target: []
        }
        
        # Simulate each move
        for i, (from_peg, to_peg) in enumerate(self.moves, 1):
            # Check if source peg has disks
            if not towers[from_peg]:
                print(f"Move {i}: ERROR - Trying to move from empty peg {from_peg}")
                return False
            
            disk = towers[from_peg].pop()
            
            # Check if move is legal (no larger disk on smaller)
            if towers[to_peg] and disk > towers[to_peg][-1]:
                print(f"Move {i}: ERROR - Illegal move disk {disk} onto disk {towers[to_peg][-1]} on peg {to_peg}")
                return False
            
            towers[to_peg].append(disk)
        
        # Check if all disks are on target peg
        final_state_correct = (
            towers[self.target] == list(range(self.num_disks, 0, -1)) and
            towers[self.source] == [] and
            towers[self.auxiliary] == []
        )
        
        if not final_state_correct:
            print("ERROR - Final state incorrect:")
            print(f"  Target peg {self.target}: {towers[self.target]} (expected: {list(range(self.num_disks, 0, -1))})")
            print(f"  Source peg {self.source}: {towers[self.source]} (expected: [])")
            print(f"  Auxiliary peg {self.auxiliary}: {towers[self.auxiliary]} (expected: [])")
        
        return final_state_correct


def solve_iteratively(num_disks=3, source='A', target='C', auxiliary='B'):
    """
    Convenience function to solve Tower of Hanoi iteratively.
    
    Args:
        num_disks (int): Number of disks
        source (str): Source peg
        target (str): Target peg
        auxiliary (str): Auxiliary peg
        
    Returns:
        list: List of moves as strings
    """
    solver = IterativeSolver(num_disks, source, target, auxiliary)
    solver.solve()
    return solver.get_move_sequence()


def run_demo():
    """Run a demonstration of the iterative solver."""
    print("="*70)
    print("ITERATIVE TOWER OF HANOI SOLVER DEMONSTRATION")
    print("="*70)
    
    # Test with different numbers of disks
    test_cases = [1, 2, 3, 4, 5]
    
    for n in test_cases:
        print(f"\n{'='*70}")
        print(f"SOLVING FOR {n} DISK{'S' if n != 1 else ''}")
        print(f"{'='*70}")
        
        solver = IterativeSolver(n, 'A', 'C', 'B')
        solver.solve()
        
        # Print solution (truncate if too long)
        if n <= 4:
            solver.print_solution()
        else:
            print(f"\nIterative Solution for {n} disks:")
            print(f"Source: A, Target: C, Auxiliary: B")
            print(f"Total moves required: {solver.get_total_moves()} (2^{n} - 1 = {(1 << n) - 1})")
            print(f"\n(Showing first 10 of {solver.get_total_moves()} moves):")
            for i, move in enumerate(solver.moves[:10], 1):
                print(f"{i:3d}. {move[0]} -> {move[1]}")
            if solver.get_total_moves() > 10:
                print(f"  ... and {solver.get_total_moves() - 10} more moves")
        
        # Verify solution
        if solver.verify_solution():
            print(f"\n[PASS] Solution verified as correct!")
        else:
            print(f"\n[FAIL] Solution verification failed!")
        
        # Check if optimal
        expected = (1 << n) - 1
        actual = solver.get_total_moves()
        if expected == actual:
            print(f"[OK] Solution is optimal (2^{n} - 1 = {expected} moves)")
        else:
            print(f"[WARNING] Solution has {actual} moves, but optimal is {expected}")
    
    print(f"\n{'='*70}")
    print("SUMMARY")
    print("="*70)
    
    # Summary table
    print(f"\n{'Disks':<8} {'Optimal (2^n-1)':<15} {'Algorithm':<12} {'Verified':<10}")
    print("-"*50)
    
    all_correct = True
    for n in range(1, 7):
        solver = IterativeSolver(n, 'A', 'C', 'B')
        solver.solve()
        optimal = (1 << n) - 1
        actual = solver.get_total_moves()
        verified = solver.verify_solution()
        
        status = "CORRECT" if (actual == optimal and verified) else "INCORRECT"
        verified_str = "YES" if verified else "NO"
        
        if status == "INCORRECT":
            all_correct = False
        
        print(f"{n:<8} {optimal:<15} {actual:<12} {verified_str:<10}")
    
    print("-"*50)
    if all_correct:
        print("[SUCCESS] All solutions are optimal and verified!")
    else:
        print("[ISSUE] Some solutions may not be optimal.")
    
    print(f"\n{'='*70}")
    print("ALGORITHM EXPLANATION")
    print("="*70)
    print("""
    The iterative algorithm works by following a simple pattern:
    
    1. For ODD number of disks (1, 3, 5, ...):
       Pattern repeats every 3 moves:
       1. source -> target
       2. source -> auxiliary  
       3. target -> auxiliary
    
    2. For EVEN number of disks (2, 4, 6, ...):
       Pattern repeats every 3 moves:
       1. source -> auxiliary
       2. source -> target
       3. auxiliary -> target
    
    At each step, if the pattern move is not legal (would place a larger
    disk on a smaller one), the reverse move is made instead.
    
    This always produces the optimal solution with 2^n - 1 moves.
    """)


if __name__ == "__main__":
    # Run the demonstration
    run_demo()
    
    # Example of using the solver programmatically
    print(f"\n{'='*70}")
    print("PROGRAMMATIC USAGE EXAMPLE")
    print("="*70)
    
    # Example 1: Get solution for 3 disks
    print("\nExample 1: Solving 3 disks programmatically")
    solver = IterativeSolver(3, 'A', 'C', 'B')
    moves = solver.solve()
    print(f"Moves: {solver.get_move_sequence()}")
    print(f"Total moves: {solver.get_total_moves()}")
    print(f"Verified: {solver.verify_solution()}")
    
    # Example 2: Get just the move sequence
    print("\nExample 2: Using convenience function")
    move_sequence = solve_iteratively(3, 'A', 'C', 'B')
    print(f"Move sequence: {move_sequence}")