# Game Hub

A colorful 2D game hub with multiple mini-games, built using Python and Pygame.

## Features

- **Colorful Name Input Popup**: Interactive popup to enter player name when the game starts
- **Animated Dashboard**: Beautiful gradient backgrounds with animated particles
- **Database Integration**: Firebase integration for game data management
- **Multiple Games**: Ready to integrate various mini-games

## Project Structure

```
game-hub/
├── main.py                          # Main entry point
├── requirements.txt                 # Dependencies
├── dbUtil.py                        # Database utilities (Firebase)
├── shared/                          # Shared resources
│   └── mind-arena.json             # Firebase configuration
├── Game/                           # Game dashboard and UI
│   ├── dashboard.py                # Game dashboard main logic
│   ├── requirements.txt            # Game-specific dependencies
│   ├── README.md                   # Game documentation
│   ├── ui/                         # UI components
│   │   ├── __init__.py
│   │   └── name_input_popup.py     # Name input popup dialog
│   ├── utils/                      # Utility functions
│   │   └── __init__.py
│   └── assets/                     # Game assets
└── [Game Folders]/                 # Individual game implementations
    ├── Eight queens' puzzle/
    ├── Snake and Ladder/
    ├── Tower of Hanoi/
    ├── Traffic Simulation/
    └── Travelling Salesman/
```

## Installation

1. Make sure you have Python 3.7+ installed
2. Clone or download this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

From the root directory, run:
```bash
python snake_and_ladder_main.py
```

This will:
1. Test database connectivity (if dbUtil.py exists)
2. Launch the colorful game dashboard
3. Show a name input popup
4. Display the main game selection screen

## How to Play

1. When the game starts, a colorful popup will appear asking for your name
2. Enter your name and click "OK" or press Enter
3. Browse through available games on the main dashboard
4. Press ESC or close the window to exit

## Controls

- **Mouse**: Click to interact with buttons and input fields
- **Keyboard**: Type to enter your name, press Enter to confirm, ESC to exit
- **Window**: Click the X button to close the game

## Development

### Adding New Games

1. Create a new folder for your game in the root directory
2. Implement your game logic
3. Add your game to the dashboard by modifying `Game/dashboard.py`

### Customizing Colors

Modify the `Colors` class in `Game/ui/name_input_popup.py`:

```python
class Colors:
    GRADIENT_START = (135, 206, 250)  # Light sky blue
    GRADIENT_END = (25, 25, 112)      # Midnight blue
    # ... customize other colors
```

## Dependencies

- **pygame**: For graphics, input handling, and game loop
- **firebase-admin** (optional): For database operations

## Troubleshooting

1. **Import errors**: Make sure you're running from the root directory
2. **Pygame installation issues**: Try `pip install pygame --user`
3. **Database errors**: Ensure `shared/mind-arena.json` exists for Firebase integration

## Future Enhancements

- Sound effects and background music
- Save player preferences and high scores
- More advanced animations and effects
- Game-specific leaderboards
- Multiplayer support

Enjoy gaming! 🎮
