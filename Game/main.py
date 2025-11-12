import pygame
import sys
import math
from typing import Optional

try:
    from ui.name_input_popup import NameInputPopup, Colors
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure you're running the script from the correct directory.")
    sys.exit(1)


class GameHub:
    """Main game hub application"""
    
    def __init__(self):
        print("Initializing Pygame...")
        # Initialize Pygame
        pygame.init()
        print("Pygame initialized successfully!")
        
        # Screen settings
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        print(f"Creating screen with dimensions {self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}...")
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Game Hub - Welcome!")
        print("Screen created successfully!")
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Game state
        self.running = True
        self.player_name = None
        self.show_name_popup = True
        
        # UI Components
        print("Creating name input popup...")
        self.name_popup = NameInputPopup(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        print("Name input popup created successfully!")
        
        # Fonts
        print("Loading fonts...")
        self.title_font = pygame.font.Font(None, 64)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.text_font = pygame.font.Font(None, 24)
        print("Fonts loaded successfully!")
        
        # Background animation
        self.bg_offset = 0
        self.bg_speed = 0.5
        print("GameHub initialization complete!")
    
    def draw_animated_background(self):
        """Draw an animated gradient background"""
        # Create animated colors
        time_factor = pygame.time.get_ticks() * 0.001
        
        # Animated gradient colors
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
        """Draw floating particle effects"""
        time_factor = pygame.time.get_ticks() * 0.001
        
        for i in range(20):
            x = (i * 40 + math.sin(time_factor + i) * 30) % self.SCREEN_WIDTH
            y = (i * 30 + math.cos(time_factor * 0.7 + i) * 20) % self.SCREEN_HEIGHT
            size = 3 + int(2 * math.sin(time_factor * 2 + i))
            
            # Particle color with transparency effect
            alpha = int(100 + 50 * math.sin(time_factor * 3 + i))
            color = (255, 255, 255, alpha)
            
            # Create a surface for the particle with alpha
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (size, size), size)
            self.screen.blit(particle_surface, (x - size, y - size))
    
    def draw_welcome_screen(self):
        """Draw the main welcome screen after name input"""
        self.draw_animated_background()
        
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
        subtitle_text = "Ready to play some amazing games?"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, Colors.WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 220))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Game options (placeholder for future games)
        games = [
            "🐍 Snake and Ladder",
            "♛ Eight Queens Puzzle", 
            "🗼 Tower of Hanoi",
            "🚗 Traffic Simulation",
            "🗺️ Travelling Salesman"
        ]
        
        start_y = 300
        for i, game in enumerate(games):
            game_surface = self.text_font.render(game, True, Colors.WHITE)
            game_rect = game_surface.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + i * 40))
            
            # Create a button-like background
            button_rect = pygame.Rect(game_rect.x - 20, game_rect.y - 10, 
                                    game_rect.width + 40, game_rect.height + 20)
            pygame.draw.rect(self.screen, Colors.BUTTON_COLOR, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, Colors.WHITE, button_rect, width=2, border_radius=10)
            
            self.screen.blit(game_surface, game_rect)
        
        # Instructions
        instruction_text = "Games coming soon! Press ESC to exit."
        instruction_surface = self.text_font.render(instruction_text, True, Colors.WHITE)
        instruction_rect = instruction_surface.get_rect(center=(self.SCREEN_WIDTH // 2, 550))
        self.screen.blit(instruction_surface, instruction_rect)
    
    def handle_events(self):
        """Handle all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            
            # Handle name popup events
            if self.show_name_popup:
                result = self.name_popup.handle_event(event)
                if result:
                    if result == "CANCEL":
                        self.running = False
                    else:
                        self.player_name = result
                        self.show_name_popup = False
                        pygame.display.set_caption(f"Game Hub - Welcome {self.player_name}!")
    
    def update(self):
        """Update game state"""
        # Update background animation
        self.bg_offset += self.bg_speed
        if self.bg_offset > self.SCREEN_WIDTH:
            self.bg_offset = 0
    
    def draw(self):
        """Draw everything to the screen"""
        if self.show_name_popup:
            # Draw a simple background behind the popup
            self.draw_animated_background()
            # Draw the name input popup
            self.name_popup.draw(self.screen)
        else:
            # Draw the main welcome screen
            self.draw_welcome_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting Game Hub...")
        print("Close the game by clicking the X button or pressing ESC")
        
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Control frame rate
            self.clock.tick(self.FPS)
        
        # Cleanup
        pygame.quit()
        print(f"Thanks for playing, {self.player_name or 'Player'}!")


def main():
    """Main entry point"""
    try:
        print("Initializing Game Hub...")
        game = GameHub()
        print("Game Hub initialized successfully!")
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to continue...")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()