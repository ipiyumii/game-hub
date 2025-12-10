import firebase_admin
from firebase_admin import credentials, firestore
import os

FIREBASE_KEY_PATH = os.path.join(os.path.dirname(__file__), "pdsa-project-firebase-adminsdk-fbsvc-4bd448c3aa.json")

def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = init_firebase()

def save_game_result(player_name, home_city, selected_cities, route, total_distance, algorithm, elapsed_time):
    try:
        doc_ref = db.collection("tsp_game_results").document()
        doc_ref.set({
            "player": player_name,
            "home_city": home_city,
            "selected_cities": selected_cities,
            "shortest_route": route,
            "total_distance": total_distance,
            "algorithm": algorithm,
            "time_taken": elapsed_time
        })
    except Exception as e:
        print("Error saving to Firebase:", e)
