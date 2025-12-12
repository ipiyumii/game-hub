import random
from board_generator import BoardGenerator

class GameState:
    
    def __init__(self):
        #Initialize game state
        self.player_name = ""
        self.board_size = 8
        self.board = None
        self.session_id = None
        self.current_position = 1
        self.is_game_active = False
        self.move_history = []
        self.dice_rolls = 0
    
    def start_new_game(self, player_name, board_size):
        
        # Validate player name
        if not player_name or not player_name.strip():
            raise ValueError("Player name cannot be empty")
        
        # Validate board size
        if not isinstance(board_size, int) or not 6 <= board_size <= 12:
            raise ValueError("Board size must be between 6 and 12")
        
        # Set player info
        self.player_name = player_name.strip()
        self.board_size = board_size
        
        # Generate NEW board with random snakes and ladders
        self.board = BoardGenerator(board_size)
        
        # Reset game state
        self.current_position = 1
        self.is_game_active = True
        self.move_history = []
        self.dice_rolls = 0
        
        print(f"\n🎮 New game started!")
        print(f"Player: {self.player_name}")
        print(f"Board: {self.board_size}×{self.board_size}")
        
        # Print board details
        self.board.print_board_info()
    
    def roll_dice(self):
       
        dice_value = random.randint(1, 6)
        self.dice_rolls += 1
        print(f"\n🎲 Dice Roll #{self.dice_rolls}: {dice_value}")
        return dice_value
    
    def move_player(self, dice_value):
        
        if not self.is_game_active:
            raise RuntimeError("No active game")
        
        old_position = self.current_position
        move_result = self.board.get_next_position(old_position, dice_value)
        
        self.current_position = move_result['final_pos']
        
        # Add to history
        self.move_history.append({
            'roll': self.dice_rolls,
            'dice': dice_value,
            'from': old_position,
            'to': self.current_position,
            'landed_on': move_result['landed_on']
        })
        
        # Check if won
        if self.current_position == self.board.total_cells:
            self.is_game_active = False
            move_result['won'] = True
            print(f"\n🎉 Congratulations {self.player_name}!")
            print(f"   You reached cell {self.board.total_cells} in {self.dice_rolls} dice rolls!")
        else:
            move_result['won'] = False
            print(f"   Current position: {self.current_position}/{self.board.total_cells}")
        
        return move_result
    
    def get_board_info(self):
        
        if not self.board:
            return None
        return self.board.get_board_info()
    
    def get_game_status(self):
       
        return {
            'player_name': self.player_name,
            'board_size': self.board_size,
            'current_position': self.current_position,
            'target_position': self.board.total_cells if self.board else 0,
            'is_active': self.is_game_active,
            'dice_rolls': self.dice_rolls,
            'progress': (self.current_position / self.board.total_cells * 100) if self.board else 0
        }
    
    def reset_game(self):
        
        self.player_name = ""
        self.board_size = 8
        self.board = None
        self.session_id = None
        self.current_position = 1
        self.is_game_active = False
        self.move_history = []
        self.dice_rolls = 0
        print("🔄 Game reset")