from tkinter import messagebox
from firebase_admin import firestore

from EightQueensPuzzle.user_alert import show_toast, show_popup
from dbUtil import delete_collection
from EightQueensPuzzle.eightqueen_dbUtil import (
    fetch_all_solutions,
    fetch_found_solutions,
    save_found_solution
)

def check_solution(self):
    player_solution = self.store_entered_solution()

    if -1 in player_solution:
        messagebox.showerror("Error", "You must place exactly 1 queen in every row.")
        return "Incorrect solution!"

        #  compare  with saved solutions in fb
    validate_player_solution(player_solution, self.player_name)

def validate_player_solution(player_solution, player_name):
    try:
        fetched_solutions = fetch_all_solutions()

        #load solved solutions
        found_solutions = fetch_found_solutions()
    except Exception as e:
        print(f"Error fetching solutions from database player_solutions: {e}")

    #check if solution is in all solutions
    is_correct = False
    i = 0
    while i < len(fetched_solutions):
        if fetched_solutions[i] == player_solution:
            is_correct = True
            break
        i += 1

    #not a valid solution
    if not is_correct:
        show_toast("Result", "Incorrect solution!")
        return

    #check if solution is already found
    already_found = False
    j = 0
    while j < len(found_solutions):
        if found_solutions[j] == player_solution:
            already_found = True
            break
        j += 1

    if already_found:
        show_popup("Info", "This solution was already found by someone else!")
        return
    else:
        #save new correct solution
        found_solutions.append({
            "player": player_name,
            "solution": player_solution
        })

        try:
            save_found_solution(player_name, player_solution)
        except Exception as e:
            print(f"Error saving found solution to database: {e}")

    #clear flag
    if len(found_solutions) == len(fetched_solutions) - 1:
        clear_found_solutions()
    show_popup(already_found,f"Congratulations {player_name}! \n You found a new solution!")
    return

#clear the flag (db)
def clear_found_solutions():
    db = firestore.client()
    collection = db.collection("eightqueens").document("player_solutions").collection("N8")
    delete_collection(collection)