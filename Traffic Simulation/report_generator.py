import matplotlib.pyplot as plt
import numpy as np

class ReportGenerator:
    def __init__(self):
        plt.style.use('seaborn-v0_8')

    def create_algorithm_comparison_chart(self, performance_data):
        """Create the main performance comparison chart"""
        # Check if performance_data is empty
        if not performance_data:
            print(" No performance data available to generate report")
            self._show_no_data_message("No performance data available yet!")
            return

        # Check if we have valid time data 
        try:
            rounds = list(range(1, len(performance_data) + 1))
            ff_times = [data['ford_fulkerson_time'] for data in performance_data]
            ek_times = [data['edmonds_karp_time'] for data in performance_data]

            # Check if we have meaningful data 
            has_meaningful_data = any(
                ff_time > 0.001 or ek_time > 0.001  # Allow very small times > 0.001ms
                for ff_time, ek_time in zip(ff_times, ek_times)
            )

            if not has_meaningful_data:
                print(" Algorithms are very fast - times are very small")
                self._show_no_data_message(
                    "Your algorithms are running very fast! \n\n"
                    "Performance data is being collected, but execution times are very small.\n"
                    "Complete a few more rounds to see the comparison trends."
                )
                return

        except (KeyError, TypeError) as e:
            print(f"❌ Invalid performance data structure: {e}")
            self._show_no_data_message("Invalid performance data structure")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Chart 1: Execution times
        ax1.plot(rounds, ff_times, 'ro-', label='Ford-Fulkerson (DFS)', linewidth=2)
        ax1.plot(rounds, ek_times, 'bs-', label='Edmonds-Karp (BFS)', linewidth=2)
        ax1.set_title('Algorithm Execution Time\nOver 15 Game Rounds')
        ax1.set_xlabel('Game Round')
        ax1.set_ylabel('Time (milliseconds)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Chart 2: Average performance
        algorithms = ['Ford-Fulkerson', 'Edmonds-Karp']

        # Safe average calculation with zero division check
        avg_ff = np.mean(ff_times) if ff_times else 0
        avg_ek = np.mean(ek_times) if ek_times else 0
        avg_times = [avg_ff, avg_ek]

        bars = ax2.bar(algorithms, avg_times, color=['red', 'blue'], alpha=0.7)
        ax2.set_title('Average Execution Time\nComparison')
        ax2.set_ylabel('Average Time (milliseconds)')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            # Show more decimal places for very small times
            if height < 1.0:
                ax2.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{height:.4f} ms', ha='center', va='bottom', fontsize=9)
            else:
                ax2.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{height:.2f} ms', ha='center', va='bottom')

        plt.tight_layout()
        plt.savefig('algorithm_performance_report.png', dpi=300, bbox_inches='tight')
        plt.show()

    def create_complexity_chart(self):
        """Create theoretical complexity comparison chart"""
        n_values = np.linspace(10, 100, 50)
        O_V_E2 = n_values ** 3  # O(V*E^2) - Edmonds-Karp
        O_E_maxflow = n_values ** 4  # O(E*max_flow) - Ford-Fulkerson (worst case)

        plt.figure(figsize=(10, 6))
        plt.plot(n_values, O_V_E2, label='O(V·E²) - Edmonds-Karp (BFS)', linewidth=2)
        plt.plot(n_values, O_E_maxflow, label='O(E·max_flow) - Ford-Fulkerson (DFS)', linewidth=2)
        plt.title('Theoretical Time Complexity Comparison')
        plt.xlabel('Input Size (V+E)')
        plt.ylabel('Operations')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('complexity_analysis.png', dpi=300, bbox_inches='tight')

    def _show_no_data_message(self, message="No performance data available yet!"):
        try:
            # Import PyQt5 inside the method to avoid circular imports
            from PyQt5.QtWidgets import QApplication, QMessageBox
            import sys

            # Check if QApplication instance exists, create if needed
            app = QApplication.instance()
            if not app:
                app = QApplication(sys.argv)

            QMessageBox.information(None, "Performance Report", message)
        except Exception as e:
            # Fallback to console message if Qt is not available
            print("No performance data available. Play some rounds first!")
            print(f"Debug: {e}")
