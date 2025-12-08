"""
Snake and Ladder Game - Complete with Firebase
Main entry point with full game flow

Game Flow:
1. Start Screen - Enter name and board size
2. Algorithms Calculate - BFS and Dijkstra find minimum moves
3. Answer Choice - Player predicts minimum moves (3 choices)
4. Play Game - Roll dice and reach last cell
5. Result Screen - Win/Lose/Draw (saves to Firebase if correct)
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

from styles import GameStyles

class SnakeLadderGame:
    """Main game controller with complete flow"""
    
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
        print("🎲 SNAKE AND LADDER GAME - ALGORITHM CHALLENGE")
        print("="*70)
        
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = StartScreen(
            self.root,
            on_start_callback=self.on_game_start
        )
        self.current_screen.show()
    
    def on_game_start(self, player_name, board_size):
        """
        Callback when game starts
        STEP 1: Generate board and run algorithms
        """
        try:
            print(f"\n{'='*70}")
            print(f"🎮 STARTING NEW GAME")
            print(f"{'='*70}")
            print(f"👤 Player: {player_name}")
            print(f"📏 Board Size: {board_size}×{board_size}")
            
            # Initialize game state (generates random board)
            self.game_state.start_new_game(player_name, board_size)
            
            # Run algorithms to calculate minimum moves
            print(f"\n🧮 RUNNING ALGORITHMS...")
            print("-" * 70)
            
            # BFS Algorithm
            bfs = BFSAlgorithm(self.game_state.board)
            bfs_moves, bfs_time = bfs.find_minimum_moves()
            
            # Dijkstra Algorithm
            dijkstra = DijkstraAlgorithm(self.game_state.board)
            dijkstra_moves, dijkstra_time = dijkstra.find_minimum_moves()
            
            # Store results
            self.algorithm_results = {
                'bfs': {'moves': bfs_moves, 'time': bfs_time},
                'dijkstra': {'moves': dijkstra_moves, 'time': dijkstra_time}
            }
            
            # Verify both algorithms give same result
            if bfs_moves != dijkstra_moves:
                print(f"⚠️  Warning: Algorithms gave different results!")
                print(f"   BFS: {bfs_moves}, Dijkstra: {dijkstra_moves}")
            
            self.correct_answer = bfs_moves
            
            print("-" * 70)
            print(f"✅ ALGORITHMS COMPLETE")
            print(f"   Minimum moves needed: {self.correct_answer}")
            print(f"   BFS time: {bfs_time*1000:.4f}ms")
            print(f"   Dijkstra time: {dijkstra_time*1000:.4f}ms")
            print("="*70)
            
            # STEP 2: Show answer choice screen
            self.show_answer_choice_screen()
            
        except Exception as e:
            print(f"❌ Error starting game: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Failed to start game:\n{str(e)}", parent=self.root)
    
    def show_answer_choice_screen(self):
        """
        STEP 2: Show answer choice screen (player predicts)
        """
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
        """
        STEP 3: Player made their prediction, now start the game
        """
        self.player_choice = choice
        
        print(f"\n{'='*70}")
        print(f"🎯 PLAYER PREDICTION")
        print(f"{'='*70}")
        print(f"   Player predicted: {self.player_choice} moves")
        print(f"   Actual minimum: {self.correct_answer} moves")
        print(f"   {'✅ CORRECT!' if self.player_choice == self.correct_answer else '❌ INCORRECT'}")
        print("="*70)
        
        # Now show the game board to play
        self.show_game_board()
    
    def show_game_board(self):
        """
        STEP 4: Display the game board for playing
        """
        print(f"\n📊 SHOWING GAME BOARD - Let's play!")
        
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
        """
        STEP 5: Game finished, show result and save to Firebase
        """
        print(f"\n{'='*70}")
        print(f"🏁 GAME COMPLETED")
        print(f"{'='*70}")
        print(f"   Dice rolls used: {self.game_state.dice_rolls}")
        print(f"   Minimum possible: {self.correct_answer}")
        print("="*70)
        
        # Determine if player's prediction was correct
        is_correct = (self.player_choice == self.correct_answer)
        
        # Save to Firebase (only if correct)
        if is_correct:
            print(f"\n💾 SAVING TO FIREBASE...")
            print("-" * 70)
            
            # Save game session
            session_id = self.firebase.save_game_session(
                player_name=self.game_state.player_name,
                board_size=self.game_state.board_size,
                player_choice=self.player_choice,
                correct_answer=self.correct_answer,
                bfs_time=self.algorithm_results['bfs']['time'],
                dijkstra_time=self.algorithm_results['dijkstra']['time'],
                is_correct=is_correct
            )
            
            # Save player details
            if session_id:
                self.firebase.save_player_details(
                    player_name=self.game_state.player_name,
                    board_size=self.game_state.board_size,
                    correct_answer=self.correct_answer,
                    session_id=session_id
                )
            
            print("-" * 70)
            print(f"✅ DATA SAVED TO FIREBASE")
            print("="*70)
        else:
            print(f"\n⏭️  SKIPPING DATABASE SAVE (incorrect answer)")
            print("="*70)
        
        # Show result screen
        self.show_result_screen()
    
    def show_result_screen(self):
        """
        STEP 6: Show final result screen
        """
        print(f"\n🏆 SHOWING RESULTS...")
        
        if self.current_screen:
            self.current_screen.destroy()
        
        self.current_screen = ResultScreen(
            self.root,
            self.game_state,
            self.player_choice,
            self.correct_answer,
            self.algorithm_results,
            on_play_again_callback=self.on_play_again
        )
        self.current_screen.show()
    
    def on_play_again(self):
        """Callback for play again"""
        print(f"\n🔄 RESTARTING GAME...")
        self.game_state.reset_game()
        self.player_choice = None
        self.correct_answer = None
        self.algorithm_results = None
        self.show_start_screen()
    
    def on_back_to_start(self):
        """Callback when returning to start screen"""
        print(f"\n⬅ BACK TO START...")
        self.game_state.reset_game()
        self.show_start_screen()
    
    def run(self):
        """Start the game application"""
        print("\n" + "="*70)
        print("🚀 SNAKE AND LADDER GAME - STARTING")
        print("="*70)
        print("\n📋 Features:")
        print("   ✅ BFS Algorithm (separate file)")
        print("   ✅ Dijkstra Algorithm (separate file)")
        print("   ✅ Firebase Firestore database")
        print("   ✅ Predict BEFORE playing")
        print("   ✅ Win/Lose/Draw result screen")
        print("   ✅ Saves only CORRECT answers")
        print("\n🎯 Game Flow:")
        print("   1. Enter name and board size")
        print("   2. Predict minimum moves (3 choices)")
        print("   3. Play the game")
        print("   4. See results (Win/Lose/Draw)")
        print("   5. Data saved if correct")
        print("="*70 + "\n")
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        """Handle window close event"""
        print("\n" + "="*70)
        print("👋 THANKS FOR PLAYING SNAKE AND LADDER GAME!")
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