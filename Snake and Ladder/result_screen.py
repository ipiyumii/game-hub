"""
Result Screen - Shows Win/Lose/Draw after game completes
"""
import tkinter as tk
from styles import GameStyles

class ResultScreen:
    """Shows game result - Win, Lose, or Draw"""
    
    def __init__(self, root, game_state, player_choice, correct_answer, 
                 algorithm_results, on_play_again_callback):
        """
        Initialize result screen
        
        Args:
            root: Tkinter root window
            game_state: GameState object
            player_choice: Player's predicted moves
            correct_answer: Actual minimum moves
            algorithm_results: Results from BFS and Dijkstra
            on_play_again_callback: Callback for play again
        """
        self.root = root
        self.game_state = game_state
        self.player_choice = player_choice
        self.correct_answer = correct_answer
        self.algorithm_results = algorithm_results
        self.on_play_again_callback = on_play_again_callback
        self.styles = GameStyles()
        
        self.frame = None
        self.is_correct = (player_choice == correct_answer)
    
    def show(self):
        """Display the result screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.frame = tk.Frame(self.root, bg=self.styles.get_color('bg_main'))
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container
        container = tk.Frame(self.frame, bg=self.styles.get_color('bg_main'))
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Result icon and title
        if self.is_correct:
            icon = "🎉"
            title = "CORRECT ANSWER!"
            subtitle = "You Win! 🏆"
            color = self.styles.get_color('success')
        else:
            icon = "❌"
            title = "INCORRECT ANSWER"
            subtitle = "Better luck next time!"
            color = self.styles.get_color('danger')
        
        # Icon
        tk.Label(
            container,
            text=icon,
            font=('Arial', 80),
            bg=self.styles.get_color('bg_main')
        ).pack(pady=(0, 20))
        
        # Title
        tk.Label(
            container,
            text=title,
            font=self.styles.get_font('title'),
            bg=self.styles.get_color('bg_main'),
            fg=color
        ).pack(pady=(0, 10))
        
        # Subtitle
        tk.Label(
            container,
            text=subtitle,
            font=self.styles.get_font('subtitle'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light')
        ).pack(pady=(0, 40))
        
        # Results frame
        results_frame = tk.Frame(
            container,
            bg=self.styles.get_color('bg_dark'),
            relief=tk.RAISED,
            bd=3,
            padx=40,
            pady=30
        )
        results_frame.pack(pady=20)
        
        # Player info
        tk.Label(
            results_frame,
            text=f"Player: {self.game_state.player_name}",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_light')
        ).pack(pady=5)
        
        board_info = self.game_state.get_board_info()
        tk.Label(
            results_frame,
            text=f"Board: {board_info['board_size']}×{board_info['board_size']} ({board_info['total_cells']} cells)",
            font=self.styles.get_font('normal'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_muted')
        ).pack(pady=5)
        
        # Separator
        tk.Frame(
            results_frame,
            bg=self.styles.get_color('border_light'),
            height=2
        ).pack(fill=tk.X, pady=20)
        
        # Comparison
        comparison_data = [
            ("Your Prediction:", f"{self.player_choice} moves", 
             self.styles.get_color('warning')),
            ("Correct Answer:", f"{self.correct_answer} moves", 
             self.styles.get_color('success')),
            ("Dice Rolls Used:", f"{self.game_state.dice_rolls} rolls", 
             self.styles.get_color('info'))
        ]
        
        for label, value, color in comparison_data:
            row = tk.Frame(results_frame, bg=self.styles.get_color('bg_dark'))
            row.pack(fill=tk.X, pady=8)
            
            tk.Label(
                row,
                text=label,
                font=self.styles.get_font('normal'),
                bg=self.styles.get_color('bg_dark'),
                fg=self.styles.get_color('text_light'),
                anchor='w'
            ).pack(side=tk.LEFT, padx=(0, 20))
            
            tk.Label(
                row,
                text=value,
                font=('Arial', 14, 'bold'),
                bg=self.styles.get_color('bg_dark'),
                fg=color,
                anchor='e'
            ).pack(side=tk.RIGHT)
        
        # Separator
        tk.Frame(
            results_frame,
            bg=self.styles.get_color('border_light'),
            height=2
        ).pack(fill=tk.X, pady=20)
        
        # Algorithm performance
        tk.Label(
            results_frame,
            text="⚡ Algorithm Performance",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('info')
        ).pack(pady=(0, 10))
        
        algo_data = [
            ("BFS:", f"{self.algorithm_results['bfs']['time']*1000:.2f}ms"),
            ("Dijkstra:", f"{self.algorithm_results['dijkstra']['time']*1000:.2f}ms")
        ]
        
        for label, value in algo_data:
            row = tk.Frame(results_frame, bg=self.styles.get_color('bg_dark'))
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(
                row,
                text=label,
                font=self.styles.get_font('small'),
                bg=self.styles.get_color('bg_dark'),
                fg=self.styles.get_color('text_light'),
                anchor='w'
            ).pack(side=tk.LEFT, padx=(0, 20))
            
            tk.Label(
                row,
                text=value,
                font=self.styles.get_font('small'),
                bg=self.styles.get_color('bg_dark'),
                fg=self.styles.get_color('success'),
                anchor='e'
            ).pack(side=tk.RIGHT)
        
        # Database info
        if self.is_correct:
            tk.Label(
                container,
                text="✅ Your result has been saved to the database!",
                font=self.styles.get_font('normal'),
                bg=self.styles.get_color('bg_main'),
                fg=self.styles.get_color('success')
            ).pack(pady=(30, 5))
        
        # Buttons
        buttons_frame = tk.Frame(container, bg=self.styles.get_color('bg_main'))
        buttons_frame.pack(pady=30)
        
        tk.Button(
            buttons_frame,
            text="🎮 Play Again",
            font=self.styles.get_font('button'),
            bg=self.styles.get_color('btn_success'),
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3,
            command=self.on_play_again_callback
        ).pack()
    
    def destroy(self):
        """Destroy the screen"""
        if self.frame:
            self.frame.destroy()