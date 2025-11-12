# Game Hub

A colorful 2D game hub with multiple mini-games, built using Python and Pygame.

## Features

- **Colorful UI**: Beautiful gradient backgrounds with animated particles
- **Name Input Popup**: Interactive popup to enter player name when the game starts
- **Animated Effects**: Smooth animations and visual effects
- **Multiple Games**: Ready to integrate various mini-games (Snake and Ladder, Eight Queens, Tower of Hanoi, etc.)

## Project Structure

```
Game/
├── main.py                 # Main game entry point
├── requirements.txt        # Python dependencies
├── ui/                     # UI components
│   ├── __init__.py
│   └── name_input_popup.py # Name input popup dialog
├── utils/                  # Utility functions
│   └── __init__.py
└── assets/                 # Game assets (images, sounds, etc.)
```

## Installation

1. Make sure you have Python 3.7+ installed
2. Navigate to the Game directory:
   ```
   cd Game
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Game

1. Navigate to the Game directory
2. Run the main game file:
   ```
   python main.py
   ```

## How to Play

1. When the game starts, a colorful popup will appear asking for your name
2. Enter your name in the input field and click "OK" or press Enter
3. The main game screen will appear with a personalized welcome message
4. Browse through the available games (coming soon!)
5. Press ESC or close the window to exit

## Controls

- **Mouse**: Click to interact with buttons and input fields
- **Keyboard**: Type to enter your name, press Enter to confirm, ESC to exit
- **Window**: Click the X button to close the game

## Features in Detail

### Name Input Popup
- Animated popup with smooth scaling effect
- Gradient background with beautiful colors
- Interactive input field with cursor
- Hover effects on buttons
- Keyboard and mouse support

### Main Game Screen
- Animated gradient background
- Floating particle effects
- Personalized welcome message
- Game selection menu (placeholder for future games)

## Customization

You can easily customize the colors by modifying the `Colors` class in `ui/name_input_popup.py`:

```python
class Colors:
    GRADIENT_START = (135, 206, 250)  # Light sky blue
    GRADIENT_END = (25, 25, 112)      # Midnight blue
    BUTTON_COLOR = (70, 130, 180)     # Steel blue
    # ... and more
```

## Adding New Games

To add new games to the hub:

1. Create a new Python file in the appropriate directory
2. Import and integrate it into `main.py`
3. Add the game option to the games list in the `draw_welcome_screen` method

## Dependencies

- **pygame**: For graphics, input handling, and game loop
- **pygame-gui**: For advanced UI components (optional)

## Future Enhancements

- Add actual game implementations
- Sound effects and background music
- Save player preferences
- High score tracking
- More advanced animations
- Fullscreen support

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check that you're running Python 3.7 or higher
3. Ensure you're in the correct directory when running the game
4. If pygame installation fails, try: `pip install pygame --user`

## Contributing

Feel free to contribute by:
- Adding new games
- Improving the UI
- Adding sound effects
- Optimizing performance
- Fixing bugs

Enjoy gaming! 🎮