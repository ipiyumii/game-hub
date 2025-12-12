from collections import deque
import time

class BFSAlgorithm:
    
    
    def __init__(self, board):
        
        self.board = board
        self.total_cells = board.total_cells
        self.snakes = board.snakes
        self.ladders = board.ladders
    
    def find_minimum_moves(self):
        
        print("\n🔍 Running BFS Algorithm...")
        start_time = time.time()
        
        # Start from cell 1, target is last cell
        start = 1
        target = self.total_cells
        
        # BFS initialization
        visited = set([start])
        queue = deque([(start, 0)])  # (current_position, number_of_moves)
        
        while queue:
            current_position, moves = queue.popleft()
            
            # Check if we reached the target
            if current_position == target:
                execution_time = time.time() - start_time
                print(f"✅ BFS Found: {moves} moves in {execution_time*1000:.4f}ms")
                return moves, execution_time
            
            # Try all possible dice rolls (1 to 6)
            for dice_value in range(1, 7):
                next_position = current_position + dice_value
                
                # Can't go beyond the board
                if next_position > target:
                    continue
                
                # Apply snake or ladder if present
                final_position = self._apply_snake_or_ladder(next_position)
                
                # If not visited, add to queue
                if final_position not in visited:
                    visited.add(final_position)
                    queue.append((final_position, moves + 1))
        
        # No path found (shouldn't happen in valid game)
        execution_time = time.time() - start_time
        print(f"❌ BFS: No path found")
        return -1, execution_time
    
    def _apply_snake_or_ladder(self, position):
        
        # Check if there's a ladder at this position
        if position in self.ladders:
            return self.ladders[position]
        
        # Check if there's a snake at this position
        if position in self.snakes:
            return self.snakes[position]
        
        # No snake or ladder
        return position
    
    def get_algorithm_info(self):
        
        return {
            'name': 'BFS (Breadth-First Search)',
            'description': 'Explores all possible moves level by level',
            'complexity': 'O(N) where N is number of cells',
            'guarantees': 'Shortest path'
        }