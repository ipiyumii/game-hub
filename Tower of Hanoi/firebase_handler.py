import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json
import uuid
import tempfile
import atexit
import csv
from io import StringIO

class FirebaseHandler:
    def __init__(self):
        self.db = None
        self.initialized = False
        
        try:
            # CORRECTED private key with proper line breaks
            private_key = """-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC1R7dADYhtCQZ0
GwxfAJFJ1eVWHS0k2VEuhwCYVt7KEvo9vDHU6H6oMDvwlB6cjljOdSQtlCAuSjgl
jQJonzmxzXyUrhOy2xfEUNlXeAmQsYoszoOIwvCIk5Zhs9myBpqimudk21Skrcr9
0mc9ExtQPiVHHeYayI1PIclb6qGicRaELBXdrFXd0BdwikSQktRkAOtAfx4EVqF+
JbdYT9BSX4wAvirgx0XavYmTni9huTldt/4cpBDTfPcU0DddDh8QxWUFM2ZKV6Ry
z+lG95IJZrPv6faReKuQEcT9UVU6yM9H552pIu2zyBDsona7ZH5/7kRH1X+zlw27
j4IvkqJ3AgMBAAECggEAUPRk5orkmOTF6AXIQYjMWS/XSdyfs2wFMAUEBAQPXCib
bgRkMJNfNJbNvcM35GxBRnnTnTMgJ+vnJQXSxIwOxNNiRjdy/pWPCJGebcxiYSaX
8SiMXv/HUQavypP5rOH8Ho+UtFqqcxxVoYJbrk+hC/WkyhyVDPLxAByzgoPGiPa8
3Hv3Q9I7xk4F15woI4YuK7415E3ZdSdmgiT8d94aYObJwr7iTFE0+G79Q25deeLa
ZSPXKZ+K/vc1uNYlendiE9F944BJfq8V5q8RoIaIMCG1oUrSG67QlPV9v7LujqO7
N7SuAf4Dagzb3j4W3QxldAl8CoA4SHUJr/WY22O98QKBgQDm0wtuFGO/eE2oZGy+
+Wctf4af+PmIFzvyz7O0dpuw0tXExooZdq7lJWCtzxZ5cciu9ms8wbgsjfYQsuXI
cCfcZN5uceZdSUW/KShFXTi4vaePzl852p/Lzm992XUPGWbve7gtWRcj3t+0GHm1
ULFTkFWxEyD2A8Lga9RIrP1FjwKBgQDJDVKw1SPjbVcDGmhzh9fHcx8Ohs8bUZd0
CVKqSvOvi2yKL412Z/lZddVO25T0XN9eIn5Se3IQ6X9WImnOHTykPjxEWrA+iVFS
/IzCA+XWQT4JZmdO34NMn8p5ILkZjOhGICPyld1mM8IhROi55uEnxATK+irsHshJ
2mVZAiLwmQKBgQC1nUY4Baj6JQENRn7dwERzYwyc3/wOHSHZCZ1+l3gmp6z017Yf
FOfFeiRYfUFUqrdZGqADvPRZchUyzF/J1p02ZtMwmUPFEHrlTs/Vy+RuTyMBHkKE
tcTXSgUlQy08hSMduP2QCLIRUjI3dK6GgAgWFNGnssJTb2AszgrIZ/wbdwKBgQCp
h+B4V+GhPmumpDf7Y0qiVgKUHzy4Tn6lS8825WjCV5C4nQxuEZKCyweJLUNXIpD/
MZrPNmSiuiGzoeUR9jlSTWBISyheMzAuB+MxHlRJ7E3BY2Ytbe+rRvpWVS9/yf96
UlO9lH1SVsaVgyOyzmqBO5rHBVf4LqS5Eb1v5otL0QKBgQDVV5rhbP0CxtbkaTz2
/IILiYJaEH2dGLvC6rI+JbHPG9bkV8kmr39Mmj2SVvDIzS243EwJZ81fNzoF9cZI
6Bvg7WTWBgsdF7mZDzZw+nmNReDuuii2L8MksfwFbJdukpDsZe4CU2K4wI0QaLVx
8zrniKJkDP7Rq/+vRFEopfGmPw==
-----END PRIVATE KEY-----"""
            
            # credentials
            cred_dict = {
                "type": "service_account",
                "project_id": "mind-arena-7c1e5",
                "private_key_id": "d00409ce55d288daf5bcdacc6f31b56139446992",
                "private_key": private_key,
                "client_email": "firebase-adminsdk-fbsvc@mind-arena-7c1e5.iam.gserviceaccount.com",
                "client_id": "106707421230553641396",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40mind-arena-7c1e5.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }
            
            print("Initializing Firebase...")
            
            # Create a temporary credentials file
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
            json.dump(cred_dict, temp_file)
            temp_file.close()
            
            # Register cleanup
            def cleanup():
                try:
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                except:
                    pass
            
            atexit.register(cleanup)
            
            # Initialize Firebase
            cred = credentials.Certificate(temp_file.name)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            self.initialized = True
            
            print("Firebase initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing Firebase: {str(e)}")
            self.initialized = False
    
    def is_connected(self):
        return self.initialized and self.db is not None
    
    def get_high_scores(self, limit=5):
        # Get high scores from hanoi_scores collection
        try:
            if not self.is_connected():
                print("Firebase not connected.")
                return []
            
            print("Fetching high scores from hanoi_scores collection...")
            scores_ref = self.db.collection('hanoi_scores')
            
            # Order by moves (ascending) and then by date (descending)
            scores_snapshot = scores_ref.order_by('num_moves').order_by('date', direction=firestore.Query.DESCENDING).limit(limit).stream()
            
            scores_list = []
            for doc in scores_snapshot:
                score_data = doc.to_dict()
                score_data['document_id'] = doc.id
                scores_list.append(score_data)
            
            print(f"Found {len(scores_list)} scores")
            return scores_list
            
        except Exception as e:
            print(f"Error fetching high scores: {str(e)}")
            return []
    
    def save_player_score(self, **kwargs):
        # Save player score to hanoi_scores collection
        try:
            if not self.is_connected():
                print("Firebase not connected. Score not saved.")
                return False
            
            # Extract parameters
            player_name = kwargs.get('player_name', 'Anonymous')
            num_disks = kwargs.get('num_disks', 3)
            num_moves = kwargs.get('num_moves', 0)
            optimal_moves = kwargs.get('optimal_moves', 0)
            game_mode = kwargs.get('game_mode', 'interactive')
            move_sequence = kwargs.get('move_sequence', '')
            is_correct = kwargs.get('is_correct', False)
            
            # Create score document
            score_data = {
                'player_name': player_name,
                'num_disks': num_disks,
                'num_moves': num_moves,
                'optimal_moves': optimal_moves,
                'game_mode': game_mode,
                'move_sequence': move_sequence,
                'is_correct': is_correct,
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'timestamp': firestore.SERVER_TIMESTAMP
            }
            
            # Save to Firestore
            scores_ref = self.db.collection('hanoi_scores')
            doc_ref = scores_ref.add(score_data)
            
            print(f"Score saved successfully for {player_name}")
            print(f"Document ID: {doc_ref[1].id}")
            return True
            
        except Exception as e:
            print(f"Error saving score to Firebase: {str(e)}")
            return False
    
    def get_all_scores(self):
        # Get all existing scores from hanoi_scores collection
        try:
            if not self.is_connected():
                print("Firebase not connected.")
                return []
            
            print("Fetching all scores from hanoi_scores collection...")
            scores_ref = self.db.collection('hanoi_scores')
            scores_snapshot = scores_ref.stream()
            
            scores_list = []
            for doc in scores_snapshot:
                score_data = doc.to_dict()
                score_data['document_id'] = doc.id
                scores_list.append(score_data)
            
            print(f"Found {len(scores_list)} scores")
            return scores_list
            
        except Exception as e:
            print(f"Error fetching scores: {str(e)}")
            return []
    
    def generate_csv_from_scores(self, scores):
        # Generate CSV data from existing scores
        csv_data = []
        
        for i, score in enumerate(scores):
            round_number = i + 1
            num_disks = score.get('num_disks', 0)
            num_moves = score.get('num_moves', 0)
            optimal_moves = score.get('optimal_moves', 0)
            player_name = score.get('player_name', 'Unknown')
            
            # Calculate simulated times based on number of moves
            recursive_time = num_moves * 0.002  
            iterative_time = num_moves * 0.0015  
            four_peg_recursive_time = num_moves * 0.001  
            four_peg_iterative_time = num_moves * 0.0008 
            
            csv_row = {
                'Round': round_number,
                'Disks': num_disks,
                'Pegs': 3,  # Default
                '3-Peg Recursive (ms)': round(recursive_time * 1000, 4),
                '3-Peg Iterative (ms)': round(iterative_time * 1000, 4),
                '4-Peg Recursive (ms)': round(four_peg_recursive_time * 1000, 4),
                '4-Peg Iterative (ms)': round(four_peg_iterative_time * 1000, 4),
                'Player': player_name,
                'Actual Moves': num_moves,
                'Optimal Moves': optimal_moves,
                'Efficiency': round(num_moves / optimal_moves * 100, 2) if optimal_moves > 0 else 0
            }
            csv_data.append(csv_row)
        
        return csv_data
    
    def create_sessions_for_existing_scores(self):
        try:
            if not self.is_connected():
                print("Firebase not connected.")
                return False
            
            # Get all existing scores
            scores = self.get_all_scores()
            
            if not scores:
                print("No scores found to create sessions for")
                return False
            
            total_sessions_created = 0
            
            # Create sessions for each score
            for score in scores:
                score_id = score.get('document_id')
                player_name = score.get('player_name', 'Unknown')
                num_disks = score.get('num_disks', 0)
                num_moves = score.get('num_moves', 0)
                
                print(f"\nCreating sessions for score: {score_id}")
                print(f"Player: {player_name}, Disks: {num_disks}, Moves: {num_moves}")
                
                # Create CSV data from this score
                csv_data = self.generate_csv_from_scores([score])
                
                # Create multiple session variations from this single score
                sessions_created = self.create_varied_sessions_for_score(
                    score_id=score_id,
                    player_name=player_name,
                    num_disks=num_disks,
                    num_moves=num_moves,
                    csv_data=csv_data
                )
                
                total_sessions_created += sessions_created
            
            print(f"\n{'='*60}")
            print(f"COMPLETE! Created {total_sessions_created} sessions total")
            print(f"for {len(scores)} existing scores")
            print(f"{'='*60}")
            return True
            
        except Exception as e:
            print(f"Error creating sessions: {str(e)}")
            return False
    
    def create_varied_sessions_for_score(self, score_id, player_name, num_disks, num_moves, csv_data):
        try:
            sessions_created = 0
            
            # Create 3 different session types for each score
            for session_num in range(1, 4):
                session_id = f"{score_id}_session_{session_num:02d}"
                
                # Create different test scenarios
                if session_num == 1:
                    # Basic performance test
                    session_name = f"Basic Test - {player_name}"
                    test_type = "performance_basic"
                elif session_num == 2:
                    # Algorithm comparison
                    session_name = f"Algorithm Comparison - {player_name}"
                    test_type = "algorithm_comparison"
                else:
                    # Efficiency analysis
                    session_name = f"Efficiency Analysis - {player_name}"
                    test_type = "efficiency_analysis"
                
                # Create session data
                session = {
                    'session_id': session_id,
                    'test_type': test_type,
                    'session_name': session_name,
                    'player_name': player_name,
                    'parent_score_id': score_id,
                    'rounds': [
                        {
                            'round_number': 1,
                            'disks': num_disks,
                            'peg_count': 3,
                            'results': {
                                'player_moves': num_moves,
                                'optimal_moves': 2**num_disks - 1,
                                'efficiency': round(num_moves / (2**num_disks - 1) * 100, 2) if num_disks > 0 else 0,
                                'completion_time': num_moves * 0.1  # Simulated time
                            }
                        }
                    ],
                    'metadata': {
                        'source': 'existing_score_conversion',
                        'original_disks': num_disks,
                        'original_moves': num_moves,
                        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
                
                # Save session as sub-collection
                if self.save_session(score_id, session):
                    sessions_created += 1
                    print(f"  ✓ Created session: {session_name}")
            
            return sessions_created
            
        except Exception as e:
            print(f"Error creating varied sessions: {str(e)}")
            return 0
    
    def save_session(self, score_doc_id, session_data):
        try:
            if not self.is_connected():
                print("Firebase not connected. Session data not saved.")
                return False
            
            # Generate session ID if not provided
            if 'session_id' not in session_data:
                session_data['session_id'] = str(uuid.uuid4())
            
            # Add timestamp
            session_data['timestamp'] = firestore.SERVER_TIMESTAMP
            session_data['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save as sub-collection under the hanoi_scores document
            session_ref = self.db.collection('hanoi_scores').document(score_doc_id).collection('sessions').document(session_data['session_id'])
            session_ref.set(session_data)
            
            return True
            
        except Exception as e:
            print(f"Error saving session to Firebase: {str(e)}")
            return False
    
    def export_scores_to_csv_file(self, filename="hanoi_scores_export.csv"):
        try:
            scores = self.get_all_scores()
            
            if not scores:
                print("No scores to export")
                return False
            
            # Define CSV headers
            fieldnames = [
                'document_id', 'player_name', 'num_disks', 'num_moves', 
                'optimal_moves', 'game_mode', 'is_correct', 'date',
                'move_sequence_length'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for score in scores:
                    row = {
                        'document_id': score.get('document_id', ''),
                        'player_name': score.get('player_name', ''),
                        'num_disks': score.get('num_disks', 0),
                        'num_moves': score.get('num_moves', 0),
                        'optimal_moves': score.get('optimal_moves', 0),
                        'game_mode': score.get('game_mode', ''),
                        'is_correct': score.get('is_correct', False),
                        'date': score.get('date', ''),
                        'move_sequence_length': len(score.get('move_sequence', '').split(',')) if score.get('move_sequence') else 0
                    }
                    writer.writerow(row)
            
            print(f"\n✓ Exported {len(scores)} scores to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
    
    def print_score_summary(self):
        scores = self.get_all_scores()
        
        print(f"\n{'='*60}")
        print("HANOI SCORES SUMMARY")
        print(f"{'='*60}")
        print(f"Total scores found: {len(scores)}")
        
        if scores:
            print("\nTop 10 Recent Scores:")
            print("-" * 80)
            print(f"{'Player':<20} {'Disks':<6} {'Moves':<6} {'Optimal':<8} {'Date':<20}")
            print("-" * 80)
            
            for score in scores[:10]:
                player = score.get('player_name', 'Unknown')[:18]
                disks = score.get('num_disks', 0)
                moves = score.get('num_moves', 0)
                optimal = score.get('optimal_moves', 0)
                date = score.get('date', '')[:19]
                
                print(f"{player:<20} {disks:<6} {moves:<6} {optimal:<8} {date:<20}")
        
        # Print statistics
        if len(scores) > 0:
            total_disks = sum(s.get('num_disks', 0) for s in scores)
            total_moves = sum(s.get('num_moves', 0) for s in scores)
            avg_disks = total_disks / len(scores)
            avg_moves = total_moves / len(scores)
            
            print(f"\nStatistics:")
            print(f"  Average disks per game: {avg_disks:.1f}")
            print(f"  Average moves per game: {avg_moves:.1f}")
            print(f"  Total moves across all games: {total_moves}")

# MAIN SCRIPT - PROCESS EXISTING SCORES
if __name__ == "__main__":
    print("="*60)
    print("HANOI SCORES PROCESSOR")
    print("Processing existing scores from Firebase")
    print("="*60)
    
    handler = FirebaseHandler()
    
    if handler.is_connected():
        # Print summary of existing scores
        handler.print_score_summary()
        
        # Ask user what they want to do
        print("\n" + "="*60)
        print("OPTIONS:")
        print("1. Create sessions for all existing scores")
        print("2. Export scores to CSV file")
        print("3. Do both")
        print("="*60)
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if choice == 1:
                print("\nCreating sessions for existing scores...")
                handler.create_sessions_for_existing_scores()
                
            elif choice == 2:
                print("\nExporting scores to CSV...")
                handler.export_scores_to_csv_file()
                
            elif choice == 3:
                print("\nExporting scores to CSV...")
                handler.export_scores_to_csv_file()
                
                print("\nCreating sessions for existing scores...")
                handler.create_sessions_for_existing_scores()
                
            else:
                print("Invalid choice")
            
        except ValueError:
            print("Please enter a valid number")
    else:
        print("Failed to connect to Firebase")