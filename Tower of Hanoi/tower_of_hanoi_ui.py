import os
import pygame
import sys
from datetime import datetime
import threading
import queue

from game_logic import HanoiLogic
from four_peg_iterative import FourPegSolver
from four_peg_recursive import FourPegRecursiveSolver
from iterative_solver import IterativeSolver, solve_iteratively
from recursive_solver import RecursiveSolver, solve_recursively
os.environ['GRPC_DNS_RESOLVER'] = 'native' 

class FirebaseManager:
    """Thread-safe Firebase manager to prevent freezing"""
    def __init__(self):
        self.scores = []
        self.connected = False
        self.error_message = ""
        self.last_update = 0
        self.update_interval = 30000  # 30 seconds
        
        # Thread-safe queues for operations
        self.score_queue = queue.Queue()
        self.save_queue = queue.Queue()
        self.result_queue = queue.Queue()
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        
        # Try to initialize Firebase
        self._init_firebase()
    
    def _init_firebase(self):
        """Initialize Firebase in background"""
        try:
            from firebase_handler import FirebaseHandler
            
            class SafeFirebaseHandler(FirebaseHandler):
                def __init__(self, *args, **kwargs):
                    try:
                        super().__init__(*args, **kwargs)
                        self._connected = True
                        print("[OK] Firebase initialized successfully!")
                    except Exception as e:
                        print(f"[WARNING] Firebase init warning: {str(e)[:100]}")
                        self._connected = False
                
                def is_connected(self):
                    return getattr(self, '_connected', False)
                
                def get_high_scores_safe(self, limit=5):
                    """Safe score fetching"""
                    try:
                        if not self.is_connected():
                            return []
                        
                        # Use the same collection name as firebase_handler.py
                        collection_name = 'hanoi_scores' 
                        
                        try:
                            # Get scores from Firebase
                            scores = super().get_high_scores(limit=limit)
                            print(f"[DEBUG] Retrieved {len(scores)} scores from Firebase")
                            return scores
                        except Exception as e:
                            print(f"[DEBUG] Error reading from {collection_name}: {str(e)[:100]}")
                            return []
                        
                    except Exception as e:
                        print(f"[DEBUG] Error in get_high_scores_safe: {str(e)[:100]}")
                        return []
                
                def save_player_score_safe(self, **kwargs):
                    """Safe score saving"""
                    try:
                        if not self.is_connected():
                            print("[DEBUG] Firebase not connected")
                            return False
                        
                        # Call the parent class method
                        success = super().save_player_score(**kwargs)
                        print(f"[DEBUG] Save result from FirebaseHandler: {success}")
                        return success
                        
                    except Exception as e:
                        print(f"[DEBUG] Error in save_player_score_safe: {str(e)[:100]}")
                        return False
            
            # Initialize the handler
            self.firebase = SafeFirebaseHandler()
            self.connected = self.firebase.is_connected()
            
            # Debug output
            print(f"[DEBUG] Firebase connected: {self.connected}")
            
        except (ImportError, Exception) as e:
            print(f"[INFO] Firebase not available: {str(e)[:100]}")
            
            # Fallback to dummy handler
            class DummyFirebaseHandler:
                def is_connected(self):
                    return False
                def get_high_scores_safe(self, limit=5):
                    return []
                def save_player_score_safe(self, **kwargs):
                    print("[DEBUG] Dummy handler: Pretending to save score")
                    return True
            
            self.firebase = DummyFirebaseHandler()
            self.connected = False
    
    def _worker(self):
        """Background worker thread for Firebase operations"""
        while True:
            try:
                # Check for score fetch requests
                if not self.score_queue.empty():
                    try:
                        limit = self.score_queue.get_nowait()
                        scores = self.firebase.get_high_scores_safe(limit)
                        self.scores = scores
                        self.error_message = ""
                        self.last_update = pygame.time.get_ticks()
                        print(f"[DEBUG] Worker updated scores: {len(scores)} items")
                    except Exception as e:
                        self.error_message = "Error fetching scores"
                        print(f"[DEBUG] Worker error fetching scores: {str(e)[:100]}")
                
                # Check for save requests
                if not self.save_queue.empty():
                    try:
                        kwargs = self.save_queue.get_nowait()
                        print(f"[DEBUG] Worker processing save for: {kwargs.get('player_name', 'Anonymous')}")
                        success = self.firebase.save_player_score_safe(**kwargs)
                        self.result_queue.put(success)
                        print(f"[DEBUG] Worker save result: {success}")
                    except Exception as e:
                        print(f"[DEBUG] Worker error saving score: {str(e)[:100]}")
                        self.result_queue.put(False)
                
                # Sleep to prevent busy waiting
                threading.Event().wait(0.1)
                
            except queue.Empty:
                threading.Event().wait(0.1)
            except Exception as e:
                print(f"[DEBUG] Worker thread error: {str(e)[:100]}")
                threading.Event().wait(0.5)
    
    def get_high_scores(self, limit=5):
        """Thread-safe score fetching"""
        # Return cached scores if recent
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update < 5000:  # 5 second cache
            return self.scores[:limit]
        
        # Request update from worker thread
        if self.connected:
            self.score_queue.put(limit)
        return self.scores[:limit]  # Return cached while waiting
    
    def save_player_score(self, **kwargs):
        """Thread-safe score saving"""
        print(f"[DEBUG] Queueing score save for: {kwargs.get('player_name', 'Anonymous')}")
        if self.connected:
            self.save_queue.put(kwargs)
            return True
        else:
            print("[DEBUG] Firebase not connected, saving locally")
            return False
    
    def is_connected(self):
        """Check connection status"""
        return self.connected
  
# Initialize Firebase manager
firebase_manager = FirebaseManager()

pygame.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi with 3 & 4 Peg Algorithm Features")

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

TITLE_FONT = pygame.font.SysFont("arial", 52, bold=True)
HEADER_FONT = pygame.font.SysFont("arial", 20, bold=True)
BUTTON_FONT = pygame.font.SysFont("arial", 15, bold=True)
NORMAL_FONT = pygame.font.SysFont("arial", 15)
SMALL_FONT = pygame.font.SysFont("arial", 15)
STATS_FONT = pygame.font.SysFont("arial", 15, bold=True)
LARGE_FONT = pygame.font.SysFont("arial", 32, bold=True)

DISK_COLORS = [
    (255, 80, 80),
    (255, 140, 80),
    (255, 200, 80),
    (80, 255, 80),
    (80, 255, 200),
    (80, 180, 255),
    (180, 80, 255),
    (255, 80, 180),
    (255, 120, 120),
    (255, 180, 120),
    (255, 220, 120),
    (120, 255, 120),
]

