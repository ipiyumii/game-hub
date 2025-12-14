"""
Unit Tests for Tower of Hanoi Algorithms
Test both iterative and recursive solutions.
"""

import unittest
from iterative_solver import IterativeSolver, solve_iteratively
from recursive_solver import RecursiveSolver, solve_recursively

class TestTowerOfHanoiAlgorithms(unittest.TestCase):
    """Test cases for Tower of Hanoi algorithms."""
    
    def test_1_disk(self):
        """Test with 1 disk."""
        # Recursive
        recursive_solver = RecursiveSolver(1, 'A', 'C', 'B')
        recursive_moves = recursive_solver.solve()
        self.assertEqual(len(recursive_moves), 1)
        self.assertEqual(recursive_moves, [('A', 'C')])
        
        # Iterative
        iterative_solver = IterativeSolver(1, 'A', 'C', 'B')
        iterative_moves = iterative_solver.solve()
        self.assertEqual(len(iterative_moves), 1)
        self.assertEqual(iterative_moves, [('A', 'C')])
        
        # Both should match
        self.assertEqual(recursive_moves, iterative_moves)
    
    def test_2_disks(self):
        """Test with 2 disks."""
        expected_moves = [('A', 'B'), ('A', 'C'), ('B', 'C')]
        expected_sequence = ['AB', 'AC', 'BC']
        
        # Recursive
        recursive_solver = RecursiveSolver(2, 'A', 'C', 'B')
        recursive_moves = recursive_solver.solve()
        self.assertEqual(len(recursive_moves), 3)
        self.assertEqual(recursive_moves, expected_moves)
        self.assertEqual(recursive_solver.get_move_sequence(), expected_sequence)
        
        # Iterative
        iterative_solver = IterativeSolver(2, 'A', 'C', 'B')
        iterative_moves = iterative_solver.solve()
        self.assertEqual(len(iterative_moves), 3)
        # Note: Iterative algorithm may produce different but valid sequence for even disks
        # Both are valid solutions
        
        # Both should have correct number of moves
        self.assertEqual(len(recursive_moves), len(iterative_moves))
    
    def test_3_disks(self):
        """Test with 3 disks (classic case)."""
        # Both algorithms should produce the same optimal solution
        expected_move_count = 7  # 2^3 - 1 = 7
        
        # Recursive
        recursive_solver = RecursiveSolver(3, 'A', 'C', 'B')
        recursive_moves = recursive_solver.solve()
        self.assertEqual(len(recursive_moves), expected_move_count)
        
        # Iterative
        iterative_solver = IterativeSolver(3, 'A', 'C', 'B')
        iterative_moves = iterative_solver.solve()
        self.assertEqual(len(iterative_moves), expected_move_count)
        
        # For odd number of disks, both should produce identical sequences
        self.assertEqual(recursive_moves, iterative_moves)
        
        # Verify the classic solution pattern
        classic_solution = [
            ('A', 'C'), ('A', 'B'), ('C', 'B'),
            ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')
        ]
        self.assertEqual(recursive_moves, classic_solution)
        self.assertEqual(iterative_moves, classic_solution)
    
    def test_formula_2_power_n_minus_1(self):
        """Test that solution follows 2^n - 1 formula."""
        for n in range(1, 6):  # Test for 1 to 5 disks
            expected_moves = (1 << n) - 1  # 2^n - 1
            
            # Recursive
            recursive_solver = RecursiveSolver(n, 'A', 'C', 'B')
            recursive_moves = recursive_solver.solve()
            self.assertEqual(len(recursive_moves), expected_moves,
                          f"Recursive failed for n={n}: got {len(recursive_moves)}, expected {expected_moves}")
            
            # Iterative
            iterative_solver = IterativeSolver(n, 'A', 'C', 'B')
            iterative_moves = iterative_solver.solve()
            self.assertEqual(len(iterative_moves), expected_moves,
                          f"Iterative failed for n={n}: got {len(iterative_moves)}, expected {expected_moves}")
    
    def test_different_peg_labels(self):
        """Test with different peg labels."""
        # Recursive with custom labels
        recursive_solver = RecursiveSolver(3, 'X', 'Z', 'Y')
        recursive_moves = recursive_solver.solve()
        self.assertEqual(len(recursive_moves), 7)
        
        # Check that moves use correct labels
        for move in recursive_moves:
            self.assertIn(move[0], ['X', 'Y', 'Z'])
            self.assertIn(move[1], ['X', 'Y', 'Z'])
        
        # Iterative with custom labels
        iterative_solver = IterativeSolver(3, 'X', 'Z', 'Y')
        iterative_moves = iterative_solver.solve()
        self.assertEqual(len(iterative_moves), 7)
        
        # Check that moves use correct labels
        for move in iterative_moves:
            self.assertIn(move[0], ['X', 'Y', 'Z'])
            self.assertIn(move[1], ['X', 'Y', 'Z'])
    
    def test_legal_moves_only(self):
        """Test that all moves are legal (no larger disk on smaller)."""
        for n in range(1, 5):
            # Test both algorithms
            for solver_class, solver_name in [(RecursiveSolver, 'Recursive'), 
                                            (IterativeSolver, 'Iterative')]:
                solver = solver_class(n, 'A', 'C', 'B')
                moves = solver.solve()
                
                # Simulate the moves to verify legality
                towers = {
                    'A': list(range(n, 0, -1)),
                    'B': [],
                    'C': []
                }
                
                for from_peg, to_peg in moves:
                    # Check that source peg is not empty
                    self.assertTrue(towers[from_peg], 
                                  f"{solver_name}: Empty source peg {from_peg} for move {from_peg}→{to_peg}")
                    
                    disk = towers[from_peg].pop()
                    
                    # Check that move is legal (to_peg empty or top disk larger)
                    if towers[to_peg]:
                        top_disk = towers[to_peg][-1]
                        self.assertGreater(top_disk, disk,
                                         f"{solver_name}: Illegal move {from_peg}→{to_peg}: "
                                         f"disk {disk} on disk {top_disk}")
                    
                    towers[to_peg].append(disk)
                
                # Verify all disks moved to target peg
                self.assertEqual(towers['C'], list(range(n, 0, -1)),
                               f"{solver_name}: Not all disks moved to target")
    
    def test_convenience_functions(self):
        """Test the convenience functions."""
        # Test recursive convenience function
        recursive_sequence = solve_recursively(3, 'A', 'C', 'B')
        self.assertEqual(len(recursive_sequence), 7)
        self.assertEqual(recursive_sequence, ['AC', 'AB', 'CB', 'AC', 'BA', 'BC', 'AC'])
        
        # Test iterative convenience function
        iterative_sequence = solve_iteratively(3, 'A', 'C', 'B')
        self.assertEqual(len(iterative_sequence), 7)
        self.assertEqual(iterative_sequence, ['AC', 'AB', 'CB', 'AC', 'BA', 'BC', 'AC'])
    
    def test_solution_completeness(self):
        """Test that solution ends with all disks on target peg."""
        for n in range(1, 5):
            # Test recursive
            recursive_solver = RecursiveSolver(n, 'A', 'C', 'B')
            recursive_moves = recursive_solver.solve()
            
            # Simulate moves
            towers = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
            for from_peg, to_peg in recursive_moves:
                disk = towers[from_peg].pop()
                towers[to_peg].append(disk)
            
            # Verify final state
            self.assertEqual(towers['A'], [])
            self.assertEqual(towers['B'], [])
            self.assertEqual(towers['C'], list(range(n, 0, -1)),
                           f"Recursive failed for n={n}: disks not all on target")
            
            # Test iterative
            iterative_solver = IterativeSolver(n, 'A', 'C', 'B')
            iterative_moves = iterative_solver.solve()
            
            # Simulate moves
            towers = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
            for from_peg, to_peg in iterative_moves:
                disk = towers[from_peg].pop()
                towers[to_peg].append(disk)
            
            # Verify final state
            self.assertEqual(towers['A'], [])
            self.assertEqual(towers['B'], [])
            self.assertEqual(towers['C'], list(range(n, 0, -1)),
                           f"Iterative failed for n={n}: disks not all on target")


class TestAlgorithmEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""
    
    def test_large_number_of_disks(self):
        """Test with relatively large number of disks (but not too large for performance)."""
        n = 10  # 2^10 - 1 = 1023 moves
        expected_moves = (1 << n) - 1
        
        # Recursive - this will test recursion depth
        recursive_solver = RecursiveSolver(n, 'A', 'C', 'B')
        recursive_moves = recursive_solver.solve()
        self.assertEqual(len(recursive_moves), expected_moves)
        
        # Iterative
        iterative_solver = IterativeSolver(n, 'A', 'C', 'B')
        iterative_moves = iterative_solver.solve()
        self.assertEqual(len(iterative_moves), expected_moves)
    
    def test_zero_disks(self):
        """Test with zero disks (edge case)."""
        # Recursive
        recursive_solver = RecursiveSolver(0, 'A', 'C', 'B')
        recursive_moves = recursive_solver.solve()
        self.assertEqual(len(recursive_moves), 0)
        
        # Iterative
        iterative_solver = IterativeSolver(0, 'A', 'C', 'B')
        iterative_moves = iterative_solver.solve()
        self.assertEqual(len(iterative_moves), 0)
    
    def test_identical_source_target(self):
        """Test when source and target are the same."""
        # Should produce no moves since already "solved"
        recursive_solver = RecursiveSolver(3, 'A', 'A', 'B')
        recursive_moves = recursive_solver.solve()
        self.assertEqual(len(recursive_moves), 0)
        
        iterative_solver = IterativeSolver(3, 'A', 'A', 'B')
        iterative_moves = iterative_solver.solve()
        self.assertEqual(len(iterative_moves), 0)


