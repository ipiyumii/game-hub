import tkinter as tk
from threading import Thread

def show_toast(title, message, duration=3):
    def toast_thread():
        toast = tk.Tk()
        toast.title(title)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.configure(bg="#FF2800")

        screen_width = toast.winfo_screenwidth()
        screen_height = toast.winfo_screenheight()
        width, height = 300, 100
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        toast.geometry(f"{width}x{height}+{x}+{y}")

        # add msg to toast
        tk.Label(
            toast,
            text="❌  " + message,
            font=("Arial", 12),
            bg="#FF2800",
            fg="white",
            wraplength=280,
            padx = 10,
            pady = 10
        ).pack(expand=True, fill="both", padx=10, pady=10)

        # Close the toast
        toast.after(duration * 1000, toast.destroy)
        toast.mainloop()

    Thread(target=toast_thread, daemon=True).start()

def show_win_popup():
    win = tk.Toplevel()
    win.title("Congratulations!")
    win.geometry("350x200")
    win.resizable(False, False)
    win.configure(bg="#ffffff")

    # Center window
    win.update_idletasks()
    x = (win.winfo_screenwidth() - win.winfo_width()) // 2
    y = (win.winfo_screenheight() - win.winfo_height()) // 2
    win.geometry(f"+{x}+{y}")
    # Icon
    icon_label = tk.Label(
        win,
        text="✔️",
        font=("Arial", 40),
        fg="green",
        bg="white"
    )
    icon_label.pack(pady=(20, 5))

    # Message
    msg_label = tk.Label(
        win,
        text="You found a new solution!",
        font=("Arial", 14, "bold"),
        bg="white"
    )
    msg_label.pack(pady=5)