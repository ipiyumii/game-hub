#!/usr/bin/env python3
"""
Mind Arena - Main Entry Point

A colorful 2D Mind Arena with multiple mini-games, built using Python and Pygame.
This is the main entry point that launches the game dashboard and handles database operations.
"""

import sys
import os

from dbUtil import fetch_games_from_database

dashboard_dir = os.path.join(os.path.dirname(__file__), 'Dashboard')
sys.path.insert(0, dashboard_dir)


def launch_game_dashboard(games=None):
    """Launch the colorful game dashboard with games from database"""
    try:
        print("\n Launching Game Dashboard")
        from dashboard import GameHub

        game_hub = GameHub(games=games)
        game_hub.run()

    except ImportError as e:
        print(f"Dashboard Import Error: {e}")
        print("Please make sure all required files are in the correct locations:")
        print("- Dashboard/dashboard.py")
        print("- Dashboard/ui/name_input_popup.py")
        print("- Dashboard/requirements.txt")
        print("\nTo install requirements, run: pip install -r Dashboard/requirements.txt")

    except Exception as e:
        print(f"Dashboard Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point for the Mind Arena application"""
    print("===Mind Arena Application ===")
    print("Welcome to the Mind Arena!")
    
    # Fetch games 
    games = fetch_games_from_database()
    
    launch_game_dashboard(games=games)
    
    print("\nThank you for using Mind Arena!")

if __name__ == "__main__":
    main()