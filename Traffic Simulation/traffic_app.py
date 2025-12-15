import sys
import traceback
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from firebase_handler import FirebaseHandler

#  GLOBAL EXCEPTION HANDLER
def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler to prevent crashes and show errors"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    print(" UNCAUGHT EXCEPTION:", exc_value)
    traceback.print_exception(exc_type, exc_value, exc_traceback)

    #  Show error message box to user
    try:
        from PyQt5.QtWidgets import QMessageBox
        app = QApplication.instance()
        if app:
            error_msg = f"An error occurred:\n{str(exc_value)}\n\nCheck console for details."
            QMessageBox.critical(None, "Application Error", error_msg)
    except:
        pass  # Fallback if Qt isn't available


sys.excepthook = handle_exception

# END EXCEPTION HANDLER
class TrafficSimulationApp:
    def __init__(self):
        self.firebase_handler = FirebaseHandler()
        self.main_window = None

    def run(self):
        # Initialize Firebase
        if not self.firebase_handler.initialize_firebase():
            print("Failed to initialize Firebase. Running in offline mode.")

        # Create and show main window
        self.main_window = MainWindow(self)
        self.main_window.show()
        return self.main_window

def main():
    try:
        app = QApplication(sys.argv)

        # Create application instance
        traffic_app = TrafficSimulationApp()
        main_window = traffic_app.run()

        if main_window is None:
            print(" Application failed to start")
            return 1

        print(" Traffic Simulation started successfully!")
        # Run the application
        return app.exec_()

    except Exception as e:
        print(f" Error starting application: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")  # Keep console open to see error
        return 1

# Prevent direct execution
if __name__ == "__main__":
    main()
