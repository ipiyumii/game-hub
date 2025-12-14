from four_peg_iterative import FourPegSolver
from four_peg_recursive import FourPegRecursiveSolver
class AlgorithmComparator:
 
    def __init__(self, max_disks=8):
        self.max_disks = max_disks
        
        # Known optimal moves for 4 pegs (Frame numbers)
        self.optimal_moves = {
            1: 1,
            2: 3,
            3: 5,
            4: 9,
            5: 13,
            6: 17,
            7: 25,
            8: 33,
            9: 41,
            10: 49,
            11: 65,
            12: 81
        }
    
    def test_iterative(self, num_disks):
        solver = FourPegSolver(num_disks)
        solver.solve()
        moves = solver.moves
        verified, message = solver.verify_solution()
        
        return {
            'moves': moves,
            'move_count': len(moves),
            'verified': verified,
            'message': message
        }
    
    def test_recursive(self, num_disks):
        solver = FourPegRecursiveSolver(num_disks)
        solver.solve()
        moves = solver.moves
        
        # Fix: The recursive solver's verify_solution returns bool, not tuple
        verified = solver.verify_solution()
        
        return {
            'moves': moves,
            'move_count': len(moves),
            'verified': verified,
            'message': "Verified" if verified else "Failed verification"
        }
    
    def run_comparison(self):
        results = []
        
        print("="*70)
        print("4-PEG TOWER OF HANOI ALGORITHM COMPARISON")
        print("="*70)
        print(f"{'Disks':<8} {'Optimal':<10} {'Recursive':<15} {'Iterative':<15} {'Status':<15}")
        print("-" * 70)
        
        for num_disks in range(1, self.max_disks + 1):
            # Get optimal move count (or None if not known)
            optimal = self.optimal_moves.get(num_disks, "?")
            
            try:
                # Test recursive algorithm
                recursive_result = self.test_recursive(num_disks)
                recursive_count = recursive_result['move_count']
                recursive_status = "PASS" if recursive_result['verified'] else "FAIL"
                
                # Test iterative algorithm  
                iterative_result = self.test_iterative(num_disks)
                iterative_count = iterative_result['move_count']
                iterative_status = "PASS" if iterative_result['verified'] else "FAIL"
                
                # Determine overall status
                if not recursive_result['verified'] or not iterative_result['verified']:
                    status = "[FAIL]"
                elif optimal != "?" and (recursive_count > optimal or iterative_count > optimal):
                    status = "[SUBOPT]"
                elif recursive_count != iterative_count:
                    status = "[DIFF]"
                else:
                    status = "[OK]"
                    
            except Exception as e:
                recursive_count = "ERR"
                iterative_count = "ERR"
                recursive_status = "ERR"
                iterative_status = "ERR"
                status = f"[ERROR: {str(e)[:20]}]"
            
            # Print results row (without Unicode symbols)
            print(f"{num_disks:<8} {str(optimal):<10} "
                  f"{str(recursive_count):<8} ({recursive_status:<6}) "
                  f"{str(iterative_count):<8} ({iterative_status:<6}) "
                  f"{status}")
            
            results.append({
                'disks': num_disks,
                'optimal_moves': optimal,
                'recursive': recursive_result if 'recursive_result' in locals() else None,
                'iterative': iterative_result if 'iterative_result' in locals() else None,
                'status': status
            })
        
        print("-" * 70)
        return results
    
    def print_detailed_analysis(self, results):
        print("\n" + "="*70)
        print("DETAILED ANALYSIS")
        print("="*70)
        
        for result in results:
            if result['status'] == "[OK]":
                continue  # Skip perfect results
                
            print(f"\n{'='*40}")
            print(f"ANALYSIS FOR {result['disks']} DISKS")
            print(f"{'='*40}")
            
            if result['optimal_moves'] != "?":
                print(f"Optimal moves: {result['optimal_moves']}")
            
            if result['recursive']:
                print(f"Recursive: {result['recursive']['move_count']} moves - {result['recursive']['message']}")
            
            if result['iterative']:
                print(f"Iterative: {result['iterative']['move_count']} moves - {result['iterative']['message']}")
            
            if result['status'] == "[SUBOPT]":
                if result['optimal_moves'] != "?":
                    rec_diff = result['recursive']['move_count'] - result['optimal_moves']
                    it_diff = result['iterative']['move_count'] - result['optimal_moves']
                    print(f"Recursive is {rec_diff} moves above optimal")
                    print(f"Iterative is {it_diff} moves above optimal")
            
            elif result['status'] == "[DIFF]":
                diff = abs(result['recursive']['move_count'] - result['iterative']['move_count'])
                print(f"Algorithms differ by {diff} moves")
            
            elif "[ERROR" in result['status']:
                print(f"Error occurred during testing")
    
    def print_summary_statistics(self, results):
        print("\n" + "="*70)
        print("SUMMARY STATISTICS")
        print("="*70)
        
        total_tests = len(results)
        passed = sum(1 for r in results if r['status'] == "[OK]")
        failed = sum(1 for r in results if "[FAIL]" in r['status'])
        suboptimal = sum(1 for r in results if r['status'] == "[SUBOPT]")
        different = sum(1 for r in results if r['status'] == "[DIFF]")
        errors = sum(1 for r in results if "[ERROR" in r['status'])
        
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed} ({passed/total_tests*100:.1f}%)")
        print(f"Failed: {failed}")
        print(f"Suboptimal: {suboptimal}")
        print(f"Different results: {different}")
        print(f"Errors: {errors}")
        
        # Calculate average speedup vs 3-peg
        three_peg_moves = []
        four_peg_best = []
        
        for r in results:
            if r['optimal_moves'] != "?" and isinstance(r['optimal_moves'], int):
                three_peg = (1 << r['disks']) - 1  # 2^n - 1
                three_peg_moves.append(three_peg)
                four_peg_best.append(r['optimal_moves'])
        
        if three_peg_moves and four_peg_best:
            avg_speedup = sum(t/f for t, f in zip(three_peg_moves, four_peg_best)) / len(three_peg_moves)
            print(f"\nAverage speedup vs 3-peg: {avg_speedup:.2f}x")


def main():
    # Set maximum disks to test
    max_disks = 8
    
    # Create comparator and run tests
    comparator = AlgorithmComparator(max_disks)
    results = comparator.run_comparison()
    
    # Print detailed analysis
    comparator.print_detailed_analysis(results)
    
    # Print summary statistics
    comparator.print_summary_statistics(results)
    
    # Show example solutions
    print("\n" + "="*70)
    print("EXAMPLE SOLUTIONS")
    print("="*70)
    
    for n in [1, 2, 3, 4]:
        print(f"\n--- {n} Disks ---")
        
        # Iterative solution
        iterative = FourPegSolver(n)
        iterative.solve()
        print(f"Iterative ({len(iterative.moves)} moves):")
        moves_str = ' '.join(f"{f}{t}" for f, t in iterative.moves[:10])
        if len(iterative.moves) > 10:
            moves_str += f" ... (+{len(iterative.moves)-10} more)"
        print(f"  {moves_str}")
        
        # Recursive solution
        recursive = FourPegRecursiveSolver(n)
        recursive.solve()
        print(f"Recursive ({len(recursive.moves)} moves):")
        moves_str = ' '.join(f"{f}{t}" for f, t in recursive.moves[:10])
        if len(recursive.moves) > 10:
            moves_str += f" ... (+{len(recursive.moves)-10} more)"
        print(f"  {moves_str}")


if __name__ == "__main__":
    main()