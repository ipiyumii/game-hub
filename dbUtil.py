import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase(json_path: str):
    creds = credentials.Certificate(json_path)
    firebase_admin.initialize_app(creds)
    return firestore.client()

def get_all_games(db):
    games_ref = db.collection("games")
    docs = games_ref.stream()
    all_games = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        all_games.append(data)
    return all_games

def fetch_games_from_database():
    try:
        print("Connecting to database...")
        
        db = initialize_firebase("shared/mind-arena.json")
        games = get_all_games(db)
        
        print("Games found in database:")
        for game in games:
            game_name = game.get('gameName', game.get('name', 'Unknown Game'))
            print(f"  - {game_name}")
        
        return games
    except ImportError:
        print("Database utilities not found. Using fallback games.")
        return None
    except Exception as e:
        print(f"Database error: {e}")
        print("Using fallback games.")
        return None

def delete_collection(coll_ref):
    docs = coll_ref.stream()
    for doc in docs:
        doc.reference.delete()