import random

class HanoiLogic:
    def __init__(self, num_pegs=3, num_disks=None, game_mode="interactive"):
        self.num_pegs = num_pegs
        if num_disks:
            self.num_disks = num_disks
        else:
            self.num_disks = random.randint(3, 6)
        self.game_mode = game_mode  # "interactive" or "sequence"
        self.tower_labels = self._labels(num_pegs)
        self.towers = {label: [] for label in self.tower_labels}
        self._initialize_disks()
        
        # Interactive mode
        self.selected_disk = None
        self.selected_peg = None
        self.move_count = 0
        
        # Sequence mode
        self.user_num_moves_input = ""
        self.user_moves_input = ""
        self.user_sequence = []
        self.sequence_validated = False
        self.sequence_result = ""
        
        self.game_state = "playing" if game_mode == "interactive" else "input"
        self.message = "Game started! Drag disks to move them." if game_mode == "interactive" else "Enter number of moves and sequence."

    def _labels(self, n):
        return ['A', 'B', 'C', 'D'][:n]

    def _initialize_disks(self):
        """Place all disks in tower A (largest at bottom)"""
        self.towers[self.tower_labels[0]] = list(range(self.num_disks, 0, -1))

    def get_min_moves(self):
        return (2 ** self.num_disks) - 1

    # ========== INTERACTIVE MODE METHODS ==========
    def can_select_disk(self, peg_label, disk_index):
        """Check if a disk can be selected (must be top disk)"""
        if peg_label not in self.tower_labels:
            return False
        tower = self.towers[peg_label]
        return len(tower) > 0 and disk_index == len(tower) - 1

    def select_disk(self, peg_label):
        """Select top disk from a peg"""
        if peg_label not in self.tower_labels:
            return False
            
        tower = self.towers[peg_label]
        if not tower:
            self.message = "No disk to select!"
            return False
            
        self.selected_disk = tower[-1]
        self.selected_peg = peg_label
        self.message = f"Selected disk {self.selected_disk} from peg {peg_label}"
        return True

    def move_disk(self, target_peg):
        """Move selected disk to target peg"""
        if not self.selected_disk or not self.selected_peg:
            self.message = "No disk selected!"
            return False
            
        if target_peg not in self.tower_labels:
            self.message = "Invalid target peg!"
            return False
            
        if target_peg == self.selected_peg:
            self.message = "Can't move to same peg!"
            self.selected_disk = None
            self.selected_peg = None
            return False
            
        source_tower = self.towers[self.selected_peg]
        target_tower = self.towers[target_peg]
        
        # Check if move is valid
        if target_tower and target_tower[-1] < self.selected_disk:
            self.message = f"Cannot place disk {self.selected_disk} on disk {target_tower[-1]}!"
            self.selected_disk = None
            self.selected_peg = None
            return False
        
        # Perform the move
        source_tower.pop()
        target_tower.append(self.selected_disk)
        self.move_count += 1
        self.message = f"Moved disk {self.selected_disk} from {self.selected_peg} to {target_peg}"
        
        # Check if game is won
        if self.is_solved():
            self.game_state = "win"
            min_moves = self.get_min_moves()
            if self.move_count == min_moves:
                self.message = f"Perfect! Solved in minimum moves ({min_moves})! 🎉"
            elif self.move_count <= min_moves + 5:
                self.message = f"Great! Solved in {self.move_count} moves (optimal: {min_moves})! 👍"
            else:
                self.message = f"Solved in {self.move_count} moves (optimal: {min_moves})"
        
        self.selected_disk = None
        self.selected_peg = None
        return True

    def cancel_selection(self):
        """Cancel current disk selection"""
        if self.selected_disk:
            self.message = f"Canceled selection of disk {self.selected_disk}"
        self.selected_disk = None
        self.selected_peg = None

    # ========== SEQUENCE MODE METHODS ==========
    def parse_moves(self, text):
        """Parse text input into list of move tuples"""
        moves = []
        parts = text.upper().replace(",", " ").split()
        
        for p in parts:
            if len(p) != 2:
                return None
            if p[0] in self.tower_labels and p[1] in self.tower_labels:
                moves.append((p[0], p[1]))
            else:
                return None
        return moves

    def validate_sequence(self, num_moves_str, moves_text):
        """Validate user's move sequence"""
        try:
            # Parse number of moves
            try:
                num_moves = int(num_moves_str)
                if num_moves <= 0:
                    self.sequence_result = "Number of moves must be positive!"
                    return False
            except ValueError:
                self.sequence_result = "Please enter a valid number for moves!"
                return False
            
            # Parse move sequence
            moves = self.parse_moves(moves_text)
            if not moves:
                self.sequence_result = "Invalid move format! Use format like 'AB AC BC'"
                return False
            
            # Check if number of moves matches
            if len(moves) != num_moves:
                self.sequence_result = f"Number of moves ({len(moves)}) doesn't match input ({num_moves})"
                return False
            
            # Store for execution
            self.user_num_moves_input = num_moves_str
            self.user_moves_input = moves_text
            self.user_sequence = moves
            self.sequence_validated = True
            self.sequence_result = f"Sequence validated! {num_moves} moves ready to execute."
            return True
            
        except Exception as e:
            self.sequence_result = f"Error: {str(e)}"
            return False

    def execute_sequence(self):
        """Execute the validated move sequence"""
        if not self.sequence_validated:
            self.sequence_result = "Please validate sequence first!"
            return False
        
        # Create a copy to test moves without affecting current state
        temp_game = HanoiLogic(self.num_pegs, self.num_disks, "interactive")
        
        move_log = []
        for i, (from_tower, to_tower) in enumerate(self.user_sequence):
            move_success, error_msg = temp_game._execute_single_move(from_tower, to_tower)
            if not move_success:
                self.sequence_result = f"Move {i+1} ({from_tower}→{to_tower}) failed: {error_msg}"
                return False
            move_log.append((from_tower, to_tower, temp_game.towers.copy()))
        
        # Check if solved
        if temp_game.is_solved():
            # Apply successful moves to actual game
            self.towers = temp_game.towers
            self.move_count = len(self.user_sequence)
            self.game_state = "win"
            min_moves = self.get_min_moves()
            
            if self.move_count == min_moves:
                self.sequence_result = f"Perfect! Solved in minimum {min_moves} moves! 🎉"
            elif self.move_count <= min_moves * 1.5:
                self.sequence_result = f"Good! Solved in {self.move_count} moves (optimal: {min_moves})"
            else:
                self.sequence_result = f"Solved in {self.move_count} moves (optimal: {min_moves})"
            return True
        else:
            self.sequence_result = f"Sequence executed but didn't solve the puzzle. Disks ended up on: {self._get_tower_state(temp_game.towers)}"
            return False

    def _execute_single_move(self, from_tower, to_tower):
        """Execute a single move (internal use)"""
        if from_tower not in self.tower_labels or to_tower not in self.tower_labels:
            return False, "Invalid tower label!"
        
        src = self.towers[from_tower]
        dst = self.towers[to_tower]

        if not src:
            return False, "No disk on source tower!"

        disk = src[-1]

        if dst and dst[-1] < disk:
            return False, "Cannot place larger disk on smaller one!"

        src.pop()
        dst.append(disk)
        return True, None

    def _get_tower_state(self, towers):
        """Get string representation of tower state"""
        result = []
        for label in self.tower_labels:
            disks = towers[label]
            result.append(f"{label}:{disks}")
        return " | ".join(result)

    # ========== COMMON METHODS ==========
    def is_solved(self):
        """Check if all disks are on last peg"""
        last_label = self.tower_labels[-1]
        return len(self.towers[last_label]) == self.num_disks

    def reset(self, num_pegs=None, num_disks=None, game_mode=None):
        """Reset the game"""
        if num_pegs:
            self.num_pegs = num_pegs
        if num_disks:
            self.num_disks = num_disks
        else:
            self.num_disks = random.randint(5, 10)
            
        if game_mode:
            self.game_mode = game_mode
            
        self.tower_labels = self._labels(self.num_pegs)
        self.towers = {label: [] for label in self.tower_labels}
        self._initialize_disks()
        
        # Reset interactive mode
        self.selected_disk = None
        self.selected_peg = None
        self.move_count = 0
        
        # Reset sequence mode
        self.user_num_moves_input = ""
        self.user_moves_input = ""
        self.user_sequence = []
        self.sequence_validated = False
        self.sequence_result = ""
        
        self.game_state = "playing" if self.game_mode == "interactive" else "input"
        self.message = "Game started! Drag disks to move them." if self.game_mode == "interactive" else "Enter number of moves and sequence."

    def switch_mode(self, new_mode):
        """Switch between interactive and sequence modes"""
        if new_mode not in ["interactive", "sequence"]:
            return False
        
        self.game_mode = new_mode
        self.reset(game_mode=new_mode)
        return True

    def get_top_disk(self, peg_label):
        """Get the top disk on a peg"""
        tower = self.towers[peg_label]
        return tower[-1] if tower else None
    