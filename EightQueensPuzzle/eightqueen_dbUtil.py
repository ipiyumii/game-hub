import firebase_admin
from firebase_admin import firestore, credentials

from dbUtil import delete_collection

if not firebase_admin._apps:  #
    cred = credentials.Certificate("../shared/mind-arena.json")
    firebase_admin.initialize_app(cred)

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
        })
        i += 1

    print(f"Saved {len(solutions)} threaded solutions to Firestore.")


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