import tkinter as tk
from tkinter import messagebox
from styles import GameStyles

class StartScreen:
    
    def __init__(self, root, on_start_callback):
        
        self.root = root
        self.on_start_callback = on_start_callback
        self.styles = GameStyles()
        
        self.frame = None
        self.name_entry = None
        self.size_var = None
    
    def show(self):
    
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main frame
        self.frame = tk.Frame(
            self.root,
            bg=self.styles.get_color('bg_main')
        )
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container
        container = tk.Frame(
            self.frame,
            bg=self.styles.get_color('bg_main')
        )
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Title
        title_label = tk.Label(
            container,
            text="🎲 SNAKE AND LADDER",
            font=self.styles.get_font('title'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light')
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = tk.Label(
            container,
            text="Algorithm Challenge Game",
            font=self.styles.get_font('subtitle'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('warning')
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Input frame
        input_frame = tk.Frame(
            container,
            bg=self.styles.get_color('bg_dark'),
            padx=50,
            pady=40,
            relief=tk.RAISED,
            bd=3
        )
        input_frame.pack(pady=20)
        
        # Player name section
        name_label = tk.Label(
            input_frame,
            text="Enter Your Name:",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_light')
        )
        name_label.grid(row=0, column=0, sticky='w', pady=15, padx=10)
        
        self.name_entry = tk.Entry(
            input_frame,
            font=self.styles.get_font('normal'),
            width=30,
            bg=self.styles.get_color('cell_light'),
            fg=self.styles.get_color('text_dark'),
            relief=tk.SOLID,
            bd=2
        )
        self.name_entry.grid(row=0, column=1, pady=15, padx=10)
        self.name_entry.focus()
        
        # Board size section
        size_label = tk.Label(
            input_frame,
            text="Board Size (6-12):",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_light')
        )
        size_label.grid(row=1, column=0, sticky='w', pady=15, padx=10)
        
        self.size_var = tk.IntVar(value=8)
        size_spinbox = tk.Spinbox(
            input_frame,
            from_=6,
            to=12,
            textvariable=self.size_var,
            font=self.styles.get_font('normal'),
            width=28,
            bg=self.styles.get_color('cell_light'),
            fg=self.styles.get_color('text_dark'),
            relief=tk.SOLID,
            bd=2,
            buttonbackground=self.styles.get_color('primary')
        )
        size_spinbox.grid(row=1, column=1, pady=15, padx=10)
        
        # Info text
        info_label = tk.Label(
            input_frame,
            text="Board will be N × N cells with N-2 snakes and N-2 ladders",
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_muted')
        )
        info_label.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
        # Start button
        start_button = tk.Button(
            container,
            text="🎮 START GAME",
            font=self.styles.get_font('button'),
            bg=self.styles.get_color('btn_success'),
            fg='white',
            padx=40,
            pady=15,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3,
            command=self._on_start_clicked
        )
        start_button.pack(pady=30)
        
        # Bind Enter key to start
        self.name_entry.bind('<Return>', lambda e: self._on_start_clicked())
        
        # Instructions
        instructions_label = tk.Label(
            container,
            text="🎯 Roll the dice and reach the last cell!",
            font=self.styles.get_font('normal'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('info')
        )
        instructions_label.pack(pady=10)
        
        # Footer
        footer_label = tk.Label(
            container,
            text="🐍 Snakes bring you DOWN  •  🪜 Ladders take you UP",
            font=self.styles.get_font('small'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_muted')
        )
        footer_label.pack(pady=5)
    
    def _on_start_clicked(self):
        
        player_name = self.name_entry.get().strip()
        board_size = self.size_var.get()
        
        # Validate player name
        if not player_name:
            messagebox.showerror(
                "Invalid Input",
                "Please enter your name!",
                parent=self.root
            )
            self.name_entry.focus()
            return
        
        # Validate board size
        if not 6 <= board_size <= 12:
            messagebox.showerror(
                "Invalid Input",
                "Board size must be between 6 and 12!",
                parent=self.root
            )
            return
        
        # Call callback with validated inputs
        self.on_start_callback(player_name, board_size)
    
    def destroy(self):
        
        if self.frame:
            self.frame.destroy()