"""
Snake and Ladder Game - COMPLETE FINAL VERSION
With Report Generator (15 rounds)
"""

import tkinter as tk
from tkinter import messagebox

from start_screen import StartScreen
from answer_choice_screen import AnswerChoiceScreen
from game_board_ui import GameBoardUI
from result_screen import ResultScreen
from game_state import GameState
from bfs_algorithm import BFSAlgorithm
from dijkstra_algorithm import DijkstraAlgorithm
from firebase_database import FirebaseDatabase
from report_generator import ReportGenerator
from styles import GameStyles

class SnakeLadderGame:
    """Main game controller with report generation"""
    
    def __init__(self):
        """Initialize the game"""
        self.root = tk.Tk()
        self.root.title("🎲 Snake and Ladder Game - Algorithm Challenge")
        
        styles = GameStyles()
        window_width = styles.get_size('window_width')
        window_height = styles.get_size('window_height')
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg=styles.get_color('bg_main'))
        
        # Initialize Firebase
        print("\n🔥 Initializing Firebase...")
        self.firebase = FirebaseDatabase()
        
        if self.firebase.enabled:
            self.firebase.test_connection()
        
        # Initialize Report Generator
        print("\n📊 Initializing Report Generator...")
        self.report_gen = ReportGenerator()
        
        # Game state
        self.game_state = GameState()
        self.current_screen = None
        
        # Game data
        self.algorithm_results = None
        self.correct_answer = None
        self.player_choice = None
        
        self.show_start_screen()
    
    def show_start_screen(self):
        """Display the start screen"""
        print("\n" + "="*70)
        print("🎲 SNAKE AND LADDER GAME")
        print("="*70)
        print(f"📊 Rounds played: {self.report_gen.get_round_count()}/15")
        
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = StartScreen(
            self.root,
            on_start_callback=self.on_game_start
        )
        self.current_screen.show()
    
    def on_game_start(self, player_name, board_size):
        """STEP 1: Generate board and run algorithms"""
        try:
            print(f"\n{'='*70}")
            print(f"🎮 STARTING GAME")
            print(f"{'='*70}")
            print(f"👤 Player: {player_name}")
            print(f"📏 Board: {board_size}×{board_size}")
            
            self.game_state.start_new_game(player_name, board_size)
            
            print(f"\n🧮 RUNNING ALGORITHMS...")
            print("-" * 70)
            
            bfs = BFSAlgorithm(self.game_state.board)
            bfs_moves, bfs_time = bfs.find_minimum_moves()
            
            dijkstra = DijkstraAlgorithm(self.game_state.board)
            dijkstra_moves, dijkstra_time = dijkstra.find_minimum_moves()
            
            self.algorithm_results = {
                'bfs': {'moves': bfs_moves, 'time': bfs_time},
                'dijkstra': {'moves': dijkstra_moves, 'time': dijkstra_time}
            }
            
            self.correct_answer = bfs_moves
            
            print("-" * 70)
            print(f"✅ COMPLETE - Minimum: {self.correct_answer}")
            print("="*70)
            
            self.show_answer_choice_screen()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed:\n{str(e)}", parent=self.root)
    
    def show_answer_choice_screen(self):
        """STEP 2: Show answer choice screen"""
        print(f"\n🎯 SHOWING ANSWER CHOICES...")
        
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = AnswerChoiceScreen(
            self.root,
            self.game_state,
            self.correct_answer,
            on_choice_callback=self.on_player_choice
        )
        self.current_screen.show()
    
    def on_player_choice(self, choice):
        """STEP 3: Player made prediction"""
        self.player_choice = choice
        
        print(f"\n{'='*70}")
        print(f"🎯 PREDICTION")
        print(f"{'='*70}")
        print(f"   Predicted: {self.player_choice}")
        print(f"   Actual: {self.correct_answer}")
        print(f"   {'✅ CORRECT!' if self.player_choice == self.correct_answer else '❌ INCORRECT'}")
        print("="*70)
        
        self.show_game_board()
    
    def show_game_board(self):
        """STEP 4: Display game board"""
        print(f"\n📊 SHOWING GAME BOARD...")
        
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = GameBoardUI(
            self.root,
            self.game_state,
            on_back_callback=self.on_back_to_start,
            on_game_complete_callback=self.on_game_complete
        )
        self.current_screen.show()
    
    def on_game_complete(self):
        """STEP 5: Game finished - Save and generate report"""
        print(f"\n{'='*70}")
        print(f"🏁 GAME COMPLETED")
        print(f"{'='*70}")
        print(f"   Dice rolls: {self.game_state.dice_rolls}")
        
        is_correct = (self.player_choice == self.correct_answer)
        
        # Add to report data (both correct and incorrect)
        report_generated = self.report_gen.add_game_round(
            player_name=self.game_state.player_name,
            board_size=self.game_state.board_size,
            player_choice=self.player_choice,
            correct_answer=self.correct_answer,
            is_correct=is_correct,
            bfs_time=self.algorithm_results['bfs']['time'],
            dijkstra_time=self.algorithm_results['dijkstra']['time'],
            dice_rolls=self.game_state.dice_rolls
        )
        
        # Save to Firebase (only correct answers)
        if is_correct and self.firebase.enabled:
            print(f"\n💾 SAVING TO FIREBASE...")
            print("-" * 70)
            
            session_id = self.firebase.save_game_session(
                player_name=self.game_state.player_name,
                board_size=self.game_state.board_size,
                snakes=self.game_state.board.snakes,
                ladders=self.game_state.board.ladders,
                player_choice=self.player_choice,
                correct_answer=self.correct_answer,
                bfs_time=self.algorithm_results['bfs']['time'],
                dijkstra_time=self.algorithm_results['dijkstra']['time']
            )
            
            if session_id:
                self.firebase.save_player_details(
                    player_name=self.game_state.player_name,
                    board_size=self.game_state.board_size,
                    correct_answer=self.correct_answer,
                    session_id=session_id
                )
            
            print("-" * 70)
            print(f"✅ DATA SAVED")
        
        print("="*70)
        
        # Show result screen
        self.show_result_screen()
        
        # Show report notification if generated
        if report_generated:
            self.root.after(1000, lambda: messagebox.showinfo(
                "Report Generated!",
                "15 rounds complete!\n\n"
                "Performance report has been generated in:\n"
                "game_reports/ folder\n\n"
                "Check for PNG charts, JSON and CSV files!",
                parent=self.root
            ))
    
    def show_result_screen(self):
        """STEP 6: Show result screen"""
        print(f"\n🏆 SHOWING RESULT...")
        
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = ResultScreen(
            self.root,
            self.game_state,
            self.player_choice,
            self.correct_answer,
            self.algorithm_results,
            on_play_again_callback=self.on_play_again,
            on_back_callback=self.on_back_to_start
        )
        self.current_screen.show()
    
    def on_play_again(self):
        """Play again"""
        print(f"\n🔄 RESTARTING...")
        self.game_state.reset_game()
        self.player_choice = None
        self.correct_answer = None
        self.algorithm_results = None
        self.show_start_screen()
    
    def on_back_to_start(self):
        """Back to start"""
        print(f"\n⬅ BACK TO START...")
        self.game_state.reset_game()
        self.player_choice = None
        self.correct_answer = None
        self.algorithm_results = None
        self.show_start_screen()
    
    def run(self):
        """Start the game"""
        print("\n" + "="*70)
        print("🚀 SNAKE AND LADDER GAME - FINAL VERSION")
        print("="*70)
        print("\n📋 Features:")
        print("   ✅ BFS & Dijkstra algorithms")
        print("   ✅ Firebase Firestore database")
        print("   ✅ Report Generator (15 rounds)")
        print("   ✅ Performance charts (PNG)")
        print("   ✅ Data export (JSON, CSV)")
        
        if self.firebase.enabled:
            print("\n🔥 Firebase: CONNECTED ✅")
        else:
            print("\n🔥 Firebase: NOT CONNECTED ⚠️")
        
        print(f"\n📊 Report Status: {self.report_gen.get_round_count()}/15 rounds")
        print("="*70 + "\n")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        """Handle window close"""
        print("\n" + "="*70)
        print("👋 THANKS FOR PLAYING!")
        print(f"📊 Rounds completed: {self.report_gen.get_round_count()}/15")
        print("="*70 + "\n")
        self.root.destroy()


def main():
    """Main function"""
    try:
        game = SnakeLadderGame()
        game.run()
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()