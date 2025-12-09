"""
Tower of Hanoi UI with 3-Peg and 4-Peg Algorithm Support
Integrated with your 4-peg solvers.
"""

import pygame
import sys
import io
from game_logic import HanoiLogic
from datetime import datetime

# Import your 4-peg solvers
from four_peg_iterative import FourPegSolver
from four_peg_recursive import FourPegRecursiveSolver

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')
try:
    from firebase_handler import FirebaseHandler
    # Create a wrapper that fixes the emoji issue
    class SafeFirebaseHandler(FirebaseHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Override any print methods that use emojis
            
        def get_high_scores(self, limit=5):
            """Get high scores - handles errors gracefully"""
            try:
                if not hasattr(self, 'db') or not self.db:
                    return []
                
                # Try multiple collection names
                collections_to_try = ['hanoi_scores', 'towerOfHand', 'tower_of_hanoi_scores', 'scores']
                
                for collection_name in collections_to_try:
                    try:
                        # Get all documents
                        docs = self.db.collection(collection_name).stream()
                        scores = []
                        for doc in docs:
                            data = doc.to_dict()
                            data['id'] = doc.id
                            scores.append(data)
                        
                        if scores:
                            # Sort by moves (lower is better)
                            scores.sort(key=lambda x: x.get('num_moves', 999999))
                            return scores[:limit]
                    except Exception as e:
                        continue
                
                return []
                
            except Exception as e:
                # Clean error message for Windows
                error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
                print(f"Error getting scores: {error_msg[:100]}")
                return []
                
        def save_player_score(self, **kwargs):
            """Save player score"""
            try:
                if not hasattr(self, 'db') or not self.db:
                    print("Firebase not connected")
                    return False
                
                # Prepare score data
                score_data = {
                    'player_name': kwargs.get('player_name', 'Anonymous'),
                    'num_disks': kwargs.get('num_disks', 3),
                    'num_moves': kwargs.get('num_moves', 0),
                    'optimal_moves': kwargs.get('optimal_moves', 7),
                    'game_mode': kwargs.get('game_mode', 'interactive'),
                    'move_sequence': kwargs.get('move_sequence', ''),
                    'is_correct': kwargs.get('is_correct', False),
                    'timestamp': datetime.now().isoformat(),
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Try multiple collections
                collections_to_try = ['hanoi_scores', 'towerOfHand', 'tower_of_hanoi_scores']
                
                for collection_name in collections_to_try:
                    try:
                        # Create a new document
                        doc_ref = self.db.collection(collection_name).document()
                        doc_ref.set(score_data)
                        print(f"Score saved to {collection_name}")
                        return True
                    except Exception as e:
                        continue
                
                print("Failed to save to any collection")
                return False
                
            except Exception as e:
                error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
                print(f"Error saving score: {error_msg[:100]}")
                return False
    
    firebase = SafeFirebaseHandler()
    FIREBASE_AVAILABLE = True
    
except (ImportError, Exception) as e:
    # Create a dummy FirebaseHandler if not available
    error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
    print(f"Firebase not available: {error_msg[:100]}")
    
    class DummyFirebaseHandler:
        def __init__(self):
            self.is_connected = lambda: False
            self.get_high_scores = lambda limit=5: []
            self.save_player_score = lambda **kwargs: True
    firebase = DummyFirebaseHandler()
    FIREBASE_AVAILABLE = False

# Import the 3-peg solver algorithms (keep existing)
from iterative_solver import IterativeSolver, solve_iteratively
from recursive_solver import RecursiveSolver, solve_recursively

class AlgorithmHelper:
    """Helper class to integrate solver algorithms with the game"""
    def __init__(self, num_disks=3, num_pegs=3):
        self.num_disks = num_disks
        self.num_pegs = num_pegs
        self.optimal_solution = None
        self.current_move_index = 0
        self.algorithm_type = 'iterative'  # Default algorithm
        self.peg_type = '3peg'  # Default: 3 pegs
        
    def set_num_disks(self, num_disks):
        """Update number of disks"""
        self.num_disks = num_disks
        self.reset_solution()
        
    def set_num_pegs(self, num_pegs):
        """Update number of pegs"""
        self.num_pegs = num_pegs
        self.peg_type = '4peg' if num_pegs == 4 else '3peg'
        self.reset_solution()
        
    def reset_solution(self):
        """Reset the solution state"""
        self.optimal_solution = None
        self.current_move_index = 0
        
    def get_optimal_solution(self, algorithm='iterative'):
        """Get optimal solution using specified algorithm."""
        self.algorithm_type = algorithm
        
        if self.num_pegs == 4:
            # Use 4-peg solvers
            if algorithm == 'iterative':
                solver = FourPegSolver(self.num_disks, ['A', 'B', 'C', 'D'])
            else:  # recursive
                solver = FourPegRecursiveSolver(self.num_disks, ['A', 'B', 'C', 'D'])
        else:
            # Use 3-peg solvers
            if algorithm == 'iterative':
                solver = IterativeSolver(self.num_disks, 'A', 'C', 'B')
            else:  # recursive
                solver = RecursiveSolver(self.num_disks, 'A', 'C', 'B')
        
        solver.solve()
        if self.num_pegs == 4:
            # 4-peg solvers return list of tuples
            self.optimal_solution = solver.moves
        else:
            # 3-peg solvers return move sequence
            self.optimal_solution = solver.get_move_sequence()
        self.current_move_index = 0
        return self.optimal_solution
    
    def get_next_hint(self):
        """Get next optimal move as a hint."""
        if not self.optimal_solution:
            self.get_optimal_solution()
        
        if self.current_move_index < len(self.optimal_solution):
            if self.num_pegs == 4:
                # 4-peg: tuple format ('A', 'D')
                hint = self.optimal_solution[self.current_move_index]
            else:
                # 3-peg: string format "AB"
                hint_str = self.optimal_solution[self.current_move_index]
                hint = (hint_str[0], hint_str[1])
            self.current_move_index += 1
            return hint  # Returns tuple like ('A', 'B')
        return None
    
    def get_current_hint(self):
        """Get current hint without advancing the index."""
        if not self.optimal_solution:
            self.get_optimal_solution()
        
        if self.current_move_index < len(self.optimal_solution):
            if self.num_pegs == 4:
                return self.optimal_solution[self.current_move_index]
            else:
                hint_str = self.optimal_solution[self.current_move_index]
                return (hint_str[0], hint_str[1])
        return None
    
    def auto_solve_step(self):
        """Execute one step of auto-solve."""
        if not self.optimal_solution:
            self.get_optimal_solution()
        
        if self.current_move_index < len(self.optimal_solution):
            if self.num_pegs == 4:
                move = self.optimal_solution[self.current_move_index]
            else:
                move_str = self.optimal_solution[self.current_move_index]
                move = (move_str[0], move_str[1])
            self.current_move_index += 1
            # Return move as tuple of pegs, e.g., ('A', 'B')
            return move
        return None
    
    def check_player_solution(self, player_moves):
        """Check if player's solution is optimal."""
        optimal = self.get_optimal_solution()
        return len(player_moves) == len(optimal)
    
    def get_algorithm_explanation(self):
        """Get educational explanation of the algorithms."""
        if self.num_pegs == 4:
            # 4-peg explanations
            if self.num_disks <= 4:
                optimal_moves = {1: 1, 2: 3, 3: 5, 4: 9}.get(self.num_disks, "?")
                moves_text = f"Optimal: {optimal_moves} moves"
            else:
                moves_text = "Using Frame-Stewart algorithm"
            
            return {
                'formula': moves_text,
                'iterative_pattern': 'Uses hardcoded optimal solutions for 1-4 disks',
                'recursive_principle': 'Frame-Stewart: divide disks into optimal groups',
                'current_algorithm': f"{self.algorithm_type} ({self.peg_type})"
            }
        else:
            # 3-peg explanations (original)
            return {
                'formula': f'2^{self.num_disks} - 1 = {(1 << self.num_disks) - 1} moves',
                'iterative_pattern': 'AB, AC, BC (odd) or AC, AB, CB (even) pattern',
                'recursive_principle': 'Divide and conquer: move n-1 disks, move nth disk, move n-1 disks',
                'current_algorithm': f"{self.algorithm_type} ({self.peg_type})"
            }
    
    def get_complete_solution(self):
        """Get complete solution for educational display."""
        if not self.optimal_solution:
            self.get_optimal_solution()
        
        # Convert to uniform format for display
        display_solution = []
        for move in self.optimal_solution:
            if self.num_pegs == 4:
                # Already tuple format
                display_solution.append(move)
            else:
                # Convert string to tuple
                display_solution.append((move[0], move[1]))
        return display_solution

pygame.init()

# Window settings
WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi with 3 & 4 Peg Algorithm Features")

# Colors (same as original)
BACKGROUND = (25, 25, 45)
PANEL_BG = (40, 40, 65)
PANEL_BORDER = (80, 80, 110)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 120)
LIGHT_GRAY = (180, 180, 200)
BLUE = (80, 150, 255)
LIGHT_BLUE = (120, 190, 255)
RED = (255, 100, 100)
LIGHT_RED = (255, 140, 140)
GREEN = (80, 220, 120)
LIGHT_GREEN = (120, 240, 160)
YELLOW = (255, 220, 80)
LIGHT_YELLOW = (255, 240, 160)
PURPLE = (180, 100, 255)
LIGHT_PURPLE = (200, 140, 255)
CYAN = (80, 220, 220)
LIGHT_CYAN = (120, 240, 240)
ORANGE = (255, 160, 80)
LIGHT_ORANGE = (255, 190, 120)
DARK_BLUE = (40, 80, 160)
DARK_GREEN = (40, 140, 80)
DARK_RED = (140, 40, 40)

# Fonts (same as original)
TITLE_FONT = pygame.font.SysFont("arial", 52, bold=True)
HEADER_FONT = pygame.font.SysFont("arial", 20, bold=True)
BUTTON_FONT = pygame.font.SysFont("arial", 15, bold=True)
NORMAL_FONT = pygame.font.SysFont("arial", 15)
SMALL_FONT = pygame.font.SysFont("arial", 15)
STATS_FONT = pygame.font.SysFont("arial", 15, bold=True)
LARGE_FONT = pygame.font.SysFont("arial", 32, bold=True)

# Disk colors (same as original)
DISK_COLORS = [
    (255, 80, 80),    # Red
    (255, 140, 80),   # Orange
    (255, 200, 80),   # Yellow
    (80, 255, 80),    # Green
    (80, 255, 200),   # Cyan
    (80, 180, 255),   # Blue
    (180, 80, 255),   # Purple
    (255, 80, 180),   # Pink
    (255, 120, 120),  # Light Red
    (255, 180, 120),  # Light Orange
    (255, 220, 120),  # Light Yellow
    (120, 255, 120),  # Light Green
]

class NameInputDialog:
    def __init__(self, x, y, width, height, title="Enter Your Name"):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.name_input = ""
        self.active = True
        self.font = pygame.font.SysFont("arial", 28)
        self.title_font = pygame.font.SysFont("arial", 32, bold=True)
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.name_input.strip():
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.name_input = "Anonymous"
                return True
            elif event.unicode.isalnum() or event.unicode in " _-.":
                if len(self.name_input) < 20:
                    self.name_input += event.unicode
        return False
        
    def update(self):
        # Blink cursor
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
    def draw(self, win):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        win.blit(overlay, (0, 0))
        
        # Draw dialog box
        pygame.draw.rect(win, (50, 50, 80), self.rect, border_radius=15)
        pygame.draw.rect(win, YELLOW, self.rect, 3, border_radius=15)
        
        # Draw title
        title_text = self.title_font.render(self.title, True, YELLOW)
        win.blit(title_text, (self.rect.centerx - title_text.get_width()//2, 
                             self.rect.y + 30))
        
        # Draw input box
        input_rect = pygame.Rect(self.rect.x + 50, self.rect.centery - 20, 
                                self.rect.width - 100, 50)
        pygame.draw.rect(win, DARK_BLUE, input_rect, border_radius=8)
        pygame.draw.rect(win, WHITE, input_rect, 2, border_radius=8)
        
        # Draw input text
        display_text = self.name_input if self.name_input else "Type your name..."
        name_text = self.font.render(display_text, 
                                    True, WHITE if self.name_input else LIGHT_GRAY)
        win.blit(name_text, (input_rect.x + 15, input_rect.centery - name_text.get_height()//2))
        
        # Draw cursor
        if self.cursor_visible and self.active:
            cursor_x = input_rect.x + 15 + name_text.get_width()
            pygame.draw.line(win, WHITE, 
                           (cursor_x, input_rect.y + 10),
                           (cursor_x, input_rect.y + input_rect.height - 10),
                           2)
        
        # Draw instructions
        instructions = [
            "Press ENTER to continue",
            "Press ESC to play as Anonymous",
            "Maximum 20 characters"
        ]
        
        for i, line in enumerate(instructions):
            inst_text = SMALL_FONT.render(line, True, WHITE)
            win.blit(inst_text, (self.rect.centerx - inst_text.get_width()//2,
                                self.rect.y + self.rect.height - 80 + i * 25))

class Panel:
    def __init__(self, x, y, width, height, title="", bg_color=PANEL_BG):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.bg_color = bg_color
        self.has_shadow = True

    def draw(self, win):
        # Draw shadow if enabled
        if self.has_shadow:
            shadow_rect = self.rect.move(4, 4)
            pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=12)
        
        # Draw panel background
        pygame.draw.rect(win, self.bg_color, self.rect, border_radius=12)
        pygame.draw.rect(win, PANEL_BORDER, self.rect, 3, border_radius=12)
        
        # Draw title if provided
        if self.title:
            title_surface = HEADER_FONT.render(self.title, True, YELLOW)
            win.blit(title_surface, (self.rect.x + 20, self.rect.y + 15))

class Button:
    def __init__(self, x, y, width, height, text, color=BLUE, text_color=WHITE, has_shadow=True):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.hover_color = self._lighten_color(color, 40)
        self.is_hovered = False
        self.active = False
        self.has_shadow = has_shadow
        self.click_effect = False
        self.click_timer = 0

    def _lighten_color(self, color, amount):
        return tuple(min(255, c + amount) for c in color)

    def update(self):
        if self.click_effect:
            self.click_timer += 1
            if self.click_timer > 10:
                self.click_effect = False
                self.click_timer = 0

    def draw(self, win):
        # Draw shadow if enabled
        if self.has_shadow and not self.click_effect:
            shadow_rect = self.rect.move(3, 3)
            pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=8)
        
        # Determine button color
        if self.click_effect:
            color = self._lighten_color(self.color, 60)
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color
        
        # Draw button with rounded corners
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        
        # Draw border - thicker if active
        border_color = YELLOW if self.active else PANEL_BORDER
        border_width = 3 if self.active else 2
        pygame.draw.rect(win, border_color, self.rect, border_width, border_radius=8)
        
        # Draw text
        text_surface = BUTTON_FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos):
        clicked = self.rect.collidepoint(pos)
        if clicked:
            self.click_effect = True
            self.click_timer = 0
        return clicked

class InputBox:
    def __init__(self, x, y, width, height, label="", default_text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = default_text
        self.active = False
        self.bg_color = DARK_BLUE
        self.active_bg_color = PURPLE
        self.label_surface = SMALL_FONT.render(label, True, WHITE) if label else None
        self.cursor_visible = True
        self.cursor_timer = 0

    def update(self):
        if self.active:
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_SPACE:
                self.text += " "
            elif event.unicode.isalnum() or event.unicode in "ABCDabcd":
                self.text += event.unicode.upper()
        return False

    def draw(self, win):
        # Draw background
        bg_color = self.active_bg_color if self.active else self.bg_color
        pygame.draw.rect(win, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.rect, 2, border_radius=6)
        
        # Draw label above
        if self.label_surface:
            win.blit(self.label_surface, (self.rect.x, self.rect.y - 25))
        
        # Draw text
        if self.text:
            display_text = self.text if len(self.text) <= 15 else "..." + self.text[-12:]
            text_surface = NORMAL_FONT.render(display_text, True, WHITE)
            win.blit(text_surface, (self.rect.x + 10, self.rect.y + (self.rect.h - text_surface.get_height()) // 2))
        elif self.active:
            placeholder = "Type here..."
            text_surface = NORMAL_FONT.render(placeholder, True, LIGHT_GRAY)
            win.blit(text_surface, (self.rect.x + 10, self.rect.y + (self.rect.h - text_surface.get_height()) // 2))
        
        # Draw cursor
        if self.active and self.cursor_visible:
            text_width = NORMAL_FONT.render(self.text if self.text else "", True, WHITE).get_width()
            cursor_x = self.rect.x + 10 + text_width
            pygame.draw.line(win, WHITE,
                           (cursor_x, self.rect.y + 10),
                           (cursor_x, self.rect.y + self.rect.height - 10),
                           2)

    def clear(self):
        self.text = ""

class PegSelector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 3
        self.value_rect = pygame.Rect(x, y, 60, 40)
        self.minus_rect = pygame.Rect(x - 45, y, 40, 40)
        self.plus_rect = pygame.Rect(x + 65, y, 40, 40)
        self.minus_hover = False
        self.plus_hover = False

    def draw(self, win):
        # Draw label
        label = NORMAL_FONT.render("Pegs:", True, WHITE)
        win.blit(label, (self.x - 100, self.y + 10))
        
        # Draw value box
        pygame.draw.rect(win, DARK_BLUE, self.value_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.value_rect, 2, border_radius=6)
        value_text = STATS_FONT.render(str(self.value), True, YELLOW)
        win.blit(value_text, (self.x + 30 - value_text.get_width()//2, self.y + 8))
        
        # Draw minus button
        minus_color = LIGHT_RED if self.minus_hover else RED
        pygame.draw.rect(win, minus_color, self.minus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.minus_rect, 2, border_radius=6)
        minus_text = BUTTON_FONT.render("-", True, WHITE)
        win.blit(minus_text, (self.minus_rect.centerx - minus_text.get_width()//2, 
                             self.minus_rect.centery - minus_text.get_height()//2))
        
        # Draw plus button
        plus_color = LIGHT_GREEN if self.plus_hover else GREEN
        pygame.draw.rect(win, plus_color, self.plus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.plus_rect, 2, border_radius=6)
        plus_text = BUTTON_FONT.render("+", True, WHITE)
        win.blit(plus_text, (self.plus_rect.centerx - plus_text.get_width()//2, 
                            self.plus_rect.centery - plus_text.get_height()//2))

    def check_hover(self, pos):
        self.minus_hover = self.minus_rect.collidepoint(pos)
        self.plus_hover = self.plus_rect.collidepoint(pos)
        return self.minus_hover or self.plus_hover

    def handle_click(self, pos):
        if self.minus_rect.collidepoint(pos):
            if self.value > 3:
                self.value -= 1
                return True
        if self.plus_rect.collidepoint(pos):
            if self.value < 5:  # Allow up to 5 pegs
                self.value += 1
                return True
        return False

class DiskSelector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.value = 5
        self.value_rect = pygame.Rect(x, y, 60, 40)
        self.minus_rect = pygame.Rect(x - 45, y, 40, 40)
        self.plus_rect = pygame.Rect(x + 65, y, 40, 40)
        self.minus_hover = False
        self.plus_hover = False

    def draw(self, win):
        # Draw label
        label = NORMAL_FONT.render("Disks:", True, WHITE)
        win.blit(label, (self.x - 100, self.y + 10))
        
        # Draw value box
        pygame.draw.rect(win, DARK_BLUE, self.value_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.value_rect, 2, border_radius=6)
        value_text = STATS_FONT.render(str(self.value), True, YELLOW)
        win.blit(value_text, (self.x + 30 - value_text.get_width()//2, self.y + 8))
        
        # Draw minus button
        minus_color = LIGHT_RED if self.minus_hover else RED
        pygame.draw.rect(win, minus_color, self.minus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.minus_rect, 2, border_radius=6)
        minus_text = BUTTON_FONT.render("-", True, WHITE)
        win.blit(minus_text, (self.minus_rect.centerx - minus_text.get_width()//2, 
                             self.minus_rect.centery - minus_text.get_height()//2))
        
        # Draw plus button
        plus_color = LIGHT_GREEN if self.plus_hover else GREEN
        pygame.draw.rect(win, plus_color, self.plus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.plus_rect, 2, border_radius=6)
        plus_text = BUTTON_FONT.render("+", True, WHITE)
        win.blit(plus_text, (self.plus_rect.centerx - plus_text.get_width()//2, 
                            self.plus_rect.centery - plus_text.get_height()//2))

    def check_hover(self, pos):
        self.minus_hover = self.minus_rect.collidepoint(pos)
        self.plus_hover = self.plus_rect.collidepoint(pos)
        return self.minus_hover or self.plus_hover

    def handle_click(self, pos):
        if self.minus_rect.collidepoint(pos):
            if self.value > 5:
                self.value -= 1
                return True
        if self.plus_rect.collidepoint(pos):
            if self.value < 10:
                self.value += 1
                return True
        return False

class Disk:
    def __init__(self, size):
        self.size = size
        self.width = 40 + size * 22
        self.height = 30
        self.color = DISK_COLORS[(size - 1) % len(DISK_COLORS)]
        self.shadow_offset = 4

    def draw(self, win, x, y, is_selected=False):
        # Draw shadow
        pygame.draw.rect(win, (20, 20, 20), 
                        (x - self.width//2 + self.shadow_offset, y + self.shadow_offset, 
                         self.width, self.height), 
                        border_radius=6)
        
        # Draw disk
        disk_color = self._lighten_color(self.color, 30) if is_selected else self.color
        pygame.draw.rect(win, disk_color, 
                        (x - self.width//2, y, self.width, self.height), 
                        border_radius=6)
        
        # Draw border
        border_color = YELLOW if is_selected else BLACK
        border_width = 3 if is_selected else 2
        pygame.draw.rect(win, border_color, 
                        (x - self.width//2, y, self.width, self.height), 
                        border_width, border_radius=6)
        
        # Draw disk number
        if self.size <= 8:
            number_color = BLACK if disk_color[0] > 150 else WHITE
            number = SMALL_FONT.render(str(self.size), True, number_color)
            win.blit(number, (x - number.get_width()//2, y + (self.height - number.get_height())//2))

    def _lighten_color(self, color, amount):
        return tuple(min(255, c + amount) for c in color)

class TowerUI:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.peg_height = 350
        self.base_width = 200
        self.highlighted = False
        self.hover_color = (255, 255, 255, 30)

    def draw(self, win):
        # Draw highlight if hovered
        if self.highlighted:
            highlight_rect = pygame.Rect(self.x - self.base_width//2, 
                                        self.y - self.peg_height, 
                                        self.base_width, 
                                        self.peg_height + 20)
            pygame.draw.rect(win, self.hover_color, highlight_rect, border_radius=8)
        
        # Draw base with shadow
        pygame.draw.rect(win, (20, 20, 20), 
                        (self.x - self.base_width//2 + 3, self.y + 3, 
                         self.base_width, 15),
                        border_radius=4)
        pygame.draw.rect(win, BLACK, 
                        (self.x - self.base_width//2, self.y, self.base_width, 15),
                        border_radius=4)
        
        # Draw peg with shadow
        pygame.draw.rect(win, (20, 20, 20), 
                        (self.x - 8 + 2, self.y - self.peg_height + 2, 
                         16, self.peg_height))
        pygame.draw.rect(win, BLACK, 
                        (self.x - 8, self.y - self.peg_height, 16, self.peg_height))
        
        # Draw label
        label_text = HEADER_FONT.render(self.label, True, YELLOW)
        win.blit(label_text, (self.x - label_text.get_width()//2, self.y + 25))

    def get_click_rect(self):
        return pygame.Rect(self.x - self.base_width//2, 
                          self.y - self.peg_height, 
                          self.base_width, 
                          self.peg_height + 20)

class ScoresPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.scores = []
        self.last_update = 0
        self.update_interval = 30000  # 30 seconds
        self.error_message = ""
        
    def update_scores(self):
        """Fetch latest scores from Firebase"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update > self.update_interval:
            try:
                self.scores = firebase.get_high_scores(limit=5)
                self.error_message = ""
                self.last_update = current_time
            except Exception as e:
                error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
                self.error_message = "No scores available"
                self.scores = []
    
    def draw(self, win):
        # Draw panel background
        pygame.draw.rect(win, (40, 40, 65), self.rect, border_radius=12)
        pygame.draw.rect(win, PANEL_BORDER, self.rect, 3, border_radius=12)
        
        # Draw title
        title = HEADER_FONT.render("Top Scores", True, YELLOW)
        win.blit(title, (self.rect.x + 20, self.rect.y + 15))
        
        # Update scores if needed
        try:
            self.update_scores()
        except:
            self.scores = []
            self.error_message = "Error fetching scores"
        
        # Draw Firebase status
        status_text = "Online" if FIREBASE_AVAILABLE else "Offline"
        status_color = GREEN if FIREBASE_AVAILABLE else RED
        status = SMALL_FONT.render(f"Status: {status_text}", True, status_color)
        win.blit(status, (self.rect.x + 20, self.rect.y + 45))
        
        # Draw scores or error message
        y = self.rect.y + 80
        if self.error_message:
            error_text = SMALL_FONT.render(self.error_message, True, RED)
            win.blit(error_text, (self.rect.x + 20, y))
            y += 30
            help_text = SMALL_FONT.render("Play to add first score!", True, YELLOW)
            win.blit(help_text, (self.rect.x + 20, y))
        elif not self.scores:
            no_scores = NORMAL_FONT.render("No scores yet!", True, WHITE)
            win.blit(no_scores, (self.rect.centerx - no_scores.get_width()//2, 
                                self.rect.centery))
        else:
            for i, score in enumerate(self.scores[:5]):
                player = score.get('player_name', 'Anonymous')[:15]
                moves = score.get('num_moves', 0)
                disks = score.get('num_disks', 3)
                
                # Different colors for top 3
                if i == 0:
                    color = YELLOW
                elif i == 1:
                    color = LIGHT_GRAY
                elif i == 2:
                    color = ORANGE
                else:
                    color = WHITE
                
                # Format: "1. Player (7 moves, 3 disks)"
                score_text = f"{i+1}. {player} ({moves} moves, {disks} disks)"
                text_surface = NORMAL_FONT.render(score_text, True, color)
                win.blit(text_surface, (self.rect.x + 20, y))
                y += 35

class GameUI:
    def __init__(self):
        self.game = HanoiLogic(game_mode="interactive")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Algorithm helper (modified to handle 3/4 pegs)
        self.algorithm_helper = AlgorithmHelper(self.game.num_disks, self.game.num_pegs)
        self.showing_solution = False
        self.solution_step = 0
        
        # Player information
        self.player_name = ""
        self.name_dialog = NameInputDialog(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
        self.show_name_dialog = True
        self.score_saved = False
        
        # Define layout areas
        self.left_panel = Panel(20, 20, 280, 450, "Game Stats")
        self.center_area = pygame.Rect(320, 150, 800, 500)
        self.right_panel = Panel(WIDTH - 320, 20, 300, 560, "Controls")
        
        # Mode selection buttons
        self.interactive_btn = Button(self.right_panel.rect.x + 30, 100, 240, 50, 
                                     "Interactive Mode", GREEN, WHITE)
        self.sequence_btn = Button(self.right_panel.rect.x + 30, 160, 240, 50, 
                                  "Sequence Mode", BLUE, WHITE)
        self.interactive_btn.active = True
        
        # Control buttons
        self.reset_btn = Button(self.right_panel.rect.x + 30, 230, 115, 45, "New Game", CYAN)
        self.undo_btn = Button(self.right_panel.rect.x + 155, 230, 115, 45, "Undo", PURPLE)
        
        # Algorithm buttons
        self.hint_btn = Button(self.right_panel.rect.x + 30, 290, 115, 45, "Get Hint", ORANGE)
        self.auto_solve_btn = Button(self.right_panel.rect.x + 155, 290, 115, 45, "Auto-Step", PURPLE)
        self.show_solution_btn = Button(self.right_panel.rect.x + 30, 345, 240, 45, "Show Solution", DARK_GREEN)
        
        # Algorithm selector
        self.iterative_algo_btn = Button(self.right_panel.rect.x + 30, 400, 115, 45, "Iterative", LIGHT_BLUE)
        self.recursive_algo_btn = Button(self.right_panel.rect.x + 155, 400, 115, 45, "Recursive", LIGHT_PURPLE)
        self.iterative_algo_btn.active = True  # Default algorithm
        
        # Sequence mode controls
        self.validate_btn = Button(self.right_panel.rect.x + 30, 455, 115, 45, "Validate", GREEN)
        self.execute_btn = Button(self.right_panel.rect.x + 155, 455, 115, 45, "Execute", BLUE)
        self.example_btn = Button(self.right_panel.rect.x + 30, 510, 240, 45, "Show Example", ORANGE)
        
        # Input boxes
        self.num_moves_box = InputBox(self.right_panel.rect.x + 30, 565, 240, 45, "Number of moves:")
        self.moves_box = InputBox(self.right_panel.rect.x + 30, 630, 240, 45, "Move sequence (e.g., AB AC):")
        
        # Scores panel
        self.scores_panel = ScoresPanel(WIDTH - 320, HEIGHT - 250, 300, 200)
        
        # Selectors
        self.peg_selector = PegSelector(150, 300)
        self.disk_selector = DiskSelector(150, 380)
        
        # Create towers
        self.towers_ui = {}
        self.update_towers_ui()
        
        # Game state
        self.dragging_disk = None
        self.hovered_peg = None
        
        # Undo stack
        self.undo_stack = []
        self.save_state()
        
        # Animation variables
        self.particle_system = ParticleSystem()
        
        # Solution display
        self.solution_display = []
        self.current_hint = None

    def update_towers_ui(self):
        """Update tower positions based on number of pegs"""
        num_pegs = self.game.num_pegs
        spacing = 800 // (num_pegs + 1)
        base_y = HEIGHT - 180
        
        self.towers_ui = {}
        for i, label in enumerate(self.game.tower_labels):
            x = 150 + spacing * (i + 1)
            self.towers_ui[label] = TowerUI(x, base_y, label)
        
        # Update algorithm helper with new peg count
        self.algorithm_helper.set_num_pegs(num_pegs)

    def save_state(self):
        """Save current game state"""
        state = {
            'towers': {k: v.copy() for k, v in self.game.towers.items()},
            'move_count': self.game.move_count,
            'game_state': self.game.game_state
        }
        self.undo_stack.append(state)
        if len(self.undo_stack) > 10:
            self.undo_stack.pop(0)

    def undo(self):
        """Undo last move"""
        if len(self.undo_stack) > 1:
            self.undo_stack.pop()
            prev_state = self.undo_stack[-1]
            
            self.game.towers = {k: v.copy() for k, v in prev_state['towers'].items()}
            self.game.move_count = prev_state['move_count']
            self.game.game_state = prev_state['game_state']
            self.game.message = "Undone last move"
            return True
        return False

    def save_score_to_firebase(self):
        """Save the current game score to Firebase"""
        if not self.player_name:
            self.player_name = "Anonymous"
            
        # Get game details
        num_disks = self.game.num_disks
        num_moves = self.game.move_count
        optimal_moves = self.game.get_min_moves()
        game_mode = self.game.game_mode
        
        # Get move sequence for sequence mode
        move_sequence = ""
        if game_mode == "sequence" and hasattr(self.game, 'user_moves_input'):
            move_sequence = self.game.user_moves_input
        
        # Save to Firebase
        try:
            success = firebase.save_player_score(
                player_name=self.player_name,
                num_disks=num_disks,
                num_moves=num_moves,
                optimal_moves=optimal_moves,
                game_mode=game_mode,
                move_sequence=move_sequence,
                is_correct=(self.game.game_state == "win")
            )
            
            if success:
                self.score_saved = True
                self.game.message = "Score saved!"
                print(f"Score saved for {self.player_name}")
            else:
                self.game.message = "Failed to save score"
                print("Could not save score")
            return success
        except Exception as e:
            error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
            self.game.message = "Error saving score"
            print(f"Error: {error_msg[:100]}")
            return False

    def draw_stats(self):
        """Draw game statistics in left panel"""
        # Draw panel
        self.left_panel.draw(WIN)
        
        # Calculate optimal moves based on peg count
        num_pegs = self.game.num_pegs
        num_disks = self.game.num_disks
        
        if num_pegs == 4:
            # 4-peg optimal moves
            optimal_4peg = {1: 1, 2: 3, 3: 5, 4: 9, 5: 13, 6: 17, 7: 25, 8: 33}
            optimal_moves = optimal_4peg.get(num_disks, "?")
        else:
            # 3-peg optimal moves (2^n - 1)
            optimal_moves = (1 << num_disks) - 1
        
        stats = [
            ("DISKS:", str(self.game.num_disks), YELLOW),
            ("PEGS:", str(self.game.num_pegs), LIGHT_CYAN if num_pegs == 4 else CYAN),
            ("MOVES:", str(self.game.move_count), WHITE),
            ("OPTIMAL:", str(optimal_moves), GREEN),
            ("MODE:", self.game.game_mode.title(), 
             GREEN if self.game.game_mode == "interactive" else BLUE),
            ("STATUS:", self.game.game_state.title(), 
             GREEN if self.game.game_state == "win" else 
             YELLOW if self.game.game_state == "playing" else 
             CYAN)
        ]
        
        x, y = 50, 80
        for label, value, color in stats:
            # Draw label
            label_surface = NORMAL_FONT.render(label, True, WHITE)
            WIN.blit(label_surface, (x, y))
            
            # Draw value
            value_surface = STATS_FONT.render(value, True, color)
            WIN.blit(value_surface, (x + 150, y - 5))
            
            y += 35

    def draw_towers(self):
        """Draw all towers and disks"""
        for label, tower in self.towers_ui.items():
            tower.draw(WIN)
            
            # Draw disks on this tower
            x = tower.x
            base_y = tower.y - 20
            disks = self.game.towers[label]
            
            for i, disk_size in enumerate(disks):
                disk = Disk(disk_size)
                is_selected = (self.game.selected_peg == label and 
                              i == len(disks) - 1 and 
                              self.game.selected_disk == disk_size)
                disk.draw(WIN, x, base_y - i * 32, is_selected)

    def draw_controls(self):
        """Draw right control panel"""
        self.right_panel.draw(WIN)
        
        # Draw algorithm info
        algo_info = self.algorithm_helper.get_algorithm_explanation()
        algo_text = SMALL_FONT.render(f"Algorithm: {algo_info['current_algorithm'].title()}", 
                                     True, YELLOW if algo_info['current_algorithm'].startswith('iterative') else LIGHT_PURPLE)
        WIN.blit(algo_text, (self.right_panel.rect.x + 30, 70))
        
        # Draw mode instructions
        if self.game.game_mode == "interactive":
            instructions = [
                "INTERACTIVE MODE",
                "Click disks to move",
                "or use algorithm",
                "buttons for help.",
                "",
                "Algorithm Features:",
                "• Get Hint - Shows next",
                "  optimal move",
                "• Auto-Step - Executes",
                "  one optimal move",
                "• Show Solution - Shows",
                "  full optimal solution"
            ]
            color = GREEN
        else:
            instructions = [
                "SEQUENCE MODE",
                "Enter move sequence",
                "and test if it solves",
                "the puzzle.",
                "",
                "Format:",
                "Number: 7",
                "Moves: AB AC BC",
                "",
                "Peg Labels:",
                " ".join(self.game.tower_labels)
            ]
            color = BLUE
        
        # Draw instructions
        x, y = self.right_panel.rect.x + 30, 460 if self.game.game_mode == "interactive" else 580
        for i, line in enumerate(instructions):
            if i == 0:
                font = BUTTON_FONT
                line_color = color
            else:
                font = SMALL_FONT
                line_color = WHITE
            
            text = font.render(line, True, line_color)
            WIN.blit(text, (x, y))
            y += 22 if i == 0 else 18

    def draw_message(self):
        """Draw game message at bottom"""
        messages = []
        
        # Main game message
        if self.game.message:
            messages.append((self.game.message, YELLOW))
        
        # Hint message
        if self.current_hint:
            messages.append((f"Current hint: Move {self.current_hint[0]} → {self.current_hint[1]}", CYAN))
        
        # Algorithm info
        if self.showing_solution:
            total_moves = len(self.solution_display)
            if self.solution_step < total_moves:
                move = self.solution_display[self.solution_step]
                messages.append((f"Solution step {self.solution_step+1}/{total_moves}: {move[0]} → {move[1]}", GREEN))
            else:
                messages.append(("Solution complete! Press ESC to return.", GREEN))
        
        # Draw all messages
        y_offset = HEIGHT - 30
        for msg_text, color in reversed(messages):
            msg_surface = NORMAL_FONT.render(msg_text, True, color)
            msg_rect = msg_surface.get_rect(center=(WIDTH//2, y_offset))
            
            # Draw background
            bg_rect = msg_rect.inflate(40, 15)
            pygame.draw.rect(WIN, (40, 40, 70, 200), bg_rect, border_radius=10)
            pygame.draw.rect(WIN, color, bg_rect, 2, border_radius=10)
            
            WIN.blit(msg_surface, msg_rect)
            y_offset -= 40
            
        # Draw score saved message
        if self.score_saved:
            score_msg = "Score saved to database!"
            score_surface = NORMAL_FONT.render(score_msg, True, GREEN)
            score_rect = score_surface.get_rect(center=(WIDTH//2, HEIGHT - 70))
            
            # Draw background
            score_bg = score_rect.inflate(40, 15)
            pygame.draw.rect(WIN, (40, 70, 40, 200), score_bg, border_radius=10)
            pygame.draw.rect(WIN, GREEN, score_bg, 2, border_radius=10)
            
            WIN.blit(score_surface, score_rect)

    def draw_solution_display(self):
        """Draw the solution step-by-step display"""
        if not self.showing_solution:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        WIN.blit(overlay, (0, 0))
        
        # Draw solution panel
        panel_rect = pygame.Rect(WIDTH//2 - 300, HEIGHT//2 - 200, 600, 400)
        pygame.draw.rect(WIN, PANEL_BG, panel_rect, border_radius=20)
        pygame.draw.rect(WIN, GREEN, panel_rect, 4, border_radius=20)
        
        # Draw title
        title = HEADER_FONT.render("OPTIMAL SOLUTION", True, YELLOW)
        WIN.blit(title, (panel_rect.centerx - title.get_width()//2, panel_rect.y + 20))
        
        # Draw algorithm info
        algo_type = "Iterative" if self.iterative_algo_btn.active else "Recursive"
        num_pegs = self.game.num_pegs
        optimal_moves = len(self.solution_display)
        
        algo_text = NORMAL_FONT.render(f"Algorithm: {algo_type} | Pegs: {num_pegs} | Disks: {self.game.num_disks} | Optimal moves: {optimal_moves}", 
                                      True, CYAN)
        WIN.blit(algo_text, (panel_rect.centerx - algo_text.get_width()//2, panel_rect.y + 60))
        
        # Draw moves
        x, y = panel_rect.x + 30, panel_rect.y + 100
        moves_per_column = 15
        column_width = 180
        
        for i, move in enumerate(self.solution_display):
            if i >= self.solution_step:
                color = LIGHT_GRAY
            else:
                color = GREEN
                
            move_text = f"{i+1:3d}. {move[0]} → {move[1]}"
            if i == self.solution_step:
                move_text = f"> {move_text} <"
                color = YELLOW
                
            text_surface = NORMAL_FONT.render(move_text, True, color)
            
            column = i // moves_per_column
            row = i % moves_per_column
            
            WIN.blit(text_surface, (x + column * column_width, y + row * 25))
        
        # Draw instructions
        instructions = [
            "Press SPACE for next move",
            "Press ENTER to auto-solve all",
            "Press ESC to exit solution view"
        ]
        
        y = panel_rect.y + panel_rect.height - 80
        for i, line in enumerate(instructions):
            inst_text = SMALL_FONT.render(line, True, WHITE)
            WIN.blit(inst_text, (panel_rect.centerx - inst_text.get_width()//2, y + i * 25))

    def draw_win_message(self):
        """Draw win celebration message"""
        if self.game.game_state == "win" and not self.showing_solution:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            WIN.blit(overlay, (0, 0))
            
            # Draw win message
            win_text = HEADER_FONT.render("PUZZLE SOLVED!", True, GREEN)
            win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            
            # Draw background box
            box_rect = win_rect.inflate(80, 40)
            pygame.draw.rect(WIN, PANEL_BG, box_rect, border_radius=20)
            pygame.draw.rect(WIN, GREEN, box_rect, 4, border_radius=20)
            
            WIN.blit(win_text, win_rect)
            
            # Draw move count
            moves_text = NORMAL_FONT.render(f"Moves: {self.game.move_count}", 
                                          True, YELLOW)
            moves_rect = moves_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 10))
            WIN.blit(moves_text, moves_rect)
            
            # Draw player name
            player_text = NORMAL_FONT.render(f"Player: {self.player_name}", True, CYAN)
            player_rect = player_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            WIN.blit(player_text, player_rect)
            
            # Draw save prompt
            if not self.score_saved:
                save_text = SMALL_FONT.render("Score automatically saved!", True, WHITE)
                save_rect = save_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 90))
                WIN.blit(save_text, save_rect)

    def draw(self):
        # Clear screen with background
        WIN.blit(pygame.image.load("bimage.jpg").convert(), (0, 0))
    
    # Draw name dialog if shown
        if self.show_name_dialog:
            self.name_dialog.draw(WIN)
            pygame.display.flip()
            return
        
        # Draw title
        title = TITLE_FONT.render("TOWER OF HANOI", True, YELLOW)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        # Draw subtitle
        mode_text = "Interactive Mode" if self.game.game_mode == "interactive" else "Sequence Mode"
        subtitle = HEADER_FONT.render(f"{mode_text} | {self.game.num_disks} Disks | {self.game.num_pegs} Pegs", True, WHITE)
        WIN.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 90))
        
        # Draw all components
        self.draw_stats()
        self.draw_towers()
        self.draw_controls()
        self.scores_panel.draw(WIN)
        
        # Draw buttons
        self.interactive_btn.draw(WIN)
        self.sequence_btn.draw(WIN)
        self.reset_btn.draw(WIN)
        self.undo_btn.draw(WIN)
        
        # Always show algorithm buttons
        self.hint_btn.draw(WIN)
        self.auto_solve_btn.draw(WIN)
        self.show_solution_btn.draw(WIN)
        self.iterative_algo_btn.draw(WIN)
        self.recursive_algo_btn.draw(WIN)
        
        if self.game.game_mode == "sequence":
            self.validate_btn.draw(WIN)
            self.execute_btn.draw(WIN)
            self.example_btn.draw(WIN)
            self.num_moves_box.draw(WIN)
            self.moves_box.draw(WIN)
        
        # Draw selectors
        self.peg_selector.draw(WIN)
        self.disk_selector.draw(WIN)
        
        # Draw messages
        self.draw_message()
        
        # Draw solution display if active
        if self.showing_solution:
            self.draw_solution_display()
        else:
            self.draw_win_message()
        
        # Draw particle effects
        self.particle_system.draw(WIN)
        
        # Update display
        pygame.display.flip()

    def update(self):
        """Update animations and effects"""
        # Update name dialog cursor
        if self.show_name_dialog:
            self.name_dialog.update()
        
        # Update button effects
        self.interactive_btn.update()
        self.sequence_btn.update()
        self.reset_btn.update()
        self.undo_btn.update()
        self.hint_btn.update()
        self.auto_solve_btn.update()
        self.show_solution_btn.update()
        self.iterative_algo_btn.update()
        self.recursive_algo_btn.update()
        
        if self.game.game_mode == "sequence":
            self.validate_btn.update()
            self.execute_btn.update()
            self.example_btn.update()
            self.num_moves_box.update()
            self.moves_box.update()
        
        # Update particle system
        self.particle_system.update()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle name dialog first if shown
        if self.show_name_dialog:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                
                if self.name_dialog.handle_event(event):
                    self.player_name = self.name_dialog.name_input.strip()
                    if not self.player_name:
                        self.player_name = "Anonymous"
                    self.show_name_dialog = False
                    print(f"Player: {self.player_name}")
                    return
            
            return
        
        # Handle solution display mode
        if self.showing_solution:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.showing_solution = False
                        self.solution_step = 0
                        self.game.message = "Exited solution view"
                        
                    elif event.key == pygame.K_SPACE:
                        # Next step
                        if self.solution_step < len(self.solution_display):
                            move = self.solution_display[self.solution_step]
                            # Execute the move
                            if hasattr(self.game, 'move_disk'):
                                # Simulate selecting and moving
                                self.game.selected_disk = self.game.get_top_disk(move[0])
                                self.game.selected_peg = move[0]
                                self.game.move_disk(move[1])
                                self.save_state()
                            self.solution_step += 1
                            
                    elif event.key == pygame.K_RETURN:
                        # Auto-solve all remaining steps
                        while self.solution_step < len(self.solution_display):
                            move = self.solution_display[self.solution_step]
                            if hasattr(self.game, 'move_disk'):
                                self.game.selected_disk = self.game.get_top_disk(move[0])
                                self.game.selected_peg = move[0]
                                self.game.move_disk(move[1])
                                self.save_state()
                            self.solution_step += 1
                        
                        if self.game.game_state == "win" and not self.score_saved:
                            self.save_score_to_firebase()
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check if clicked outside solution panel
                        panel_rect = pygame.Rect(WIDTH//2 - 300, HEIGHT//2 - 200, 600, 400)
                        if not panel_rect.collidepoint(mouse_pos):
                            self.showing_solution = False
                            self.solution_step = 0
                            
            return
        
        # Check button hovers
        self.interactive_btn.check_hover(mouse_pos)
        self.sequence_btn.check_hover(mouse_pos)
        self.reset_btn.check_hover(mouse_pos)
        self.undo_btn.check_hover(mouse_pos)
        self.hint_btn.check_hover(mouse_pos)
        self.auto_solve_btn.check_hover(mouse_pos)
        self.show_solution_btn.check_hover(mouse_pos)
        self.iterative_algo_btn.check_hover(mouse_pos)
        self.recursive_algo_btn.check_hover(mouse_pos)
        
        # Check selector hovers
        self.peg_selector.check_hover(mouse_pos)
        self.disk_selector.check_hover(mouse_pos)
        
        if self.game.game_mode == "sequence":
            self.validate_btn.check_hover(mouse_pos)
            self.execute_btn.check_hover(mouse_pos)
            self.example_btn.check_hover(mouse_pos)
        
        # Check peg hovers
        self.hovered_peg = None
        for label, tower in self.towers_ui.items():
            tower.highlighted = False
            if tower.get_click_rect().collidepoint(mouse_pos):
                self.hovered_peg = label
                tower.highlighted = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Mode buttons
                    if self.interactive_btn.is_clicked(mouse_pos):
                        self.game.switch_mode("interactive")
                        self.interactive_btn.active = True
                        self.sequence_btn.active = False
                        self.update_towers_ui()
                        self.game.message = "Switched to Interactive Mode"
                    
                    elif self.sequence_btn.is_clicked(mouse_pos):
                        self.game.switch_mode("sequence")
                        self.interactive_btn.active = False
                        self.sequence_btn.active = True
                        self.update_towers_ui()
                        self.game.message = "Switched to Sequence Mode"
                    
                    # Control buttons
                    elif self.reset_btn.is_clicked(mouse_pos):
                        self.save_state()
                        self.game.reset(num_pegs=self.peg_selector.value, num_disks=self.disk_selector.value)
                        self.algorithm_helper.set_num_disks(self.game.num_disks)
                        self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                        self.update_towers_ui()
                        self.score_saved = False
                        self.current_hint = None
                        self.game.message = "New game started!"
                    
                    elif self.undo_btn.is_clicked(mouse_pos) and self.game.game_mode == "interactive":
                        if self.undo():
                            self.score_saved = False
                            self.current_hint = None
                    
                    # Algorithm buttons
                    elif self.hint_btn.is_clicked(mouse_pos) and self.game.game_mode == "interactive":
                        # Get next hint
                        algorithm = 'iterative' if self.iterative_algo_btn.active else 'recursive'
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        self.current_hint = self.algorithm_helper.get_current_hint()
                        if self.current_hint:
                            self.game.message = f"Hint: Move {self.current_hint[0]} to {self.current_hint[1]}"
                        else:
                            self.game.message = "No more hints available"
                    
                    elif self.auto_solve_btn.is_clicked(mouse_pos) and self.game.game_mode == "interactive":
                        # Execute one auto-solve step
                        algorithm = 'iterative' if self.iterative_algo_btn.active else 'recursive'
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        move = self.algorithm_helper.auto_solve_step()
                        if move:
                            # Execute the move
                            if hasattr(self.game, 'move_disk'):
                                self.save_state()
                                self.game.selected_disk = self.game.get_top_disk(move[0])
                                self.game.selected_peg = move[0]
                                success = self.game.move_disk(move[1])
                                if success:
                                    # Add particles for auto-solve move
                                    for _ in range(10):
                                        self.particle_system.add_particle(
                                            self.towers_ui[move[1]].x,
                                            self.towers_ui[move[1]].y - 100,
                                            color=PURPLE,
                                            speed=2
                                        )
                                    if self.game.game_state == "win" and not self.score_saved:
                                        self.save_score_to_firebase()
                        else:
                            self.game.message = "Auto-solve complete!"
                    
                    elif self.show_solution_btn.is_clicked(mouse_pos):
                        # Show complete solution
                        algorithm = 'iterative' if self.iterative_algo_btn.active else 'recursive'
                        solution = self.algorithm_helper.get_optimal_solution(algorithm)
                        self.solution_display = [(move[0], move[1]) for move in solution]
                        self.solution_step = 0
                        self.showing_solution = True
                        self.game.message = "Showing optimal solution. Press SPACE for next move."
                    
                    elif self.iterative_algo_btn.is_clicked(mouse_pos):
                        self.iterative_algo_btn.active = True
                        self.recursive_algo_btn.active = False
                        self.algorithm_helper.get_optimal_solution('iterative')
                        self.current_hint = None
                        self.game.message = "Using Iterative algorithm"
                    
                    elif self.recursive_algo_btn.is_clicked(mouse_pos):
                        self.iterative_algo_btn.active = False
                        self.recursive_algo_btn.active = True
                        self.algorithm_helper.get_optimal_solution('recursive')
                        self.current_hint = None
                        self.game.message = "Using Recursive algorithm"
                    
                    # Sequence mode buttons
                    elif self.game.game_mode == "sequence":
                        if self.validate_btn.is_clicked(mouse_pos):
                            self.game.validate_sequence(
                                self.num_moves_box.text,
                                self.moves_box.text
                            )
                        
                        elif self.execute_btn.is_clicked(mouse_pos):
                            if hasattr(self.game, 'sequence_validated') and self.game.sequence_validated:
                                success = self.game.execute_sequence()
                                if success:
                                    self.save_state()
                                    # Auto-save score when puzzle is solved
                                    if self.game.game_state == "win" and not self.score_saved:
                                        self.save_score_to_firebase()
                                        # Add celebration particles
                                        for _ in range(50):
                                            self.particle_system.add_particle(
                                                WIDTH//2, HEIGHT//2,
                                                color=YELLOW,
                                                speed=5
                                            )
                        
                        elif self.example_btn.is_clicked(mouse_pos):
                            # Show example solution for current peg count
                            if self.game.num_pegs == 4:
                                # 4-peg examples
                                if self.game.num_disks == 3:
                                    self.num_moves_box.text = "5"
                                    self.moves_box.text = "AC AB AD BD CD"
                                elif self.game.num_disks == 4:
                                    self.num_moves_box.text = "9"
                                    self.moves_box.text = "AB AC BC AB AD BD CA CD AD"
                            else:
                                # 3-peg examples
                                min_moves = self.game.get_min_moves()
                                self.num_moves_box.text = str(min_moves)
                                if self.game.num_disks == 3:
                                    self.moves_box.text = "AB AC BC AB CA CB AB"
                                elif self.game.num_disks == 4:
                                    self.moves_box.text = "AB AC BC AB CA CB AB AC BC BA CA BC AB AC BC"
                                elif self.game.num_disks == 5:
                                    self.moves_box.text = "AB AC BC AB CA CB AB AC BC BA CA BC AB AC BC AB CA CB AB AC BC BA CA BC AB AC BC AB"
                    
                    # Selectors
                    elif self.peg_selector.handle_click(mouse_pos):
                        self.save_state()
                        self.game.reset(num_pegs=self.peg_selector.value, num_disks=self.disk_selector.value)
                        self.algorithm_helper.set_num_disks(self.game.num_disks)
                        self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                        self.update_towers_ui()
                        self.score_saved = False
                        self.current_hint = None
                        self.game.message = f"Changed to {self.peg_selector.value} pegs"
                    
                    elif self.disk_selector.handle_click(mouse_pos):
                        self.save_state()
                        self.game.reset(num_pegs=self.peg_selector.value, num_disks=self.disk_selector.value)
                        self.algorithm_helper.set_num_disks(self.game.num_disks)
                        self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                        self.update_towers_ui()
                        self.score_saved = False
                        self.current_hint = None
                        self.game.message = f"Changed to {self.disk_selector.value} disks"
                    
                    # Disk dragging (interactive mode only)
                    elif self.game.game_mode == "interactive" and self.game.game_state == "playing":
                        for label, tower in self.towers_ui.items():
                            x = tower.x
                            base_y = tower.y - 20
                            disks = self.game.towers[label]
                            
                            for j, disk_size in enumerate(reversed(disks)):
                                actual_index = len(disks) - 1 - j
                                disk = Disk(disk_size)
                                disk_rect = pygame.Rect(x - disk.width//2, 
                                                       base_y - actual_index * 32,
                                                       disk.width, disk.height)
                                
                                if disk_rect.collidepoint(mouse_pos) and \
                                   hasattr(self.game, 'can_select_disk') and \
                                   self.game.can_select_disk(label, actual_index):
                                    self.save_state()
                                    if hasattr(self.game, 'select_disk'):
                                        self.game.select_disk(label)
                                        self.current_hint = None
                                    break
                            else:
                                continue
                            break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.game.game_mode == "interactive":
                    if self.hovered_peg and hasattr(self.game, 'selected_peg') and self.game.selected_peg:
                        self.save_state()
                        if hasattr(self.game, 'move_disk'):
                            success = self.game.move_disk(self.hovered_peg)
                            if success:
                                # Add particles for successful move
                                for _ in range(10):
                                    self.particle_system.add_particle(
                                        self.towers_ui[self.hovered_peg].x,
                                        self.towers_ui[self.hovered_peg].y - 100,
                                        color=GREEN,
                                        speed=2
                                    )
                                if self.game.game_state == "win" and not self.score_saved:
                                    # Auto-save score when puzzle is solved
                                    self.save_score_to_firebase()
                                self.current_hint = None
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.showing_solution:
                        self.showing_solution = False
                        self.solution_step = 0
                        self.game.message = "Exited solution view"
                    elif hasattr(self.game, 'selected_disk') and self.game.selected_disk:
                        if hasattr(self.game, 'cancel_selection'):
                            self.game.cancel_selection()
                            self.current_hint = None
                
                elif event.key == pygame.K_r:
                    self.save_state()
                    self.game.reset(num_pegs=self.peg_selector.value, num_disks=self.disk_selector.value)
                    self.algorithm_helper.set_num_disks(self.game.num_disks)
                    self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                    self.update_towers_ui()
                    self.score_saved = False
                    self.current_hint = None
                    self.game.message = "Game reset!"
                
                elif event.key == pygame.K_u and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if self.game.game_mode == "interactive":
                        if self.undo():
                            self.score_saved = False
                            self.current_hint = None
                
                elif event.key == pygame.K_m:
                    new_mode = "sequence" if self.game.game_mode == "interactive" else "interactive"
                    if hasattr(self.game, 'switch_mode'):
                        self.game.switch_mode(new_mode)
                    self.interactive_btn.active = (new_mode == "interactive")
                    self.sequence_btn.active = (new_mode == "sequence")
                    self.update_towers_ui()
                    self.game.message = f"Switched to {new_mode} mode"
                    self.current_hint = None
                
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Manual save with Ctrl+S
                    if self.game.move_count > 0:
                        self.save_score_to_firebase()
                        self.game.message = "Score saved manually!"
                
                elif event.key == pygame.K_h:
                    # Show hint
                    if self.game.game_mode == "interactive":
                        algorithm = 'iterative' if self.iterative_algo_btn.active else 'recursive'
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        self.current_hint = self.algorithm_helper.get_current_hint()
                        if self.current_hint:
                            self.game.message = f"Hint: Move {self.current_hint[0]} to {self.current_hint[1]}"
                
                elif event.key == pygame.K_a:
                    # Auto-solve step
                    if self.game.game_mode == "interactive":
                        algorithm = 'iterative' if self.iterative_algo_btn.active else 'recursive'
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        move = self.algorithm_helper.auto_solve_step()
                        if move:
                            self.save_state()
                            self.game.selected_disk = self.game.get_top_disk(move[0])
                            self.game.selected_peg = move[0]
                            success = self.game.move_disk(move[1])
                            if success and self.game.game_state == "win" and not self.score_saved:
                                self.save_score_to_firebase()
                
                elif event.key == pygame.K_i:
                    # Switch to iterative algorithm
                    self.iterative_algo_btn.active = True
                    self.recursive_algo_btn.active = False
                    self.algorithm_helper.get_optimal_solution('iterative')
                    self.current_hint = None
                    self.game.message = "Using Iterative algorithm"
                
                elif event.key == pygame.K_c:
                    # Switch to recursive algorithm
                    self.iterative_algo_btn.active = False
                    self.recursive_algo_btn.active = True
                    self.algorithm_helper.get_optimal_solution('recursive')
                    self.current_hint = None
                    self.game.message = "Using Recursive algorithm"
                
                elif event.key == pygame.K_v:
                    # Show solution view
                    algorithm = 'iterative' if self.iterative_algo_btn.active else 'recursive'
                    solution = self.algorithm_helper.get_optimal_solution(algorithm)
                    self.solution_display = [(move[0], move[1]) for move in solution]
                    self.solution_step = 0
                    self.showing_solution = True
                    self.game.message = "Showing optimal solution. Press SPACE for next move."
                
                elif event.key == pygame.K_p:
                    # Toggle between 3 and 4 pegs
                    new_pegs = 4 if self.game.num_pegs == 3 else 3
                    self.peg_selector.value = new_pegs
                    self.save_state()
                    self.game.reset(num_pegs=new_pegs, num_disks=self.disk_selector.value)
                    self.algorithm_helper.set_num_disks(self.game.num_disks)
                    self.algorithm_helper.set_num_pegs(new_pegs)
                    self.update_towers_ui()
                    self.score_saved = False
                    self.current_hint = None
                    self.game.message = f"Changed to {new_pegs} pegs"
                
                elif event.key == pygame.K_F1:
                    # Show help
                    self.game.message = "Help: R=Reset, Ctrl+Z=Undo, M=Toggle Mode, H=Hint, A=Auto-step, I/C=Algorithm, V=Solution, P=Toggle Pegs, F1=Help"
            
            # Handle input box events
            if self.game.game_mode == "sequence":
                self.num_moves_box.handle_event(event)
                self.moves_box.handle_event(event)

    def run(self):
        print("Starting Tower of Hanoi Game with 3 & 4 Peg Algorithm Features")
        print(f"Firebase available: {FIREBASE_AVAILABLE}")
        print("Algorithm Features:")
        print("  * 3-Peg (default) and 4-Peg solvers")
        print("  * Get Hint (H key or Hint button)")
        print("  * Auto-Solve Step (A key or Auto-Step button)")
        print("  * Show Solution (V key or Show Solution button)")
        print("  * Toggle Algorithm: Iterative (I) / Recursive (C)")
        print("  * Toggle Pegs: 3-Peg <-> 4-Peg (P key)")
        print("  * Solution View with step-by-step execution")
        
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()
class ParticleSystem:
    """Simple particle system for visual effects"""
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, color=WHITE, speed=3, lifetime=60):
        self.particles.append({
            'x': x,
            'y': y,
            'vx': (pygame.time.get_ticks() % 10 - 5) * 0.5,
            'vy': -speed - (pygame.time.get_ticks() % 10) * 0.1,
            'color': color,
            'lifetime': lifetime,
            'size': pygame.time.get_ticks() % 5 + 2
        })
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.1  # Gravity
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, win):
        for particle in self.particles:
            alpha = min(255, particle['lifetime'] * 4)
            color = (*particle['color'][:3], alpha)
            size = particle['size']
            pygame.draw.circle(win, color, 
                             (int(particle['x']), int(particle['y'])), 
                             size)

def main():
    game_ui = GameUI()
    game_ui.run()

if __name__ == "__main__":
    main() 