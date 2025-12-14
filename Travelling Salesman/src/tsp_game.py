import pygame
import math
import game_logic

class TravelingSalesmanGame:
    def __init__(self, player_name=None):
        # CONFIG
        self.WIDTH, self.HEIGHT = 1200, 720
        self.FPS = 30
        self.CITY_RADIUS = 20
        self.RIGHT_PANEL_W = 380
        self.MAP_TOP_OFFSET = 40

        self.player_name = player_name or "Player"
        pygame.init()
        self.FONT = pygame.font.SysFont(None, 18)
        self.BIG = pygame.font.SysFont(None, 22)
        self.TITLE = pygame.font.SysFont(None, 24, bold=True)

        # Map positions
        self.LEFT_PANEL_W = self.WIDTH - self.RIGHT_PANEL_W - 40
        self.POSITIONS = self.make_positions((self.LEFT_PANEL_W//2, (self.HEIGHT-150)//2 + self.MAP_TOP_OFFSET//2), 200)

        self.run_game()

    def make_positions(self, center, radius):
        positions = {}
        n = len(game_logic.CITIES)
        cx, cy = center
        for i, city in enumerate(game_logic.CITIES):
            angle = 2 * math.pi * i / n
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            positions[city] = (int(x), int(y))
        return positions

    def run_game(self):
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(f"Traveling Salesman - {self.player_name}")
        clock = pygame.time.Clock()

        # --- Game state ---
        dist_matrix = None
        home_label = None
        selected = []
        player_route = []
        results = None
        message = "Press New Round to begin."
        player_name = self.player_name
        input_active = False
        input_text = ""
        home_idx = None
        win_status = None

        running = True
        while running:
            delta_time = clock.tick(self.FPS)
            screen.fill((20,20,20))
         
            pygame.display.flip()
        pygame.quit()