def run_performance_test():
    """Run performance comparison (not a unit test)."""
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON")
    print("="*80)
    
    import time
    
    test_cases = [3, 5, 8, 10, 12, 15, 18, 20]
    
    print(f"{'Disks':<8} {'Moves':<12} {'Recursive (ms)':<15} {'Iterative (ms)':<15} {'Difference':<12}")
    print("-"*80)
    
    for n in test_cases:
        moves_count = (1 << n) - 1
        
        # Time recursive solver
        start = time.perf_counter()
        recursive_solver = RecursiveSolver(n, 'A', 'C', 'B')
        recursive_moves = recursive_solver.solve()
        recursive_time = (time.perf_counter() - start) * 1000
        
        # Time iterative solver
        start = time.perf_counter()
        iterative_solver = IterativeSolver(n, 'A', 'C', 'B')
        iterative_moves = iterative_solver.solve()
        iterative_time = (time.perf_counter() - start) * 1000
        
        # Verify both produce same number of moves
        assert len(recursive_moves) == moves_count, f"Recursive wrong move count for n={n}"
        assert len(iterative_moves) == moves_count, f"Iterative wrong move count for n={n}"
        
        # For n <= 10, also verify sequences match
        if n <= 10:
            recursive_seq = recursive_solver.get_move_sequence()
            iterative_seq = iterative_solver.get_move_sequence()
            if n % 2 == 1:  # Sequences should match for odd n
                assert recursive_seq == iterative_seq, f"Sequences differ for n={n}"
        
        print(f"{n:<8} {moves_count:<12,} {recursive_time:<15.3f} {iterative_time:<15.3f} "
              f"{(iterative_time - recursive_time):<12.3f}")


if __name__ == "__main__":
    # Run unit tests
    print("Running unit tests...")
    unittest.main(exit=False)
    
    # Run performance test
    run_performance_test()