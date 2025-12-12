import os
import json
import csv
from datetime import datetime
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

class ReportGenerator:
    
    def __init__(self):
        
        self.rounds = []
        self.max_rounds = 15
        self.report_dir = 'game_reports'
        self.create_report_directory()
        
        print(f"\n📊 Report Generator initialized")
        print(f"   Max rounds: {self.max_rounds}")
        print(f"   Output directory: {self.report_dir}")
    
    def create_report_directory(self):
        
        try:
            Path(self.report_dir).mkdir(exist_ok=True)
            print(f"   ✅ Report directory ready: {self.report_dir}/")
        except Exception as e:
            print(f"   ⚠️  Could not create report directory: {e}")
    
    def add_game_round(self, player_name, board_size, player_choice, 
                      correct_answer, is_correct, bfs_time, dijkstra_time, dice_rolls):
        
        round_data = {
            'round_number': len(self.rounds) + 1,
            'timestamp': datetime.now().isoformat(),
            'player_name': player_name,
            'board_size': board_size,
            'total_cells': board_size * board_size,
            'player_choice': player_choice,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'difference': abs(player_choice - correct_answer),
            'bfs_time_ms': round(bfs_time * 1000, 4),
            'dijkstra_time_ms': round(dijkstra_time * 1000, 4),
            'dice_rolls': dice_rolls
        }
        
        self.rounds.append(round_data)
        
        print(f"\n📊 ROUND {len(self.rounds)}/15 recorded")
        print(f"   Player: {player_name}")
        print(f"   Prediction: {player_choice} (Correct: {correct_answer})")
        print(f"   Result: {'✅ CORRECT' if is_correct else '❌ INCORRECT'}")
        
        # Check if 15 rounds completed
        if len(self.rounds) >= self.max_rounds:
            self.generate_final_report()
            return True
        
        return False
    
    def generate_final_report(self):
        
        print(f"\n{'='*70}")
        print(f"🎉 GENERATING FINAL REPORT - 15 ROUNDS COMPLETED!")
        print(f"{'='*70}")
        
        try:
            # Generate JSON report
            self._generate_json_report()
            
            # Generate CSV report
            self._generate_csv_report()
            
            # Generate statistics file
            self._generate_statistics()
            
            # Generate Algorithm Performance Chart (PNG)
            self._generate_algorithm_performance_chart()
            
            # Generate Performance Comparison Chart (PNG)
            self._generate_performance_comparison_chart()
            
            print(f"\n✅ ALL REPORTS GENERATED SUCCESSFULLY!")
            print(f"   Location: {self.report_dir}/")
            print(f"{'='*70}\n")
            
        except Exception as e:
            print(f"❌ Error generating reports: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_json_report(self):
       
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/report_{timestamp}.json"
        
        report_data = {
            'report_title': '15-Round Game Performance Report',
            'generated_at': datetime.now().isoformat(),
            'total_rounds': len(self.rounds),
            'rounds': self.rounds,
            'summary': self._calculate_summary()
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"   ✅ JSON Report: {filename}")
    
    def _generate_csv_report(self):
       
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/report_{timestamp}.csv"
        
        if not self.rounds:
            print(f"   ⚠️  No rounds to export")
            return
        
        # Define CSV headers
        headers = [
            'Round', 'Timestamp', 'Player', 'Board Size', 'Cells',
            'Prediction', 'Correct', 'Is Correct', 'Difference',
            'BFS Time (ms)', 'Dijkstra Time (ms)', 'Dice Rolls'
        ]
        
        try:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for round_data in self.rounds:
                    writer.writerow([
                        round_data['round_number'],
                        round_data['timestamp'],
                        round_data['player_name'],
                        round_data['board_size'],
                        round_data['total_cells'],
                        round_data['player_choice'],
                        round_data['correct_answer'],
                        'Yes' if round_data['is_correct'] else 'No',
                        round_data['difference'],
                        round_data['bfs_time_ms'],
                        round_data['dijkstra_time_ms'],
                        round_data['dice_rolls']
                    ])
            
            print(f"   ✅ CSV Report: {filename}")
        
        except Exception as e:
            print(f"   ❌ CSV Error: {e}")
    
    def _generate_statistics(self):
      
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/statistics_{timestamp}.txt"
        
        summary = self._calculate_summary()
        
        stats_text = f"""
{'='*70}
SNAKE AND LADDER GAME - 15 ROUND PERFORMANCE STATISTICS
{'='*70}

PREDICTION ACCURACY
{'-'*70}
Total Rounds:           {summary['total_rounds']}
Correct Predictions:    {summary['correct_predictions']} ({summary['accuracy_percentage']:.1f}%)
Incorrect Predictions:  {summary['incorrect_predictions']} ({100-summary['accuracy_percentage']:.1f}%)

PREDICTION DIFFERENCE (Moves)
{'-'*70}
Average Difference:     {summary['avg_difference']:.2f} moves
Min Difference:         {summary['min_difference']} moves
Max Difference:         {summary['max_difference']} moves

ALGORITHM PERFORMANCE (Execution Time)
{'-'*70}
BFS Average Time:       {summary['avg_bfs_time']:.4f} ms
Dijkstra Avg Time:      {summary['avg_dijkstra_time']:.4f} ms
Faster Algorithm:       {summary['fastest_algorithm']}

GAME STATISTICS
{'-'*70}
Average Dice Rolls:     {summary['avg_dice_rolls']:.2f} rolls
Min Dice Rolls:         {summary['min_dice_rolls']} rolls
Max Dice Rolls:         {summary['max_dice_rolls']} rolls

BOARD STATISTICS
{'-'*70}
Most Used Board Size:   {summary['most_used_board_size']}×{summary['most_used_board_size']} ({summary['most_used_board_size']**2} cells)
Board Sizes Used:       {', '.join(str(x) for x in sorted(set(r['board_size'] for r in self.rounds)))}

REPORT GENERATED
{'-'*70}
Date & Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Location:    {os.path.abspath(filename)}
{'='*70}
"""
        
        try:
            with open(filename, 'w') as f:
                f.write(stats_text)
            
            print(f"   ✅ Statistics: {filename}")
        
        except Exception as e:
            print(f"   ❌ Statistics Error: {e}")
    
    def _generate_algorithm_performance_chart(self):
      
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/algorithm_performance_{timestamp}.png"
        
        try:
            # Extract data
            rounds_num = [r['round_number'] for r in self.rounds]
            bfs_times = [r['bfs_time_ms'] for r in self.rounds]
            dijkstra_times = [r['dijkstra_time_ms'] for r in self.rounds]
            
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#1a1a2e')
            ax.set_facecolor('#16213e')
            
            # Plot lines
            ax.plot(rounds_num, bfs_times, marker='o', linestyle='-', linewidth=2.5, 
                   markersize=8, label='BFS Algorithm', color='#2ecc71')
            ax.plot(rounds_num, dijkstra_times, marker='s', linestyle='-', linewidth=2.5, 
                   markersize=8, label='Dijkstra Algorithm', color='#3498db')
            
            # Customize chart
            ax.set_xlabel('Game Round', fontsize=12, color='#ecf0f1', fontweight='bold')
            ax.set_ylabel('Execution Time (milliseconds)', fontsize=12, color='#ecf0f1', fontweight='bold')
            ax.set_title('Algorithm Performance Comparison\nExecution Time per Round', 
                        fontsize=14, color='#ecf0f1', fontweight='bold', pad=20)
            
            # Customize grid
            ax.grid(True, alpha=0.2, color='#34495e', linestyle='--')
            ax.set_axisbelow(True)
            
            # Customize ticks
            ax.tick_params(colors='#ecf0f1', labelsize=10)
            ax.spines['bottom'].set_color('#34495e')
            ax.spines['left'].set_color('#34495e')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Add legend
            legend = ax.legend(loc='upper left', fontsize=11, framealpha=0.95, 
                             facecolor='#16213e', edgecolor='#34495e')
            for text in legend.get_texts():
                text.set_color('#ecf0f1')
            
            # Add value labels on points
            for i, (r, b, d) in enumerate(zip(rounds_num, bfs_times, dijkstra_times)):
                ax.text(r, b, f'{b:.2f}', ha='center', va='bottom', fontsize=8, color='#2ecc71')
                ax.text(r, d, f'{d:.2f}', ha='center', va='bottom', fontsize=8, color='#3498db')
            
            plt.tight_layout()
            plt.savefig(filename, dpi=300, facecolor='#1a1a2e', edgecolor='none')
            plt.close()
            
            print(f"   ✅ Algorithm Performance Chart: {filename}")
            
        except Exception as e:
            print(f"   ❌ Algorithm Performance Chart Error: {e}")
    
    def _generate_performance_comparison_chart(self):
      
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.report_dir}/performance_comparison_{timestamp}.png"
        
        try:
            # Extract data
            summary = self._calculate_summary()
            
            # Create figure with subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            fig.patch.set_facecolor('#1a1a2e')
            
            # ===== LEFT: Prediction Accuracy Bar Chart =====
            ax1.set_facecolor('#16213e')
            
            accuracy_data = [summary['correct_predictions'], summary['incorrect_predictions']]
            accuracy_labels = ['Correct\nPredictions', 'Incorrect\nPredictions']
            accuracy_colors = ['#2ecc71', '#e74c3c']
            
            bars1 = ax1.bar(accuracy_labels, accuracy_data, color=accuracy_colors, 
                           edgecolor='#ecf0f1', linewidth=2, width=0.6)
            
            ax1.set_ylabel('Count', fontsize=12, color='#ecf0f1', fontweight='bold')
            ax1.set_title('Prediction Accuracy\n15 Rounds', fontsize=12, color='#ecf0f1', 
                         fontweight='bold', pad=15)
            ax1.set_ylim(0, max(accuracy_data) + 3)
            
            # Add value labels on bars
            for bar, val in zip(bars1, accuracy_data):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(val)}\n({val/summary["total_rounds"]*100:.1f}%)',
                        ha='center', va='bottom', fontsize=11, color='#ecf0f1', fontweight='bold')
            
            ax1.tick_params(colors='#ecf0f1', labelsize=10)
            ax1.spines['bottom'].set_color('#34495e')
            ax1.spines['left'].set_color('#34495e')
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.grid(True, axis='y', alpha=0.2, color='#34495e', linestyle='--')
            ax1.set_axisbelow(True)
            
            # ===== RIGHT: Algorithm Speed Comparison =====
            ax2.set_facecolor('#16213e')
            
            algo_names = ['BFS', 'Dijkstra']
            algo_times = [summary['avg_bfs_time'], summary['avg_dijkstra_time']]
            algo_colors = ['#2ecc71', '#3498db']
            
            bars2 = ax2.bar(algo_names, algo_times, color=algo_colors, 
                           edgecolor='#ecf0f1', linewidth=2, width=0.5)
            
            ax2.set_ylabel('Average Time (milliseconds)', fontsize=12, color='#ecf0f1', fontweight='bold')
            ax2.set_title('Algorithm Speed Comparison\nAverage Execution Time', fontsize=12, 
                         color='#ecf0f1', fontweight='bold', pad=15)
            ax2.set_ylim(0, max(algo_times) * 1.2)
            
            # Add value labels on bars
            for bar, val in zip(bars2, algo_times):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{val:.4f} ms',
                        ha='center', va='bottom', fontsize=11, color='#ecf0f1', fontweight='bold')
            
            ax2.tick_params(colors='#ecf0f1', labelsize=10)
            ax2.spines['bottom'].set_color('#34495e')
            ax2.spines['left'].set_color('#34495e')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.grid(True, axis='y', alpha=0.2, color='#34495e', linestyle='--')
            ax2.set_axisbelow(True)
            
            # Add faster algorithm indicator
            faster = 'BFS' if summary['avg_bfs_time'] < summary['avg_dijkstra_time'] else 'Dijkstra'
            fig.suptitle(f'⚡ Faster Algorithm: {faster}', fontsize=10, color='#f39c12', 
                        fontweight='bold', y=0.98)
            
            plt.tight_layout()
            plt.savefig(filename, dpi=300, facecolor='#1a1a2e', edgecolor='none')
            plt.close()
            
            print(f"   ✅ Performance Comparison Chart: {filename}")
            
        except Exception as e:
            print(f"   ❌ Performance Comparison Chart Error: {e}")
    
    def _calculate_summary(self):
        
        if not self.rounds:
            return {
                'total_rounds': 0,
                'correct_predictions': 0,
                'incorrect_predictions': 0,
                'accuracy_percentage': 0,
                'avg_difference': 0,
                'min_difference': 0,
                'max_difference': 0,
                'avg_bfs_time': 0,
                'avg_dijkstra_time': 0,
                'fastest_algorithm': 'N/A',
                'avg_dice_rolls': 0,
                'min_dice_rolls': 0,
                'max_dice_rolls': 0,
                'most_used_board_size': 8
            }
        
        correct = sum(1 for r in self.rounds if r['is_correct'])
        total = len(self.rounds)
        
        differences = [r['difference'] for r in self.rounds]
        bfs_times = [r['bfs_time_ms'] for r in self.rounds]
        dijkstra_times = [r['dijkstra_time_ms'] for r in self.rounds]
        dice_rolls = [r['dice_rolls'] for r in self.rounds]
        board_sizes = [r['board_size'] for r in self.rounds]
        
        avg_bfs = sum(bfs_times) / len(bfs_times) if bfs_times else 0
        avg_dijkstra = sum(dijkstra_times) / len(dijkstra_times) if dijkstra_times else 0
        
        # Find most used board size
        board_size_counts = {}
        for size in board_sizes:
            board_size_counts[size] = board_size_counts.get(size, 0) + 1
        most_used_board = max(board_size_counts, key=board_size_counts.get) if board_size_counts else 8
        
        return {
            'total_rounds': total,
            'correct_predictions': correct,
            'incorrect_predictions': total - correct,
            'accuracy_percentage': (correct / total * 100) if total > 0 else 0,
            'avg_difference': sum(differences) / len(differences) if differences else 0,
            'min_difference': min(differences) if differences else 0,
            'max_difference': max(differences) if differences else 0,
            'avg_bfs_time': avg_bfs,
            'avg_dijkstra_time': avg_dijkstra,
            'fastest_algorithm': 'BFS' if avg_bfs < avg_dijkstra else 'Dijkstra',
            'avg_dice_rolls': sum(dice_rolls) / len(dice_rolls) if dice_rolls else 0,
            'min_dice_rolls': min(dice_rolls) if dice_rolls else 0,
            'max_dice_rolls': max(dice_rolls) if dice_rolls else 0,
            'most_used_board_size': most_used_board
        }
    
    def get_round_count(self):
        return len(self.rounds)
    
    def get_rounds(self):
        return self.rounds.copy()
    
    def reset(self):
        self.rounds = []
        print("\n🔄 Report generator reset")