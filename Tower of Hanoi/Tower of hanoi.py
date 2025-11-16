import pygame
import sys

pygame.init()
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower of Hanoi — UI Only")

try:
    bg_image = pygame.image.load(
        "C:\\Users\\mihik\\OneDrive\\Documents\\BSC Computing\\PDSA GAMES\\TOWER OF HANOI\\bimage.jpg"
    ).convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image.fill((240, 240, 250))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR = (51, 0, 25)
LIGHT_BLUE = (100, 149, 237)
TITLE_COLOR = (0, 0, 51)

font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 64)

# ---------------- UI VARIABLES ----------------
NUM_DISKS = 5          # 5–10
NUM_PEGS = 3           # 3–4

BASE_WIDTH = 250
BASE_HEIGHT = 20
PEG_WIDTH = 15
PEG_HEIGHT = 280
DISK_HEIGHT = 25
MIN_DISK_WIDTH = 60
MAX_DISK_WIDTH = 200

DISK_COLORS = [
    (220, 20, 60),
    (255, 140, 0),
    (255, 215, 0),
    (50, 205, 50),
    (30, 144, 255),
]

# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, x, y, w, h, text, callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

    def draw(self, surf):
        color = LIGHT_BLUE if self.rect.collidepoint(pygame.mouse.get_pos()) else COLOR
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        t = font.render(self.text, True, WHITE)
        surf.blit(t, t.get_rect(center=self.rect.center))

    def check_click(self, pos):
        if self.callback and self.rect.collidepoint(pos):
            self.callback()


# ----------- CALLBACKS FOR UI BUTTONS -----------
def inc_disks():
    global NUM_DISKS
    if NUM_DISKS < 10:
        NUM_DISKS += 1

def dec_disks():
    global NUM_DISKS
    if NUM_DISKS > 5:
        NUM_DISKS -= 1

def inc_pegs():
    global NUM_PEGS
    if NUM_PEGS < 4:
        NUM_PEGS += 1

def dec_pegs():
    global NUM_PEGS
    if NUM_PEGS > 3:
        NUM_PEGS -= 1

def solve(): print("Solve Clicked")
def restart(): print("Restart Clicked")
def algo_time(): print("Algorithm Time Clicked")
def saved(): print("Saved Result Clicked")

buttons = [
    Button(170, 120, 130, 36, "Solve", solve),
    Button(330, 120, 160, 36, "Restart Game", restart),
    Button(520, 120, 160, 36, "Algorithm Time", algo_time),
    Button(710, 120, 160, 36, "Saved Result", saved),

    # DISK buttons
    Button(500, 160, 40, 40, "+", inc_disks),
    Button(550, 160, 40, 40, "-", dec_disks),

    # PEGS buttons
    Button(750, 160, 40, 40, "+", inc_pegs),
    Button(800, 160, 40, 40, "-", dec_pegs),
]




# ---------------- DRAW PEGS ----------------
def get_peg_positions():
    gap = SCREEN_WIDTH // (NUM_PEGS + 1)
    return [(gap * (i + 1), SCREEN_HEIGHT - 150) for i in range(NUM_PEGS)]

def draw_pegs():
    for i, pos in enumerate(get_peg_positions()):
        base = pygame.Rect(pos[0] - BASE_WIDTH // 2, pos[1], BASE_WIDTH, BASE_HEIGHT)
        peg = pygame.Rect(pos[0] - PEG_WIDTH // 2, pos[1] - PEG_HEIGHT, PEG_WIDTH, PEG_HEIGHT)

        pygame.draw.rect(screen, BLACK, base, border_radius=6)
        pygame.draw.rect(screen, BLACK, peg)

        label = font.render(f"Peg {i+1}", True, TITLE_COLOR)
        screen.blit(label, (pos[0] - label.get_width() // 2, pos[1] + 30))

# ---------------- DRAW STATIC DISKS ----------------
def get_disk_width(size):
    return MIN_DISK_WIDTH + (size - 1) * (MAX_DISK_WIDTH - MIN_DISK_WIDTH) // (NUM_DISKS - 1)

def draw_disks():
    peg_positions = get_peg_positions()
    if not peg_positions:
        return

    peg_x, peg_y = peg_positions[0]  # All disks on peg 1 (UI only)

    for i in range(NUM_DISKS):
        disk_size = NUM_DISKS - i
        width = get_disk_width(disk_size)
        y = peg_y - BASE_HEIGHT - (i + 1) * DISK_HEIGHT

        rect = pygame.Rect(peg_x - width // 2, y, width, DISK_HEIGHT - 2)
        color = DISK_COLORS[(disk_size - 1) % len(DISK_COLORS)]

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        num = font.render(str(disk_size), True, WHITE)
        screen.blit(num, (peg_x - num.get_width() // 2, y + 3))


# ---------------- MAIN LOOP ----------------
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.check_click(event.pos)

    # Background
    screen.blit(bg_image, (0, 0))

    # Title
    title = title_font.render("Tower of Hanoi", True, TITLE_COLOR)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))

    # Moves (UI only)
    text = font.render(f"Moves: 0 | Optimal: {2**NUM_DISKS - 1}", True, TITLE_COLOR)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 100))

  # Labels
    disk_label = font.render(f"DISK : [{NUM_DISKS}]", True, BLACK)
    screen.blit(disk_label, (400, 170))  

    peg_label = font.render(f"PEGS : [{NUM_PEGS}]", True, BLACK)
    screen.blit(peg_label, (650, 170))   

  

    # Draw buttons + UI
    for b in buttons:
        b.draw(screen)

    # Pegs + disks
    draw_pegs()
    draw_disks()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
