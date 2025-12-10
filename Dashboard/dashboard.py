import os
import subprocess
import sys

import pygame
import math
# from EightQueensPuzzle.launch_game import launch_eight_queens

try:
    from Dashboard.ui.name_input_popup import NameInputPopup, Colors

except ImportError as e:
    print(f"Import error: {e}")


class GameHub:
    def __init__(self, games=None):
        print("Initializing Pygame...")
        # Initialize Pygame
        pygame.init()

        # Screen settings
        self.SCREEN_WIDTH = 1100
        self.SCREEN_HEIGHT = 750
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Mind Arena - Welcome!")

        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Game state
        self.running = True
        self.player_name = None
        self.show_name_popup = True

        # Games from db
        self.games = games if games is not None else []

        print(f"Loaded {len(self.games)} games")

        # UI Components
        self.name_popup = NameInputPopup(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Fonts
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)

        # Background animation
        self.bg_offset = 0
        self.bg_speed = 0.5

        self.game_buttons = []

    def draw_animated_background(self):
        # Create animated colors
        time_factor = pygame.time.get_ticks() * 0.001

        # animated gradient colors
        r1 = int(135 + 30 * math.cos(time_factor))
        g1 = int(206 + 20 * math.sin(time_factor * 1.2))
        b1 = int(250 + 5 * math.cos(time_factor * 0.8))

        r2 = int(25 + 15 * math.sin(time_factor * 0.7))
        g2 = int(25 + 10 * math.cos(time_factor * 1.1))
        b2 = int(112 + 20 * math.sin(time_factor * 0.9))

        start_color = (r1, g1, b1)
        end_color = (r2, g2, b2)

        # Draw gradient
        for y in range(self.SCREEN_HEIGHT):
            ratio = y / self.SCREEN_HEIGHT
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (self.SCREEN_WIDTH, y))

        # Add floating particles effect
        self.draw_particles()

    def draw_particles(self):
        time_factor = pygame.time.get_ticks() * 0.001

        for i in range(20):
            x = (i * 40 + math.sin(time_factor + i) * 30) % self.SCREEN_WIDTH
            y = (i * 30 + math.cos(time_factor * 0.7 + i) * 20) % self.SCREEN_HEIGHT
            size = 3 + int(2 * math.sin(time_factor * 2 + i))

            alpha = int(100 + 50 * math.sin(time_factor * 3 + i))
            color = (255, 255, 255, alpha)

            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (size, size), size)
            self.screen.blit(particle_surface, (x - size, y - size))

    def draw_welcome_screen(self):
        self.draw_animated_background()

        self.game_buttons = []

        # Welcome title
        title_text = f"Welcome, {self.player_name}!"
        title_surface = self.title_font.render(title_text, True, Colors.TITLE_COLOR)
        title_rect = title_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 150))

        # Add text shadow
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(self.SCREEN_WIDTH // 2 + 3, 153))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)

        # Subtitle
        subtitle_text = "Select a game to play:"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, Colors.WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle_surface, subtitle_rect)

        # Display games from database
        if len(self.games) > 0:
            start_y = 280
            max_games_to_show = min(len(self.games), 6)

            for i in range(max_games_to_show):
                game = self.games[i]
                game_name = game.get('gameName', game.get('name', f'Game {i + 1}'))
                game_id = game.get('gameId', f'game_{i}')

                if len(game_name) > 30:
                    display_name = game_name[:27] + "..."
                else:
                    display_name = game_name

                game_surface = self.text_font.render(display_name, True, Colors.WHITE)
                game_rect = game_surface.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + i * 45))

                button_rect = pygame.Rect(game_rect.x - 30, game_rect.y - 12,
                                          game_rect.width + 60, game_rect.height + 24)

                # Store button info for click detection
                self.game_buttons.append({
                    'rect': button_rect,
                    'game_id': game_id,
                    'game_name': game_name
                })

                # Check if mouse is hovering
                mouse_pos = pygame.mouse.get_pos()
                is_hovering = button_rect.collidepoint(mouse_pos)

                color_offset = i * 20
                if is_hovering:
                    button_color = (
                        min(255, Colors.BUTTON_COLOR[0] + color_offset + 30),
                        min(255, Colors.BUTTON_COLOR[1] + color_offset // 2 + 30),
                        min(255, Colors.BUTTON_COLOR[2] + color_offset // 3 + 30)
                    )
                else:
                    button_color = (
                        min(255, Colors.BUTTON_COLOR[0] + color_offset),
                        min(255, Colors.BUTTON_COLOR[1] + color_offset // 2),
                        min(255, Colors.BUTTON_COLOR[2] + color_offset // 3)
                    )

                pygame.draw.rect(self.screen, button_color, button_rect, border_radius=12)
                pygame.draw.rect(self.screen, Colors.WHITE, button_rect, width=2, border_radius=12)

                for j in range(5):
                    inner_rect = pygame.Rect(button_rect.x + j, button_rect.y + j,
                                             button_rect.width - 2 * j, button_rect.height - 2 * j)
                    alpha_color = (*button_color, max(0, 50 - j * 10))
                    gradient_surface = pygame.Surface((inner_rect.width, inner_rect.height), pygame.SRCALPHA)
                    gradient_surface.fill(alpha_color)
                    self.screen.blit(gradient_surface, inner_rect)

                self.screen.blit(game_surface, game_rect)

            # Show game count info
            if len(self.games) > max_games_to_show:
                more_text = f"... and {len(self.games) - max_games_to_show} more games"
                more_surface = self.text_font.render(more_text, True, Colors.WHITE)
                more_rect = more_surface.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + max_games_to_show * 45))
                self.screen.blit(more_surface, more_rect)

            # Instructions
            instruction_text = f"Have Fun Playing......!!!!!!"
        else:
            # No games available
            no_games_text = "No games available in the database."
            no_games_surface = self.subtitle_font.render(no_games_text, True, Colors.WHITE)
            no_games_rect = no_games_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 350))
            self.screen.blit(no_games_surface, no_games_rect)

            suggestion_text = "Please check your database connection or contact administrator."
            suggestion_surface = self.text_font.render(suggestion_text, True, Colors.WHITE)
            suggestion_rect = suggestion_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 390))
            self.screen.blit(suggestion_surface, suggestion_rect)

            instruction_text = "Press ESC to exit."

        instruction_surface = self.text_font.render(instruction_text, True, Colors.WHITE)
        instruction_rect = instruction_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 570))
        self.screen.blit(instruction_surface, instruction_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.show_name_popup:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if any game button was clicked
                    for button_info in self.game_buttons:
                        if button_info['rect'].collidepoint(mouse_pos):
                            self.launch_game(button_info['game_id'], button_info['game_name'])
                            break

            # Handle name popup events
            if self.show_name_popup:
                result = self.name_popup.handle_event(event)
                if result:
                    if result == "CANCEL":
                        self.running = False
                    else:
                        self.player_name = result
                        self.show_name_popup = False
                        pygame.display.set_caption(f"Mind Arena - Welcome {self.player_name}!")

    def update(self):
        self.bg_offset += self.bg_speed
        if self.bg_offset > self.SCREEN_WIDTH:
            self.bg_offset = 0

    def draw(self):
        if self.show_name_popup:
            self.draw_animated_background()
            self.name_popup.draw(self.screen)
        else:
            self.draw_welcome_screen()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)

        pygame.quit()

    def launch_game(self, game_id, game_name):
        """Handle Eight Queens game with various possible IDs
        if (game_id == "eight_queens" or
                "eight queens" in game_name.lower() or
                "queens" in game_name.lower()):
            launch_eight_queens(self)
        elif "Coming Soon" in game_name:
            print(f"{game_name} is not yet implemented.")
            # You could show a message on screen here
        else:
            print(f"Game {game_name} is not implemented yet.")"""

        if (game_id == "traffic_simulation" or
                "traffic" in game_name.lower() or
                "simulation" in game_name.lower()):
            try:
                print(f"Launching Traffic Simulation: {game_name}...")
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                traffic_game_path = os.path.join(base_path, "Traffic Simulation", "traffic_app.py")
                print("Running Traffic Simulation from:", traffic_game_path)
                subprocess.Popen([sys.executable, traffic_game_path])
            except Exception as e:
                print(f"Failed to launch Traffic Simulation: {e}")
            return
        print(f"Game '{game_name}' is not implemented or recognized.")
        
