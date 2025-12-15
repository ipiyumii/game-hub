from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class ResultWindow(QWidget):
    def __init__(self, player_name, stats):
        super().__init__()
        self.player_name = player_name
        self.stats = stats  # This statement could be None if there is no data in Firebase
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Player Statistics - {self.player_name}")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)

        # Header
        header = QLabel(f"📊 Player Statistics")
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2E86AB; margin: 10px;")
        layout.addWidget(header)

        # Player name
        name_label = QLabel(f"Player: {self.player_name}")
        name_label.setFont(QFont("Arial", 14, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)

        # Statistics frame
        stats_frame = QFrame()
        stats_frame.setFrameStyle(QFrame.Box)
        stats_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #2E86AB;
                border-radius: 5px;
                padding: 5px;
                background-color: white;
                margin: 2px;
            }
        """)
        stats_layout = QVBoxLayout(stats_frame)

        if self.stats:
            # Total games
            total_games = QLabel(f"Total Games Played: {self.stats['total_games']}")
            total_games.setFont(QFont("Arial", 10, QFont.Bold))
            stats_layout.addWidget(total_games)

            # Total wins
            total_wins = QLabel(f"Games Won: {self.stats['total_wins']}")
            total_wins.setFont(QFont("Arial", 10, QFont.Bold))
            stats_layout.addWidget(total_wins)

            # Win rate
            win_rate = QLabel(f"Win Rate: {self.stats['win_rate']}%")
            win_rate.setFont(QFont("Arial", 10, QFont.Bold))
            win_rate.setStyleSheet("color: #4CAF50;")
            stats_layout.addWidget(win_rate)

            # Performance comment
            if self.stats['win_rate'] >= 70:
                comment = "🎯 Excellent performance!"
            elif self.stats['win_rate'] >= 50:
                comment = "👍 Good job! Keep practicing!"
            else:
                comment = "💪 Keep practicing! You'll improve!"

            comment_label = QLabel(comment)
            comment_label.setFont(QFont("Arial", 11, QFont.Bold))
            comment_label.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(comment_label)

        else:
            no_data = QLabel("No game data available yet.\nPlay some games to see your statistics!")
            no_data.setFont(QFont("Arial", 12))
            no_data.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(no_data)

        layout.addWidget(stats_frame)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setFont(QFont("Arial", 12))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)