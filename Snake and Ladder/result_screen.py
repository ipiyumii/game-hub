"""
Result Screen - Shows Win/Lose/Draw based on prediction accuracy
Layout: Details (left) | Summary & Actions (right)
"""
import tkinter as tk
from styles import GameStyles

class ResultScreen:                                                                                                                                                                 
    """Shows game result - Left details panel, right summary + actions"""
    
    def __init__(self, root, game_state, player_choice, correct_answer, 
                 algorithm_results, on_play_again_callback, on_back_callback=None):
        """
        Initialize result screen
        
        Args:
            root: Tkinter root window
            game_state: GameState object
            player_choice: Player's predicted moves
            correct_answer: Actual minimum moves
            algorithm_results: Results from BFS and Dijkstra
            on_play_again_callback: Callback for play again
            on_back_callback: Callback for back to start (optional)
        """
        self.root = root
        self.game_state = game_state
        self.player_choice = player_choice
        self.correct_answer = correct_answer
        self.algorithm_results = algorithm_results or {
            'bfs': {'time': 0},
            'dijkstra': {'time': 0}
        }
        self.on_play_again_callback = on_play_again_callback
        self.on_back_callback = on_back_callback
        self.styles = GameStyles()
        
        self.frame = None
        self.determine_result()
    
    def determine_result(self):
        """Determine win/lose/draw based on prediction"""
        if self.player_choice == self.correct_answer:
            self.result_type = 'win'
            self.is_correct = True
        else:
            self.result_type = 'lose'
            self.is_correct = False
    
    def show(self):
        """Display the result screen with left details and right actions"""
        print("\n🏆 Displaying Result Screen...")
        print(f"   Player Choice: {self.player_choice}")
        print(f"   Correct Answer: {self.correct_answer}")
        print(f"   Result Type: {self.result_type}")
        
        # Destroy existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Root frame
        self.frame = tk.Frame(self.root, bg=self.styles.get_color('bg_main'))
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Main container with some padding
        main_container = tk.Frame(self.frame, bg=self.styles.get_color('bg_main'))
        main_container.pack(fill=tk.BOTH, expand=True, padx=24, pady=20)
        
        # -----------------------
        # LEFT PANEL - DETAILS
        # -----------------------
        left_width = 520  # reduced width
        details_panel = tk.Frame(
            main_container,
            bg=self.styles.get_color('bg_dark'),
            bd=3,
            relief=tk.RIDGE,
            width=left_width,
            padx=16,
            pady=16
        )
        details_panel.pack(side=tk.LEFT, fill=tk.Y, expand=False)
        details_panel.pack_propagate(False)   # keep exact size
        
        # Heading inside details
        heading = tk.Label(
            details_panel,
            text="📋 RESULT DETAILS",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_light')
        )
        heading.pack(anchor='w', pady=(0,12))
        
        # Player & board info
        player_label = tk.Label(
            details_panel,
            text=f"🎮 Player: {self.game_state.player_name}",
            font=self.styles.get_font('normal'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_light'),
            anchor='w'
        )
        player_label.pack(fill=tk.X, pady=6)
        
        board_info = self.game_state.get_board_info()
        board_label = tk.Label(
            details_panel,
            text=f"📍 Board: {board_info['board_size']}×{board_info['board_size']}  —  {board_info['total_cells']} cells",
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_muted'),
            anchor='w',
            wraplength=left_width - 40,
            justify='left'
        )
        board_label.pack(fill=tk.X, pady=4)
        
        # Compact separator
        sep = tk.Frame(details_panel, height=2, bg=self.styles.get_color('border_light'))
        sep.pack(fill=tk.X, pady=12)
        
        # Prediction comparison grid (use frames to align left/right)
        comp_frame = tk.Frame(details_panel, bg=self.styles.get_color('bg_dark'))
        comp_frame.pack(fill=tk.X, pady=6)
        
        # Row helper
        def _add_row(parent, label_text, value_text, value_fg=None, value_font=None):
            row = tk.Frame(parent, bg=self.styles.get_color('bg_dark'))
            row.pack(fill=tk.X, pady=6)
            lbl = tk.Label(
                row,
                text=label_text,
                font=self.styles.get_font('small'),
                bg=self.styles.get_color('bg_dark'),
                fg=self.styles.get_color('text_light'),
                anchor='w'
            )
            lbl.pack(side=tk.LEFT)
            val = tk.Label(
                row,
                text=value_text,
                font=value_font or ('Arial', 14, 'bold'),
                bg=self.styles.get_color('bg_dark'),
                fg=value_fg or self.styles.get_color('text_light'),
                anchor='e'
            )
            val.pack(side=tk.RIGHT)
            return row
        
        _add_row(comp_frame, "Your Prediction:", f"{self.player_choice} moves", value_fg=self.styles.get_color('warning'))
        _add_row(comp_frame, "Correct Answer:", f"{self.correct_answer} moves", value_fg=self.styles.get_color('success'))
        
        difference = abs(self.player_choice - self.correct_answer)
        diff_color = self.styles.get_color('success') if difference == 0 else self.styles.get_color('danger')
        _add_row(comp_frame, "Difference:", f"{difference} moves", value_fg=diff_color, value_font=('Arial', 16, 'bold'))
        
        # compact separator
        sep2 = tk.Frame(details_panel, height=2, bg=self.styles.get_color('border_light'))
        sep2.pack(fill=tk.X, pady=12)
        
        # Game performance (dice rolls)
        perf_frame = tk.Frame(details_panel, bg=self.styles.get_color('bg_dark'))
        perf_frame.pack(fill=tk.X, pady=6)
        rolls_label = tk.Label(
            perf_frame,
            text="Dice Rolls Used:",
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_light'),
            anchor='w'
        )
        rolls_label.pack(side=tk.LEFT)
        rolls_val = tk.Label(
            perf_frame,
            text=f"{self.game_state.dice_rolls} rolls",
            font=('Arial', 14, 'bold'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('info'),
            anchor='e'
        )
        rolls_val.pack(side=tk.RIGHT)
        
        # Algorithm performance area
        algo_title = tk.Label(
            details_panel,
            text="⚡ Algorithm Performance",
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('info'),
            anchor='w'
        )
        algo_title.pack(fill=tk.X, pady=(12,6))
        
        algo_frame = tk.Frame(details_panel, bg=self.styles.get_color('bg_dark'))
        algo_frame.pack(fill=tk.X)
        bfs_time = f"{self.algorithm_results['bfs']['time']*1000:.2f}ms"
        dijkstra_time = f"{self.algorithm_results['dijkstra']['time']*1000:.2f}ms"
        _add_row(algo_frame, "BFS:", bfs_time, value_fg=self.styles.get_color('success'), value_font=('Arial', 13, 'bold'))
        _add_row(algo_frame, "Dijkstra:", dijkstra_time, value_fg=self.styles.get_color('success'), value_font=('Arial', 13, 'bold'))
        
        # Small spacer to push content up slightly
        tk.Frame(details_panel, bg=self.styles.get_color('bg_dark'), height=6).pack()
        
        # -----------------------
        # RIGHT PANEL - SUMMARY & ACTIONS
        # -----------------------
        # Top summary (icon/title)
        right_panel = tk.Frame(main_container, bg=self.styles.get_color('bg_main'))
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(18,0))
        
        summary_top = tk.Frame(right_panel, bg=self.styles.get_color('bg_main'))
        summary_top.pack(fill=tk.X, pady=(8,12))
        
        # Icon large, centered
        icon_text = "🎉" if self.result_type == 'win' else "❌"
        icon_color = self.styles.get_color('success') if self.result_type == 'win' else self.styles.get_color('danger')
        icon_lbl = tk.Label(
            summary_top,
            text=icon_text,
            font=('Arial', 120),
            bg=self.styles.get_color('bg_main')
        )
        icon_lbl.pack(anchor='n', pady=(6,8))
        
        title_text = "YOU WON!" if self.result_type == 'win' else "YOU LOST!"
        title_lbl = tk.Label(
            summary_top,
            text=title_text,
            font=('Arial', 36, 'bold'),
            bg=self.styles.get_color('bg_main'),
            fg=icon_color
        )
        title_lbl.pack(anchor='n')
        
        subtitle_text = "Prediction Correct! ✨" if self.result_type == 'win' else "Prediction Incorrect! Try again 😢"
        subtitle_lbl = tk.Label(
            summary_top,
            text=subtitle_text,
            font=('Arial', 14),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light'),
            wraplength=360,
            justify='center'
        )
        subtitle_lbl.pack(anchor='n', pady=(6,12))
        
        # Middle summary card showing compact stats
        summary_card = tk.Frame(right_panel, bg=self.styles.get_color('bg_dark'), bd=2, relief=tk.RIDGE, padx=14, pady=14)
        summary_card.pack(fill=tk.BOTH, expand=True, padx=(0,6), pady=(6,12))
        
        # Compact stats inside summary card
        stat_row = tk.Frame(summary_card, bg=self.styles.get_color('bg_dark'))
        stat_row.pack(fill=tk.X, pady=6)
        s1 = tk.Label(stat_row, text="Prediction:", font=self.styles.get_font('small'), bg=self.styles.get_color('bg_dark'), fg=self.styles.get_color('text_light'))
        s1.pack(side=tk.LEFT)
        s1v = tk.Label(stat_row, text=f"{self.player_choice} moves", font=('Arial', 13, 'bold'), bg=self.styles.get_color('bg_dark'), fg=self.styles.get_color('warning'))
        s1v.pack(side=tk.RIGHT)
        
        stat_row2 = tk.Frame(summary_card, bg=self.styles.get_color('bg_dark'))
        stat_row2.pack(fill=tk.X, pady=6)
        s2 = tk.Label(stat_row2, text="Minimum (BFS):", font=self.styles.get_font('small'), bg=self.styles.get_color('bg_dark'), fg=self.styles.get_color('text_light'))
        s2.pack(side=tk.LEFT)
        s2v = tk.Label(stat_row2, text=f"{self.correct_answer} moves", font=('Arial', 13, 'bold'), bg=self.styles.get_color('bg_dark'), fg=self.styles.get_color('success'))
        s2v.pack(side=tk.RIGHT)
        
        stat_row3 = tk.Frame(summary_card, bg=self.styles.get_color('bg_dark'))
        stat_row3.pack(fill=tk.X, pady=6)
        s3 = tk.Label(stat_row3, text="Rolls:", font=self.styles.get_font('small'), bg=self.styles.get_color('bg_dark'), fg=self.styles.get_color('text_light'))
        s3.pack(side=tk.LEFT)
        s3v = tk.Label(stat_row3, text=f"{self.game_state.dice_rolls}", font=('Arial', 13, 'bold'), bg=self.styles.get_color('bg_dark'), fg=self.styles.get_color('info'))
        s3v.pack(side=tk.RIGHT)
        
        # DB / message (prominent)
        if self.is_correct:
            db_msg = tk.Label(
                right_panel,
                text="✅ Saved to database (correct prediction).",
                font=('Arial', 12, 'bold'),
                bg=self.styles.get_color('bg_main'),
                fg=self.styles.get_color('success'),
                wraplength=380,
                justify='center'
            )
        else:
            db_msg = tk.Label(
                right_panel,
                text="⚠️ Prediction was incorrect. Results are not saved.",
                font=('Arial', 12, 'bold'),
                bg=self.styles.get_color('bg_main'),
                fg=self.styles.get_color('warning'),
                wraplength=380,
                justify='center'
            )
        db_msg.pack(pady=(6,12))
        
        # Buttons area (right aligned)
        btn_frame = tk.Frame(right_panel, bg=self.styles.get_color('bg_main'))
        btn_frame.pack(fill=tk.X, pady=(8,18))
        
        # Play Again (primary)
        play_btn = tk.Button(
            btn_frame,
            text="🎮 Play Again",
            font=self.styles.get_font('button'),
            bg=self.styles.get_color('btn_success'),
            fg='white',
            padx=26,
            pady=12,
            bd=3,
            relief=tk.RAISED,
            command=self.on_play_again_callback,
            cursor='hand2'
        )
        play_btn.pack(side=tk.LEFT, padx=8)
        
        
        
        # Small help / hint at bottom of right panel
        hint = tk.Label(
            right_panel,
            text="Tip: Try different predictions to see how close your guess is to the algorithm result.",
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_muted'),
            wraplength=380,
            justify='center'
        )
        hint.pack(side=tk.BOTTOM, pady=(12,6))
        
        print("✅ Result screen displayed successfully")
    
    def destroy(self):
        """Destroy the screen"""
        if self.frame:
            self.frame.destroy()
