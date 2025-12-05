import time
from functools import wraps
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import json


def timer(func):
    """Decorator to measure function execution time"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        return result, round(execution_time, 2)
    return wrapper

class PerformanceTracker:
    def __init__(self):
        self.performance_data = []

    def record_performance(self, round_num, ff_time, ek_time, max_flow):
        """Record algorithm performance for charts and analysis"""
        self.performance_data.append({
            'round': round_num,
            'ford_fulkerson_time': ff_time,
            'edmonds_karp_time': ek_time,
            'max_flow': max_flow,
            'timestamp': datetime.now().isoformat()
        })

        # Auto-generate chart after 15 rounds (for coursework requirement)
        if len(self.performance_data) >= 15:
            self.generate_performance_chart()

    def generate_performance_chart(self):
        """Generate professional performance charts for coursework report"""
        if len(self.performance_data) < 2:
            print("  Not enough data to generate chart. Need at least 2 rounds.")
            return

        rounds = [data['round'] for data in self.performance_data]
        ff_times = [data['ford_fulkerson_time'] for data in self.performance_data]
        ek_times = [data['edmonds_karp_time'] for data in self.performance_data]

        # Create the main performance chart
        plt.figure(figsize=(12, 6))
        plt.plot(rounds, ff_times, 'r-', marker='o', label='Ford-Fulkerson (DFS)', linewidth=2, markersize=6)
        plt.plot(rounds, ek_times, 'b-', marker='s', label='Edmonds-Karp (BFS)', linewidth=2, markersize=6)

        plt.title('Algorithm Execution Time Comparison\nTraffic Simulation Game',
                  fontsize=14, fontweight='bold')
        plt.xlabel('Game Round', fontsize=12)
        plt.ylabel('Execution Time (milliseconds)', fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.xticks(rounds)

        # Add average lines
        avg_ff = sum(ff_times) / len(ff_times)
        avg_ek = sum(ek_times) / len(ek_times)
        plt.axhline(y=avg_ff, color='red', linestyle='--', alpha=0.7, label=f'FF Avg: {avg_ff:.2f}ms')
        plt.axhline(y=avg_ek, color='blue', linestyle='--', alpha=0.7, label=f'EK Avg: {avg_ek:.2f}ms')

        plt.tight_layout()
        plt.savefig('Traffic Simulation/algorithm_performance.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(f" Performance chart generated: 'algorithm_performance.png' ({len(self.performance_data)} rounds)")

        # Also generate a bar chart for average comparison
        self.generate_average_comparison_chart()

    def generate_average_comparison_chart(self):
        """Generate average performance comparison chart"""
        if len(self.performance_data) < 2:
            return

        ff_times = [data['ford_fulkerson_time'] for data in self.performance_data]
        ek_times = [data['edmonds_karp_time'] for data in self.performance_data]

        algorithms = ['Ford-Fulkerson\n(DFS)', 'Edmonds-Karp\n(BFS)']
        avg_times = [sum(ff_times) / len(ff_times), sum(ek_times) / len(ek_times)]
        min_times = [min(ff_times), min(ek_times)]
        max_times = [max(ff_times), max(ek_times)]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Chart 1: Average execution time
        bars = ax1.bar(algorithms, avg_times, color=['lightcoral', 'lightblue'], alpha=0.7, edgecolor='black')
        ax1.set_title('Average Execution Time Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Time (milliseconds)', fontsize=12)
        ax1.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                     f'{height:.2f} ms', ha='center', va='bottom', fontweight='bold')

        # Chart 2: Performance range
        ax2.bar(algorithms, avg_times, yerr=[[avg_times[i] - min_times[i] for i in range(2)],
                                             [max_times[i] - avg_times[i] for i in range(2)]],
                capsize=5, color=['lightcoral', 'lightblue'], alpha=0.7, edgecolor='black')
        ax2.set_title('Performance Range (Min-Max)', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Time (milliseconds)', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()

        print(" Average comparison chart generated: 'performance_comparison.png'")

    def save_to_csv(self, filename="performance_data.csv"):
        """Save performance data to CSV for Excel analysis"""
        if not self.performance_data:
            print("  No performance data to save.")
            return None

        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['round', 'ford_fulkerson_time', 'edmonds_karp_time', 'max_flow', 'timestamp']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for data in self.performance_data:
                    writer.writerow(data)

            print(f" Performance data saved to {filename}")
            return filename
        except Exception as e:
            print(f" Error saving CSV: {e}")
            return None

    def save_to_json(self, filename="performance_data.json"):
        """Save performance data to JSON for further processing"""
        if not self.performance_data:
            print("  No performance data to save.")
            return None

        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(self.performance_data, jsonfile, indent=2, ensure_ascii=False)

            print(f" Performance data saved to {filename}")
            return filename
        except Exception as e:
            print(f" Error saving JSON: {e}")
            return None

    def generate_text_report(self):
        """Generate a text-based performance report for quick viewing"""
        if not self.performance_data:
            return "No performance data collected yet."

        report = []
        report.append("=" * 60)
        report.append("ALGORITHM PERFORMANCE REPORT - Traffic Simulation Game")
        report.append("=" * 60)
        report.append("Round | Ford-Fulkerson | Edmonds-Karp | Max Flow")
        report.append("-" * 60)

        for data in self.performance_data:
            report.append(f"{data['round']:5} | {data['ford_fulkerson_time']:14.2f} ms | "
                          f"{data['edmonds_karp_time']:13.2f} ms | {data['max_flow']:8}")

        # Calculate statistics
        ff_times = [d['ford_fulkerson_time'] for d in self.performance_data]
        ek_times = [d['edmonds_karp_time'] for d in self.performance_data]

        avg_ff = sum(ff_times) / len(ff_times)
        avg_ek = sum(ek_times) / len(ek_times)
        min_ff = min(ff_times)
        min_ek = min(ek_times)
        max_ff = max(ff_times)
        max_ek = max(ek_times)

        report.append("-" * 60)
        report.append("PERFORMANCE SUMMARY:")
        report.append(f"Total Rounds: {len(self.performance_data)}")
        report.append(f"Ford-Fulkerson: Avg={avg_ff:.2f}ms, Min={min_ff:.2f}ms, Max={max_ff:.2f}ms")
        report.append(f"Edmonds-Karp:    Avg={avg_ek:.2f}ms, Min={min_ek:.2f}ms, Max={max_ek:.2f}ms")

        if avg_ek < avg_ff:
            faster_algo = "Edmonds-Karp (BFS)"
            speedup = ((avg_ff - avg_ek) / avg_ff) * 100
            report.append(f"FASTER ALGORITHM: {faster_algo} ({speedup:.1f}% faster)")
        else:
            faster_algo = "Ford-Fulkerson (DFS)"
            speedup = ((avg_ek - avg_ff) / avg_ek) * 100
            report.append(f"FASTER ALGORITHM: {faster_algo} ({speedup:.1f}% faster)")

        report.append("=" * 60)

        return "\n".join(report)

    def print_report(self):
        """Print the performance report to console"""
        print(self.generate_text_report())

    def clear_data(self):
        """Clear all performance data"""
        self.performance_data.clear()
        print(" Performance data cleared")

    def get_statistics(self):
        """Get performance statistics as a dictionary"""
        if not self.performance_data:
            return None

        ff_times = [d['ford_fulkerson_time'] for d in self.performance_data]
        ek_times = [d['edmonds_karp_time'] for d in self.performance_data]

        return {
            'total_rounds': len(self.performance_data),
            'ford_fulkerson': {
                'average': sum(ff_times) / len(ff_times),
                'min': min(ff_times),
                'max': max(ff_times),
                'total': sum(ff_times)
            },
            'edmonds_karp': {
                'average': sum(ek_times) / len(ek_times),
                'min': min(ek_times),
                'max': max(ek_times),
                'total': sum(ek_times)
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Test the PerformanceTracker
    tracker = PerformanceTracker()

    # Add some sample data
    sample_data = [
        (1, 15.2, 12.1, 23),
        (2, 14.8, 11.8, 24),
        (3, 16.1, 12.5, 22),
        (4, 15.5, 11.9, 25),
        (5, 14.9, 12.2, 23)
    ]

    for round_num, ff_time, ek_time, max_flow in sample_data:
        tracker.record_performance(round_num, ff_time, ek_time, max_flow)

    # Generate reports
    tracker.print_report()
    tracker.save_to_csv("sample_performance.csv")
    tracker.save_to_json("sample_performance.json")
    print("\n PerformanceTracker test completed successfully!")
