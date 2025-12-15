from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QLineEdit, QFrame, QGraphicsView,
                             QGraphicsScene, QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPen, QBrush, QColor, QPainter
import random
from collections import defaultdict
from ford_fulkerson import create_ford_fulkerson
from edmonds_karp import create_edmonds_karp
from validation import Validation
from timer import PerformanceTracker  # Added  this import

class GameWindow(QWidget):
    def __init__(self, app, player_name):
        super().__init__()
        self.app = app
        self.player_name = player_name
        self.current_graph = None
        self.correct_answer = None
        self.algorithm_data = {}
        self.performance_tracker = PerformanceTracker()  # Add PerformanceTracker
        self.round_count = 0  # Add round counter
        self.performance_data = []
        self.init_ui()
        self.start_new_round()

    def init_ui(self):
        self.setWindowTitle(f"Traffic Simulation Game - Player: {self.player_name}")
        self.setFixedSize(1000, 700)

        layout = QVBoxLayout(self)

        # Header
        header = QLabel("🚦Welcome to Traffic Network Analysis Game🚗🚕")
        header.setFont(QFont("Arial", 20, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2E86AB; margin: 10px;")
        layout.addWidget(header)

        # Network visualization
        network_frame = QFrame()
        network_frame.setStyleSheet("border: 1px solid #cccccc; border-radius: 5px;")
        network_layout = QVBoxLayout(network_frame)

        network_label = QLabel("Traffic Network (Capacities in vehicles per minute)")
        network_label.setFont(QFont("Arial", 12, QFont.Bold))
        network_layout.addWidget(network_label)

        self.network_view = QGraphicsView()
        self.network_scene = QGraphicsScene()
        self.network_view.setScene(self.network_scene)
        self.network_view.setRenderHint(QPainter.Antialiasing)
        self.network_view.setStyleSheet("background-color: #f8f9fa; border: none;")
        network_layout.addWidget(self.network_view)

        layout.addWidget(network_frame)

        # Controls frame
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)

        # Answer input
        answer_label = QLabel("Your Answer:")
        answer_label.setFont(QFont("Arial", 12, QFont.Bold))
        controls_layout.addWidget(answer_label)

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Enter maximum flow...")
        self.answer_input.setFont(QFont("Arial", 12))
        self.answer_input.setStyleSheet("padding: 8px; border: 1px solid #ccc; border-radius: 5px;")
        self.answer_input.returnPressed.connect(self.submit_answer)
        controls_layout.addWidget(self.answer_input)

        # Submit button
        self.submit_button = QPushButton("Submit Answer")
        self.submit_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #2E86AB;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1B6B93;
            }
        """)
        self.submit_button.clicked.connect(self.submit_answer)
        controls_layout.addWidget(self.submit_button)

        # New round button
        self.new_round_button = QPushButton("New Round")
        self.new_round_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.new_round_button.setStyleSheet("""
            QPushButton {
                background-color: #A23B72;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7D2B56;
            }
        """)
        self.new_round_button.clicked.connect(self.start_new_round)
        controls_layout.addWidget(self.new_round_button)

        # Performance Report button (NEW)
        self.report_button = QPushButton("Show Report")
        self.report_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.report_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        self.report_button.clicked.connect(self.show_performance_report)
        controls_layout.addWidget(self.report_button)

        layout.addWidget(controls_frame)

        # Analysis help
        help_text = QTextEdit()
        help_text.setHtml("""
        <h4>Analysis Tips:</h4>
        <ul>
            <li>Look at roads leading to T (G→T, H→T) - these are often bottlenecks</li>
            <li>Consider all possible paths from A to T</li>
            <li>Remember: Flow cannot exceed any road's capacity</li>
            <li>Typical flows range from 15-30 vehicles/minute</li>
        </ul>
        <p><b>Performance Tracking:</b> Charts automatically generate after 15 rounds!</p>
        """)
        help_text.setReadOnly(True)
        help_text.setMaximumHeight(140)
        help_text.setStyleSheet("border: 1px solid #cccccc; border-radius: 5px; padding: 10px;")
        layout.addWidget(help_text)

        # Status label
        self.status_label = QLabel("Analyze the network and find the maximum flow from A to T!")
        self.status_label.setFont(QFont("Arial", 11))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #666666; margin: 10px;")
        layout.addWidget(self.status_label)

    def generate_traffic_network(self):
        # Generate a random traffic network
        graph = defaultdict(dict)
        edges = [
            ('A', 'B'), ('A', 'C'), ('A', 'D'),
            ('B', 'E'), ('B', 'F'), ('C', 'E'), ('C', 'F'), ('D', 'F'),
            ('E', 'G'), ('E', 'H'), ('F', 'H'),
            ('G', 'T'), ('H', 'T')
        ]

        for u, v in edges:
            capacity = random.randint(5, 15)
            graph[u][v] = capacity
        return graph

    def calculate_max_flow(self, graph):
        # Ford-Fulkerson (DFS)
        ff = create_ford_fulkerson()
        max_flow_ff, time_ff = ff.max_flow(graph, 'A', 'T')

        # Edmonds-Karp (BFS)
        ek = create_edmonds_karp()
        max_flow_ek, time_ek = ek.max_flow(graph, 'A', 'T')

        # Both should give same result
        if max_flow_ff != max_flow_ek:
            print(f"Warning: Algorithms disagree! FF: {max_flow_ff}, EK: {max_flow_ek}")

        self.algorithm_data = {
            'ford_fulkerson': {'time': time_ff, 'flow': max_flow_ff},
            'edmonds_karp': {'time': time_ek, 'flow': max_flow_ek}
        }

        # Record performance data for charts
        self.round_count += 1
        self.performance_tracker.record_performance(
            self.round_count, time_ff, time_ek, max_flow_ff
        )
        self.performance_data.append({
            'ford_fulkerson_time': time_ff,
            'edmonds_karp_time': time_ek,
            'max_flow': max_flow_ff
        })
        return max_flow_ff

    def draw_network(self, graph):
        # Draw the traffic network visually
        self.network_scene.clear()

        # Node positions for optimal layout
        node_positions = {
            'A': (100, 300),  
            'B': (250, 150),
            'C': (250, 300), 
            'D': (250, 450),
            'E': (450, 200), 
            'F': (450, 400), 
            'G': (650, 150),  
            'H': (650, 450), 
            'T': (800, 300)
        }

        # Draw edges first
        for u, neighbors in graph.items():
            for v, capacity in neighbors.items():
                if capacity > 0:
                    self.draw_edge(node_positions[u], node_positions[v], capacity, f"{u}→{v}")

        # Draw nodes
        for node, pos in node_positions.items():
            self.draw_node(pos, node)

    def draw_node(self, position, label):
        from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem

        x, y = position

        # Draw node circle
        node = QGraphicsEllipseItem(x - 25, y - 25, 50, 50)

        # Color coding
        if label == 'A':
            node.setBrush(QBrush(QColor("#4CAF50"))) 
        elif label == 'T':
            node.setBrush(QBrush(QColor("#F44336")))  
        else:
            node.setBrush(QBrush(QColor("#2196F3")))  

        node.setPen(QPen(Qt.black, 2))
        self.network_scene.addItem(node)

        # Add label
        text = QGraphicsTextItem(label)
        text.setFont(QFont("Arial", 14, QFont.Bold))
        text.setDefaultTextColor(Qt.white)
        text.setPos(x - 8, y - 12)
        self.network_scene.addItem(text)

    def draw_edge(self, start_pos, end_pos, capacity, label):
        from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem

        x1, y1 = start_pos
        x2, y2 = end_pos

        # Draw line
        line = QGraphicsLineItem(x1, y1, x2, y2)

        # Color based on capacity
        if capacity >= 12:
            pen_color = QColor("#4CAF50") 
        elif capacity >= 8:
            pen_color = QColor("#FF9800")  
        else:
            pen_color = QColor("#F44336")  

        pen = QPen(pen_color, 4)
        line.setPen(pen)
        self.network_scene.addItem(line)

        # Add capacity label at midpoint
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        cap_text = QGraphicsTextItem(f"{capacity}")
        cap_text.setFont(QFont("Arial", 14, QFont.Bold))
        cap_text.setDefaultTextColor(pen_color)
        cap_text.setPos(mid_x - 8, mid_y - 8)
        self.network_scene.addItem(cap_text)

    def start_new_round(self):
        self.answer_input.clear()
        self.status_label.setText("🔄 Generating new traffic network...")

        # Generate new network
        self.current_graph = self.generate_traffic_network()

        # Calculate max flow
        self.correct_answer = self.calculate_max_flow(self.current_graph)

        # Draw network
        self.draw_network(self.current_graph)

        # Update status with round info (NEW)
        round_info = f" (Round {self.round_count})" if self.round_count > 0 else ""
        self.status_label.setText(f"🎯 Analyze the network! What's the maximum flow from A to T?{round_info}")

    def submit_answer(self):
        user_answer_text = self.answer_input.text().strip()

        # Validate input
        is_valid,message = Validation.validate_flow_answer(user_answer_text)
        if not is_valid:
            QMessageBox.warning(self, "Input Error", message)
            return

        user_answer = int(user_answer_text)
        is_correct = (user_answer == self.correct_answer)

        # Save to database
        self.app.firebase_handler.save_game_session(
            self.player_name, user_answer, self.correct_answer,
            is_correct, self.algorithm_data
        )

        # Show result
        if is_correct:
            QMessageBox.information(self, "✅ Correct!",
                                    f"🥳🎉 Excellent! The maximum flow is indeed {self.correct_answer}!\n\n"
                                    f"Algorithm Performance:\n"
                                    f"• Ford-Fulkerson: {self.algorithm_data['ford_fulkerson']['time']} ms\n"
                                    f"• Edmonds-Karp: {self.algorithm_data['edmonds_karp']['time']} ms\n\n"
                                    f"Total Rounds Played: {self.round_count}")
        else:
            QMessageBox.warning(self, "❌ Incorrect",
                                f"😬 Wrong answer! The maximum flow is {self.correct_answer}\n"
                                f"Your answer: {user_answer}\n\n"
                                f"Algorithm Performance:\n"
                                f"• Ford-Fulkerson: {self.algorithm_data['ford_fulkerson']['time']} ms\n"
                                f"• Edmonds-Karp: {self.algorithm_data['edmonds_karp']['time']} ms\n\n"
                                f"Total Rounds Played: {self.round_count}")

        # Start new round
        self.start_new_round()

    def show_performance_report(self):
        # Show performance report and charts

        if self.round_count == 0:
            QMessageBox.information(self, "No Data",
                                    "Play at least one round to generate performance data.")
            return

        # Check if performance_data exists and has valid data
        if not hasattr(self, 'performance_data') or not self.performance_data:
            QMessageBox.information(self, "No Data",
                                    "No performance data available yet!\n\n"
                                    "Play at least one round to generate reports.")
            return

        # Generate text report
        report = self.performance_tracker.generate_text_report()

        # Show report in message box
        QMessageBox.information(self, "Performance Report",
                                f"Performance Data for {self.player_name}\n\n"
                                f"Total Rounds: {self.round_count}\n\n"
                                "Check the following files for detailed analysis:\n"
                                "• algorithm_performance.png - Line chart\n"
                                "• performance_comparison.png - Bar chart\n"
                                "• performance_data.csv - Raw data for Excel\n\n"
                                "Full report has been saved to files!")

        # Save data files
        self.performance_tracker.save_to_csv()
        self.performance_tracker.save_to_json()

        # Print detailed report to console
        print("\n" + "=" * 60)
        print("PERFORMANCE REPORT - Traffic Simulation Game")
        print("=" * 60)
        print(report)
