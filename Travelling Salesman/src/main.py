# src/main.py
import pygame
import sys
import math
import game_logic
from firebase_config import save_game_result

# CONFIG
WIDTH, HEIGHT = 1100, 720
FPS = 30
CITY_RADIUS = 20

pygame.init()
FONT = pygame.font.SysFont(None, 20)
BIGFONT = pygame.font.SysFont(None, 28)

# arrange cities in a circle
def make_positions(center, radius):
    positions = {}
    n = len(game_logic.CITIES)
    cx, cy = center
    for i, city in enumerate(game_logic.CITIES):
        angle = 2 * math.pi * i / n
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        positions[city] = (int(x), int(y))
    return positions

POSITIONS = make_positions((400, 360), 240)

# UI helpers
def draw_text(screen, text, pos, color=(0,0,0), font=FONT):
    surf = font.render(text, True, color)
    screen.blit(surf, pos)

def distance_of_route(dist_matrix, route_labels):
    # convert to indices
    idxs = [game_logic.index_of(l) for l in route_labels]
    total = 0
    for i in range(len(idxs)-1):
        total += dist_matrix[idxs[i]][idxs[i+1]]
    return total

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Traveling Salesman Problem - Game")
    clock = pygame.time.Clock()

    # game state
    dist_matrix = None
    home_label = None
    selected = []        # list of labels selected to visit
    player_route = []    # sequence of labels clicked by player as proposed route
    results = None       # algorithm outputs
    message = "Press 'N' to start a new round (random distances & home)."
    player_name = ""

    input_active = False
    input_text = ""

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((245,245,245))

        # Left panel: map
        pygame.draw.rect(screen, (230,230,230), (20,20,760,680))
        # title
        draw_text(screen, "Cities (click to select/deselect to visit). Click sequence to propose route.", (30,30), font=BIGFONT)
        # draw cities
        for city, (x,y) in POSITIONS.items():
            color = (255,255,255)
            border = (0,0,0)
            # if home
            if city == home_label:
                color = (255, 215, 0)
                border = (200,100,0)
            # if selected to visit
            if city in selected:
                color = (173,216,230)
            pygame.draw.circle(screen, color, (x,y), CITY_RADIUS)
            pygame.draw.circle(screen, border, (x,y), CITY_RADIUS, 2)
            draw_text(screen, city, (x-6, y-8))

        # draw player's proposed route lines if any
        if len(player_route) >= 2:
            coords = [POSITIONS[c] for c in player_route]
            pygame.draw.lines(screen, (0, 100, 200), False, coords, 4)
            # draw line back to home if last not home and route complete?
            if player_route:
                # if last and route contains all selected + home return not included, show return line if clicked home
                pass

        # Right panel: controls & info
        pygame.draw.rect(screen, (250,250,250), (800,20,280,680))
        draw_text(screen, "Controls:", (810,30), font=BIGFONT)
        draw_text(screen, "N - New Round (random distances & home)", (810,70))
        draw_text(screen, "R - Run algorithms on current selection", (810,95))
        draw_text(screen, "C - Clear player's proposed route", (810,120))
        draw_text(screen, "S - Save results (only saves if player route matches optimal)", (810,145))
        draw_text(screen, "Enter player name below, then press Save to store result.", (810,170))

        draw_text(screen, f"Message: {message}", (810, 200))
        # show selected list and home
        draw_text(screen, f"Home City: {home_label}", (810, 230))
        draw_text(screen, f"Selected to visit: {', '.join(selected) if selected else '(none)'}", (810, 255))

        # show table of algorithm results
        draw_text(screen, "Algorithm results:", (810, 290), font=BIGFONT)
        if results:
            y = 330
            for algo, data in results.items():
                draw_text(screen, f"{algo}", (810, y))
                draw_text(screen, f"Route: {'→'.join(data['route'])}", (810, y+18))
                draw_text(screen, f"Distance: {data['distance']}  Time: {data['time']:.6f}s  Complexity: {data['complexity']}", (810, y+36))
                y += 70

        # player name input box
        pygame.draw.rect(screen, (255,255,255), (810, 560, 240, 28))
        pygame.draw.rect(screen, (0,0,0), (810, 560, 240, 28), 2)
        draw_text(screen, input_text or "Player name...", (815, 565))

        # draw legend of distances (optional small table)
        if dist_matrix:
            ym = 480
            draw_text(screen, "Sample distances (A-B, A-C, ...):", (810, 420))
            # show first row few distances
            row = 0
            labels = game_logic.CITIES
            for j in range(1, 6):  # show A-B..A-F
                a = labels[0]
                b = labels[j]
                d = dist_matrix[0][j]
                draw_text(screen, f"{a}-{b}: {d}", (810, 440 + 16*(j-1)))

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    # new round
                    dist_matrix = game_logic.generate_distance_matrix()
                    home_idx = game_logic.pick_random_home()
                    home_label = game_logic.CITIES[home_idx]
                    selected = []
                    player_route = []
                    results = None
                    message = f"New round created. Home={home_label}. Select cities to visit (click)."
                elif event.key == pygame.K_r:
                    if dist_matrix is None or home_label is None:
                        message = "Create a new round first (press N)."
                    else:
                        if len(selected) == 0:
                            message = "Select at least one city to visit."
                        else:
                            try:
                                results = game_logic.run_all(dist_matrix, home_label, selected)
                                message = "Algorithms computed. Compare your route with optimal (Brute Force)."
                            except Exception as e:
                                message = f"Error computing algorithms: {e}"
                elif event.key == pygame.K_c:
                    player_route = []
                    message = "Player route cleared."
                elif event.key == pygame.K_s:
                    if not results:
                        message = "Run algorithms first (R)."
                    elif len(player_route) < 2:
                        message = "You must propose a route by clicking cities in order."
                    else:
                        # validate player's route visits each selected exactly once and returns to home
                        valid = True
                        # route must start at home and end at home
                        if player_route[0] != home_label:
                            valid = False
                            message = "Your proposed route must start at the home city."
                        if player_route[-1] != home_label:
                            valid = False
                            message = "Your proposed route must end at the home city."
                        # internal cities visited exactly once and equal to selected set
                        middle = player_route[1:-1]
                        if sorted(middle) != sorted(selected):
                            valid = False
                            message = "Your proposed route must visit each selected city exactly once."
                        if valid:
                            # compute player's distance and compare with brute force optimal distance
                            player_dist = distance_of_route(dist_matrix, player_route)
                            bf = results["Brute Force"]["distance"]
                            if player_dist == bf:
                                # success -> save
                                player = input_text.strip()
                                if not player:
                                    message = "Enter player name in the input box before saving."
                                else:
                                    # save all algorithm results and times
                                    saved = save_game_result(player, home_label, selected, player_route, results)
                                    if saved:
                                        message = "Correct! Saved to Firebase."
                                    else:
                                        message = "Correct route but failed to save (see console)."
                            else:
                                message = f"Route found but not optimal. Your distance {player_dist}, optimal {bf}."
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    # confirm input
                    player_name = input_text.strip()
                    message = f"Player name set: {player_name}"
                else:
                    # capture alphanumeric for player name (simple)
                    if len(input_text) < 24 and (event.unicode.isprintable()):
                        input_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                # check if click on a city (left panel)
                for city, (cx, cy) in POSITIONS.items():
                    if (mx - cx)**2 + (my - cy)**2 <= CITY_RADIUS**2:
                        # if algorithms already run and user is clicking sequence: treat as route addition
                        # if city is already the first or last in player_route allow removing last
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            # shift+click toggles selection to visit
                            if city in selected:
                                selected.remove(city)
                            else:
                                if city == home_label:
                                    message = "Cannot select home city to visit."
                                else:
                                    selected.append(city)
                        else:
                            # normal click: add to player's proposed route
                            # if player_route empty, require starting at home
                            if not player_route:
                                if city != home_label:
                                    message = "Your route must start at the home city. Click the home city first."
                                else:
                                    player_route.append(city)
                                    message = "Added home to route. Click next city to continue (click home at end to finish)."
                            else:
                                # append city unless invalid repetition
                                if city in player_route and not (city == home_label and len(player_route) == len(selected)+1):
                                    # allow final click of home to close
                                    message = "City already in route. Do not repeat cities (except home at end)."
                                else:
                                    player_route.append(city)
                                    message = f"Added {city} to route."
                        break

        # update display for player input text (mirror input_text)
        # draw bottom instructions for SHIFT selection hint
        draw_text(screen, "Tip: SHIFT+Click toggles selecting a city to visit. Normal click appends to your proposed route (start at home).", (30, 640))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
