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
