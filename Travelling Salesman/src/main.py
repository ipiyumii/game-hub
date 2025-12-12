# src/main.py
import pygame
import sys
import math
import traceback
import game_logic
from firebase_config import save_game_result

# CONFIG
WIDTH, HEIGHT = 1200, 720
FPS = 30
CITY_RADIUS = 20
RIGHT_PANEL_W = 380
MAP_TOP_OFFSET = 40

pygame.init()
FONT = pygame.font.SysFont(None, 18)
BIG = pygame.font.SysFont(None, 22)
TITLE = pygame.font.SysFont(None, 24, bold=True)

# Map positions
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

LEFT_PANEL_W = WIDTH - RIGHT_PANEL_W - 40
POSITIONS = make_positions((LEFT_PANEL_W//2, (HEIGHT-150)//2 + MAP_TOP_OFFSET//2), 200)

def draw_text(screen, text, pos, font=FONT, color=(255,255,255), maxw=None):
    if maxw is None:
        surf = font.render(text, True, color)
        screen.blit(surf, pos)
    else:
        words = text.split()
        x, y = pos
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            surf = font.render(test, True, color)
            if surf.get_width() > maxw and line:
                screen.blit(font.render(line, True, color), (x, y))
                y += surf.get_height() + 2
                line = w
            else:
                line = test
        if line:
            screen.blit(font.render(line, True, color), (x, y))

def split_message(msg, max_len=45):
    return [msg] if len(msg) <= max_len else [msg[:max_len], msg[max_len:]]

def log_exception(e):
    tb = traceback.format_exc()
    print(tb)
    try:
        with open("error.log", "a", encoding="utf-8") as f:
            f.write(tb + "\n\n")
    except Exception:
        pass

def distance_of_route(dist_matrix, route_labels):
    idxs = [game_logic.CITIES.index(l) for l in route_labels]
    total = sum(dist_matrix[idxs[i]][idxs[i + 1]] for i in range(len(idxs) - 1))
    return total

def button_rect(x, y, w, h):
    return pygame.Rect(x, y, w, h)

def draw_button(screen, rect, text, active=True):
    pygame.draw.rect(screen, (76, 175, 80) if active else (100, 100, 100), rect)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2)
    txt = BIG.render(text, True, (255, 255, 255))
    txt_r = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_r)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Traveling Salesman - Game (Pygame)")
    clock = pygame.time.Clock()

    dist_matrix = None
    home_label = None
    selected = []
    player_route = []
    results = None
    message = "Press New Round to begin."
    player_name = ""
    input_active = False
    input_text = ""
    home_idx = None
    win_status = None

    bottom_h = 100
    bottom_y = HEIGHT - bottom_h - 20
    btn_w, btn_h, btn_gap = 140, 32, 10
    x0, y0 = 30, bottom_y + 10

    btn_new = button_rect(x0, y0, btn_w, btn_h); x0 += btn_w + btn_gap
    btn_run = button_rect(x0, y0, btn_w, btn_h); x0 += btn_w + btn_gap
    btn_clear = button_rect(x0, y0, btn_w, btn_h); x0 += btn_w + btn_gap
    btn_save = button_rect(x0, y0, btn_w, btn_h); x0 += btn_w + btn_gap
    btn_quit = button_rect(x0, y0, btn_w, btn_h)
    input_rect = button_rect(30, bottom_y + 50, 300, 28)

    results_area = pygame.Rect(WIDTH - RIGHT_PANEL_W - 20, 20, RIGHT_PANEL_W, HEIGHT - 40)
    running = True

    while running:
        delta_time = clock.tick(FPS)
        screen.fill((20,20,20))

        # --- Map panel ---
        pygame.draw.rect(screen, (40,40,40), (20, MAP_TOP_OFFSET, LEFT_PANEL_W, HEIGHT - bottom_h - 40 - MAP_TOP_OFFSET))
        draw_text(screen, "Map: cities A-J (click to build route). SHIFT+click to select target.",
                  (30, MAP_TOP_OFFSET+4), font=BIG, color=(255,255,255))

        for city, (cx, cy) in POSITIONS.items():
            color = (255, 215, 0) if city == home_label else (173,216,230) if city in selected else (200,200,200)
            if city in player_route:
                color = (0,120,215)
            outline = (255,255,255) if city == home_label else (100,100,100)
            pygame.draw.circle(screen, color, (cx,cy), CITY_RADIUS)
            pygame.draw.circle(screen, outline, (cx,cy), CITY_RADIUS, 3 if city==home_label else 2)
            draw_text(screen, city, (cx-8, cy-8), color=(0,0,0))
            if city == home_label:
                draw_text(screen, "HOME", (cx+CITY_RADIUS+6, cy-8), color=(255,200,0))

        # Draw route lines
        if len(player_route) >= 2:
            pts = [POSITIONS[c] for c in player_route]
            pygame.draw.lines(screen, (0,200,255), False, pts, 5)
            for i in range(len(player_route)-1):
                c1, c2 = player_route[i], player_route[i+1]
                x1, y1 = POSITIONS[c1]
                x2, y2 = POSITIONS[c2]
                midx, midy = (x1+x2)//2, (y1+y2)//2
                dist = dist_matrix[game_logic.CITIES.index(c1)][game_logic.CITIES.index(c2)] if dist_matrix else 0
                draw_text(screen, f"{dist:.1f}", (midx, midy), font=FONT, color=(255,255,0))
            if player_route[-1] == home_label and len(player_route) == len(selected) + 2:
                x, y0_ = POSITIONS[home_label]
                draw_text(screen, "CLOSED", (x-20, y0_+CITY_RADIUS+5), color=(0,200,255), font=BIG)

        # --- Bottom controls ---
        pygame.draw.rect(screen, (50,50,50), (20, bottom_y, LEFT_PANEL_W, bottom_h))
        draw_button(screen, btn_new, "New Round (@)")
        draw_button(screen, btn_run, "Run Algorithms (#)")
        draw_button(screen, btn_clear, "Clear Route ($)")
        draw_button(screen, btn_save, "Save Result (%)")
        draw_button(screen, btn_quit, "Quit Game (Esc)")

        # Player input
        pygame.draw.rect(screen, (30,30,30), input_rect)
        pygame.draw.rect(screen, (255,255,255), input_rect, 2)
        text_to_show = input_text if input_active else player_name or "Enter player name (click/Enter)"
        draw_text(screen, text_to_show, (input_rect.x + 6, input_rect.y + 6))
        if input_active and pygame.time.get_ticks() % 1000 < 500:
            txt_surf = FONT.render(input_text, True, (255,255,255))
            cursor_x = input_rect.x + 6 + txt_surf.get_width()
            pygame.draw.line(screen, (255,255,255), (cursor_x, input_rect.y + 8), (cursor_x, input_rect.y + 24), 2)

        # --- Right panel: results ---
        pygame.draw.rect(screen, (35,35,35), results_area)
        info_y = results_area.y + 10
        draw_text(screen, "Click cities to build your route.", (results_area.x+6, info_y), font=BIG, color=(200,200,255))
        draw_text(screen, "Use SHIFT+click to select target cities.", (results_area.x+6, info_y+22), font=BIG, color=(200,200,255))
        info_y += 50
        message_lines = split_message(message)
        for i, line in enumerate(message_lines):
            draw_text(screen, line, (results_area.x+6, info_y + i*20), color=(255,255,0))
        info_y_bottom = info_y + len(message_lines)*20
        draw_text(screen, f"Home: {home_label}", (results_area.x+6, info_y_bottom + 2))
        draw_text(screen, f"Selected: {', '.join(selected) if selected else '(none)'}",
                  (results_area.x+6, info_y_bottom + 22))
        results_y = info_y_bottom + 50
        draw_text(screen, "Algorithm results (route, distance, time):", (results_area.x+6, results_y), font=BIG)
        if results:
            y0 = results_y + 30
            player_dist = distance_of_route(dist_matrix, player_route) if len(player_route) >= 2 else None
            if player_dist is not None:
                draw_text(screen, "Player Route:", (results_area.x+6, y0), font=BIG, color=(0,200,255))
                draw_text(screen, f"Distance: {player_dist:.2f}", (results_area.x+6, y0+18), color=(0,200,255))
                y0 += 40
            for algo, data in results.items():
                draw_text(screen, algo+":", (results_area.x+6, y0))
                draw_text(screen, "Route: " + " → ".join(data["route"]), (results_area.x+6, y0+18), maxw=results_area.w-12)
                draw_text(screen, f"Distance: {data['distance']:.2f} | Time: {data['time']:.6f}s | Complexity: {data['complexity']}", (results_area.x+6, y0+36))
                y0 += 70

            # Display Win/Lose if route closed
            if player_route and player_route[0]==home_label and player_route[-1]==home_label and set(player_route[1:-1])==set(selected):
                best_dist = results["Held-Karp (DP)"]["distance"]
                if abs(player_dist - best_dist) < 1e-6:
                    win_status = ("You Win!", (0,255,0))
                else:
                    win_status = ("You Lose!", (255,0,0))
            if win_status:
                draw_text(screen, win_status[0], (results_area.x+6, y0+10), font=BIG, color=win_status[1])

        # --- Event Handling ---
        for event in pygame.event.get():
            try:
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx,my = event.pos
                    city_clicked = None
                    for city,(cx,cy) in POSITIONS.items():
                        if (mx-cx)**2+(my-cy)**2 <= CITY_RADIUS**2:
                            city_clicked = city
                            break
                    if city_clicked:
                        if pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]:
                            if city_clicked != home_label:
                                if city_clicked in selected:
                                    selected.remove(city_clicked)
                                    message=f"Unselected {city_clicked}."
                                else:
                                    selected.append(city_clicked)
                                    message=f"Selected {city_clicked} to visit."
                            else:
                                message="Cannot select home city as target."
                        else:
                            if not player_route:
                                if city_clicked != home_label:
                                    message="Start route by clicking HOME city first."
                                else:
                                    player_route.append(city_clicked)
                                    message="Home added to route."
                            else:
                                if city_clicked in player_route and city_clicked != home_label:
                                    message="City already in route."
                                elif city_clicked == home_label and len(player_route) < len(selected)+1:
                                    message="Visit all selected cities before returning home."
                                else:
                                    player_route.append(city_clicked)
                                    message=f"Added {city_clicked}."
                    elif btn_new.collidepoint((mx,my)):
                        dist_matrix = game_logic.generate_distance_matrix()
                        home_idx = game_logic.pick_random_home()
                        home_label = game_logic.CITIES[home_idx]
                        selected=[]
                        player_route=[]
                        results=None
                        message=f"New round created. Home={home_label}."
                        win_status=None
                    elif btn_run.collidepoint((mx,my)):
                        if dist_matrix is None or home_label is None:
                            message="No round active."
                        elif not selected:
                            message="Select at least one city."
                        else:
                            try:
                                results=game_logic.run_all(dist_matrix, home_label, selected)
                                message="Algorithms computed."
                                win_status=None
                            except Exception as e:
                                log_exception(e)
                                message=f"Error: {e}"
                    elif btn_clear.collidepoint((mx,my)):
                        player_route=[]
                        message="Player route cleared."
                        win_status=None
                    elif btn_save.collidepoint((mx,my)):
                        if results and len(player_route)>=2:
                            valid=player_route[0]==home_label and player_route[-1]==home_label
                            mid=player_route[1:-1]
                            if valid and set(mid)==set(selected):
                                player=player_name.strip() or input_text.strip()
                                if player:
                                    player_dist=distance_of_route(dist_matrix, player_route)
                                    best_algo_dist=min(data["distance"] for data in results.values())
                                    ok=save_game_result(player, home_label, selected, player_route, player_dist, best_algo_dist, results)
                                    message="Saved!" if ok else "Save failed."
                                else:
                                    message="Enter player name."
                            else:
                                message="Invalid route."
                        else:
                            message="Run algorithms & propose a route first."
                    elif btn_quit.collidepoint((mx,my)):
                        running=False
                    input_active = input_rect.collidepoint((mx,my))
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_BACKSPACE:
                            input_text=input_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            player_name=input_text.strip()
                            input_text=""
                            input_active=False
                            message=f"Player set: {player_name}"
                        else:
                            if event.unicode.isprintable() and len(input_text)<32:
                                input_text+=event.unicode
                    if event.key == pygame.K_ESCAPE:
                        running=False
            except Exception as e:
                log_exception(e)
                message=f"Unexpected error: {e}"

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()
