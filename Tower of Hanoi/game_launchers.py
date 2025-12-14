# game_launchers.py
import sys
import os
import pygame
import subprocess
import time

def launch_tower_of_hanoi(dashboard):
    print(f"\n{'='*50}")
    print(f"LAUNCHING TOWER OF HANOI")
    print(f"Player: {dashboard.player_name}")
    print(f"{'='*50}")
    
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    GAME_PATH = os.path.join(current_dir, "tower_of_hanoi_ui.py")
    
    if not os.path.exists(GAME_PATH):
        print(f"[ERROR] Game file not found at: {GAME_PATH}")
        print("Please check if your game is at this location.")
        return False
    
    try:
        # Pause dashboard
        dashboard.running = False
        
        # Show loading message
        dashboard.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        loading_text = font.render("Launching Tower of Hanoi...", True, (255, 255, 255))
        dashboard.screen.blit(loading_text, 
                            (dashboard.SCREEN_WIDTH//2 - loading_text.get_width()//2,
                             dashboard.SCREEN_HEIGHT//2 - loading_text.get_height()//2))
        pygame.display.flip()
        
        time.sleep(0.5)
        
        # Launch as subprocess
        env = os.environ.copy()
        env['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
        if dashboard.player_name:
            env['PLAYER_NAME'] = dashboard.player_name
        
        print(f"[OK] Launching game from: {GAME_PATH}")
        process = subprocess.Popen(
            [sys.executable, GAME_PATH],
            env=env
        )
        
        print("[OK] Game launched successfully!")
        print("Game is running in separate window...")
        
        # Wait for game to finish
        process.wait()
        print(f"[OK] Game completed. Exit code: {process.returncode}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to launch game: {e}")
        return False
        
    finally:
        # Restore dashboard
        print("[LAUNCHER] Restoring dashboard...")
        try:
            dashboard.screen = pygame.display.set_mode(
                (dashboard.SCREEN_WIDTH, dashboard.SCREEN_HEIGHT)
            )
            pygame.display.set_caption(f"Mind Arena - Welcome {dashboard.player_name}!")
            dashboard.running = True
            dashboard.draw()
            pygame.display.flip()
            print("[LAUNCHER] Dashboard restored!")
        except:
            pygame.quit()
            pygame.init()
            dashboard.screen = pygame.display.set_mode((dashboard.SCREEN_WIDTH, dashboard.SCREEN_HEIGHT))
            dashboard.running = True
    
    return True

def test_launcher():
    # Create a mock dashboard object for testing
    class MockDashboard:
        def __init__(self):
            self.player_name = "TestPlayer"
            self.SCREEN_WIDTH = 800
            self.SCREEN_HEIGHT = 600
            self.running = False
            self.screen = None
            self.show_name_popup = False
            
        def draw(self):
            pass
            
    mock_dash = MockDashboard()
    
    # Initialize pygame for testing
    pygame.init()
    mock_dash.screen = pygame.display.set_mode((mock_dash.SCREEN_WIDTH, mock_dash.SCREEN_HEIGHT))
    
    # Test Tower of Hanoi launcher
    print("\nTesting Tower of Hanoi launcher...")
    result = launch_tower_of_hanoi(mock_dash)
    print(f"Result: {'Success' if result else 'Failed'}")
    
    pygame.quit()

if __name__ == "__main__":
    test_launcher()