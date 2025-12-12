import random

class HanoiLogic:
    def __init__(self, num_pegs=3, num_disks=None, game_mode="interactive"):
        """Initialize the Tower of Hanoi game logic."""
        self.num_pegs = num_pegs

        # If num_disks is not provided, choose a reasonable default range
        if num_disks is not None:
            self.num_disks = num_disks
        else:
            self.num_disks = random.randint(3, 6)

        self.game_mode = game_mode  # "interactive" or "sequence"

        # Tower labels based on number of pegs
        self.tower_labels = self._labels(num_pegs)
        self.towers = {label: [] for label in self.tower_labels}
        self._initialize_disks()

        # Interactive mode state
        self.selected_disk = None
        self.selected_peg = None
        self.move_count = 0

        # Sequence mode state
        self.user_num_moves_input = ""
        self.user_moves_input = ""
        self.user_sequence = []
        self.sequence_validated = False
        self.sequence_result = ""

        # Game state and messages
        self.game_state = "playing" if game_mode == "interactive" else "input"
        self.message = (
            "Game started! Drag disks to move them."
            if game_mode == "interactive"
            else "Enter number of moves and sequence."
        )

    # ---------- Internal helpers ----------

    def _labels(self, n):
        """Return peg labels for n pegs."""
        return ['A', 'B', 'C', 'D'][:n]

    def _initialize_disks(self):
        """Place all disks on the first tower (largest at bottom)."""
        self.towers[self.tower_labels[0]] = list(range(self.num_disks, 0, -1))

    # ---------- Minimum moves ----------

    def get_min_moves(self):
        """Return theoretical minimum moves based on pegs and disks."""
        if self.num_pegs == 3:
            # Classic 3-peg formula: 2^n - 1
            return (2 ** self.num_disks) - 1
        else:
            # Approximation / known optimal for small n for 4 pegs (Frame–Stewart)
            optimal_4peg = {
                1: 1,
                2: 3,
                3: 5,
                4: 9,
                5: 13,
                6: 17,
                7: 25,
                8: 33,
            }
            return optimal_4peg.get(self.num_disks, (2 ** self.num_disks) - 1)

    # ========== INTERACTIVE MODE METHODS ==========

    def can_select_disk(self, peg_label, disk_index):
        """Check if a disk can be selected (must be top disk on a valid peg)."""
        if peg_label not in self.tower_labels:
            return False
        tower = self.towers[peg_label]
        return len(tower) > 0 and disk_index == len(tower) - 1

    def select_disk(self, peg_label):
        """Select top disk from a peg."""
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
        """Move selected disk to target peg."""
        if self.selected_disk is None or self.selected_peg is None:
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

        # Check validity: can't put larger disk on smaller one
        if target_tower and target_tower[-1] < self.selected_disk:
            self.message = (
                f"Cannot place disk {self.selected_disk} "
                f"on disk {target_tower[-1]}!"
            )
            self.selected_disk = None
            self.selected_peg = None
            return False

        # Perform the move
        source_tower.pop()
        target_tower.append(self.selected_disk)
        self.move_count += 1
        self.message = (
            f"Moved disk {self.selected_disk} from {self.selected_peg} to {target_peg}"
        )

        # Check if game is won
        if self.is_solved():
            self.game_state = "win"
            min_moves = self.get_min_moves()
            if self.move_count == min_moves:
                self.message = (
                    f"Perfect! Solved in minimum moves ({min_moves})!"
                )
            elif self.move_count <= min_moves + 5:
                self.message = (
                    f"Great! Solved in {self.move_count} moves "
                    f"(optimal: {min_moves})!"
                )
            else:
                self.message = (
                    f"Solved in {self.move_count} moves (optimal: {min_moves})"
                )

        self.selected_disk = None
        self.selected_peg = None
        return True

    def cancel_selection(self):
        """Cancel current disk selection."""
        if self.selected_disk is not None:
            self.message = f"Canceled selection of disk {self.selected_disk}"
        self.selected_disk = None
        self.selected_peg = None

    # ========== SEQUENCE MODE METHODS ==========

    def parse_moves(self, text):
        """Parse text input into list of move tuples (e.g., 'AB AC BC')."""
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
        """Validate user's move sequence input."""
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
                self.sequence_result = (
                    "Invalid move format! Use format like 'AB AC BC'"
                )
                return False

            # Check if number of moves matches
            if len(moves) != num_moves:
                self.sequence_result = (
                    f"Number of moves ({len(moves)}) "
                    f"doesn't match input ({num_moves})"
                )
                return False

            # Store for execution
            self.user_num_moves_input = num_moves_str
            self.user_moves_input = moves_text
            self.user_sequence = moves
            self.sequence_validated = True
            self.sequence_result = (
                f"Sequence validated! {num_moves} moves ready to execute."
            )
            return True

        except Exception as e:
            self.sequence_result = f"Error: {str(e)}"
            return False

    def execute_sequence(self):
        """Execute the validated move sequence on a temporary game first."""
        if not self.sequence_validated:
            self.sequence_result = "Please validate sequence first!"
            return False

        # Create a temp interactive game with the same setup
        temp_game = HanoiLogic(
            num_pegs=self.num_pegs,
            num_disks=self.num_disks,
            game_mode="interactive",
        )

        for i, (from_tower, to_tower) in enumerate(self.user_sequence):
            move_success, error_msg = temp_game._execute_single_move(
                from_tower, to_tower
            )
            if not move_success:
                self.sequence_result = (
                    f"Move {i+1} ({from_tower}→{to_tower}) failed: {error_msg}"
                )
                return False

        # Check if solved on temp game
        if temp_game.is_solved():
            # Apply final state to actual game
            self.towers = {
                label: temp_game.towers[label].copy()
                for label in self.tower_labels
            }
            self.move_count = len(self.user_sequence)
            self.game_state = "win"
            min_moves = self.get_min_moves()

            if self.move_count == min_moves:
                self.sequence_result = (
                    f"Perfect! Solved in minimum {min_moves} moves!"
                )
            elif self.move_count <= int(min_moves * 1.5):
                self.sequence_result = (
                    f"Good! Solved in {self.move_count} moves "
                    f"(optimal: {min_moves})"
                )
            else:
                self.sequence_result = (
                    f"Solved in {self.move_count} moves "
                    f"(optimal: {min_moves})"
                )
            return True
        else:
            self.sequence_result = (
                "Sequence executed but did not solve the puzzle. "
                f"Disks ended up on: {self._get_tower_state(temp_game.towers)}"
            )
            return False

    def _execute_single_move(self, from_tower, to_tower):
        """Execute a single move (used by execute_sequence)."""
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
        """Get string representation of tower state (for debugging / messages)."""
        result = []
        for label in self.tower_labels:
            disks = towers[label]
            result.append(f"{label}:{disks}")
        return " | ".join(result)

    # ========== COMMON METHODS ==========

    def is_solved(self):
        """Check if all disks are on the last peg."""
        last_label = self.tower_labels[-1]
        return len(self.towers[last_label]) == self.num_disks

    def reset(self, num_pegs=None, num_disks=None, game_mode=None):
        """Reset the game state while keeping explicit parameters stable."""
        if num_pegs is not None:
            self.num_pegs = num_pegs
        if num_disks is not None:
            # Respect the caller's disk count (no random override)
            self.num_disks = num_disks

        if game_mode is not None:
            self.game_mode = game_mode

        # Rebuild labels and towers based on current num_pegs/num_disks
        self.tower_labels = self._labels(self.num_pegs)
        self.towers = {label: [] for label in self.tower_labels}
        self._initialize_disks()

        # Reset interactive mode state
        self.selected_disk = None
        self.selected_peg = None
        self.move_count = 0

        # Reset sequence mode state
        self.user_num_moves_input = ""
        self.user_moves_input = ""
        self.user_sequence = []
        self.sequence_validated = False
        self.sequence_result = ""

        self.game_state = "playing" if self.game_mode == "interactive" else "input"
        self.message = (
            "Game started! Drag disks to move them."
            if self.game_mode == "interactive"
            else "Enter number of moves and sequence."
        )

    def switch_mode(self, new_mode):
        """Switch between interactive and sequence modes (keeping pegs & disks)."""
        if new_mode not in ["interactive", "sequence"]:
            return False

        self.game_mode = new_mode
        # Keep current num_pegs and num_disks; only change mode
        self.reset(num_pegs=self.num_pegs, num_disks=self.num_disks, game_mode=new_mode)
        return True

    def get_top_disk(self, peg_label):
        """Get the top disk on a peg."""
        if peg_label not in self.tower_labels:
            return None
        tower = self.towers[peg_label]
        return tower[-1] if tower else None
