from firebase_config import db

try:
    doc_ref = db.collection("tsp_game_results").document("test_doc")
    doc_ref.set({"test": "success"})
    print("Firebase connected successfully!")
except Exception as e:
    print("Firebase connection failed:", e)
