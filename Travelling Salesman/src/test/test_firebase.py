from src.firebase_config import db

if db:
    print("✅ Firebase is initialized successfully!")
    # Try writing a test document
    try:
        db.collection("Traveling_Salesman_Problem").add({"test": "connection_ok"})
        print("✅ Test document saved successfully!")
    except Exception as e:
        print("❌ Error writing to Firestore:", e)
else:
    print("❌ Firebase not initialized. Check JSON path and credentials.")
