import sys
import os

from Dashboard.dashboard import GameHub
from dbUtil import fetch_games_from_database

dashboard_dir = os.path.join(os.path.dirname(__file__), 'Dashboard')
sys.path.insert(0, dashboard_dir)


def launch_game_dashboard(games=None):
    try:
        print("\n Launching Game Dashboard")

        game_hub = GameHub(games=games)
        game_hub.run()

    except ImportError as e:
        print(f"Dashboard Import Error: {e}")

    except Exception as e:
        print(f"Dashboard Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    # Fetch games
    games = fetch_games_from_database()

    launch_game_dashboard(games=games)

if __name__ == "__main__":
    main()