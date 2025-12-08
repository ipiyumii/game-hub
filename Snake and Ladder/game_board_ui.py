"""
Game Board UI - Fixed player marker and darker ladder
"""
import tkinter as tk
from tkinter import messagebox
from styles import GameStyles
import math

class GameBoardUI:
    """Game board display with realistic visuals"""
    
    def __init__(self, root, game_state, on_back_callback, on_game_complete_callback):
        """Initialize game board UI"""
        self.root = root
        self.game_state = game_state
        self.on_back_callback = on_back_callback
        self.on_game_complete_callback = on_game_complete_callback
        self.styles = GameStyles()
        
        self.frame = None
        self.canvas = None
        self.cell_size = 50
        self.current_dice_value = 0
        self.dice_canvas = None
        self.player_marker_id = None  # Track player marker ID
        self.player_text_id = None    # Track player text ID
        self.position_label = None
        self.rolls_label = None
    
    def show(self):
        """Display the game board screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.frame = tk.Frame(self.root, bg=self.styles.get_color('bg_main'))
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self._create_header()
        
        content_frame = tk.Frame(self.frame, bg=self.styles.get_color('bg_main'))
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self._create_info_panel(content_frame)
        self._create_board_area(content_frame)
        self._create_dice_panel(content_frame)
    
    def _create_header(self):
        """Create header"""
        header = tk.Frame(self.frame, bg=self.styles.get_color('bg_dark'), height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        status = self.game_state.get_game_status()
        title_text = f"🎲 {status['player_name']}"
        
        tk.Label(
            header, text=title_text,
            font=self.styles.get_font('subtitle'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_light')
        ).pack(side=tk.LEFT, padx=30, pady=20)
        
        self.position_label = tk.Label(
            header, text=f"Position: {status['current_position']}/{status['target_position']}",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('success')
        )
        self.position_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        self.rolls_label = tk.Label(
            header, text=f"Rolls: {status['dice_rolls']}",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('warning')
        )
        self.rolls_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        tk.Button(
            header, text="⬅ New Game",
            font=self.styles.get_font('normal'),
            bg=self.styles.get_color('btn_danger'),
            fg='white', padx=20, pady=10,
            cursor='hand2', command=self.on_back_callback
        ).pack(side=tk.RIGHT, padx=30, pady=20)
    
    def _create_info_panel(self, parent):
        """Create info panel"""
        info_panel = tk.Frame(
            parent, bg=self.styles.get_color('bg_dark'),
            width=220, relief=tk.RAISED, bd=3
        )
        info_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        info_panel.pack_propagate(False)
        
        tk.Label(
            info_panel, text="📊 BOARD INFO",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('warning')
        ).pack(pady=20)
        
        board_info = self.game_state.get_board_info()
        
        details = [
            ("Board Size", f"{board_info['board_size']}×{board_info['board_size']}"),
            ("Total Cells", board_info['total_cells']),
            ("", ""),
            ("Start Cell", "1"),
            ("End Cell", board_info['total_cells']),
            ("", ""),
            ("🐍 Snakes", board_info['num_snakes']),
            ("🪜 Ladders", board_info['num_ladders'])
        ]
        
        for label, value in details:
            if label == "":
                tk.Frame(
                    info_panel,
                    bg=self.styles.get_color('border_light'),
                    height=2
                ).pack(fill=tk.X, padx=20, pady=12)
            else:
                row = tk.Frame(info_panel, bg=self.styles.get_color('bg_dark'))
                row.pack(fill=tk.X, padx=20, pady=8)
                
                tk.Label(
                    row, text=f"{label}:",
                    font=self.styles.get_font('small'),
                    bg=self.styles.get_color('bg_dark'),
                    fg=self.styles.get_color('text_light'),
                    anchor='w'
                ).pack(side=tk.LEFT)
                
                tk.Label(
                    row, text=str(value),
                    font=('Arial', 11, 'bold'),
                    bg=self.styles.get_color('bg_dark'),
                    fg=self.styles.get_color('success'),
                    anchor='e'
                ).pack(side=tk.RIGHT)
        
        tk.Frame(
            info_panel,
            bg=self.styles.get_color('border_light'),
            height=2
        ).pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            info_panel, text="HOW TO PLAY:",
            font=('Arial', 11, 'bold'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('info')
        ).pack(pady=(10, 8))
        
        instructions = [
            "1. Click 'ROLL DICE'",
            "2. Player moves automatically",
            "3. 🐍 Snakes = DOWN",
            "4. 🪜 Ladders = UP",
            "5. Reach last cell to WIN!"
        ]
        
        for instruction in instructions:
            tk.Label(
                info_panel, text=instruction,
                font=self.styles.get_font('small'),
                bg=self.styles.get_color('bg_dark'),
                fg=self.styles.get_color('text_light'),
                anchor='w', justify=tk.LEFT
            ).pack(padx=20, pady=3, anchor='w')
    
    def _create_board_area(self, parent):
        """Create game board"""
        board_frame = tk.Frame(parent, bg=self.styles.get_color('bg_main'))
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)
        
        tk.Label(
            board_frame, text="🎮 GAME BOARD",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_main'),
            fg=self.styles.get_color('text_light')
        ).pack(pady=8)
        
        canvas_frame = tk.Frame(board_frame, bg=self.styles.get_color('bg_main'))
        canvas_frame.pack(expand=True)
        
        board_size = self.game_state.board_size
        max_size = 550
        self.cell_size = min(max_size // board_size, 70)
        
        canvas_width = self.cell_size * board_size
        canvas_height = self.cell_size * board_size
        
        self.canvas = tk.Canvas(
            canvas_frame, width=canvas_width, height=canvas_height,
            bg=self.styles.get_color('cell_light'),
            highlightthickness=3,
            highlightbackground=self.styles.get_color('primary')
        )
        self.canvas.pack()
        
        self._draw_board()
        self._draw_player()
    
    def _draw_board(self):
        """Draw complete board"""
        board = self.game_state.board
        board_size = board.board_size
        
        cell_num = 1
        for row in range(board_size - 1, -1, -1):
            if (board_size - 1 - row) % 2 == 0:
                col_range = range(board_size)
            else:
                col_range = range(board_size - 1, -1, -1)
            
            for col in col_range:
                self._draw_cell(row, col, cell_num)
                cell_num += 1
        
        for base, top in board.ladders.items():
            self._draw_realistic_ladder(base, top)
        
        for head, tail in board.snakes.items():
            self._draw_realistic_snake(head, tail)
    
    def _draw_cell(self, row, col, cell_num):
        """Draw single cell"""
        x1, y1 = col * self.cell_size, row * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        
        if (row + col) % 2 == 0:
            color = self.styles.get_color('cell_light')
        else:
            color = self.styles.get_color('cell_dark')
        
        if cell_num == 1:
            color = self.styles.get_color('cell_start')
        elif cell_num == self.game_state.board.total_cells:
            color = self.styles.get_color('cell_end')
        
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color,
            outline=self.styles.get_color('border_dark'), width=1
        )
        
        font_size = max(8, self.cell_size // 5)
        self.canvas.create_text(
            (x1 + x2) / 2, (y1 + y2) / 2, text=str(cell_num),
            font=('Arial', font_size, 'bold'),
            fill=self.styles.get_color('text_dark')
        )
    
    def _draw_realistic_snake(self, head, tail):
        """Draw realistic snake"""
        board = self.game_state.board
        hr, hc = board.get_position_coordinates(head)
        tr, tc = board.get_position_coordinates(tail)
        
        x1 = hc * self.cell_size + self.cell_size // 2
        y1 = hr * self.cell_size + self.cell_size // 2
        x2 = tc * self.cell_size + self.cell_size // 2
        y2 = tr * self.cell_size + self.cell_size // 2
        
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        dx = x2 - x1
        dy = y2 - y1
        curve_offset = distance * 0.2
        offset_x = -dy / distance * curve_offset if distance > 0 else 0
        offset_y = dx / distance * curve_offset if distance > 0 else 0
        
        widths = [12, 10, 8]
        colors = [
            self.styles.get_color('snake_body'),
            self.styles.get_color('snake_pattern'),
            self.styles.get_color('snake_body')
        ]
        
        for width, color in zip(widths, colors):
            self.canvas.create_line(
                x1, y1, mid_x + offset_x, mid_y + offset_y, x2, y2,
                fill=color, width=max(width, self.cell_size // 6),
                smooth=True, splinesteps=50
            )
        
        segments = 8
        for i in range(1, segments):
            t = i / segments
            bx = (1-t)**2 * x1 + 2*(1-t)*t * (mid_x + offset_x) + t**2 * x2
            by = (1-t)**2 * y1 + 2*(1-t)*t * (mid_y + offset_y) + t**2 * y2
            
            scale_r = max(3, self.cell_size // 15)
            self.canvas.create_oval(
                bx-scale_r, by-scale_r, bx+scale_r, by+scale_r,
                fill=self.styles.get_color('snake_pattern'), outline=''
            )
        
        head_r = max(self.cell_size // 3, 15)
        
        self.canvas.create_oval(
            x1-head_r, y1-head_r, x1+head_r, y1+head_r,
            fill=self.styles.get_color('snake_head'),
            outline='black', width=2
        )
        
        eye_offset_x = head_r // 2.5
        eye_offset_y = head_r // 3
        eye_r = max(3, head_r // 4)
        
        self.canvas.create_oval(
            x1-eye_offset_x-eye_r, y1-eye_offset_y-eye_r,
            x1-eye_offset_x+eye_r, y1-eye_offset_y+eye_r,
            fill=self.styles.get_color('snake_eye'),
            outline='black', width=1
        )
        pupil_r = eye_r // 2
        self.canvas.create_oval(
            x1-eye_offset_x-pupil_r, y1-eye_offset_y-pupil_r,
            x1-eye_offset_x+pupil_r, y1-eye_offset_y+pupil_r,
            fill='black'
        )
        
        self.canvas.create_oval(
            x1+eye_offset_x-eye_r, y1-eye_offset_y-eye_r,
            x1+eye_offset_x+eye_r, y1-eye_offset_y+eye_r,
            fill=self.styles.get_color('snake_eye'),
            outline='black', width=1
        )
        self.canvas.create_oval(
            x1+eye_offset_x-pupil_r, y1-eye_offset_y-pupil_r,
            x1+eye_offset_x+pupil_r, y1-eye_offset_y+pupil_r,
            fill='black'
        )
        
        tongue_len = head_r // 2
        self.canvas.create_line(
            x1, y1+head_r//2, x1, y1+head_r+tongue_len,
            fill='#FF0000', width=2
        )
        self.canvas.create_line(
            x1, y1+head_r+tongue_len,
            x1-tongue_len//2, y1+head_r+tongue_len+3,
            fill='#FF0000', width=2
        )
        self.canvas.create_line(
            x1, y1+head_r+tongue_len,
            x1+tongue_len//2, y1+head_r+tongue_len+3,
            fill='#FF0000', width=2
        )
        
        tail_r = max(self.cell_size // 6, 8)
        self.canvas.create_oval(
            x2-tail_r, y2-tail_r, x2+tail_r, y2+tail_r,
            fill=self.styles.get_color('snake_body'),
            outline='black', width=2
        )
    
    def _draw_realistic_ladder(self, base, top):
        """Draw realistic darker wooden ladder"""
        board = self.game_state.board
        br, bc = board.get_position_coordinates(base)
        tr, tc = board.get_position_coordinates(top)
        
        x1 = bc * self.cell_size + self.cell_size // 2
        y1 = br * self.cell_size + self.cell_size // 2
        x2 = tc * self.cell_size + self.cell_size // 2
        y2 = tr * self.cell_size + self.cell_size // 2
        
        rail_width = max(6, self.cell_size // 9)
        offset = max(self.cell_size // 5, 10)
        
        shadow_offset = 3
        self.canvas.create_line(
            x1-offset+shadow_offset, y1+shadow_offset,
            x2-offset+shadow_offset, y2+shadow_offset,
            fill=self.styles.get_color('ladder_shadow'),
            width=rail_width+2, capstyle=tk.ROUND
        )
        self.canvas.create_line(
            x1+offset+shadow_offset, y1+shadow_offset,
            x2+offset+shadow_offset, y2+shadow_offset,
            fill=self.styles.get_color('ladder_shadow'),
            width=rail_width+2, capstyle=tk.ROUND
        )
        
        self.canvas.create_line(
            x1-offset, y1, x2-offset, y2,
            fill=self.styles.get_color('ladder_rail'),
            width=rail_width, capstyle=tk.ROUND
        )
        
        self.canvas.create_line(
            x1+offset, y1, x2+offset, y2,
            fill=self.styles.get_color('ladder_rail'),
            width=rail_width, capstyle=tk.ROUND
        )
        
        steps = max(4, int(math.sqrt((x2-x1)**2 + (y2-y1)**2) / (self.cell_size // 2)))
        
        for i in range(1, steps + 1):
            ratio = i / (steps + 1)
            rx1 = x1 + (x2-x1) * ratio - offset
            rx2 = x1 + (x2-x1) * ratio + offset
            ry = y1 + (y2-y1) * ratio
            
            self.canvas.create_line(
                rx1+shadow_offset, ry+shadow_offset,
                rx2+shadow_offset, ry+shadow_offset,
                fill=self.styles.get_color('ladder_shadow'),
                width=rail_width, capstyle=tk.ROUND
            )
            
            self.canvas.create_line(
                rx1, ry, rx2, ry,
                fill=self.styles.get_color('ladder_rung'),
                width=rail_width-1, capstyle=tk.ROUND
            )
            
            self.canvas.create_line(
                rx1+2, ry-1, rx2-2, ry-1,
                fill='#8D6E63', width=2
            )
    
    def _draw_player(self):
        """Draw player marker - DELETE old one first"""
        pos = self.game_state.current_position
        board = self.game_state.board
        row, col = board.get_position_coordinates(pos)
        
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        r = self.cell_size // 3
        
        # DELETE old player marker if exists
        if self.player_marker_id:
            self.canvas.delete(self.player_marker_id)
        if self.player_text_id:
            self.canvas.delete(self.player_text_id)
        
        # Draw new player marker
        self.player_marker_id = self.canvas.create_oval(
            x-r, y-r, x+r, y+r,
            fill=self.styles.get_color('cell_player'),
            outline='white', width=4
        )
        self.player_text_id = self.canvas.create_text(
            x, y, text="👤",
            font=('Arial', int(r*1.8))
        )
    
    def _update_player_position(self):
        """Update player position WITHOUT full refresh"""
        self._draw_player()
        
        status = self.game_state.get_game_status()
        self.position_label.config(text=f"Position: {status['current_position']}/{status['target_position']}")
        self.rolls_label.config(text=f"Rolls: {status['dice_rolls']}")
    
    def _create_dice_panel(self, parent):
        """Create dice panel"""
        dice_panel = tk.Frame(
            parent, bg=self.styles.get_color('bg_dark'),
            width=260, relief=tk.RAISED, bd=3
        )
        dice_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        dice_panel.pack_propagate(False)
        
        tk.Label(
            dice_panel, text="🎲 DICE",
            font=self.styles.get_font('heading'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('warning')
        ).pack(pady=15)
        
        dice_frame = tk.Frame(dice_panel, bg=self.styles.get_color('bg_dark'))
        dice_frame.pack(pady=15)
        
        dice_size = self.styles.get_size('dice_size')
        self.dice_canvas = tk.Canvas(
            dice_frame, width=dice_size, height=dice_size,
            bg=self.styles.get_color('dice_bg'),
            highlightthickness=4,
            highlightbackground=self.styles.get_color('dice_border'),
            relief=tk.RAISED, bd=3
        )
        self.dice_canvas.pack()
        
        self._draw_dice_face(0)
        
        self.roll_button = tk.Button(
            dice_panel, text="🎲 ROLL DICE",
            font=self.styles.get_font('button'),
            bg=self.styles.get_color('btn_success'),
            fg='white', padx=25, pady=18,
            cursor='hand2', relief=tk.RAISED, bd=3,
            command=self._on_roll_dice
        )
        self.roll_button.pack(pady=25)
        
        tk.Label(
            dice_panel, text="Click to roll!",
            font=self.styles.get_font('normal'),
            bg=self.styles.get_color('bg_dark'),
            fg=self.styles.get_color('text_muted')
        ).pack(pady=5)
    
    def _draw_dice_face(self, value):
        """Draw dice face with dots"""
        self.dice_canvas.delete('all')
        size = self.styles.get_size('dice_size')
        
        if value == 0:
            self.dice_canvas.create_text(
                size//2, size//2, text="?",
                font=('Arial', 50, 'bold'),
                fill=self.styles.get_color('text_muted')
            )
            return
        
        dot_positions = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
            6: [(0.25, 0.2), (0.75, 0.2), (0.25, 0.5), (0.75, 0.5), (0.25, 0.8), (0.75, 0.8)]
        }
        
        r = max(size // 10, 8)
        for pos in dot_positions.get(value, []):
            x, y = pos[0] * size, pos[1] * size
            self.dice_canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill=self.styles.get_color('dice_dot'),
                outline=''
            )
    
    def _on_roll_dice(self):
        """Handle dice roll"""
        if not self.game_state.is_game_active:
            messagebox.showinfo("Game Over", "Start a new game!", parent=self.root)
            return
        
        dice_value = self.game_state.roll_dice()
        self.current_dice_value = dice_value
        
        self._draw_dice_face(dice_value)
        
        result = self.game_state.move_player(dice_value)
        
        self._update_player_position()
        
        if result.get('won'):
            msg = f"🎉 CONGRATULATIONS!\n\nYou reached cell {self.game_state.board.total_cells}!\n\nTotal Rolls: {self.game_state.dice_rolls}"
            messagebox.showinfo("YOU WON!", msg, parent=self.root)
            self.roll_button.config(state=tk.DISABLED, bg='gray')
            
            # Trigger algorithm challenge
            self.on_game_complete_callback()
    
    def destroy(self):
        """Destroy UI"""
        if self.frame:
            self.frame.destroy() 