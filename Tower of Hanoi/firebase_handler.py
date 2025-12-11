# firebase_handler.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

class FirebaseHandler:
    def __init__(self):
        self.db = None
        self.initialized = False
        
        try:
            # Create the exact private key with proper line breaks
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
            
            # Your credentials
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
            import tempfile
            import atexit
            
            # Create temp file
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
            
            print(" Firebase initialized successfully!")
            
        except Exception as e:
            print(f" Error initializing Firebase: {str(e)}")
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
            
            print(f"Saving score for player: {player_name}")
            
            # Save to Firebase
            doc_ref = self.db.collection('hanoi_scores').document()
            doc_ref.set(score_data)
            
            print(f" Score saved successfully! Document ID: {doc_ref.id}")
            return True
            
        except Exception as e:
            print(f" Error saving score to Firebase: {str(e)}")
            return False
    
    def get_high_scores(self, limit=10):
        """Get high scores from Firebase"""
        try:
            if not self.is_connected():
                return []
            
            # Get all scores
            docs = self.db.collection('hanoi_scores').stream()
            
            scores = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                scores.append(data)
            
            # Sort by number of moves (ascending = better)
            scores.sort(key=lambda x: x.get('num_moves', 999999))
            
            print(f" Retrieved {len(scores[:limit])} scores from Firebase")
            return scores[:limit]
            
        except Exception as e:
            print(f" Error getting scores from Firebase: {str(e)}")
            return []

# For testing
if __name__ == "__main__":
    print("Testing Firebase connection...")
    handler = FirebaseHandler()
    print(f"Connected: {handler.is_connected()}")
    
    if handler.is_connected():
        # Test save
        print("\nTesting save operation...")
        success = handler.save_player_score(
            player_name="Test Player",
            num_disks=3,
            num_moves=15,
            optimal_moves=7,
            game_mode="test",
            is_correct=True
        )
        print(f"Test save successful: {success}")
        
        if success:
            # Wait a moment
            import time
            time.sleep(2)
            
            # Test get
            print("\nTesting get operation...")
            scores = handler.get_high_scores(limit=3)
            print(f"Retrieved {len(scores)} scores")
            
            if scores:
                print("\nLatest scores:")
                for i, score in enumerate(scores):
                    print(f"{i+1}. {score.get('player_name')}: {score.get('num_moves')} moves")