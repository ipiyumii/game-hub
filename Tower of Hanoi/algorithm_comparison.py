import time
from iterative_solver import IterativeSolver, solve_iteratively
from recursive_solver import RecursiveSolver, solve_recursively

class AlgorithmComparator:
    def __init__(self, max_disks=8):
        self.max_disks = max_disks
        
    def compare_solutions(self, num_disks):
        results = {
            'num_disks': num_disks,
            'expected_moves': (1 << num_disks) - 1  # 2^n - 1
        }
        
        # Test iterative solver
        start_time = time.perf_counter()
        iterative_solver = IterativeSolver(num_disks, 'A', 'C', 'B')
        iterative_moves = iterative_solver.solve()
        iterative_time = time.perf_counter() - start_time
        
        results['iterative'] = {
            'moves': len(iterative_moves),
            'time_ms': iterative_time * 1000,
            'sequence': iterative_solver.get_move_sequence()[:10] + ['...'] if len(iterative_moves) > 10 else iterative_solver.get_move_sequence()
        }
        
        # Test recursive solver
        start_time = time.perf_counter()
        recursive_solver = RecursiveSolver(num_disks, 'A', 'C', 'B')
        recursive_moves = recursive_solver.solve()
        recursive_time = time.perf_counter() - start_time
        
        results['recursive'] = {
            'moves': len(recursive_moves),
            'time_ms': recursive_time * 1000,
            'sequence': recursive_solver.get_move_sequence()[:10] + ['...'] if len(recursive_moves) > 10 else recursive_solver.get_move_sequence()
        }
        
        # Verify solutions are identical
        iterative_seq = iterative_solver.get_move_sequence()
        recursive_seq = recursive_solver.get_move_sequence()
        
        results['solutions_match'] = iterative_seq == recursive_seq
        results['time_difference'] = abs(iterative_time - recursive_time) * 1000
        
        return results
    
    def run_comparison(self):
        print("="*80)
        print("TOWER OF HANOI ALGORITHM COMPARISON")
        print("="*80)
        print(f"{'Disks':<8} {'Expected':<10} {'Iterative':<15} {'Recursive':<15} {'Match':<8} {'Time Diff (ms)':<15}")
        print("-"*80)
        
        all_results = []
        
        for num_disks in range(1, self.max_disks + 1):
            results = self.compare_solutions(num_disks)
            all_results.append(results)
            
            print(f"{num_disks:<8} {results['expected_moves']:<10} "
                  f"{results['iterative']['moves']:<5} ({results['iterative']['time_ms']:6.3f} ms)  "
                  f"{results['recursive']['moves']:<5} ({results['recursive']['time_ms']:6.3f} ms)  "
                  f"{str(results['solutions_match']):<8} {results['time_difference']:12.3f}")
        
        print("="*80)
        return all_results
    
    def print_detailed_analysis(self, num_disks=3):
        print(f"\n{'='*80}")
        print(f"DETAILED ANALYSIS FOR {num_disks} DISKS")
        print(f"{'='*80}")
        
        results = self.compare_solutions(num_disks)
        
        print(f"\nNumber of disks: {num_disks}")
        print(f"Expected minimum moves: 2^{num_disks} - 1 = {results['expected_moves']}")
        
        print(f"\nIterative Solution:")
        print(f"  Moves: {results['iterative']['moves']}")
        print(f"  Time: {results['iterative']['time_ms']:.3f} ms")
        print(f"  First 10 moves: {', '.join(results['iterative']['sequence'])}")
        
        print(f"\nRecursive Solution:")
        print(f"  Moves: {results['recursive']['moves']}")
        print(f"  Time: {results['recursive']['time_ms']:.3f} ms")
        print(f"  First 10 moves: {', '.join(results['recursive']['sequence'])}")
        
        print(f"\nComparison:")
        print(f"  Solutions match: {results['solutions_match']}")
        print(f"  Time difference: {results['time_difference']:.3f} ms")
        
        # Space complexity analysis
        print(f"\nSpace Complexity Analysis:")
        print(f"  Iterative: O(n) - stores disk positions in arrays")
        print(f"  Recursive: O(n) - recursion depth (call stack)")
        
        # Algorithm characteristics
        print(f"\nAlgorithm Characteristics:")
        print(f"  Iterative:")
        print(f"    - Uses explicit stack/arrays")
        print(f"    - No recursion overhead")
        print(f"    - Based on disk parity and mathematical patterns")
        print(f"    - More complex to understand but efficient")
        
        print(f"\n  Recursive:")
        print(f"    - Elegant mathematical solution")
        print(f"    - Easy to understand (divide and conquer)")
        print(f"    - Recursion overhead for large n")
        print(f"    - Follows principle of mathematical induction")
        
        if results['solutions_match']:
            print(f"\n✓ Both algorithms produce the same optimal solution!")
        else:
            print(f"\n⚠ Warning: Algorithms produce different solutions!")


def demonstrate_algorithms():
    """
    Demonstrate both algorithms with examples.
    """
    print("\n" + "="*80)
    print("DEMONSTRATION OF BOTH ALGORITHMS")
    print("="*80)
    
    # Example 1: 3 disks
    print("\nExample 1: 3 Disks")
    print("-"*40)
    
    print("\nRecursive Solution:")
    recursive_solver = RecursiveSolver(3, 'A', 'C', 'B')
    recursive_solver.solve()
    recursive_solver.print_solution()
    
    print("\nIterative Solution:")
    iterative_solver = IterativeSolver(3, 'A', 'C', 'B')
    iterative_solver.solve()
    iterative_solver.print_solution()
    
    # Example 2: 4 disks
    print("\n" + "="*80)
    print("\nExample 2: 4 Disks")
    print("-"*40)
    
    print("\nRecursive Solution (first 15 moves):")
    recursive_solver2 = RecursiveSolver(4, 'A', 'C', 'B')
    moves2 = recursive_solver2.solve()
    for i, move in enumerate(moves2[:15], 1):
        print(f"{i:3d}. {move[0]} → {move[1]}")
    print(f"... and {len(moves2)-15} more moves")
    print(f"Total: {len(moves2)} moves")
    
    print("\nNotice the pattern in recursive solution:")
    print("The solution for n disks builds upon solution for n-1 disks")
    print("This demonstrates the principle of mathematical induction!")


def integration_with_game():
    """
    Show how these algorithms could integrate with your Tower of Hanoi game.
    """
    print("\n" + "="*80)
    print("INTEGRATION WITH TOWER OF HANOI GAME")
    print("="*80)
    
    print("\nThese algorithms can be integrated into your game in several ways:")
    print("\n1. HINT SYSTEM:")
    print("   - Use the algorithms to provide next optimal move hints")
    print("   - Show players the optimal solution path")
    
    print("\n2. AUTO-SOLVE FEATURE:")
    print("   - Add buttons to demonstrate solution step-by-step")
    print("   - Visualize the algorithm in action")
    
    print("\n3. EDUCATIONAL MODE:")
    print("   - Show recursive call tree")
    print("   - Explain the mathematical formula 2^n - 1")
    print("   - Compare iterative vs recursive approaches")
    
    print("\n4. SOLUTION VALIDATION:")
    print("   - Check if player's solution is optimal")
    print("   - Validate sequence mode input against optimal solution")


if __name__ == "__main__":
    # Run comparison
    comparator = AlgorithmComparator(max_disks=6)
    comparator.run_comparison()
    
    # Show detailed analysis for 3 disks
    comparator.print_detailed_analysis(3)
    
    # Demonstrate algorithms
    demonstrate_algorithms()
    
    # Show integration ideas
    integration_with_game()