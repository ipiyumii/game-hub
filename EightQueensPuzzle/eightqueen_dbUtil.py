import firebase_admin
from firebase_admin import firestore, credentials

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("../shared/mind-arena.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase initialization error: {e}")

def save_program_solutions(solutions, N, program_type, time_took=None, player_name=None):
    db = firestore.client()
    all_sols = db.collection("eightqueens").document(f"{program_type}").collection(f"N{N}")
    
    # Check if solutions already exist
    existing_docs = list(all_sols.stream())
    
    if not existing_docs:
        #if no solutions; save
        for sol in solutions:
            all_sols.add({
                "solution": sol,
                "board_size": N,
            })
    else:
        print(f"Solutions already exist in database. Skipping solution insertion.")
    
    # save game round with time took
    if time_took is not None:
        save_game_round(program_type, N, player_name, time_took, len(solutions))
        
def save_game_round(program_type, N, player_name, time_took, solutions_count):
    db = firestore.client()
    game_rounds = db.collection("eightqueens").document("game_rounds").collection(f"{program_type}_N{N}")
    
    from datetime import datetime
    
    existing_rounds = list(game_rounds.stream())
    round_number = len(existing_rounds) + 1
    round_id = f"round{round_number}"
    
    game_rounds.document(round_id).set({
        "program_type": program_type,
        "player_name": player_name,
        "time_taken": time_took,
        "solutions_count": solutions_count,
    })
    
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
    collection = db.collection("eightqueens").document("player_solutions").collection("N8")

    collection.add({
        "player": player_name,
        "solution": player_solution
    })

