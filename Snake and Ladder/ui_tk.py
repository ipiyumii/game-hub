# ui_tk.py
import tkinter as tk
from tkinter import ttk, messagebox
import time
from typing import Tuple

from game import GameState

CANVAS_SIZE = 600

class StartScreen(ttk.Frame):
    def __init__(self, parent, on_start):
        super().__init__(parent)
        self.on_start = on_start
        self.build()

    def build(self):
        ttk.Label(self, text="Snake & Ladder", font=("Helvetica", 20, "bold")).pack(pady=12)
        frm = ttk.Frame(self)
        frm.pack(pady=8)
        ttk.Label(frm, text="Player name:").grid(row=0, column=0, sticky="e")
        self.name_entry = ttk.Entry(frm)
        self.name_entry.grid(row=0, column=1, padx=8, pady=4)
        self.name_entry.insert(0, "Player1")

        ttk.Label(frm, text="Board size N (6 - 12):").grid(row=1, column=0, sticky="e")
        self.n_entry = ttk.Entry(frm)
        self.n_entry.grid(row=1, column=1, padx=8, pady=4)
        self.n_entry.insert(0, "8")

        btn = ttk.Button(self, text="Create Board", command=self.handle_create)
        btn.pack(pady=12)

    def handle_create(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Validation", "Please enter a player name.")
            return
        try:
            N = int(self.n_entry.get().strip())
            if N < 6 or N > 12:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation", "Board size must be an integer between 6 and 12.")
            return
        self.on_start(name, N)

class BoardScreen(ttk.Frame):
    def __init__(self, parent, player_name: str, N: int, on_game_end):
        super().__init__(parent)
        self.player_name = player_name
        self.N = N
        self.on_game_end = on_game_end
        self.cell_size = CANVAS_SIZE / N
        self.canvas = None
        self.token_id = None
        self.build_ui()
        self.init_game()

    def build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", pady=6)
        ttk.Label(top, text=f"Player: {self.player_name}").pack(side="left", padx=8)
        self.pos_label = ttk.Label(top, text="Position: 1")
        self.pos_label.pack(side="left", padx=8)

        self.canvas = tk.Canvas(self, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="white")
        self.canvas.pack(padx=8, pady=8)

        ctrl = ttk.Frame(self)
        ctrl.pack(pady=6)
        self.roll_btn = ttk.Button(ctrl, text="Roll Dice (1-6)", command=self.handle_roll)
        self.roll_btn.grid(row=0, column=0, padx=6)
        self.dice_var = tk.StringVar(value="-")
        ttk.Label(ctrl, text="Dice result:").grid(row=0, column=1, sticky="e")
        ttk.Label(ctrl, textvariable=self.dice_var, width=4).grid(row=0, column=2, sticky="w")
        ttk.Button(ctrl, text="New Round", command=self.new_round).grid(row=0, column=3, padx=8)

    def init_game(self):
        try:
            self.game = GameState(self.N)
        except Exception as e:
            messagebox.showerror("Board Error", f"Could not create board: {e}")
            return
        self.draw_board()
        self.draw_token()

    def draw_board(self):
        self.canvas.delete("all")
        N = self.N
        cs = CANVAS_SIZE
        self.cell_size = cs / N
        font_size = max(8, int(self.cell_size * 0.15))
        for r in range(N):
            for c in range(N):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                fill = "white" if ((r + c) % 2 == 0) else "#f0f0f0"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="black")
                cell_num = self.game.cell_rc_map[(r, c)]
                self.canvas.create_text(x1 + 6, y2 - 6, anchor="sw", text=str(cell_num), font=("Arial", font_size))

        # ladders (green) and snakes (red)
        for bottom, top in self.game.ladders.items():
            self._draw_connection(bottom, top, color="green", label="L")
        for head, tail in self.game.snakes.items():
            self._draw_connection(head, tail, color="red", label="S")

    def _coord_center_of_cell(self, cell_num: int) -> Tuple[float,float]:
        r, c = self.game.num_to_rc[cell_num]
        x = c * self.cell_size + self.cell_size/2
        y = r * self.cell_size + self.cell_size/2
        return x, y

    def _draw_connection(self, a: int, b: int, color: str = "green", label: str = ""):
        x1, y1 = self._coord_center_of_cell(a)
        x2, y2 = self._coord_center_of_cell(b)
        self.canvas.create_line(x1, y1, x2, y2, width=3, fill=color, arrow=tk.LAST)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        self.canvas.create_text(mx, my, text=label, font=("Arial", 10, "bold"), fill=color)

    def draw_token(self):
        if getattr(self, "token_id", None):
            self.canvas.delete(self.token_id)
        x, y = self._coord_center_of_cell(self.game.position)
        r = max(6, self.cell_size * 0.18)
        self.token_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="blue", outline="black")
        self.pos_label.config(text=f"Position: {self.game.position}")

    def handle_roll(self):
        if self.game.is_win():
            messagebox.showinfo("Round finished", "Round already finished.")
            return
        dice = self.game.roll_dice()
        self.dice_var.set(str(dice))
        start, final = self.game.move_by_dice(dice)
        self.animate_movement(start, final)
        if self.game.is_win():
            duration = time.perf_counter() - self.game.round_start_time
            messagebox.showinfo("You Win!", f"Reached {self.game.max_cell} in {len(self.game.history)} moves.\nTime: {duration:.2f}s")
            self.on_game_end(self.game, duration)

    def animate_movement(self, start: int, final: int):
        if final == start:
            self.draw_token()
            return
        step = 1 if final > start else -1
        for cell in range(start + step, final + step, step):
            x, y = self._coord_center_of_cell(cell)
            r = max(6, self.cell_size * 0.18)
            self.canvas.coords(self.token_id, x - r, y - r, x + r, y + r)
            self.update()
            time.sleep(0.09)
        self.draw_token()

    def new_round(self):
        self.game.reset()
        self.draw_board()
        self.draw_token()
        self.dice_var.set("-")

