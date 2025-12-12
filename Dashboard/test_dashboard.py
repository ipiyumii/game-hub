# test_dashboard.py - FIXED VERSION
import pygame
import sys
import os

# Fix 1: Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Fix 2: Use simple symbols
CHECK = "[OK]"
CROSS = "[ERROR]"

# Force games list
test_games = [
    {'gameName': 'Tower of Hanoi', 'gameId': 'tower_of_hanoi'},
    {'gameName': 'Traffic Simulation', 'gameId': 'traffic_simulation'},
    {'gameName': 'Eight Queens', 'gameId': 'eight_queens'},
    {'gameName': 'Sudoku', 'gameId': 'sudoku'},
    {'gameName': 'Tic Tac Toe', 'gameId': 'tic_tac_toe'},
    {'gameName': 'Memory Game', 'gameId': 'memory_game'}
]

print(f"Testing with {len(test_games)} games")
for game in test_games:
    print(f"  - {game['gameName']}")

try:
    from Dashboard.dashboard import GameHub
    print(f"{CHECK} GameHub imported")
    
    # Run with forced games
    hub = GameHub(games=test_games)
    print(f"{CHECK} Dashboard created")
    hub.run()
    
except Exception as e:
    print(f"{CROSS} Error: {e}")
    import traceback
    traceback.print_exc()