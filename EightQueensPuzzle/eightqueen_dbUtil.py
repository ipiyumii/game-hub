from firebase_admin import firestore
from dbUtil import delete_collection

def save_program_solutions(solutions, N, program_type, time_took=None):
    db = firestore.client()
    all_sols = db.collection("eightqueens").document(f"{program_type}").collection(f"N{N}")
    time_taken = db.collection("eightqueens").document(f"{program_type}").collection("timeTaken")

    delete_collection(all_sols)
    delete_collection(time_taken)

    i = 0
    while i < len(solutions):
        sol = solutions[i]
        all_sols.add({
            "solution": sol,
            "board_size": N,
        })
        i += 1

    if time_took is not None:
        time_taken.document("time").set({
            "program": f"{program_type}",
            "solutions_count": len(solutions),
            "time_taken": time_took,
        })

    print(f"Saved {len(solutions)} solutions to Firestore.")