class ResultScreen(ttk.Frame):
    def __init__(self, parent, player_name, game_state: GameState, duration_s: float, on_restart):
        super().__init__(parent)
        self.player_name = player_name
        self.game_state = game_state
        self.duration = duration_s
        self.on_restart = on_restart
        self.build()

    def build(self):
        ttk.Label(self, text="Round Complete", font=("Helvetica", 16, "bold")).pack(pady=12)
        ttk.Label(self, text=f"Player: {self.player_name}").pack()
        ttk.Label(self, text=f"Board size: {self.game_state.N}").pack()
        ttk.Label(self, text=f"Moves: {len(self.game_state.history)}").pack()
        ttk.Label(self, text=f"Duration: {self.duration:.2f}s").pack()
        ladders_txt = ", ".join(f"{k}->{v}" for k, v in self.game_state.ladders.items())
        snakes_txt = ", ".join(f"{k}->{v}" for k, v in self.game_state.snakes.items())
        ttk.Label(self, text=f"Ladders: {ladders_txt}").pack(pady=4)
        ttk.Label(self, text=f"Snakes: {snakes_txt}").pack(pady=4)
        ttk.Button(self, text="Play Again", command=self.on_restart).pack(pady=8)
        ttk.Button(self, text="Quit", command=self.quit_app).pack(pady=8)

    def quit_app(self):
        self.master.quit()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake & Ladder")
        self.geometry("760x760")
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.player_name = ""
        self.N = 8
        self.show_start()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_start(self):
        self.clear_frame()
        frame = StartScreen(self.container, self.start_game)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def start_game(self, player_name: str, N: int):
        self.player_name = player_name
        self.N = N
        self.show_board()

    def show_board(self):
        self.clear_frame()
        frame = BoardScreen(self.container, self.player_name, self.N, on_game_end=self.handle_game_end)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def handle_game_end(self, game_state: GameState, duration: float):
        self.clear_frame()
        frame = ResultScreen(self.container, self.player_name, game_state, duration, on_restart=self.show_start)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame
