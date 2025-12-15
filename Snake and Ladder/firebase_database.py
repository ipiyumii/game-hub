import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

class FirebaseDatabase:
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseDatabase, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
       
        if not FirebaseDatabase._initialized:
            try:
                # Path to credentials file
                cred_path = "../shared/mind-arena.json"
                
                if not os.path.exists(cred_path):
                    print(f"⚠️  {cred_path} NOT FOUND!")
                    print("❌ Firebase will NOT work without credentials file.")
                    print(f"📍 Expected location: {os.path.abspath(cred_path)}")
                    self.db = None
                    self.enabled = False
                    FirebaseDatabase._initialized = True
                    return
                
                # Initialize Firebase
                cred = credentials.Certificate(cred_path)
                
                if not firebase_admin._apps:
                    firebase_admin.initialize_app(cred)
                
                # Get Firestore client
                self.db = firestore.client()
                self.enabled = True
                
                print("✅ Firebase Firestore connected!")
                print(f"   Using: {os.path.abspath(cred_path)}")
                
                # Create collection structure
                self._create_collection_structure()
                
                FirebaseDatabase._initialized = True
                
            except FileNotFoundError as e:
                print(f"❌ File not found: {e}")
                self.db = None
                self.enabled = False
                FirebaseDatabase._initialized = True
            except ValueError as e:
                print(f"❌ Invalid credentials: {e}")
                self.db = None
                self.enabled = False
                FirebaseDatabase._initialized = True
            except Exception as e:
                print(f"❌ Firebase error: {e}")
                self.db = None
                self.enabled = False
                FirebaseDatabase._initialized = True
    
    def _create_collection_structure(self): 
        try:
            collection_ref = self.db.collection('snake_and_ladder')
            
            # Create _info document
            info_doc_ref = collection_ref.document('_info')
            info_doc_ref.set({
                'collection_name': 'snake_and_ladder',
                'description': 'Snake and Ladder Game Data',
                'created_at': firestore.SERVER_TIMESTAMP,
                'version': '1.0'
            }, merge=True)
            
            print("✅ Collection 'snake_and_ladder' ready!")
            
        except Exception as e:
            print(f"⚠️  Collection creation: {e}")
    
    def save_game_session(self, player_name, board_size, snakes, ladders, 
                         player_choice, correct_answer, bfs_time, dijkstra_time):
        
        if not self.enabled:
            print("⚠️  Firebase not enabled")
            return None
        
        try:
            session_data = {
                'player_name': player_name,
                'board_size': board_size,
                'total_cells': board_size * board_size,
                'num_snakes': len(snakes),
                'num_ladders': len(ladders),
                'snakes': {str(k): v for k, v in snakes.items()},
                'ladders': {str(k): v for k, v in ladders.items()},
                'player_choice': player_choice,
                'correct_answer': correct_answer,
                'is_correct': player_choice == correct_answer,
                'bfs_time_ms': round(bfs_time * 1000, 4),
                'dijkstra_time_ms': round(dijkstra_time * 1000, 4),
                'timestamp': firestore.SERVER_TIMESTAMP,
                'created_at': datetime.now().isoformat()
            }
            
            # Save to game_sessions collection
            sessions_ref = self.db.collection('snake_and_ladder').document('game_sessions').collection('sessions')
            doc_ref = sessions_ref.add(session_data)
            session_id = doc_ref[1].id
            
            print(f"✅ Game session saved: {session_id}")
            return session_id
            
        except Exception as e:
            print(f"❌ Error saving session: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_player_details(self, player_name, board_size, correct_answer, session_id):
        
        if not self.enabled:
            print("⚠️  Firebase not enabled")
            return None
        
        try:
            players_ref = self.db.collection('snake_and_ladder').document('players').collection('player_records')
            
            # Query for existing player
            query = players_ref.where('player_name', '==', player_name).limit(1).stream()
            existing_docs = list(query)
            
            if existing_docs:
                # Update existing player
                player_doc = existing_docs[0]
                player_id = player_doc.id
                
                players_ref.document(player_id).update({
                    'total_correct_answers': firestore.Increment(1),
                    'last_played': firestore.SERVER_TIMESTAMP,
                    'last_board_size': board_size,
                    'last_correct_answer': correct_answer,
                    'last_session_id': session_id,
                    'updated_at': datetime.now().isoformat()
                })
                
                print(f"✅ Player updated: {player_name}")
                return player_id
                
            else:
                # Create new player
                new_player = {
                    'player_name': player_name,
                    'total_correct_answers': 1,
                    'first_played': firestore.SERVER_TIMESTAMP,
                    'last_played': firestore.SERVER_TIMESTAMP,
                    'last_board_size': board_size,
                    'last_correct_answer': correct_answer,
                    'last_session_id': session_id,
                    'created_at': datetime.now().isoformat()
                }
                
                doc_ref = players_ref.add(new_player)
                player_id = doc_ref[1].id
                
                print(f"✅ New player created: {player_name}")
                return player_id
            
        except Exception as e:
            print(f"❌ Error saving player: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def test_connection(self):
       
        if not self.enabled:
            print("⚠️  Firebase not enabled - skipping connection test")
            return False
        
        try:
            doc_ref = self.db.collection('snake_and_ladder').document('_info')
            doc = doc_ref.get()
            
            if doc.exists:
                print("✅ Firebase connection test: SUCCESS")
                return True
            else:
                print("⚠️  Collection accessible but _info not found")
                return False
                
        except Exception as e:
            print(f"❌ Firebase connection test: FAILED - {e}")
            return False
    
    def get_player_stats(self, player_name):
       
        if not self.enabled:
            return None
        
        try:
            players_ref = self.db.collection('snake_and_ladder').document('players').collection('player_records')
            query = players_ref.where('player_name', '==', player_name).limit(1).stream()
            existing_docs = list(query)
            
            if existing_docs:
                return existing_docs[0].to_dict()
            return None
        except Exception as e:
            print(f"❌ Error getting player stats: {e}")
            return None
    
    def get_all_sessions(self):
        
        if not self.enabled:
            return []
        
        try:
            sessions_ref = self.db.collection('snake_and_ladder').document('game_sessions').collection('sessions')
            sessions = [doc.to_dict() for doc in sessions_ref.stream()]
            return sessions
        except Exception as e:
            print(f"❌ Error getting sessions: {e}")
            return []
    
    def is_connected(self):
        
        return self.enabled