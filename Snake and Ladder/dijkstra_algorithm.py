import heapq
import time

class DijkstraAlgorithm:
    
    def __init__(self, board):
        
        self.board = board
        self.total_cells = board.total_cells
        self.snakes = board.snakes
        self.ladders = board.ladders
    
    def find_minimum_moves(self):
        
        print("\n🔍 Running Dijkstra's Algorithm...")
        start_time = time.time()
        
        # Start from cell 1, target is last cell
        start = 1
        target = self.total_cells
        
        # Dijkstra's initialization
        # Priority queue: (distance/moves, position)
        heap = [(0, start)]
        distances = {start: 0}
        
        while heap:
            current_moves, current_position = heapq.heappop(heap)
            
            # Check if reached the target
            if current_position == target:
                execution_time = time.time() - start_time
                print(f"✅ Dijkstra Found: {current_moves} moves in {execution_time*1000:.4f}ms")
                return current_moves, execution_time
            
            # Skip if already found a path 
            if current_position in distances and distances[current_position] < current_moves:
                continue
            
            # Try all possible dice rolls (1 to 6)
            for dice_value in range(1, 7):
                next_position = current_position + dice_value
                
                # Can't go beyond the board
                if next_position > target:
                    continue
                
                # Apply snake or ladder
                final_position = self._apply_snake_or_ladder(next_position)
                
                # Calculate new distance
                new_moves = current_moves + 1
                
                # If found a shorter path to final_position
                if final_position not in distances or new_moves < distances[final_position]:
                    distances[final_position] = new_moves
                    heapq.heappush(heap, (new_moves, final_position))
        
        # No path found
        execution_time = time.time() - start_time
        print(f"❌ Dijkstra: No path found")
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
            'name': 'Dijkstra\'s Algorithm',
            'description': 'Uses priority queue to find shortest path',
            'complexity': 'O(N log N) where N is number of cells',
            'guarantees': 'Optimal solution'
        }