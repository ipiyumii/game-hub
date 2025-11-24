
import tkinter as tk
import sys
import os

# Add the Eight Queens directory to Python path
eight_queens_dir = r"C:\Users\PiyumiWarnakulasuriy\Desktop\game-hub\EightQueensPuzzle"
sys.path.insert(0, eight_queens_dir)

from eightqeensUi import EightQueensUI

root = tk.Tk()
game = EightQueensUI(root, "f", tk)

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
