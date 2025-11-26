from firebase_admin import firestore

from dbUtil import delete_collection


def save_sequencial_solutions_eigh_queens(solutions, N=8):
    db = firestore.client()
    parent = db.collection("eightqueens").document("sequential").collection(f"N{N}")

    delete_collection(parent)

    i = 0
    while i < len(solutions):
        sol = solutions[i]
        parent.add({
            "solution": sol,
            "board_size": N,
            "saved_at": firestore.SERVER_TIMESTAMP
        })
        i += 1

    print(f"Saved {len(solutions)} sequential solutions to Firestore.")

def save_threaded_solutions_eight_queens(solutions, N=8):
    db = firestore.client()
    parent = db.collection("eightqueens").document("threaded").collection(f"N{N}")

    delete_collection(parent)

    i = 0
    while i < len(solutions):
        sol = solutions[i]
        parent.add({
            "solution": sol,
            "board_size": N,
            "saved_at": firestore.SERVER_TIMESTAMP
        })
        i += 1

    print(f"Saved {len(solutions)} threaded solutions to Firestore.")