import random
class BoardGenerator:
    
    def __init__(self, board_size):
        
        if not isinstance(board_size, int):
            raise ValueError("Board size must be an integer")
        
        if not 6 <= board_size <= 12:
            raise ValueError("Board size must be between 6 and 12")
        
        self.board_size = board_size
        self.total_cells = board_size * board_size
        self.num_snakes = board_size - 2
        self.num_ladders = board_size - 2
        
        self.snakes = {}  # {head_position: tail_position}
        self.ladders = {}  # {base_position: top_position}
        
        # Generate NEW random board each time
        self._generate_board()
    
    def _generate_board(self):

        print(f"\n🎲 Generating NEW random board...")
        
        # Available cells (exclude cell 1 and last cell)
        available_cells = set(range(2, self.total_cells))
        
        # Generate ladders first
        self._generate_ladders(available_cells)
        
        # Generate snakes
        self._generate_snakes(available_cells)
        
        print(f"✅ Board generated: {len(self.ladders)} ladders, {len(self.snakes)} snakes")
        print(f"   Snakes will bring you DOWN ⬇️")
        print(f"   Ladders will take you UP ⬆️")
    
    def _generate_ladders(self, available_cells):

        ladder_count = 0
        attempts = 0
        max_attempts = 1000
        
        while ladder_count < self.num_ladders and attempts < max_attempts:
            attempts += 1

            # Ladder base should be in lower/middle portion of board
            max_base = self.total_cells - (self.board_size * 2)
            possible_bases = [c for c in available_cells if c <= max_base]
            
            if not possible_bases:
                break
            
            base = random.choice(possible_bases)
            
            # Calculate minimum and maximum climb
            min_climb = max(5, self.board_size)
            max_top = min(self.total_cells - 1, base + (self.board_size * 3))
            
            if base + min_climb > max_top:
                continue
            
            # Find valid top positions
            valid_tops = [t for t in range(base + min_climb, max_top + 1) 
                         if t in available_cells and t != self.total_cells]
            
            if not valid_tops:
                continue
            
            top = random.choice(valid_tops)
            
            # Add ladder
            self.ladders[base] = top
            available_cells.discard(base)
            available_cells.discard(top)
            ladder_count += 1
    
    def _generate_snakes(self, available_cells):

        snake_count = 0
        attempts = 0
        max_attempts = 1000
        
        while snake_count < self.num_snakes and attempts < max_attempts:
            attempts += 1
            
            # Snake head should be in upper/middle portion
            min_head = self.total_cells // 3
            possible_heads = [c for c in available_cells if c >= min_head]
            
            if not possible_heads:
                break
            
            head = random.choice(possible_heads)
            
            # Calculate minimum descent and tail range
            min_descent = max(5, self.board_size)
            min_tail = max(2, head - (self.board_size * 3))
            
            if head - min_descent < min_tail:
                continue
            
            # Find valid tail positions
            valid_tails = [t for t in range(min_tail, head - min_descent + 1) 
                          if t in available_cells and t > 1]
            
            if not valid_tails:
                continue
            
            tail = random.choice(valid_tails)
            
            # Add snake
            self.snakes[head] = tail
            available_cells.discard(head)
            available_cells.discard(tail)
            snake_count += 1
    
    def get_position_coordinates(self, cell_num):
       
        if cell_num < 1 or cell_num > self.total_cells:
            raise ValueError(f"Cell number must be between 1 and {self.total_cells}")
        
        # Convert to 0-indexed
        cell_num -= 1
        
        # Calculate row (from bottom)
        row = self.board_size - 1 - (cell_num // self.board_size)
        
        # Calculate column (serpentine pattern)
        row_from_bottom = cell_num // self.board_size
        
        if row_from_bottom % 2 == 0:
            # Even rows (from bottom): left to right
            col = cell_num % self.board_size
        else:
            # Odd rows (from bottom): right to left
            col = self.board_size - 1 - (cell_num % self.board_size)
        
        return (row, col)
    
    def get_next_position(self, current_pos, dice_roll):
        """
        Get next position after dice roll
        Automatically applies snake/ladder if landing on one
        
        Args:
            current_pos: Current cell position (1 to N²)
            dice_roll: Dice value (1-6)
        
        Returns:
            dict: Movement information with 'next_pos', 'landed_on', 'final_pos'
        
        Raises:
            ValueError: If dice_roll is not between 1 and 6
        """
        if not 1 <= dice_roll <= 6:
            raise ValueError("Dice roll must be between 1 and 6")
        
        next_pos = current_pos + dice_roll
        landed_on = None
        final_pos = next_pos
        
        # Can't move beyond the board
        if next_pos > self.total_cells:
            return {
                'next_pos': current_pos,
                'landed_on': 'out_of_bounds',
                'final_pos': current_pos,
                'message': f"Need exactly {self.total_cells - current_pos} to win!"
            }
        
        # Check for ladder at new position
        if next_pos in self.ladders:
            final_pos = self.ladders[next_pos]
            landed_on = 'ladder'
            message = f"🪜 Ladder! Climbed from {next_pos} to {final_pos}"
            print(message)
        
        # Check for snake at new position
        elif next_pos in self.snakes:
            final_pos = self.snakes[next_pos]
            landed_on = 'snake'
            message = f"🐍 Snake! Fell from {next_pos} to {final_pos}"
            print(message)
        
        else:
            message = f"Moved to {next_pos}"
        
        return {
            'next_pos': next_pos,
            'landed_on': landed_on,
            'final_pos': final_pos,
            'message': message
        }
    
    def get_board_info(self):
        
        return {
            'board_size': self.board_size,
            'total_cells': self.total_cells,
            'num_snakes': len(self.snakes),
            'num_ladders': len(self.ladders),
            'snakes': self.snakes.copy(),
            'ladders': self.ladders.copy()
        }
    
    def print_board_info(self):
        """Print board information to console"""
        print(f"\n{'='*60}")
        print(f"🎲 SNAKE AND LADDER BOARD")
        print(f"{'='*60}")
        print(f"Board Size: {self.board_size} × {self.board_size}")
        print(f"Total Cells: {self.total_cells}")
        print(f"Start: Cell 1  |  End: Cell {self.total_cells}")
        
        print(f"\n🐍 SNAKES ({len(self.snakes)}):")
        if self.snakes:
            for head, tail in sorted(self.snakes.items()):
                print(f"   Cell {head} → Cell {tail} (down {head - tail} cells)")
        else:
            print("   No snakes generated")
        
        print(f"\n🪜 LADDERS ({len(self.ladders)}):")
        if self.ladders:
            for base, top in sorted(self.ladders.items()):
                print(f"   Cell {base} → Cell {top} (up {top - base} cells)")
        else:
            print("   No ladders generated")
        
        print(f"{'='*60}\n")