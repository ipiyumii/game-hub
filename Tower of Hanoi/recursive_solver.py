class RecursiveSolver:
    # Recursive solver for Tower of Hanoi with 3 pegs.
    
    def __init__(self, num_disks=3, source='A', target='C', auxiliary='B'):
        self.num_disks = num_disks
        self.source = source
        self.target = target
        self.auxiliary = auxiliary
        self.moves = []
        self.total_moves = 0
        self.step_counter = 0
        
    def solve(self, num_disks=None, source=None, target=None, auxiliary=None):
        # Use provided parameters or default to initialized values
        if num_disks is None:
            num_disks = self.num_disks
        if source is None:
            source = self.source
        if target is None:
            target = self.target
        if auxiliary is None:
            auxiliary = self.auxiliary
        
        # Reset moves list if this is the initial call
        if num_disks == self.num_disks:
            self.moves = []
            self.step_counter = 0
        
        # Base case: if only one disk, move it directly
        if num_disks == 1:
            self.moves.append((source, target))
            self.step_counter += 1
        else:
            # Step 1: Move n-1 disks from source to auxiliary
            self.solve(num_disks - 1, source, auxiliary, target)
            
            # Step 2: Move the nth disk from source to target
            self.moves.append((source, target))
            self.step_counter += 1
            
            # Step 3: Move n-1 disks from auxiliary to target
            self.solve(num_disks - 1, auxiliary, target, source)
        
        # Only set total_moves on the final return
        if num_disks == self.num_disks:
            self.total_moves = len(self.moves)
        
        return self.moves
    
    def solve_with_trace(self, num_disks=None, source=None, target=None, auxiliary=None, depth=0):
        if num_disks is None:
            num_disks = self.num_disks
        if source is None:
            source = self.source
        if target is None:
            target = self.target
        if auxiliary is None:
            auxiliary = self.auxiliary
            
        indent = "  " * depth
        print(f"{indent}solve({num_disks}, {source}, {target}, {auxiliary})")
        
        if num_disks == 1:
            print(f"{indent}  Move disk 1 from {source} to {target}")
            self.moves.append((source, target))
        else:
            # Move n-1 disks from source to auxiliary
            print(f"{indent}  Step 1: Move {num_disks-1} disks from {source} to {auxiliary}")
            self.solve_with_trace(num_disks-1, source, auxiliary, target, depth+1)
            
            # Move nth disk from source to target
            print(f"{indent}  Step 2: Move disk {num_disks} from {source} to {target}")
            self.moves.append((source, target))
            
            # Move n-1 disks from auxiliary to target
            print(f"{indent}  Step 3: Move {num_disks-1} disks from {auxiliary} to {target}")
            self.solve_with_trace(num_disks-1, auxiliary, target, source, depth+1)
        
        return self.moves
    
    def get_move_sequence(self):
        return [f"{move[0]}{move[1]}" for move in self.moves]
    
    def get_total_moves(self):
        return self.total_moves
    
    def print_solution(self):
        """Print the solution in a readable format."""
        print(f"\nRecursive Solution for {self.num_disks} disks:")
        print(f"Source: {self.source}, Target: {self.target}, Auxiliary: {self.auxiliary}")
        print(f"Total moves required: {self.total_moves} (2^{self.num_disks} - 1 = {(1 << self.num_disks) - 1})")
        print("\nMove sequence:")
        for i, move in enumerate(self.moves, 1):
            # Use ASCII arrow -> instead of Unicode →
            print(f"{i:3d}. {move[0]} -> {move[1]}")
    
    def get_formula_explanation(self):
        return f"""
        Mathematical Formula:
        For n disks, the minimum number of moves required is: 2^n - 1
        
        Proof by mathematical induction:
        1. Base case (n=1): 2^1 - 1 = 1 move [OK]
        2. Inductive step:
           - To move n disks from source to target:
             1. Move n-1 disks from source to auxiliary (2^(n-1) - 1 moves)
             2. Move the nth disk from source to target (1 move)
             3. Move n-1 disks from auxiliary to target (2^(n-1) - 1 moves)
           - Total moves = 2*(2^(n-1) - 1) + 1 = 2^n - 1
        
        For {self.num_disks} disks: 2^{self.num_disks} - 1 = {(1 << self.num_disks) - 1} moves
        """


def solve_recursively(num_disks=3, source='A', target='C', auxiliary='B'):
    solver = RecursiveSolver(num_disks, source, target, auxiliary)
    solver.solve()
    return solver.get_move_sequence()


def visualize_towers(disks_on_A, disks_on_B, disks_on_C, move_description=""):
    max_disks = max(len(disks_on_A), len(disks_on_B), len(disks_on_C))
    
    print("\n" + "="*50)
    if move_description:
        print(f"After: {move_description}")
    print("Current state:")
    print("A    B    C")
    print("-" * 15)
    
    for i in range(max_disks - 1, -1, -1):
        a_disk = disks_on_A[i] if i < len(disks_on_A) else 0
        b_disk = disks_on_B[i] if i < len(disks_on_B) else 0
        c_disk = disks_on_C[i] if i < len(disks_on_C) else 0
        
        a_str = " " + str(a_disk) + " " if a_disk > 0 else " | "
        b_str = " " + str(b_disk) + " " if b_disk > 0 else " | "
        c_str = " " + str(c_disk) + " " if c_disk > 0 else " | "
        
        print(f"{a_str}  {b_str}  {c_str}")
    
    print("="*50)


def solve_with_visualization(num_disks=3):
    print(f"\nSolving Tower of Hanoi with {num_disks} disks (with visualization)")
    
    # Initialize towers
    towers = {
        'A': list(range(num_disks, 0, -1)),  # Largest to smallest
        'B': [],
        'C': []
    }
    
    solver = RecursiveSolver(num_disks, 'A', 'C', 'B')
    moves = solver.solve()
    
    # Show initial state
    visualize_towers(towers['A'], towers['B'], towers['C'], "Initial state")
    
    # Execute moves and show each step
    for i, (source, target) in enumerate(moves, 1):
        # Move disk
        disk = towers[source].pop()
        towers[target].append(disk)
        
        # Show state after move
        visualize_towers(towers['A'], towers['B'], towers['C'], 
                        f"Move {i}: Disk {disk} from {source} to {target}")
    
    print(f"\nSolved in {len(moves)} moves!")


if __name__ == "__main__":
    # Example usage
    print("=== Recursive Tower of Hanoi Solver ===")
    
    # Test with 3 disks
    solver = RecursiveSolver(3, 'A', 'C', 'B')
    solver.solve()
    solver.print_solution()
    print(solver.get_formula_explanation())
    
    # Test with visualization (commented out to avoid long output)
    # solve_with_visualization(3)