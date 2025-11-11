from dbUtil import initialize_firebase, get_all_games


def main():
    db = initialize_firebase("shared/mind-arena.json")

    games = get_all_games(db)
    for game in games:
        print(game)

if __name__ == "__main__":
    main()