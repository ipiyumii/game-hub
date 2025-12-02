from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QLineEdit, QMessageBox,
                             QFrame, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from game_window import GameWindow
from validation import Validation
from result_window import ResultWindow


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.game_window = None
        self.results_window = None

        # Initialize all instance attributes
        self.name_input = None
        self.play_button = None
        self.stats_button = None
        self.player_info = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("🚦TRAFFIC SIMULATION GAME🚦")
        self.setFixedSize(600, 500)

        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                font-weight: bold;
                border-radius: 5px;
                padding: 8px 16px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel("🚦🚙TRAFFIC SIMULATION GAME🚕🚗")
        header.setFont(QFont("Arial", 22, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2E86AB; margin: 20px;")
        layout.addWidget(header)

        # Subtitle
        subtitle = QLabel("Find the Maximum Flow from Road A to T! \n🎮 Let's Play !")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #666666; margin-bottom: 30px;")
        layout.addWidget(subtitle)

        # Player info frame
        player_frame = QFrame()
        player_frame.setFrameStyle(QFrame.Box)
        player_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #2E86AB; 
                border-radius: 10px; 
                padding: 20px;
                background-color: white;
            }
        """)
        player_layout = QVBoxLayout(player_frame)

        # Player name input
        name_label = QLabel("Enter Your Name")
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        player_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Type your name here...")
        self.name_input.setFont(QFont("Arial", 12))
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 22px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                font-size: 12px;
            }
        """)
        self.name_input.textChanged.connect(self.on_name_changed)
        player_layout.addWidget(self.name_input)

        layout.addWidget(player_frame)

        # Buttons frame
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)

        # Play button
        self.play_button = QPushButton("🎮 Play Game")
        self.play_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #2E86AB;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #1B6B93;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.play_button.clicked.connect(self.start_game)
        self.play_button.setEnabled(False)
        buttons_layout.addWidget(self.play_button)

        # Stats button
        self.stats_button = QPushButton("📊 View Statistics")
        self.stats_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.stats_button.setStyleSheet("""
            QPushButton {
                background-color: #A23B72;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #7D2B56;
            }
        """)
        self.stats_button.clicked.connect(self.show_statistics)
        buttons_layout.addWidget(self.stats_button)

        layout.addWidget(buttons_frame)

        # Instructions
        instructions = QTextEdit()
        instructions.setHtml("""
        <h3>How to Play:</h3>
        <ul>
            <li>Analyze the traffic network showing roads and their capacities</li>
            <li>Find the maximum number of vehicles that can travel from A to T per minute</li>
            <li>Consider road capacities and possible paths</li>
            <li>Submit your answer and see if you're correct!</li>
        </ul>
        <p><b>Tip:</b> Look for bottleneck capacity and multiple paths from A to T</p>
        """)
        instructions.setReadOnly(True)
        instructions.setMaximumHeight(150)
        instructions.setStyleSheet("""
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                background-color: white;
            }
        """)
        layout.addWidget(instructions)

        # Current player info
        self.player_info = QLabel("No player selected")
        self.player_info.setFont(QFont("Arial", 10))
        self.player_info.setStyleSheet("color: #666666; margin-top: 10px;")
        self.player_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.player_info)

    def on_name_changed(self):
        name = self.name_input.text().strip()
        is_valid, message = Validation.validate_player_name(name)

        self.play_button.setEnabled(is_valid)
        if is_valid and name:
            self.player_info.setText(f"My Player Name is 🤖: {name}")
        else:
            self.player_info.setText(message)

    def start_game(self):
        player_name = self.name_input.text().strip()
        if player_name:
            if self.game_window:
                self.game_window.close()

            self.game_window = GameWindow(self.app, player_name)
            self.game_window.show()
            self.hide()

    def show_statistics(self):
        player_name = self.name_input.text().strip()
        if player_name:
            stats = self.app.firebase_handler.get_player_stats(player_name)
            if self.results_window:
                self.results_window.close()

            self.results_window = ResultWindow(player_name, stats)
            self.results_window.show()
        else:
            QMessageBox.warning(self, "Input Error❗", "Please enter your name first!")