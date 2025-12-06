from tkinter import messagebox
from firebase_admin import firestore
from dbUtil import delete_collection
from eightqueen_dbUtil import fetch_all_solutions, fetch_found_solutions, save_found_solution

def check_solution(self):
    player_solution = self.store_entered_solution()

    if -1 in player_solution:
        messagebox.showerror("Error", "You must place exactly 1 queen in every row.")
        return "Incorrect solution!"

        #  compare  with saved solutions in fb
    result = validate_player_solution(player_solution, self.player_name)

    messagebox.showinfo("Result", result)

def validate_player_solution(player_solution, player_name):
    fetched_solutions = fetch_all_solutions()

    #load solved solutions
    found_solutions = fetch_found_solutions()

    #check if solution is in all solutions
    is_correct = False
    i = 0
    while i < len(fetched_solutions):
        if fetched_solutions[i] == player_solution:
            is_correct = True
            break
        i += 1

    if not is_correct:
        #not a valid solution
        messagebox.showinfo("Incorrect", "Incorrect solution!")
        return "Incorrect solution!"

    #check if solution is already found
    already_found = False
    j = 0
    while j < len(found_solutions):
        if found_solutions[j] == player_solution:
            already_found = True
            break
        j += 1

    if already_found:
        messagebox.showinfo("Info", "This solution was already found by someone else!")
        return "This solution was already found by someone else!"

    #save new correct solution
    found_solutions.append({
        "player": player_name,
        "solution": player_solution
    })

    save_found_solution(player_name, player_solution)

    if len(found_solutions) == len(fetched_solutions) - 1:
        clear_found_solutions()

    return f"Congratulations {player_name}! You found a new solution!"

#clear the flag (db)
def clear_found_solutions():
    db = firestore.client()
    collection = db.collection("eightqueens").document("player_solutions").collection("N8")
    delete_collection(collection)