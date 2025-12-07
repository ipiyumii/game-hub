 # run_game.py
import sys
import os

# ensure local folder is in sys.path so local imports work even if cwd differs
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui_tk import App

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
