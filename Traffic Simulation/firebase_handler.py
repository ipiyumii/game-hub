import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

class FirebaseHandler:
    def __init__(self):
        self.db = None
        self.initialized = False
        self.traffic_sim_collection = "traffic_simulation"  # collection name

    def initialize_firebase(self):
        try:
            print("FIREBASE INITIALIZATION DEBUG")
            print("Current directory:", os.getcwd())
            print("Files in directory:", [f for f in os.listdir('.') if f.endswith('.json')])

            # multiple possible locations for the service account file
            possible_paths = [
                "../shared/mind-arena.json",  
                "./shared/mind-arena.json",  
                "shared/mind-arena.json",  # Extra fallback
            ]

            cred_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    cred_path = path
                    print(f" Found credentials file at: {path}")
                    break
                else:
                    print(f"  Not found at: {path}")

            if not cred_path:
                print("  Credentials file not found in any expected location")
                return False

            print(f" Using credentials from: {cred_path}")
            cred = credentials.Certificate(cred_path)  
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            self.initialized = True
            print(" Firebase initialized successfully!")
            print(f" Data will be saved under '{self.traffic_sim_collection}' collection")
            return True
        except Exception as e:
            print(f" Firebase initialization failed: {e}")
            return False

    def save_game_session(self, player_name, user_answer, correct_answer, was_correct, algorithm_data):
        if not self.initialized:
            print("Firebase not initialized. Skipping save.")
            return None

        #  Only save if answer was correct
        if not was_correct:
            print(f" Skipping save - incorrect answer by {player_name}")
            print(f"   User answer: {user_answer}, Correct: {correct_answer}")
            return None

        try:
            # Save to traffic_simulation collection
            traffic_ref = self.db.collection(self.traffic_sim_collection)

            # Save game session in game_sessions sub collection
            sessions_ref = traffic_ref.document('game_sessions').collection('sessions')
            session_doc = sessions_ref.document()  # Auto-generate document ID

            session_data = {
                'player_name': player_name,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'was_correct': was_correct,
                'timestamp': datetime.now(),
                'algorithm_data': algorithm_data,
                'session_id': session_doc.id
            }
            session_doc.set(session_data)

            # Only update player stats for correct answers
            self._update_player_stats(player_name, was_correct)

            print(
                f" Game session saved (correct answer) in '{self.traffic_sim_collection}/game_sessions/sessions/{session_doc.id}'")
            return session_doc.id

        except Exception as e:
            print(f" Error saving game session: {e}")
            return None

    def _update_player_stats(self, player_name, was_correct):
        try:
            traffic_ref = self.db.collection(self.traffic_sim_collection)
            players_ref = traffic_ref.document('players').collection('player_data')

            # Query for existing player
            query = players_ref.where('player_name', '==', player_name).get()

            if query:
                # Update existing player - increment both games and wins
                player_doc = query[0]
                player_data = player_doc.to_dict()
                new_games = player_data.get('total_games', 0) + 1
                new_wins = player_data.get('total_wins', 0) + 1  # Always +1 since only correct answers
                win_rate = (new_wins / new_games * 100) if new_games > 0 else 0

                player_doc.reference.update({
                    'total_games': new_games,
                    'total_wins': new_wins,
                    'win_rate': round(win_rate, 2),
                    'last_played': datetime.now(),
                    'updated_at': datetime.now()
                })
                print(f" Updated player '{player_name}' (correct answer)")
            else:
                # Create new player with first correct answer
                players_ref.add({
                    'player_name': player_name,
                    'total_games': 1,
                    'total_wins': 1,  # First correct answer
                    'win_rate': 100.0,  # 100% win rate
                    'created_at': datetime.now(),
                    'last_played': datetime.now(),
                    'updated_at': datetime.now()
                })
                print(f" Created new player '{player_name}' (first correct answer)")

        except Exception as e:
            print(f" Error updating player stats: {e}")

    def get_player_stats(self, player_name):
        if not self.initialized:
            return None

        try:
            traffic_ref = self.db.collection(self.traffic_sim_collection)
            players_ref = traffic_ref.document('players').collection('player_data')

            query = players_ref.where('player_name', '==', player_name).get()

            if query:
                player_data = query[0].to_dict()
                return {
                    'total_games': player_data.get('total_games', 0),
                    'total_wins': player_data.get('total_wins', 0),
                    'win_rate': player_data.get('win_rate', 0.0),
                    'last_played': player_data.get('last_played'),
                    'player_name': player_data.get('player_name')
                }

            # Player not found in new structure 
            print(f"  Player '{player_name}' not found in new collection (fresh start)")
            return None

        except Exception as e:
            print(f"  Error getting player stats: {e}")
            return None

    def get_all_game_sessions(self, player_name=None, limit=50):
        if not self.initialized:
            return []

        try:
            traffic_ref = self.db.collection(self.traffic_sim_collection)
            sessions_ref = traffic_ref.document('game_sessions').collection('sessions')

            # Order by timestamp descending
            query = sessions_ref.order_by('timestamp', direction=firestore.Query.DESCENDING)

            if player_name:
                query = query.where('player_name', '==', player_name)

            sessions = query.limit(limit).stream()

            result = []
            for session in sessions:
                data = session.to_dict()
                data['id'] = session.id
                # Convert Firestore timestamp to string for display
                if 'timestamp' in data:
                    data['timestamp'] = str(data['timestamp'])
                result.append(data)

            return result

        except Exception as e:
            print(f"  Error getting game sessions: {e}")
            return []
