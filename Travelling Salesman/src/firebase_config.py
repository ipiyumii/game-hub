import firebase_admin
from firebase_admin import credentials, firestore
import os

KEY_FILENAME = "mind-arena.json"
THIS_DIR = os.path.dirname(__file__)
KEY_PATH = os.path.join(THIS_DIR, KEY_FILENAME)

def init_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(KEY_PATH)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print("Firebase init error:", e)
        print("Looking for JSON at:", KEY_PATH)
        return None

db = init_firebase()

def save_game_result(player_name, home_city, selected_cities, player_route,
                     player_dist, best_algo_dist, best_results):

    if db is None:
        print("Firebase not initialized. Skipping save.")
        return False

    try:
        doc = {
            "player": player_name,
            "home_city": home_city,
            "selected_cities": selected_cities,
            "player_route": player_route,
            "player_distance": player_dist,
            "best_algorithm_distance": best_algo_dist,
            "results": best_results
        }

        # Saves to db
        db.collection("Traveling_Salesman_Problem").add(doc)

        print("Saved to Firebase in 'Traveling_Salesman_Problem' collection!")
        return True

    except Exception as e:
        print("Error saving to Firestore:", e)
        return False