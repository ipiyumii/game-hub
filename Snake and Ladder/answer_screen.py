"""
Answer Screen - Ask player to guess minimum moves with 3 choices
"""
import tkinter as tk
from tkinter import messagebox
from styles import GameStyles

class AnswerScreen:
    """Screen where player chooses minimum moves"""
    
    def __init__(self, root, game_state, choices, correct_answer, algorithm_results, on_answer_callback):
        """
        Initialize answer screen
        
        Args:
            root: Tkinter root window
            game_state: GameState object
            choices: List of 3 answer choices
            correct_answer: Correct answer
            algorithm_results: Results from both algorithms
            on_answer_callback: Callback when answer is selected
        """
        self.root = root
        self.game_state = game_state
        self.choices = sorted(choices)  # Sort for better display
        self.correct_answer = correct_answer
        self.algorithm_results = algorithm_results
        self.on_answer_callback = on_answer_callback
        self.styles = GameStyles()
        
        self.frame = None
        self.selected_choice = None
    
    def show(self):
        """Display the answer screen"""
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
            text="🎯 ALGORITHM CHALLENGE",
            font=self.styles.get_font('title'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('warning')
        ).pack(pady=(0, 20))
        
        # Question
        board_info = self.game_state.get_board_info()
        question_text = f"What is the MINIMUM number of dice throws\nneeded to reach cell {board_info['total_cells']}?"
        
        tk.Label(
            container,
            text=question_text,
            font=self.styles.get_font('subtitle'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light'),
            justify=tk.CENTER
        ).pack(pady=(0, 40))
        
        # Choice buttons frame
        choices_frame = tk.Frame(container, bg=self.styles.get_color('bg_main'))
        choices_frame.pack(pady=20)
        
        # Create choice buttons
        for i, choice in enumerate(self.choices):
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
        
        # Algorithm performance info
        tk.Label(
            container,
            text="⚡ Algorithms calculated the answer for you!",
            font=self.styles.get_font('normal'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_muted')
        ).pack(pady=(30, 5))
        
        perf_text = (f"BFS: {self.algorithm_results['bfs']['time']*1000:.2f}ms  •  "
                    f"Dijkstra: {self.algorithm_results['dijkstra']['time']*1000:.2f}ms")
        
        tk.Label(
            container,
            text=perf_text,
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('info')
        ).pack()
    
    def _on_choice_selected(self, choice):
        """Handle choice selection"""
        self.selected_choice = choice
        
        # Check if correct
        is_correct = (choice == self.correct_answer)
        
        # Show result
        if is_correct:
            result_msg = f"🎉 CORRECT!\n\nThe minimum number of moves is {self.correct_answer}!"
            messagebox.showinfo("Correct Answer!", result_msg, parent=self.root)
        else:
            result_msg = f"❌ Wrong Answer!\n\nYou chose: {choice} moves\nCorrect answer: {self.correct_answer} moves"
            messagebox.showwarning("Incorrect", result_msg, parent=self.root)
        
        # Callback with result
        self.on_answer_callback(choice, is_correct)
    
    def destroy(self):
        """Destroy the screen"""
        if self.frame:
            self.frame.destroy()