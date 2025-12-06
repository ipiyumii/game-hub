from tkinter import messagebox
import math

class EightQueensUI:
    def __init__(self, root, player_name, tk=None):
        self.root = root
        self.player_name = player_name
        self.root.title("Eight Queens Puzzle ♕")
        self.root.geometry("1100x750")
        self.root.resizable(False, False)
        
        self.root.configure(bg='#1a1a2e')

        self.board_size = 8
        self.cell_size = 70
        self.queens = set()
        self.remaining_queens = 8  # Initialize remaining queens counter
        
        self.animation_time = 0
        
        self.bg_canvas = tk.Canvas(
            root,
            width=1100,
            height=750,
            highlightthickness=0
        )
        self.bg_canvas.place(x=0, y=0)

        # Canvas for Chessboard 
        self.board_offset_x = 70 
        self.board_offset_y = 130 
        
        self.canvas = tk.Canvas(
            root,
            width=self.board_size * self.cell_size,
            height=self.board_size * self.cell_size,
            highlightthickness=0,
            bd=0
        )
        self.canvas.place(x=self.board_offset_x, y=self.board_offset_y)
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.animate_background()

        style_btn = {
            "font": ("Arial", 12, "bold"),
            "relief": tk.FLAT,
            "bd": 0,
            "highlightthickness": 0,
            "activebackground": "#00adb5",
            "activeforeground": "white",
            "fg": "white",
            "cursor": "hand2",
            "width": 15,
            "height": 2
        }

        check_btn = tk.Button(
            root,
            text="Check Solution",
            command=self.check_solution,
            bg="#00adb5",
            **style_btn
        )
        check_btn.place(x=800, y=150) 

        # Clear Board button
        clear_btn = tk.Button(
            root,
            text="Clear Board",
            command=self.clear_board,
            bg="#393e46",
            **style_btn
        )
        clear_btn.place(x=800, y=210)

        # Draw initial board
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "white" if (row + col) % 2 == 0 else "gray20"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        # Draw queens
        for (r, c) in self.queens:
            self.draw_queen(r, c)
        
        # Update remaining queens counter
        self.update_remaining_queens()

    def draw_queen(self, row, col):
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        self.canvas.create_text(x, y, text="♕", font=("Arial", 28), fill="#DAA520")

    def on_click(self, event):
        #mouse click
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if (row, col) in self.queens:
            self.queens.remove((row, col))
        else:
            if len(self.queens) < 8:
                self.queens.add((row, col))
            else:
                messagebox.showinfo("Limit", "You can only place 8 queens.")

        self.draw_board()

    def check_solution(self):
        if len(self.queens) != 8:
            messagebox.showinfo("Incomplete", "You must place exactly 8 queens.")
            return

        # Validation logic
        rows = set()
        cols = set()
        diag1 = set()  # r - c
        diag2 = set()  # r + c

        for (r, c) in self.queens:
            if r in rows or c in cols or (r - c) in diag1 or (r + c) in diag2:
                messagebox.showinfo("Invalid", "Queens are attacking each other!")
                return
            rows.add(r)
            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)

        messagebox.showinfo("Success", f"Congratulations {self.player_name}! You solved the puzzle.")

    def clear_board(self):
        self.queens.clear()
        self.draw_board()
    
    def update_remaining_queens(self):
        remaining = 8 - len(self.queens)
  
        self.remaining_queens = remaining
    
    def animate_background(self):
        
        self.animation_time += 0.02
        
        r1 = int(135 + 30 * math.cos(self.animation_time))
        g1 = int(206 + 20 * math.sin(self.animation_time * 1.2))
        b1 = int(250 + 5 * math.cos(self.animation_time * 0.8))
        
        r2 = int(25 + 15 * math.sin(self.animation_time * 0.7))
        g2 = int(25 + 10 * math.cos(self.animation_time * 1.1))
        b2 = int(112 + 20 * math.sin(self.animation_time * 0.9))
        
        self.bg_canvas.delete("all")
        
        for y in range(0, 750, 5):
            ratio = y / 750
            r = int(r1 * (1 - ratio) + r2 * ratio)
            g = int(g1 * (1 - ratio) + g2 * ratio)
            b = int(b1 * (1 - ratio) + b2 * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.bg_canvas.create_rectangle(0, y, 1100, y+5, fill=color, outline=color)
        
        for i in range(15):
            x = (i * 60 + math.sin(self.animation_time + i) * 40) % 1100
            y = (i * 50 + math.cos(self.animation_time * 0.7 + i) * 30) % 750
            size = 2 + int(2 * math.sin(self.animation_time * 2 + i))
            
            alpha_val = int(100 + 50 * math.sin(self.animation_time * 3 + i))
            if alpha_val > 150:
                particle_color = "#ffffff"
            else:
                particle_color = "#dddddd"
            
            self.bg_canvas.create_oval(x-size, y-size, x+size, y+size, 
                                     fill=particle_color, outline=particle_color)
        
        self.bg_canvas.create_text(
            550, 30, 
            text="Eight Queens Puzzle ♕",
            font=("Arial", 20, "bold"),
            fill="Black"
        )
        
        self.bg_canvas.create_text(
            550, 70,  
            text=f"Player: {self.player_name}",
            font=("Arial", 14),
            fill="black"
        )
        
        for row in range(self.board_size):
            y_pos = self.board_offset_y + row * self.cell_size + self.cell_size // 2
            self.bg_canvas.create_text(
                self.board_offset_x - 20, 
                y_pos, 
                text=str(row), 
                font=("Arial", 12, "bold"), 
                fill="white"
            )
        
        for col in range(self.board_size):
            x_pos = self.board_offset_x + col * self.cell_size + self.cell_size // 2
            self.bg_canvas.create_text(
                x_pos, 
                self.board_offset_y - 20, 
                text=str(col), 
                font=("Arial", 12, "bold"), 
                fill="white"
            )
        
        remaining = getattr(self, 'remaining_queens', 8)
        self.bg_canvas.create_text(
            870, 300,
            text=f"Remaining Queens: {remaining}",
            font=("Arial", 11, "bold"),
            fill="white"
        )
        
        self.root.after(50, self.animate_background)