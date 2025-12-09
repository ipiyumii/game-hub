# firebase_handler_fixed.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

class FirebaseHandler:
    def __init__(self, credential_path=None):
        self.db = None
        self.credential_path = credential_path
        self.initialized = False
        
        try:
            # Look for credentials in common locations
            if not self.credential_path:
                possible_paths = [
                    'mind-arena-7c1e5-firebase-adminsdk-fbsvc-8982f8357a.json',
                    'firebase_credentials.json',
                    'credentials.json',
                    os.path.join(os.path.dirname(__file__), 'mind-arena-7c1e5-firebase-adminsdk-fbsvc-8982f8357a.json')
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        self.credential_path = path
                        break
            
            if self.credential_path and os.path.exists(self.credential_path):
                # Safe print for Windows
                print(f"Found Firebase credentials at: {self.credential_path}")
                print("Initializing Firebase...")
                
                cred = credentials.Certificate(self.credential_path)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.initialized = True
                print("Firebase initialized successfully")
            else:
                print("No Firebase credentials found. Using simulation mode.")
                self.initialized = False
                
        except Exception as e:
            error_msg = str(e)
            # Remove any emojis or non-ASCII characters for Windows
            error_msg = ''.join(char for char in error_msg if ord(char) < 128)
            print(f"Error initializing Firebase: {error_msg}")
            print("Using local simulation mode")
            self.initialized = False
    
    def is_connected(self):
        return self.initialized and self.db is not None
    
    def save_player_score(self, player_name, num_disks, num_moves, optimal_moves, game_mode, move_sequence="", is_correct=False):
        """Save player score to Firebase"""
        try:
            if not self.is_connected():
                print("Firebase not connected. Score not saved.")
                return False
            
            # Prepare score data
            score_data = {
                'player_name': player_name,
                'num_disks': num_disks,
                'num_moves': num_moves,
                'optimal_moves': optimal_moves,
                'game_mode': game_mode,
                'move_sequence': move_sequence,
                'is_correct': is_correct,
                'timestamp': firestore.SERVER_TIMESTAMP,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Try to save to different collections
            collections_to_try = ['hanoi_scores', 'towerOfHand', 'tower_of_hanoi_scores']
            
            for collection_name in collections_to_try:
                try:
                    # Use keyword arguments instead of positional
                    doc_ref = self.db.collection(collection_name).document()
                    doc_ref.set(score_data)
                    print(f"Score saved to {collection_name} collection for player: {player_name}")
                    return True
                except Exception as e:
                    error_msg = str(e)
                    error_msg = ''.join(char for char in error_msg if ord(char) < 128)
                    print(f"Failed to save to {collection_name}: {error_msg[:100]}")
                    continue
            
            print("Could not save to any collection")
            return False
            
        except Exception as e:
            error_msg = str(e)
            error_msg = ''.join(char for char in error_msg if ord(char) < 128)
            print(f"Error saving score: {error_msg[:100]}")
            return False
    
    def get_high_scores(self, limit=10):
        """Get high scores from Firebase"""
        try:
            if not self.is_connected():
                return []
            
            # Try different collections
            collections_to_try = ['hanoi_scores', 'towerOfHand', 'tower_of_hanoi_scores']
            
            for collection_name in collections_to_try:
                try:
                    # Get all documents without filtering first (to avoid index requirement)
                    docs = self.db.collection(collection_name).stream()
                    
                    scores = []
                    for doc in docs:
                        data = doc.to_dict()
                        data['id'] = doc.id
                        scores.append(data)
                    
                    if scores:
                        # Sort locally by number of moves (ascending = better)
                        scores.sort(key=lambda x: x.get('num_moves', 999999))
                        
                        # Add ranking
                        for i, score in enumerate(scores[:limit]):
                            score['rank'] = i + 1
                        
                        print(f"Found {len(scores[:limit])} scores from {collection_name}")
                        return scores[:limit]
                        
                except Exception as e:
                    error_msg = str(e)
                    error_msg = ''.join(char for char in error_msg if ord(char) < 128)
                    print(f"Error reading from {collection_name}: {error_msg[:100]}")
                    continue
            
            return []
            
        except Exception as e:
            error_msg = str(e)
            error_msg = ''.join(char for char in error_msg if ord(char) < 128)
            print(f"Error getting scores: {error_msg[:100]}")
            return []

# For quick testing
if __name__ == "__main__":
    handler = FirebaseHandler()
    print(f"Connected: {handler.is_connected()}")