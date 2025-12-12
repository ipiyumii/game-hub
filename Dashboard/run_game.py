
"""
Simple test script to run the Game Hub
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"Current directory: {current_dir}")
print(f"Python path: {sys.path[:3]}")  
try:
    print("Attempting to import main module...")
    from main import main
    print("Main module imported successfully!")
    
    print("Starting the game...")
    main()
    
except ImportError as e:
    print(f"Import error: {e}")
    print("\nChecking file structure:")
    for item in os.listdir(current_dir):
        print(f"  {item}")
    
except Exception as e:
    print(f"Error running game: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")