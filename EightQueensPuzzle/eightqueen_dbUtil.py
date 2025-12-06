import firebase_admin
from firebase_admin import firestore, credentials

from dbUtil import delete_collection

if not firebase_admin._apps:  #
    cred = credentials.Certificate("../shared/mind-arena.json")
    firebase_admin.initialize_app(cred)

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


def fetch_all_solutions():
    db = firestore.client()
    solutions_ref = db.collection("eightqueens").document("sequential").collection("N8")

    docs = solutions_ref.stream()
    all_solutions = []
    for doc in docs:
        data = doc.to_dict()
        # stored solution is a list of row, col pairs
        all_solutions.append(data['solution'])
    return all_solutions

def fetch_found_solutions():
    db = firestore.client()
    found_solutions = db.collection("eightqueens").document("player_solutions").collection("N8")
    found_docs = found_solutions.stream()
    found_solutions_list = []
    for doc in found_docs:
        data = doc.to_dict()
        found_solutions_list.append(data['solution'])

    return found_solutions_list

def save_found_solution(player_name, player_solution):
    db = firestore.client()
    coll = db.collection("eightqueens").document("player_solutions").collection("N8")

    coll.add({
        "player": player_name,
        "solution": player_solution
    })