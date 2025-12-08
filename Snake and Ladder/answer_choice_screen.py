"""
Answer Choice Screen - Player predicts minimum moves BEFORE playing
"""
import tkinter as tk
from styles import GameStyles
import random

class AnswerChoiceScreen:
    """Screen where player predicts minimum moves before playing"""
    
    def __init__(self, root, game_state, correct_answer, on_choice_callback):
        """
        Initialize answer choice screen
        
        Args:
            root: Tkinter root window
            game_state: GameState object
            correct_answer: Actual minimum moves (calculated by algorithms)
            on_choice_callback: Callback when choice is selected
        """
        self.root = root
        self.game_state = game_state
        self.correct_answer = correct_answer
        self.on_choice_callback = on_choice_callback
        self.styles = GameStyles()
        
        self.frame = None
        self.choices = self._generate_choices()
    
    def _generate_choices(self):
        """Generate 3 answer choices including the correct one"""
        choices = [self.correct_answer]
        
        # Generate wrong answer 1 (higher)
        offset1 = random.randint(2, max(3, self.correct_answer // 3))
        wrong1 = self.correct_answer + offset1
        choices.append(wrong1)
        
        # Generate wrong answer 2 (lower or higher)
        if self.correct_answer > 3:
            offset2 = random.randint(1, min(self.correct_answer - 1, self.correct_answer // 2))
            wrong2 = self.correct_answer - offset2
        else:
            offset2 = random.randint(3, 5)
            wrong2 = self.correct_answer + offset2
        
        choices.append(wrong2)
        
        # Shuffle and sort
        random.shuffle(choices)
        return sorted(choices)
    
    def show(self):
        """Display the answer choice screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.frame = tk.Frame(self.root, bg=self.styles.get_color('bg_main'))
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container
        container = tk.Frame(self.frame, bg=self.styles.get_color('bg_main'))
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        tk.Label(
            container,
            text="🎯 PREDICT THE MINIMUM MOVES",
            font=self.styles.get_font('title'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('warning')
        ).pack(pady=(0, 20))
        
        # Player info
        board_info = self.game_state.get_board_info()
        info_text = (f"Player: {self.game_state.player_name}\n"
                    f"Board: {board_info['board_size']}×{board_info['board_size']} "
                    f"({board_info['total_cells']} cells)")
        
        tk.Label(
            container,
            text=info_text,
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light'),
            justify=tk.CENTER
        ).pack(pady=(0, 30))
        
        # Question
        question_text = (f"What is the MINIMUM number of dice throws\n"
                        f"needed to reach cell {board_info['total_cells']}?\n\n"
                        f"Make your prediction:")
        
        tk.Label(
            container,
            text=question_text,
            font=self.styles.get_font('subtitle'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light'),
            justify=tk.CENTER
        ).pack(pady=(0, 40))
        
        # Choice buttons
        choices_frame = tk.Frame(container, bg=self.styles.get_color('bg_main'))
        choices_frame.pack(pady=20)
        
        for choice in self.choices:
            btn = tk.Button(
                choices_frame,
                text=f"{choice} moves",
                font=self.styles.get_font('choice'),
                bg=self.styles.get_color('btn_primary'),
                fg='white',
                width=15,
                height=2,
                cursor='hand2',
                relief=tk.RAISED,
                bd=4,
                command=lambda c=choice: self._on_choice_selected(c)
            )
            btn.pack(pady=15)
        
        # Info text
        tk.Label(
            container,
            text="Choose wisely! After playing, we'll check your prediction.",
            font=self.styles.get_font('normal'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_muted')
        ).pack(pady=(30, 5))
        
        tk.Label(
            container,
            text="🧮 Algorithms: BFS & Dijkstra already calculated the answer",
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('info')
        ).pack()
    
    def _on_choice_selected(self, choice):
        """Handle choice selection"""
        print(f"\n🎯 Player predicted: {choice} moves")
        print(f"   Actual answer: {self.correct_answer} moves")
        
        # Callback to start the game
        self.on_choice_callback(choice)
    
    def destroy(self):
        """Destroy the screen"""
        if self.frame:
            self.frame.destroy()