import tkinter as tk
from styles import GameStyles
import random

class AnswerChoiceScreen:
     
    def __init__(self, root, game_state, correct_answer, on_choice_callback):
       
        self.root = root
        self.game_state = game_state
        self.correct_answer = correct_answer
        self.on_choice_callback = on_choice_callback
        self.styles = GameStyles()
        
        self.frame = None
        self.choices = self._generate_choices()
    
    def _generate_choices(self):
        
        choices = [self.correct_answer]
        
        offset1 = random.randint(2, max(3, self.correct_answer // 3))
        wrong1 = self.correct_answer + offset1
        choices.append(wrong1)
        
        if self.correct_answer > 3:
            offset2 = random.randint(1, min(self.correct_answer - 1, self.correct_answer // 2))
            wrong2 = self.correct_answer - offset2
        else:
            offset2 = random.randint(3, 5)
            wrong2 = self.correct_answer + offset2
        
        choices.append(wrong2)
        
        random.shuffle(choices)
        return sorted(choices)
    
    def show(self):
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.frame = tk.Frame(self.root, bg=self.styles.get_color('bg_main'))
        self.frame.pack(fill=tk.BOTH, expand=True)
        
       
        top = tk.Frame(self.frame, bg=self.styles.get_color('bg_main'))
        top.pack(fill=tk.X, pady=(20, 8))
        
        emoji_lbl = tk.Label(
            top,
            text="🤔",
            font=('Arial', 70),
            bg=self.styles.get_color('bg_main')
        )
        emoji_lbl.pack(anchor='n')
        
        title_lbl = tk.Label(
            top,
            text="MAKE YOUR PREDICTION",
            font=('Arial', 32, 'bold'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('warning')
        )
        title_lbl.pack(anchor='n', pady=(6, 6))
        
        # Main content area
        content = tk.Frame(self.frame, bg=self.styles.get_color('bg_main'))
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Left column (info box)
        left_col = tk.Frame(content, bg=self.styles.get_color('bg_main'))
        left_col.pack(side=tk.LEFT, fill=tk.Y, padx=(120, 80),pady=60)  
        
        info_frame = tk.Frame(
            left_col,
            bg=self.styles.get_color('bg_dark'),
            relief=tk.RAISED,
            bd=2,
            padx=18,
            pady=14,
            width=360
        )
        info_frame.pack(anchor='nw', fill=tk.Y)
        
        board_info = self.game_state.get_board_info()
        
        info_grid = tk.Frame(info_frame, bg=self.styles.get_color('bg_dark'))
        info_grid.pack()
        
        info_data = [
            ("👤 Player", self.game_state.player_name),
            ("📏 Board Size", f"{board_info['board_size']}×{board_info['board_size']}"),
            ("🎯 Total Cells", str(board_info['total_cells'])),
            ("🐍 Snakes", str(board_info['num_snakes'])),
            ("🪜 Ladders", str(board_info['num_ladders']))
        ]
        
        for i, (label, value) in enumerate(info_data):
            tk.Label(
                info_grid, 
                text=label,
                font=('Arial', 13),
                bg=self.styles.get_color('bg_dark'),
                fg=self.styles.get_color('text_light'),
                anchor='w',
                width=16
            ).grid(row=i, column=0, sticky='w', padx=(0, 16), pady=6)
            
            tk.Label(
                info_grid, 
                text=value,
                font=('Arial', 13, 'bold'),
                bg=self.styles.get_color('bg_dark'),
                fg=self.styles.get_color('success'),
                anchor='e',
                width=20
            ).grid(row=i, column=1, sticky='e', pady=6)
        
        # Right column (question + choices)
        right_col = tk.Frame(content, bg=self.styles.get_color('bg_main'))
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        question_area = tk.Frame(right_col, bg=self.styles.get_color('bg_main'))
        question_area.pack(fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        
        tk.Label(
            question_area,
            text="What is the MINIMUM number of dice throws\nneeded to reach the last cell?",
            font=('Arial', 15, 'bold'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light'),
            justify=tk.CENTER
        ).pack(pady=(6, 18))
        
        choices_frame = tk.Frame(question_area, bg=self.styles.get_color('bg_main'))
        choices_frame.pack(pady=6)
        
        for choice in self.choices:
            btn = tk.Button(
                choices_frame,
                text=f"🎲 {choice} moves",
                font=('Arial', 18, 'bold'),
                bg=self.styles.get_color('btn_primary'),
                fg='white',
                width=20,
                height=2,
                cursor='hand2',
                relief=tk.RAISED,
                bd=4,
                activebackground=self.styles.get_color('btn_hover'),
                command=lambda c=choice: self._on_choice_selected(c)
            )
            btn.pack(pady=10)
        
        footer = tk.Frame(right_col, bg=self.styles.get_color('bg_main'))
        footer.pack(fill=tk.X, pady=(10, 18))
        
        tk.Label(
            footer,
            text="⚡ Algorithms (BFS & Dijkstra) have calculated the answer",
            font=('Arial', 11),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('info')
        ).pack()
        
        tk.Label(
            footer,
            text="Choose carefully! Then play the game to verify.",
            font=('Arial', 10),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_muted')
        ).pack()
    
    def _on_choice_selected(self, choice):
        print(f"\n🎯 Player predicted: {choice} moves")
        self.on_choice_callback(choice)
    
    def destroy(self):
        if self.frame:
            self.frame.destroy()