class AlgorithmHelper:
    """Helper class to integrate solver algorithms with the game"""
    def __init__(self, num_disks=3, num_pegs=3):
        self.num_disks = num_disks
        self.num_pegs = num_pegs
        self.optimal_solution = None
        self.current_move_index = 0
        self.algorithm_type = 'iterative'
        self.peg_type = '3peg'

    def set_num_disks(self, num_disks):
        self.num_disks = num_disks
        self.reset_solution()

    def set_num_pegs(self, num_pegs):
        self.num_pegs = num_pegs
        self.peg_type = '4peg' if num_pegs == 4 else '3peg'
        self.reset_solution()

    def reset_solution(self):
        self.optimal_solution = None
        self.current_move_index = 0

    def get_optimal_solution(self, algorithm='iterative'):
        """Get optimal solution using specified algorithm (cached)."""
        if self.optimal_solution is not None and self.algorithm_type == algorithm:
            return self.optimal_solution

        self.algorithm_type = algorithm

        if self.num_pegs == 4:
            if algorithm == 'iterative':
                solver = FourPegSolver(self.num_disks, ['A', 'B', 'C', 'D'])
            else:
                solver = FourPegRecursiveSolver(self.num_disks, ['A', 'B', 'C', 'D'])
        else:
            if algorithm == 'iterative':
                solver = IterativeSolver(self.num_disks, 'A', 'C', 'B')
            else:
                solver = RecursiveSolver(self.num_disks, 'A', 'C', 'B')

        solver.solve()

        if self.num_pegs == 4:
            self.optimal_solution = solver.moves
        else:
            self.optimal_solution = solver.get_move_sequence()

        self.current_move_index = 0
        return self.optimal_solution

    def get_next_hint(self):
        if not self.optimal_solution:
            self.get_optimal_solution()

        if self.current_move_index < len(self.optimal_solution):
            if self.num_pegs == 4:
                hint = self.optimal_solution[self.current_move_index]
            else:
                hint_str = self.optimal_solution[self.current_move_index]
                hint = (hint_str[0], hint_str[1])
            self.current_move_index += 1
            return hint
        return None

    def get_current_hint(self):
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
        if not self.optimal_solution:
            self.get_optimal_solution()

        if self.current_move_index < len(self.optimal_solution):
            if self.num_pegs == 4:
                move = self.optimal_solution[self.current_move_index]
            else:
                move_str = self.optimal_solution[self.current_move_index]
                move = (move_str[0], move_str[1])
            self.current_move_index += 1
            return move
        return None

    def check_player_solution(self, player_moves):
        optimal = self.get_optimal_solution()
        return len(player_moves) == len(optimal)

    def get_algorithm_explanation(self):
        if self.num_pegs == 4:
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
            return {
                'formula': f'2^{self.num_disks} - 1 = {(1 << self.num_disks) - 1} moves',
                'iterative_pattern': 'AB, AC, BC (odd) or AC, AB, CB (even) pattern',
                'recursive_principle': 'Divide and conquer: move n-1 disks, move nth disk, move n-1 disks',
                'current_algorithm': f"{self.algorithm_type} ({self.peg_type})"
            }

    def get_complete_solution(self):
        if not self.optimal_solution:
            self.get_optimal_solution()

        display_solution = []
        for move in self.optimal_solution:
            if self.num_pegs == 4:
                display_solution.append(move)
            else:
                display_solution.append((move[0], move[1]))
        return display_solution

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
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, win):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        win.blit(overlay, (0, 0))

        pygame.draw.rect(win, (50, 50, 80), self.rect, border_radius=15)
        pygame.draw.rect(win, YELLOW, self.rect, 3, border_radius=15)

        title_text = self.title_font.render(self.title, True, YELLOW)
        win.blit(
            title_text,
            (self.rect.centerx - title_text.get_width() // 2, self.rect.y + 30),
        )

        input_rect = pygame.Rect(
            self.rect.x + 50,
            self.rect.centery - 20,
            self.rect.width - 100,
            50,
        )
        pygame.draw.rect(win, DARK_BLUE, input_rect, border_radius=8)
        pygame.draw.rect(win, WHITE, input_rect, 2, border_radius=8)

        display_text = self.name_input if self.name_input else "Type your name..."
        name_text = self.font.render(
            display_text, True, WHITE if self.name_input else LIGHT_GRAY
        )
        win.blit(
            name_text,
            (
                input_rect.x + 15,
                input_rect.centery - name_text.get_height() // 2,
            ),
        )

        if self.cursor_visible and self.active:
            cursor_x = input_rect.x + 15 + name_text.get_width()
            pygame.draw.line(
                win,
                WHITE,
                (cursor_x, input_rect.y + 10),
                (cursor_x, input_rect.y + input_rect.height - 10),
                2,
            )

        instructions = [
            "Press ENTER to continue",
            "Press ESC to play as Anonymous",
            "Maximum 20 characters",
        ]
        for i, line in enumerate(instructions):
            inst_text = SMALL_FONT.render(line, True, WHITE)
            win.blit(
                inst_text,
                (
                    self.rect.centerx - inst_text.get_width() // 2,
                    self.rect.y + self.rect.height - 80 + i * 25,
                ),
            )


class Panel:
    def __init__(self, x, y, width, height, title="", bg_color=PANEL_BG):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.bg_color = bg_color
        self.has_shadow = True

    def draw(self, win):
        if self.has_shadow:
            shadow_rect = self.rect.move(4, 4)
            pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=12)

        pygame.draw.rect(win, self.bg_color, self.rect, border_radius=12)
        pygame.draw.rect(win, PANEL_BORDER, self.rect, 3, border_radius=12)

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
        if self.has_shadow and not self.click_effect:
            shadow_rect = self.rect.move(3, 3)
            pygame.draw.rect(win, (0, 0, 0, 100), shadow_rect, border_radius=8)

        if self.click_effect:
            color = self._lighten_color(self.color, 60)
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color

        pygame.draw.rect(win, color, self.rect, border_radius=8)
        border_color = YELLOW if self.active else PANEL_BORDER
        border_width = 3 if self.active else 2
        pygame.draw.rect(win, border_color, self.rect, border_width, border_radius=8)

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
        bg_color = self.active_bg_color if self.active else self.bg_color
        pygame.draw.rect(win, bg_color, self.rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.rect, 2, border_radius=6)

        if self.label_surface:
            win.blit(self.label_surface, (self.rect.x, self.rect.y - 25))

        if self.text:
            display_text = self.text if len(self.text) <= 15 else "..." + self.text[-12:]
            text_surface = NORMAL_FONT.render(display_text, True, WHITE)
            win.blit(
                text_surface,
                (self.rect.x + 10, self.rect.y + (self.rect.h - text_surface.get_height()) // 2),
            )
        elif self.active:
            placeholder = "Type here..."
            text_surface = NORMAL_FONT.render(placeholder, True, LIGHT_GRAY)
            win.blit(
                text_surface,
                (self.rect.x + 10, self.rect.y + (self.rect.h - text_surface.get_height()) // 2),
            )

        if self.active and self.cursor_visible:
            text_width = NORMAL_FONT.render(self.text if self.text else "", True, WHITE).get_width()
            cursor_x = self.rect.x + 10 + text_width
            pygame.draw.line(
                win,
                WHITE,
                (cursor_x, self.rect.y + 10),
                (cursor_x, self.rect.y + self.rect.height - 10),
                2,
            )

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
        label = NORMAL_FONT.render("Pegs:", True, WHITE)
        win.blit(label, (self.x - 100, self.y + 10))

        pygame.draw.rect(win, DARK_BLUE, self.value_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.value_rect, 2, border_radius=6)
        value_text = STATS_FONT.render(str(self.value), True, YELLOW)
        win.blit(value_text, (self.x + 30 - value_text.get_width() // 2, self.y + 8))

        minus_color = LIGHT_RED if self.minus_hover else RED
        pygame.draw.rect(win, minus_color, self.minus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.minus_rect, 2, border_radius=6)
        minus_text = BUTTON_FONT.render("-", True, WHITE)
        win.blit(
            minus_text,
            (
                self.minus_rect.centerx - minus_text.get_width() // 2,
                self.minus_rect.centery - minus_text.get_height() // 2,
            ),
        )

        plus_color = LIGHT_GREEN if self.plus_hover else GREEN
        pygame.draw.rect(win, plus_color, self.plus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.plus_rect, 2, border_radius=6)
        plus_text = BUTTON_FONT.render("+", True, WHITE)
        win.blit(
            plus_text,
            (
                self.plus_rect.centerx - plus_text.get_width() // 2,
                self.plus_rect.centery - plus_text.get_height() // 2,
            ),
        )

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
            if self.value < 5:
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
        label = NORMAL_FONT.render("Disks:", True, WHITE)
        win.blit(label, (self.x - 100, self.y + 10))

        pygame.draw.rect(win, DARK_BLUE, self.value_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.value_rect, 2, border_radius=6)
        value_text = STATS_FONT.render(str(self.value), True, YELLOW)
        win.blit(value_text, (self.x + 30 - value_text.get_width() // 2, self.y + 8))

        minus_color = LIGHT_RED if self.minus_hover else RED
        pygame.draw.rect(win, minus_color, self.minus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.minus_rect, 2, border_radius=6)
        minus_text = BUTTON_FONT.render("-", True, WHITE)
        win.blit(
            minus_text,
            (
                self.minus_rect.centerx - minus_text.get_width() // 2,
                self.minus_rect.centery - minus_text.get_height() // 2,
            ),
        )

        plus_color = LIGHT_GREEN if self.plus_hover else GREEN
        pygame.draw.rect(win, plus_color, self.plus_rect, border_radius=6)
        pygame.draw.rect(win, WHITE, self.plus_rect, 2, border_radius=6)
        plus_text = BUTTON_FONT.render("+", True, WHITE)
        win.blit(
            plus_text,
            (
                self.plus_rect.centerx - plus_text.get_width() // 2,
                self.plus_rect.centery - plus_text.get_height() // 2,
            ),
        )

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

    def _lighten_color(self, color, amount):
        return tuple(min(255, c + amount) for c in color)

    def draw(self, win, x, y, is_selected=False):
        pygame.draw.rect(
            win,
            (20, 20, 20),
            (
                x - self.width // 2 + self.shadow_offset,
                y + self.shadow_offset,
                self.width,
                self.height,
            ),
            border_radius=6,
        )

        disk_color = self._lighten_color(self.color, 30) if is_selected else self.color
        pygame.draw.rect(
            win,
            disk_color,
            (x - self.width // 2, y, self.width, self.height),
            border_radius=6,
        )

        border_color = YELLOW if is_selected else BLACK
        border_width = 3 if is_selected else 2
        pygame.draw.rect(
            win,
            border_color,
            (x - self.width // 2, y, self.width, self.height),
            border_width,
            border_radius=6,
        )

        if self.size <= 8:
            number_color = BLACK if disk_color[0] > 150 else WHITE
            number = SMALL_FONT.render(str(self.size), True, number_color)
            win.blit(
                number,
                (
                    x - number.get_width() // 2,
                    y + (self.height - number.get_height()) // 2,
                ),
            )


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
        if self.highlighted:
            highlight_rect = pygame.Rect(
                self.x - self.base_width // 2,
                self.y - self.peg_height,
                self.base_width,
                self.peg_height + 20,
            )
            pygame.draw.rect(win, self.hover_color, highlight_rect, border_radius=8)

        pygame.draw.rect(
            win,
            (20, 20, 20),
            (
                self.x - self.base_width // 2 + 3,
                self.y + 3,
                self.base_width,
                15,
            ),
            border_radius=4,
        )
        pygame.draw.rect(
            win,
            BLACK,
            (self.x - self.base_width // 2, self.y, self.base_width, 15),
            border_radius=4,
        )

        pygame.draw.rect(
            win,
            (20, 20, 20),
            (self.x - 8 + 2, self.y - self.peg_height + 2, 16, self.peg_height),
        )
        pygame.draw.rect(
            win,
            BLACK,
            (self.x - 8, self.y - self.peg_height, 16, self.peg_height),
        )

        label_text = HEADER_FONT.render(self.label, True, YELLOW)
        win.blit(label_text, (self.x - label_text.get_width() // 2, self.y + 25))

    def get_click_rect(self):
        return pygame.Rect(
            self.x - self.base_width // 2,
            self.y - self.peg_height,
            self.base_width,
            self.peg_height + 20,
        )


class ScoresPanel:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.scores = []
        self.last_update = 0
        self.update_interval = 30000
        self.error_message = ""
        self.last_draw_time = 0
        self.update_cooldown = 2000  # Update every 2 seconds at most

    def update_scores(self):
        """Non-blocking score update with cooldown"""
        current_time = pygame.time.get_ticks()
        
        # Rate limiting
        if current_time - self.last_draw_time < self.update_cooldown:
            return
            
        self.last_draw_time = current_time
        
        # Get scores from thread-safe manager
        self.scores = firebase_manager.get_high_scores(limit=5)
        
        # Check connection status
        if not firebase_manager.is_connected():
            self.error_message = "Offline mode"
        elif not self.scores:
            self.error_message = "No scores yet"
        else:
            self.error_message = ""

    def draw(self, win):
        pygame.draw.rect(win, (40, 40, 65), self.rect, border_radius=12)
        pygame.draw.rect(win, PANEL_BORDER, self.rect, 3, border_radius=12)

        title = HEADER_FONT.render("Top Scores", True, YELLOW)
        win.blit(title, (self.rect.x + 20, self.rect.y + 15))

        # Non-blocking update
        self.update_scores()

        # Connection status
        is_connected = firebase_manager.is_connected()
        status_text = "Online" if is_connected else "Offline"
        status_color = GREEN if is_connected else RED
        
        status = SMALL_FONT.render(f"Status: {status_text}", True, status_color)
        win.blit(status, (self.rect.x + 20, self.rect.y + 45))

        y = self.rect.y + 80
        if self.error_message and not self.scores:
            error_text = SMALL_FONT.render(self.error_message, True, RED)
            win.blit(error_text, (self.rect.x + 20, y))
            y += 30
            help_text = SMALL_FONT.render("Play to add first score!", True, YELLOW)
            win.blit(help_text, (self.rect.x + 20, y))
        elif not self.scores:
            no_scores = NORMAL_FONT.render("No scores yet!", True, WHITE)
            win.blit(
                no_scores,
                (self.rect.centerx - no_scores.get_width() // 2, self.rect.centery),
            )
        else:
            for i, score in enumerate(self.scores[:5]):
                player = score.get('player_name', 'Anonymous')[:15]
                moves = score.get('num_moves', 0)
                disks = score.get('num_disks', 3)

                if i == 0:
                    color = YELLOW
                elif i == 1:
                    color = LIGHT_GRAY
                elif i == 2:
                    color = ORANGE
                else:
                    color = WHITE

                score_text = f"{i + 1}. {player} ({moves} moves, {disks} disks)"
                text_surface = NORMAL_FONT.render(score_text, True, color)
                win.blit(text_surface, (self.rect.x + 20, y))
                y += 35


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_particle(self, x, y, color=WHITE, speed=3, lifetime=60):
        self.particles.append(
            {
                'x': x,
                'y': y,
                'vx': (pygame.time.get_ticks() % 10 - 5) * 0.5,
                'vy': -speed - (pygame.time.get_ticks() % 10) * 0.1,
                'color': color,
                'lifetime': lifetime,
                'size': pygame.time.get_ticks() % 5 + 2,
            }
        )

    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['vy'] += 0.1
            particle['lifetime'] -= 1
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)

    def draw(self, win):
        for particle in self.particles:
            alpha = min(255, particle['lifetime'] * 4)
            color = (*particle['color'][:3], alpha)
            size = particle['size']
            pygame.draw.circle(
                win,
                color,
                (int(particle['x']), int(particle['y'])),
                size,
            )


class GameUI:
    def __init__(self):
        self.game = HanoiLogic(game_mode="interactive")
        self.clock = pygame.time.Clock()
        self.running = True

        self.algorithm_helper = AlgorithmHelper(self.game.num_disks, self.game.num_pegs)
        self.showing_solution = False
        self.solution_step = 0

        self.player_name = ""
        self.name_dialog = NameInputDialog(
            WIDTH // 2 - 250, HEIGHT // 2 - 150, 500, 300
        )
        self.show_name_dialog = True
        self.score_saved = False

        self.left_panel = Panel(20, 20, 280, 450, "Game Stats")
        self.center_area = pygame.Rect(320, 150, 800, 500)
        self.right_panel = Panel(WIDTH - 320, 20, 300, 700, "Controls")

        self.interactive_btn = Button(
            self.right_panel.rect.x + 30, 100, 240, 50, "Interactive Mode", GREEN, WHITE
        )
        self.sequence_btn = Button(
            self.right_panel.rect.x + 30, 160, 240, 50, "Sequence Mode", BLUE, WHITE
        )
        self.interactive_btn.active = True

        self.reset_btn = Button(
            self.right_panel.rect.x + 30, 230, 115, 45, "New Game", CYAN
        )
        self.undo_btn = Button(
            self.right_panel.rect.x + 155, 230, 115, 45, "Undo", PURPLE
        )

        self.hint_btn = Button(
            self.right_panel.rect.x + 30, 290, 115, 45, "Get Hint", ORANGE
        )
        self.auto_solve_btn = Button(
            self.right_panel.rect.x + 155, 290, 115, 45, "Auto-Step", PURPLE
        )
        self.show_solution_btn = Button(
            self.right_panel.rect.x + 30, 345, 240, 45, "Show Solution", DARK_GREEN
        )

        self.iterative_algo_btn = Button(
            self.right_panel.rect.x + 30, 400, 115, 45, "Iterative", LIGHT_BLUE
        )
        self.recursive_algo_btn = Button(
            self.right_panel.rect.x + 155, 400, 115, 45, "Recursive", LIGHT_PURPLE
        )
        self.iterative_algo_btn.active = True

        self.validate_btn = Button(
            self.right_panel.rect.x + 30, 455, 115, 45, "Validate", GREEN
        )
        self.execute_btn = Button(
            self.right_panel.rect.x + 155, 455, 115, 45, "Execute", BLUE
        )
        self.example_btn = Button(
            self.right_panel.rect.x + 30, 510, 240, 45, "Show Example", ORANGE
        )

        self.num_moves_box = InputBox(
            self.right_panel.rect.x + 30, 565, 240, 40, "Number of moves:"
        )
        self.moves_box = InputBox(
            self.right_panel.rect.x + 30,
            620,
            240,
            40,
            "Move sequence:",
        )

        self.scores_panel = ScoresPanel(WIDTH - 320, HEIGHT - 250, 300, 200)

        self.peg_selector = PegSelector(150, 300)
        self.disk_selector = DiskSelector(150, 380)

        self.towers_ui = {}
        self.update_towers_ui()

        self.dragging_disk = None
        self.hovered_peg = None

        self.undo_stack = []
        self.save_state()

        self.particle_system = ParticleSystem()

        self.solution_display = []
        self.current_hint = None

        self.sequence_validated = False
        self.sequence_moves = []
        self.current_sequence_step = 0

        try:
            self.background_image = pygame.image.load(
                "Tower of Hanoi/bimage.jpg"
            ).convert()
        except Exception as e:
            print("Could not load background image, using solid color.")
            self.background_image = None

    def update_towers_ui(self):
        """Update the tower UI positions based on number of pegs"""
        num_pegs = self.game.num_pegs
        spacing = 800 // (num_pegs + 1)
        base_y = HEIGHT - 180

        self.towers_ui = {}
        for i, label in enumerate(self.game.tower_labels):
            x = 150 + spacing * (i + 1)
            self.towers_ui[label] = TowerUI(x, base_y, label)

        self.algorithm_helper.set_num_pegs(num_pegs)
        print(f"Updated towers UI for {num_pegs} pegs")

    def save_state(self):
        """Save current game state to undo stack"""
        state = {
            'towers': {k: v.copy() for k, v in self.game.towers.items()},
            'move_count': self.game.move_count,
            'game_state': self.game.game_state,
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
        """Save score to Firebase"""
        if not self.player_name:
            self.player_name = "Anonymous"

        num_disks = self.game.num_disks
        num_moves = self.game.move_count
        optimal_moves = self.game.get_min_moves()
        game_mode = self.game.game_mode

        move_sequence = ""
        if game_mode == "sequence" and hasattr(self.game, 'user_moves_input'):
            move_sequence = self.game.user_moves_input

        # Debug output
        print("\n" + "="*50)
        print(" DEBUG: Attempting to save score to Firebase")
        print(f"  Player: {self.player_name}")
        print(f"  Disks: {num_disks}")
        print(f"  Moves: {num_moves}")
        print(f"  Optimal: {optimal_moves}")
        print(f"  Game State: {self.game.game_state}")
        print(f"  Firebase connected: {firebase_manager.is_connected()}")
        print("="*50)

        # Use thread-safe Firebase manager
        success = firebase_manager.save_player_score(
            player_name=self.player_name,
            num_disks=num_disks,
            num_moves=num_moves,
            optimal_moves=optimal_moves,
            game_mode=game_mode,
            move_sequence=move_sequence,
            is_correct=(self.game.game_state == "win"),
        )

        if success:
            self.score_saved = True
            self.game.message = "Score saved!"
            print(f" SUCCESS: Score saved for {self.player_name}")
        else:
            self.game.message = "Score saved locally"
            print(" WARNING: Score saved locally (offline mode or Firebase error)")
        
        return True

    def draw_stats(self):
        """Draw game statistics panel"""
        self.left_panel.draw(WIN)

        num_pegs = self.game.num_pegs
        num_disks = self.game.num_disks

        if num_pegs == 4:
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
            optimal_moves = optimal_4peg.get(num_disks, "?")
        else:
            optimal_moves = (1 << num_disks) - 1

        stats = [
            ("DISKS:", str(self.game.num_disks), YELLOW),
            ("PEGS:", str(self.game.num_pegs), LIGHT_CYAN if num_pegs == 4 else CYAN),
            ("MOVES:", str(self.game.move_count), WHITE),
            ("OPTIMAL:", str(optimal_moves), GREEN),
            (
                "MODE:",
                self.game.game_mode.title(),
                GREEN if self.game.game_mode == "interactive" else BLUE,
            ),
            (
                "STATUS:",
                self.game.game_state.title(),
                GREEN
                if self.game.game_state == "win"
                else YELLOW
                if self.game.game_state == "playing"
                else CYAN,
            ),
        ]

        x, y = 50, 80
        for label, value, color in stats:
            label_surface = NORMAL_FONT.render(label, True, WHITE)
            WIN.blit(label_surface, (x, y))

            value_surface = STATS_FONT.render(value, True, color)
            WIN.blit(value_surface, (x + 150, y - 5))

            y += 35

    def draw_towers(self):
        """Draw towers and disks"""
        for label, tower in self.towers_ui.items():
            tower.draw(WIN)

            x = tower.x
            base_y = tower.y - 20
            disks = self.game.towers[label]

            for i, disk_size in enumerate(disks):
                disk = Disk(disk_size)
                is_selected = (
                    self.game.selected_peg == label
                    and i == len(disks) - 1
                    and self.game.selected_disk == disk_size
                )
                disk.draw(WIN, x, base_y - i * 32, is_selected)

    def draw_controls(self):
        """Draw controls panel"""
        self.right_panel.draw(WIN)

        # Show current algorithm
        algo_info = self.algorithm_helper.get_algorithm_explanation()
        algo_text = SMALL_FONT.render(
            f"Algorithm: {algo_info['current_algorithm'].title()}",
            True,
            YELLOW
            if algo_info['current_algorithm'].startswith('iterative')
            else LIGHT_PURPLE,
        )
        WIN.blit(algo_text, (self.right_panel.rect.x + 30, 70))

        # Show instructions based on mode
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
                "  full optimal solution",
            ]
            color = GREEN
        else:
            instructions = [
                "SEQUENCE MODE",
                "1. Enter number of moves",
                "2. Enter move sequence",
                "3. Click VALIDATE",
                "4. Click EXECUTE",
                "",
                "Format examples:",
                "3-Peg: AB AC BC",
                "4-Peg: AB AC AD BC",
                "",
                f"Valid pegs: {' '.join(self.game.tower_labels)}",
            ]
            color = BLUE

        # Draw instructions at bottom of panel
        x, y = self.right_panel.rect.x + 30, self.right_panel.rect.y + 670
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
        """Draw status messages"""
        messages = []

        if self.game.message:
            messages.append((self.game.message, YELLOW))

        if self.current_hint:
            messages.append(
                (
                    f"Current hint: Move {self.current_hint[0]} → {self.current_hint[1]}",
                    CYAN,
                )
            )

        if self.showing_solution:
            total_moves = len(self.solution_display)
            if self.solution_step < total_moves:
                move = self.solution_display[self.solution_step]
                messages.append(
                    (
                        f"Solution step {self.solution_step+1}/{total_moves}: {move[0]} → {move[1]}",
                        GREEN,
                    )
                )
            else:
                messages.append(("Solution complete! Press ESC to return.", GREEN))

        y_offset = HEIGHT - 30
        for msg_text, color in reversed(messages):
            msg_surface = NORMAL_FONT.render(msg_text, True, color)
            msg_rect = msg_surface.get_rect(center=(WIDTH // 2, y_offset))

            bg_rect = msg_rect.inflate(40, 15)
            pygame.draw.rect(
                WIN, (40, 40, 70, 200), bg_rect, border_radius=10
            )
            pygame.draw.rect(WIN, color, bg_rect, 2, border_radius=10)

            WIN.blit(msg_surface, msg_rect)
            y_offset -= 40

        if self.score_saved:
            score_msg = "Score saved to database!"
            score_surface = NORMAL_FONT.render(score_msg, True, GREEN)
            score_rect = score_surface.get_rect(
                center=(WIDTH // 2, HEIGHT - 70)
            )

            score_bg = score_rect.inflate(40, 15)
            pygame.draw.rect(
                WIN, (40, 70, 40, 200), score_bg, border_radius=10
            )
            pygame.draw.rect(WIN, GREEN, score_bg, 2, border_radius=10)

            WIN.blit(score_surface, score_rect)

    def draw_solution_display(self):
        """Draw solution view"""
        if not self.showing_solution:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        WIN.blit(overlay, (0, 0))

        panel_rect = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 200, 600, 400)
        pygame.draw.rect(WIN, PANEL_BG, panel_rect, border_radius=20)
        pygame.draw.rect(WIN, GREEN, panel_rect, 4, border_radius=20)

        title = HEADER_FONT.render("OPTIMAL SOLUTION", True, YELLOW)
        WIN.blit(
            title,
            (panel_rect.centerx - title.get_width() // 2, panel_rect.y + 20),
        )

        algo_type = "Iterative" if self.iterative_algo_btn.active else "Recursive"
        num_pegs = self.game.num_pegs
        optimal_moves = len(self.solution_display)

        algo_text = NORMAL_FONT.render(
            f"Algorithm: {algo_type} | Pegs: {num_pegs} | Disks: {self.game.num_disks} | Optimal moves: {optimal_moves}",
            True,
            CYAN,
        )
        WIN.blit(
            algo_text,
            (
                panel_rect.centerx - algo_text.get_width() // 2,
                panel_rect.y + 60,
            ),
        )

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

        instructions = [
            "Press SPACE for next move",
            "Press ENTER to auto-solve all",
            "Press ESC to exit solution view",
        ]

        y = panel_rect.y + panel_rect.height - 80
        for i, line in enumerate(instructions):
            inst_text = SMALL_FONT.render(line, True, WHITE)
            WIN.blit(
                inst_text,
                (panel_rect.centerx - inst_text.get_width() // 2, y + i * 25),
            )

    def draw_win_message(self):
        """Draw win message"""
        if self.game.game_state == "win" and not self.showing_solution:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            WIN.blit(overlay, (0, 0))

            win_text = HEADER_FONT.render("PUZZLE SOLVED!", True, GREEN)
            win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

            box_rect = win_rect.inflate(80, 40)
            pygame.draw.rect(WIN, PANEL_BG, box_rect, border_radius=20)
            pygame.draw.rect(WIN, GREEN, box_rect, 4, border_radius=20)

            WIN.blit(win_text, win_rect)

            moves_text = NORMAL_FONT.render(
                f"Moves: {self.game.move_count}", True, YELLOW
            )
            moves_rect = moves_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 10)
            )
            WIN.blit(moves_text, moves_rect)

            player_text = NORMAL_FONT.render(
                f"Player: {self.player_name}", True, CYAN
            )
            player_rect = player_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50)
            )
            WIN.blit(player_text, player_rect)

            if not self.score_saved:
                save_text = SMALL_FONT.render(
                    "Score automatically saved!", True, WHITE
                )
                save_rect = save_text.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 + 90)
                )
                WIN.blit(save_text, save_rect)

    def draw(self):
        """Draw everything"""
        if self.background_image:
            WIN.blit(self.background_image, (0, 0))
        else:
            WIN.fill(BACKGROUND)

        if self.show_name_dialog:
            self.name_dialog.draw(WIN)
            pygame.display.flip()
            return

        # Title and subtitle
        title = TITLE_FONT.render("TOWER OF HANOI", True, YELLOW)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        mode_text = (
            "Interactive Mode"
            if self.game.game_mode == "interactive"
            else "Sequence Mode"
        )
        subtitle = HEADER_FONT.render(
            f"{mode_text} | {self.game.num_disks} Disks | {self.game.num_pegs} Pegs",
            True,
            WHITE,
        )
        WIN.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 90))

        # Draw panels and elements
        self.draw_stats()
        self.draw_towers()
        self.draw_controls()
        self.scores_panel.draw(WIN)

        # Always show these buttons
        self.interactive_btn.draw(WIN)
        self.sequence_btn.draw(WIN)
        self.reset_btn.draw(WIN)
        self.undo_btn.draw(WIN)
        self.hint_btn.draw(WIN)
        self.auto_solve_btn.draw(WIN)
        self.show_solution_btn.draw(WIN)
        self.iterative_algo_btn.draw(WIN)
        self.recursive_algo_btn.draw(WIN)

        # Show sequence mode controls only in sequence mode
        if self.game.game_mode == "sequence":
            self.validate_btn.draw(WIN)
            self.execute_btn.draw(WIN)
            self.example_btn.draw(WIN)
            self.num_moves_box.draw(WIN)
            self.moves_box.draw(WIN)

        self.peg_selector.draw(WIN)
        self.disk_selector.draw(WIN)

        # Status message
        self.draw_message()

        if self.showing_solution:
            self.draw_solution_display()
        else:
            self.draw_win_message()

        self.particle_system.draw(WIN)

        pygame.display.flip()

    def update(self):
        """Update game state"""
        if self.show_name_dialog:
            self.name_dialog.update()

        # Update buttons
        self.interactive_btn.update()
        self.sequence_btn.update()
        self.reset_btn.update()
        self.undo_btn.update()
        self.hint_btn.update()
        self.auto_solve_btn.update()
        self.show_solution_btn.update()
        self.iterative_algo_btn.update()
        self.recursive_algo_btn.update()

        # Update sequence controls
        if self.game.game_mode == "sequence":
            self.validate_btn.update()
            self.execute_btn.update()
            self.example_btn.update()
            self.num_moves_box.update()
            self.moves_box.update()

        self.particle_system.update()

    def handle_events(self):
        """Handle all pygame events"""
        mouse_pos = pygame.mouse.get_pos()

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
                        if self.solution_step < len(self.solution_display):
                            move = self.solution_display[self.solution_step]
                            if hasattr(self.game, 'move_disk'):
                                self.game.selected_disk = self.game.get_top_disk(
                                    move[0]
                                )
                                self.game.selected_peg = move[0]
                                self.game.move_disk(move[1])
                                self.save_state()
                            self.solution_step += 1

                    elif event.key == pygame.K_RETURN:
                        while self.solution_step < len(self.solution_display):
                            move = self.solution_display[self.solution_step]
                            if hasattr(self.game, 'move_disk'):
                                self.game.selected_disk = self.game.get_top_disk(
                                    move[0]
                                )
                                self.game.selected_peg = move[0]
                                self.game.move_disk(move[1])
                                self.save_state()
                            self.solution_step += 1

                        if self.game.game_state == "win" and not self.score_saved:
                            self.save_score_to_firebase()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        panel_rect = pygame.Rect(
                            WIDTH // 2 - 300, HEIGHT // 2 - 200, 600, 400
                        )
                        if not panel_rect.collidepoint(mouse_pos):
                            self.showing_solution = False
                            self.solution_step = 0

            return

        # Update button hovers
        self.interactive_btn.check_hover(mouse_pos)
        self.sequence_btn.check_hover(mouse_pos)
        self.reset_btn.check_hover(mouse_pos)
        self.undo_btn.check_hover(mouse_pos)
        self.hint_btn.check_hover(mouse_pos)
        self.auto_solve_btn.check_hover(mouse_pos)
        self.show_solution_btn.check_hover(mouse_pos)
        self.iterative_algo_btn.check_hover(mouse_pos)
        self.recursive_algo_btn.check_hover(mouse_pos)
        
        # Only show sequence buttons in sequence mode
        if self.game.game_mode == "sequence":
            self.validate_btn.check_hover(mouse_pos)
            self.execute_btn.check_hover(mouse_pos)
            self.example_btn.check_hover(mouse_pos)

        self.peg_selector.check_hover(mouse_pos)
        self.disk_selector.check_hover(mouse_pos)

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
                if event.button == 1:
                    # MODE BUTTONS
                    if self.interactive_btn.is_clicked(mouse_pos):
                        self.game.switch_mode("interactive")
                        self.interactive_btn.active = True
                        self.sequence_btn.active = False
                        self.update_towers_ui()
                        self.game.message = "Switched to Interactive Mode"
                        print("Switched to Interactive Mode")

                    elif self.sequence_btn.is_clicked(mouse_pos):
                        self.game.switch_mode("sequence")
                        self.interactive_btn.active = False
                        self.sequence_btn.active = True
                        self.update_towers_ui()
                        self.game.message = "Switched to Sequence Mode"
                        print("Switched to Sequence Mode")

                    # GAME CONTROLS
                    elif self.reset_btn.is_clicked(mouse_pos):
                        self.save_state()
                        self.game.reset(
                            num_pegs=self.peg_selector.value,
                            num_disks=self.disk_selector.value,
                        )
                        self.algorithm_helper.set_num_disks(self.game.num_disks)
                        self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                        self.update_towers_ui()
                        self.score_saved = False
                        self.current_hint = None
                        self.sequence_validated = False
                        self.sequence_moves = []
                        self.game.message = "New game started!"

                    elif (
                        self.undo_btn.is_clicked(mouse_pos)
                        and self.game.game_mode == "interactive"
                    ):
                        if self.undo():
                            self.score_saved = False
                            self.current_hint = None

                    # ALGORITHM FEATURES (only in interactive mode)
                    elif (
                        self.hint_btn.is_clicked(mouse_pos)
                        and self.game.game_mode == "interactive"
                    ):
                        algorithm = (
                            'iterative'
                            if self.iterative_algo_btn.active
                            else 'recursive'
                        )
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        self.current_hint = self.algorithm_helper.get_current_hint()
                        if self.current_hint:
                            self.game.message = (
                                f"Hint: Move {self.current_hint[0]} to {self.current_hint[1]}"
                            )
                        else:
                            self.game.message = "No more hints available"

                    elif (
                        self.auto_solve_btn.is_clicked(mouse_pos)
                        and self.game.game_mode == "interactive"
                    ):
                        algorithm = (
                            'iterative'
                            if self.iterative_algo_btn.active
                            else 'recursive'
                        )
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        move = self.algorithm_helper.auto_solve_step()
                        if move:
                            if hasattr(self.game, 'move_disk'):
                                self.save_state()
                                self.game.selected_disk = self.game.get_top_disk(
                                    move[0]
                                )
                                self.game.selected_peg = move[0]
                                success = self.game.move_disk(move[1])
                                if success:
                                    for _ in range(10):
                                        self.particle_system.add_particle(
                                            self.towers_ui[move[1]].x,
                                            self.towers_ui[move[1]].y - 100,
                                            color=PURPLE,
                                            speed=2,
                                        )
                                    if (
                                        self.game.game_state == "win"
                                        and not self.score_saved
                                    ):
                                        self.save_score_to_firebase()
                        else:
                            self.game.message = "Auto-solve complete!"

                    elif self.show_solution_btn.is_clicked(mouse_pos):
                        algorithm = (
                            'iterative'
                            if self.iterative_algo_btn.active
                            else 'recursive'
                        )
                        solution = self.algorithm_helper.get_optimal_solution(algorithm)
                        self.solution_display = [
                            (move[0], move[1]) for move in solution
                        ]
                        self.solution_step = 0
                        self.showing_solution = True
                        self.game.message = (
                            "Showing optimal solution. Press SPACE for next move."
                        )

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

                    # SEQUENCE MODE CONTROLS
                    elif self.game.game_mode == "sequence":
                        if self.validate_btn.is_clicked(mouse_pos):
                            # Proper validation
                            try:
                                expected_moves = int(self.num_moves_box.text.strip())
                                moves_text = self.moves_box.text.strip().upper()
                                
                                # Parse moves
                                move_parts = moves_text.split()
                                if len(move_parts) != expected_moves:
                                    self.game.message = f"Error: Expected {expected_moves} moves, got {len(move_parts)}"
                                    self.sequence_validated = False
                                else:
                                    # Validate each move
                                    valid_moves = []
                                    for move in move_parts:
                                        if len(move) == 2:
                                            from_peg = move[0]
                                            to_peg = move[1]
                                            if from_peg in self.game.tower_labels and to_peg in self.game.tower_labels:
                                                valid_moves.append((from_peg, to_peg))
                                            else:
                                                self.game.message = f"Invalid peg labels in move: {move}"
                                                self.sequence_validated = False
                                                break
                                    else:
                                        self.sequence_moves = valid_moves
                                        self.sequence_validated = True
                                        self.game.message = f"Sequence validated! {expected_moves} moves ready."
                                        print(f"Sequence validated: {valid_moves}")
                            except ValueError:
                                self.game.message = "Please enter a valid number of moves"
                                self.sequence_validated = False

                        elif self.execute_btn.is_clicked(mouse_pos):
                            if self.sequence_validated and self.sequence_moves:
                                print(f"Executing sequence: {self.sequence_moves}")
                                
                                # Reset game first
                                self.game.reset(
                                    num_pegs=self.peg_selector.value,
                                    num_disks=self.disk_selector.value,
                                )
                                
                                # Execute each move
                                all_valid = True
                                for i, (from_peg, to_peg) in enumerate(self.sequence_moves):
                                    # Get top disk from source peg
                                    if from_peg in self.game.towers and self.game.towers[from_peg]:
                                        disk = self.game.towers[from_peg][-1]
                                        self.game.selected_disk = disk
                                        self.game.selected_peg = from_peg
                                        
                                        # Try to move
                                        success = self.game.move_disk(to_peg)
                                        if not success:
                                            self.game.message = f"Move {i+1} failed: {from_peg}->{to_peg}"
                                            all_valid = False
                                            break
                                        
                                        # Add visual feedback
                                        for _ in range(5):
                                            self.particle_system.add_particle(
                                                self.towers_ui[to_peg].x,
                                                self.towers_ui[to_peg].y - 100,
                                                color=BLUE,
                                                speed=2,
                                            )
                                    
                                if all_valid:
                                    self.save_state()
                                    if self.game.game_state == "win":
                                        self.game.message = "Sequence executed successfully! Puzzle solved!"
                                        if not self.score_saved:
                                            self.save_score_to_firebase()
                                            for _ in range(50):
                                                self.particle_system.add_particle(
                                                    WIDTH // 2,
                                                    HEIGHT // 2,
                                                    color=YELLOW,
                                                    speed=5,
                                                )
                                    else:
                                        self.game.message = "Sequence executed but puzzle not solved"
                            else:
                                self.game.message = "Please validate sequence first"

                        elif self.example_btn.is_clicked(mouse_pos):
                            # Provide better examples based on peg count
                            if self.game.num_pegs == 4:
                                if self.game.num_disks == 3:
                                    self.num_moves_box.text = "5"
                                    self.moves_box.text = "AC AB AD BD CD"
                                elif self.game.num_disks == 4:
                                    self.num_moves_box.text = "9"
                                    self.moves_box.text = "AB AC BC AB AD BD CA CD AD"
                                else:
                                    self.num_moves_box.text = "13"
                                    self.moves_box.text = "AB AC AD BC BD CA CB CD AB AC AD BC"
                            else:
                                # 3-peg examples
                                if self.game.num_disks == 3:
                                    self.num_moves_box.text = "7"
                                    self.moves_box.text = "AB AC BC AB CA CB AB"
                                elif self.game.num_disks == 4:
                                    self.num_moves_box.text = "15"
                                    self.moves_box.text = "AB AC BC AB CA CB AB AC BC BA CA BC AB AC BC"
                                elif self.game.num_disks == 5:
                                    self.num_moves_box.text = "31"
                                    self.moves_box.text = "AB AC BC AB CA CB AB AC BC BA CA BC AB AC BC AB CA CB AB AC BC BA CA BC AB AC BC AB CA CB AB AC"
                            
                            self.game.message = "Example sequence loaded. Click Validate first."

                    # PEG AND DISK SELECTORS
                    elif self.peg_selector.handle_click(mouse_pos):
                        self.save_state()
                        self.game.reset(
                            num_pegs=self.peg_selector.value,
                            num_disks=self.disk_selector.value,
                        )
                        self.algorithm_helper.set_num_disks(self.game.num_disks)
                        self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                        self.update_towers_ui()
                        self.score_saved = False
                        self.current_hint = None
                        self.sequence_validated = False
                        self.sequence_moves = []
                        self.game.message = (
                            f"Changed to {self.peg_selector.value} pegs"
                        )

                    elif self.disk_selector.handle_click(mouse_pos):
                        self.save_state()
                        self.game.reset(
                            num_pegs=self.peg_selector.value,
                            num_disks=self.disk_selector.value,
                        )
                        self.algorithm_helper.set_num_disks(self.game.num_disks)
                        self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                        self.update_towers_ui()
                        self.score_saved = False
                        self.current_hint = None
                        self.sequence_validated = False
                        self.sequence_moves = []
                        self.game.message = (
                            f"Changed to {self.disk_selector.value} disks"
                        )

                    # INTERACTIVE MODE DISK SELECTION
                    elif (
                        self.game.game_mode == "interactive"
                        and self.game.game_state == "playing"
                    ):
                        for label, tower in self.towers_ui.items():
                            x = tower.x
                            base_y = tower.y - 20
                            disks = self.game.towers[label]

                            for j, disk_size in enumerate(reversed(disks)):
                                actual_index = len(disks) - 1 - j
                                disk = Disk(disk_size)
                                disk_rect = pygame.Rect(
                                    x - disk.width // 2,
                                    base_y - actual_index * 32,
                                    disk.width,
                                    disk.height,
                                )

                                if disk_rect.collidepoint(mouse_pos):
                                    # Select the disk if it's on top
                                    if actual_index == len(disks) - 1:
                                        self.save_state()
                                        if hasattr(self.game, 'select_disk'):
                                            self.game.select_disk(label)
                                            self.current_hint = None
                                        break
                            else:
                                continue
                            break

            elif event.type == pygame.MOUSEBUTTONUP:
                if (
                    event.button == 1
                    and self.game.game_mode == "interactive"
                ):
                    if (
                        self.hovered_peg
                        and hasattr(self.game, 'selected_peg')
                        and self.game.selected_peg
                    ):
                        self.save_state()
                        if hasattr(self.game, 'move_disk'):
                            success = self.game.move_disk(self.hovered_peg)
                            if success:
                                for _ in range(10):
                                    self.particle_system.add_particle(
                                        self.towers_ui[self.hovered_peg].x,
                                        self.towers_ui[self.hovered_peg].y - 100,
                                        color=GREEN,
                                        speed=2,
                                    )
                                if (
                                    self.game.game_state == "win"
                                    and not self.score_saved
                                ):
                                    self.save_score_to_firebase()
                                self.current_hint = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.showing_solution:
                        self.showing_solution = False
                        self.solution_step = 0
                        self.game.message = "Exited solution view"
                    elif (
                        hasattr(self.game, 'selected_disk')
                        and self.game.selected_disk
                    ):
                        if hasattr(self.game, 'cancel_selection'):
                            self.game.cancel_selection()
                            self.current_hint = None

                elif event.key == pygame.K_r:
                    self.save_state()
                    self.game.reset(
                        num_pegs=self.peg_selector.value,
                        num_disks=self.disk_selector.value,
                    )
                    self.algorithm_helper.set_num_disks(self.game.num_disks)
                    self.algorithm_helper.set_num_pegs(self.peg_selector.value)
                    self.update_towers_ui()
                    self.score_saved = False
                    self.current_hint = None
                    self.sequence_validated = False
                    self.sequence_moves = []
                    self.game.message = "Game reset!"

                elif (
                    event.key == pygame.K_u
                    and pygame.key.get_mods() & pygame.KMOD_CTRL
                ):
                    if self.game.game_mode == "interactive":
                        if self.undo():
                            self.score_saved = False
                            self.current_hint = None

                elif event.key == pygame.K_m:
                    new_mode = (
                        "sequence"
                        if self.game.game_mode == "interactive"
                        else "interactive"
                    )
                    if hasattr(self.game, 'switch_mode'):
                        self.game.switch_mode(new_mode)
                    self.interactive_btn.active = new_mode == "interactive"
                    self.sequence_btn.active = new_mode == "sequence"
                    self.update_towers_ui()
                    self.game.message = f"Switched to {new_mode} mode"
                    self.current_hint = None
                    self.sequence_validated = False
                    self.sequence_moves = []

                elif (
                    event.key == pygame.K_s
                    and pygame.key.get_mods() & pygame.KMOD_CTRL
                ):
                    if self.game.move_count > 0:
                        self.save_score_to_firebase()
                        self.game.message = "Score saved manually!"

                elif event.key == pygame.K_h:
                    if self.game.game_mode == "interactive":
                        algorithm = (
                            'iterative'
                            if self.iterative_algo_btn.active
                            else 'recursive'
                        )
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        self.current_hint = self.algorithm_helper.get_current_hint()
                        if self.current_hint:
                            self.game.message = (
                                f"Hint: Move {self.current_hint[0]} to {self.current_hint[1]}"
                            )

                elif event.key == pygame.K_a:
                    if self.game.game_mode == "interactive":
                        algorithm = (
                            'iterative'
                            if self.iterative_algo_btn.active
                            else 'recursive'
                        )
                        self.algorithm_helper.get_optimal_solution(algorithm)
                        move = self.algorithm_helper.auto_solve_step()
                        if move:
                            self.save_state()
                            self.game.selected_disk = self.game.get_top_disk(
                                move[0]
                            )
                            self.game.selected_peg = move[0]
                            success = self.game.move_disk(move[1])
                            if (
                                success
                                and self.game.game_state == "win"
                                and not self.score_saved
                            ):
                                self.save_score_to_firebase()

                elif event.key == pygame.K_i:
                    self.iterative_algo_btn.active = True
                    self.recursive_algo_btn.active = False
                    self.algorithm_helper.get_optimal_solution('iterative')
                    self.current_hint = None
                    self.game.message = "Using Iterative algorithm"

                elif event.key == pygame.K_c:
                    self.iterative_algo_btn.active = False
                    self.recursive_algo_btn.active = True
                    self.algorithm_helper.get_optimal_solution('recursive')
                    self.current_hint = None
                    self.game.message = "Using Recursive algorithm"

                elif event.key == pygame.K_v:
                    algorithm = (
                        'iterative'
                        if self.iterative_algo_btn.active
                        else 'recursive'
                    )
                    solution = self.algorithm_helper.get_optimal_solution(algorithm)
                    self.solution_display = [(move[0], move[1]) for move in solution]
                    self.solution_step = 0
                    self.showing_solution = True
                    self.game.message = (
                        "Showing optimal solution. Press SPACE for next move."
                    )

                elif event.key == pygame.K_p:
                    new_pegs = 4 if self.game.num_pegs == 3 else 3
                    self.peg_selector.value = new_pegs
                    self.save_state()
                    self.game.reset(
                        num_pegs=new_pegs, num_disks=self.disk_selector.value
                    )
                    self.algorithm_helper.set_num_disks(self.game.num_disks)
                    self.algorithm_helper.set_num_pegs(new_pegs)
                    self.update_towers_ui()
                    self.score_saved = False
                    self.current_hint = None
                    self.sequence_validated = False
                    self.sequence_moves = []
                    self.game.message = f"Changed to {new_pegs} pegs"

                elif event.key == pygame.K_F1:
                    self.game.message = (
                        "Help: R=Reset, Ctrl+Z=Undo, M=Toggle Mode, H=Hint, "
                        "A=Auto-step, I/C=Algorithm, V=Solution, P=Toggle Pegs, F1=Help"
                    )

            # Handle input box events for sequence mode
            if self.game.game_mode == "sequence":
                self.num_moves_box.handle_event(event)
                self.moves_box.handle_event(event)

    def run(self):
        """Main game loop"""
        print("Starting Tower of Hanoi Game with 3 & 4 Peg Algorithm Features")
        print("Firebase Status:", "Connected" if firebase_manager.is_connected() else "Offline")
        print("Algorithm Features:")
        print("  * 3-Peg (default) and 4-Peg solvers")
        print("  * Get Hint (H key or Hint button)")
        print("  * Auto-Solve Step (A key or Auto-Step button)")
        print("  * Show Solution (V key or Show Solution button)")
        print("  * Toggle Algorithm: Iterative (I) / Recursive (C)")
        print("  * Toggle Pegs: 3-Peg <-> 4-Peg (P key)")
        print("  * Solution View with step-by-step execution")
        print("  * Sequence Mode: Enter and test move sequences")

        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


def main():
    game_ui = GameUI()
    game_ui.run()


if __name__ == "__main__":
    main()