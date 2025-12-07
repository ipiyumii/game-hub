import os
import subprocess
import sys
import pygame

from EightQueensPuzzle.Solutions.sequential import find_max_solutions_sequantial
from EightQueensPuzzle.Solutions.threaded import find_max_solutions_threaded

def launch_eight_queens(self):
    find_max_solutions_sequantial()
    find_max_solutions_threaded()

    try:
        # Hide the pygame window temporarily
        pygame.display.iconify()

        # Path to the Eight Queens game directory
        game_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "EightQueensPuzzle")
        game_file = os.path.join(game_dir, "eightqeensUi.py")

        if os.path.exists(game_file):
            # Create a simple launcher script that passes the player name
            launcher_code = f'''
import tkinter as tk
import sys
import os

# Add the Eight Queens directory to Python path
eight_queens_dir = r"{game_dir}"
sys.path.insert(0, eight_queens_dir)

from eightqeensUi import EightQueensUI

root = tk.Tk()
game = EightQueensUI(root, "{self.player_name}", tk)

# Add return to hub button at bottom right
return_btn = tk.Button(
    root,
    text="Return to Game Hub",
    command=root.quit,
    bg="#2d3748",
    fg="white",
    font=("Arial", 12, "bold"),
    relief=tk.FLAT,
    bd=0,
    activebackground="#4a5568",
    activeforeground="white",
    cursor="hand2",
    padx=15,
    pady=5
)
return_btn.place(x=780, y=570, width=180, height=50)

root.mainloop()
'''
            # Write launcher to temp file
            temp_launcher = os.path.join(os.path.dirname(__file__), "temp_eight_queens_launcher.py")
            with open(temp_launcher, 'w') as f:
                f.write(launcher_code)

            # Launch the game
            result = subprocess.run([sys.executable, temp_launcher], cwd=game_dir)

            # Clean up temp file
            if os.path.exists(temp_launcher):
                os.remove(temp_launcher)

            # Restore the pygame window
            pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption(f"Mind Arena - Welcome {self.player_name}!")

        else:
            print(f"Eight Queens game not found at: {game_file}")

    except Exception as e:
        print(f"Error launching Eight Queens: {e}")
        pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))