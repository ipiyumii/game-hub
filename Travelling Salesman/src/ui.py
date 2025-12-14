import tkinter as tk
from tkinter import ttk
import game_logic
from firebase_config import save_game_result

def apply_custom_theme(style):
    style.theme_use('clam')
    style.configure("TButton", foreground="white", background="#4CAF50", font=("Helvetica", 10, "bold"))
    style.map("TButton", background=[('active','#45A049')])
    style.configure("TLabel", foreground="white", background="#1E1E1E", font=("Helvetica",10))
    style.configure("Treeview", background="#2E2E2E", foreground="white", fieldbackground="#2E2E2E", font=("Helvetica",10))
    style.configure("Treeview.Heading", background="#444444", foreground="white", font=("Helvetica",10,"bold"))
    style.configure("TCheckbutton", background="#1E1E1E", foreground="white", font=("Helvetica",10,"bold"))

class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Game")
        self.root.geometry("950x650")
        self.root.configure(bg="#1E1E1E")
        style = ttk.Style()
        apply_custom_theme(style)

        self.dist_matrix = None
        self.home_idx = None
        self.latest_results = None
        self.city_positions = game_logic.city_positions(center=(210,210), radius=160)

        # Top controls
        top = ttk.Frame(root, padding=8)
        top.pack(fill="x")
        ttk.Label(top, text="Player name:").pack(side="left")
        self.player_entry = ttk.Entry(top, width=25, font=("Helvetica",12))
        self.player_entry.pack(side="left", padx=6)
        ttk.Button(top, text="New Round", command=self.new_round).pack(side="left", padx=6)
        ttk.Button(top, text="Run Algorithms", command=self.run_algorithms).pack(side="left", padx=6)
        ttk.Button(top, text="Save Results", command=self.save_results).pack(side="left", padx=6)

        # Left panel: City selection & Map
        left = ttk.Frame(root, padding=8)
        left.pack(side="left", fill="y")
        ttk.Label(left, text="Select cities:").pack(anchor="w")
        self.city_vars = {}
        for city in game_logic.CITIES:
            var = tk.IntVar()
            ttk.Checkbutton(left, text=city, variable=var).pack(anchor="w", pady=2)
            self.city_vars[city] = var

        # Map visualization
        self.canvas = tk.Canvas(left, width=420, height=420, bg="#222222", highlightthickness=0)
        self.canvas.pack(pady=10)

        # Right panel: Algorithm results only
        right = ttk.Frame(root, padding=8)
        right.pack(side="right", fill="both", expand=True)
        columns = ("Algorithm","Route","Distance","Time (s)","Complexity")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", height=20)
        for c in columns:
            self.tree.heading(c,text=c)
            self.tree.column(c, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True)

        #  Bottom: Info / Messages
        bottom = ttk.Frame(root, padding=8)
        bottom.pack(fill="x")
        self.info_label = ttk.Label(bottom, text="Press 'New Round' to start.")
        self.info_label.pack(anchor="w", pady=4)

if __name__=="__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()
