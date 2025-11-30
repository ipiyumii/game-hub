from firebase_admin import firestore

from dbUtil import delete_collection


def save_sequencial_solutions_eigh_queens(solutions, N=8, timeTaken = None):
    db = firestore.client()
    all_sols = db.collection("eightqueens").document("sequential").collection(f"N{N}")
    timetaken = db.collection("eightqueens").document("sequential").collection("timeTaken")

    delete_collection(all_sols)

    i = 0
    while i < len(solutions):
        sol = solutions[i]
        all_sols.add({
            "solution": sol,
            "board_size": N,
        })
        i += 1

    if timeTaken is not None:
        timetaken.document("time").set({
            "program": "sequential",
            "solutions_count": len(solutions),
            "time_taken": timeTaken,
        })

    print(f"Saved {len(solutions)} sequential solutions to Firestore.")

def save_threaded_solutions_eight_queens(solutions, N=8, timeTaken = None):
    db = firestore.client()
    all_sols = db.collection("eightqueens").document("threaded").collection(f"N{N}")
    timetaken = db.collection("eightqueens").document("sequential").collection("timeTaken")

    delete_collection(all_sols)

    i = 0
    while i < len(solutions):
        sol = solutions[i]
        all_sols.add({
            "solution": sol,
            "board_size": N,
        })
        i += 1
    
        if timeTaken is not None:
            timetaken.document("time").set({
            "program": "threaded",
            "solutions_count": len(solutions),
            "time_taken": timeTaken,
        })

    print(f"Saved {len(solutions)} threaded solutions to Firestore.")