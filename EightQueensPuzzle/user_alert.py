import random
import tkinter as tk
from threading import Thread

def show_popup(already_found, message):
    root = tk._default_root
    if root is None:
        raise RuntimeError("Tkinter root window was not initialized.")

    popup = tk.Toplevel(root)
    popup.transient(root)
    popup.grab_set()
    popup.resizable(False, False)

    if not already_found:
        bg = "#E6F4EA"
        fg = "#2E7D32"
        btn_bg = "#2E7D32"
        title = "🎉 Success!"
        text = message
        width, height = 360, 100

    else:
        bg = "#FFF8E1"
        fg = "#FF8F00"
        title = "⚠️ Warning!"
        text = ("⚠️ " + message)
        width, height = 360, 100

    popup.title(title)
    popup.configure(bg=bg)

    popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 3
    popup.geometry(f"{width}x{height}+{x}+{y}")

    if not already_found:
        canvas = tk.Canvas(popup, bg=bg, highlightthickness=0)
        canvas.place(relwidth=1, relheight=0.45, y=0)

        confetti_items = []

        def create_confetti():
            # random position at top
            x = random.randint(10, width - 10)
            size = random.randint(6, 12)
            color = random.choice([
                "#FF5252", "#FFEB3B", "#69F0AE",
                "#448AFF", "#FF4081", "#7C4DFF"
            ])
            item = canvas.create_oval(x, -10, x + size, size, fill=color, outline="")
            confetti_items.append(item)

        def animate_confetti():
            remove_list = []
            for item in confetti_items:
                canvas.move(item, 0, random.randint(2, 6))
                x1, y1, x2, y2 = canvas.coords(item)
                if y1 > 100:  # stop area
                    remove_list.append(item)

            for item in remove_list:
                canvas.delete(item)
                confetti_items.remove(item)

            if popup.winfo_exists():
                popup.after(40, animate_confetti)

        def confetti_loop():
            if popup.winfo_exists():
                create_confetti()
                popup.after(120, confetti_loop)

        # Start animation
        confetti_loop()
        animate_confetti()

    label = tk.Label(
        popup,
        text= text,
        font=("Arial",10),
        fg=fg,
        bg=bg,
        wraplength=300,
        justify="center"
    )
    label.pack(pady=(10, 10))

    # close_btn = tk.Button(
    #     popup,
    #     text="OK",
    #     command=popup.destroy,
    #     font=("Arial", 11, "bold"),
    #     bg=btn_bg,
    #     fg="white",
    #     activebackground=btn_bg,
    #     relief="flat",
    #     padx=16,
    #     pady=6
    # )
    # close_btn.pack(pady=(0, 12))
    #
    # close_btn.focus_set()
    popup.bind("<Return>", lambda e: popup.destroy())
    popup.bind("<Escape>", lambda e: popup.destroy())

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


