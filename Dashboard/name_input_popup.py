import pygame
import pygame.font
from typing import Optional


class Colors:
    GRADIENT_START = (135, 206, 250)  
    GRADIENT_END = (25, 25, 112)     
    
    # UI Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    
    # Button colors
    BUTTON_COLOR = (70, 130, 180)     
    BUTTON_HOVER = (100, 149, 237) 
    BUTTON_PRESSED = (65, 105, 225)   
    
    # Input field colors
    INPUT_BG = (240, 248, 255)      
    INPUT_BORDER = (30, 144, 255)    
    INPUT_ACTIVE = (0, 191, 255)      
    
    # Text colors
    TITLE_COLOR = (255, 215, 0)     
    TEXT_COLOR = (25, 25, 112)      
    PLACEHOLDER_COLOR = (128, 128, 128)  


class NameInputPopup:    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Popup dimensions
        self.width = 600
        self.height = 300
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # Input field
        self.input_rect = pygame.Rect(self.x + (self.width - 300) // 2, self.y + 150, 300, 40)
        self.input_active = False
        self.player_name = ""
        self.placeholder_text = "Enter your name..."
        
        # Buttons
        button_y = self.y + 220
        total_button_width = 80 + 20 + 80  # OK button + gap + Cancel button
        button_start_x = self.x + (self.width - total_button_width) // 2
        self.ok_button = pygame.Rect(button_start_x, button_y, 80, 40)
        self.cancel_button = pygame.Rect(button_start_x + 80 + 20, button_y, 80, 40)
        
        # Button states
        self.ok_button_hovered = False
        self.cancel_button_hovered = False
        self.ok_button_pressed = False
        self.cancel_button_pressed = False
        
        # Fonts
        self.title_font = None
        self.text_font = None
        self.button_font = None
        
        # Animation
        self.popup_scale = 0.0
        self.animation_speed = 0.1
        self.is_animating = True
        
    def initialize_fonts(self):
        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 28)
    
    def draw_gradient_background(self, surface: pygame.Surface, rect: pygame.Rect, 
                               start_color: tuple, end_color: tuple):
        for y in range(rect.height):
            ratio = y / rect.height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            color = (r, g, b)
            pygame.draw.line(surface, color, 
                           (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))
    
    def draw_button(self, surface: pygame.Surface, rect: pygame.Rect, text: str, 
                   is_hovered: bool, is_pressed: bool):
        # Determine button color
        if is_pressed:
            color = Colors.BUTTON_PRESSED
        elif is_hovered:
            color = Colors.BUTTON_HOVER
        else:
            color = Colors.BUTTON_COLOR
        
        # Draw button 
        pygame.draw.rect(surface, color, rect, border_radius=10)
        pygame.draw.rect(surface, Colors.WHITE, rect, width=2, border_radius=10)
        
        # Add shadow effect
        shadow_rect = rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(surface, (0, 0, 0, 50), shadow_rect, border_radius=10)
        
        # Draw text
        text_surface = self.button_font.render(text, True, Colors.WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check input field click
            if self.input_rect.collidepoint(mouse_pos):
                self.input_active = True
            else:
                self.input_active = False
            
            # Check button clicks
            if self.ok_button.collidepoint(mouse_pos):
                self.ok_button_pressed = True
                if self.player_name.strip():
                    return self.player_name.strip()
            
            if self.cancel_button.collidepoint(mouse_pos):
                self.cancel_button_pressed = True
                return "CANCEL"
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.ok_button_pressed = False
            self.cancel_button_pressed = False
        
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.ok_button_hovered = self.ok_button.collidepoint(mouse_pos)
            self.cancel_button_hovered = self.cancel_button.collidepoint(mouse_pos)
        
        elif event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    if self.player_name.strip():
                        return self.player_name.strip()
                elif event.key == pygame.K_ESCAPE:
                    return "CANCEL"
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    if len(self.player_name) < 20: 
                        self.player_name += event.unicode
        
        return None
    
    def update_animation(self):
        if self.is_animating:
            self.popup_scale = min(1.0, self.popup_scale + self.animation_speed)
            if self.popup_scale >= 1.0:
                self.is_animating = False
    
    def draw(self, surface: pygame.Surface):
        if self.title_font is None:
            self.initialize_fonts()
        
        self.update_animation()
        
        # Create a temporary surface for the popup
        popup_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw popup background with gradient
        popup_rect = pygame.Rect(0, 0, self.width, self.height)
        self.draw_gradient_background(popup_surface, popup_rect, 
                                    Colors.GRADIENT_START, Colors.GRADIENT_END)
        
        # Draw border
        pygame.draw.rect(popup_surface, Colors.WHITE, popup_rect, width=3, border_radius=15)
        
        # Draw title
        title_text = "Welcome to Mind Arena!"
        title_surface = self.title_font.render(title_text, True, Colors.TITLE_COLOR)
        title_rect = title_surface.get_rect(centerx=self.width//2, y=30)
        popup_surface.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_text = "Please enter your name to continue"
        subtitle_surface = self.text_font.render(subtitle_text, True, Colors.WHITE)
        subtitle_rect = subtitle_surface.get_rect(centerx=self.width//2, y=80)
        popup_surface.blit(subtitle_surface, subtitle_rect)
        
        # Draw input field
        input_local_rect = pygame.Rect((self.width - 300) // 2, 150, 300, 40)
        input_color = Colors.INPUT_ACTIVE if self.input_active else Colors.INPUT_BORDER
        
        # Input field background
        pygame.draw.rect(popup_surface, Colors.INPUT_BG, input_local_rect, border_radius=5)
        pygame.draw.rect(popup_surface, input_color, input_local_rect, width=2, border_radius=5)
        
        # Input text or placeholder
        display_text = self.player_name if self.player_name else self.placeholder_text
        text_color = Colors.TEXT_COLOR if self.player_name else Colors.PLACEHOLDER_COLOR
        
        input_text_surface = self.text_font.render(display_text, True, text_color)
        text_x = input_local_rect.x + 10
        text_y = input_local_rect.centery - input_text_surface.get_height() // 2
        popup_surface.blit(input_text_surface, (text_x, text_y))
        
        # Draw cursor if input is active
        if self.input_active and pygame.time.get_ticks() % 1000 < 500:
            cursor_x = text_x + input_text_surface.get_width() + 2
            cursor_y = input_local_rect.y + 5
            pygame.draw.line(popup_surface, Colors.TEXT_COLOR, 
                           (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)
        
        # Draw buttons
        button_y_local = 220
        total_button_width = 80 + 20 + 80  # OK button + gap + Cancel button
        button_start_x_local = (self.width - total_button_width) // 2
        ok_local_rect = pygame.Rect(button_start_x_local, button_y_local, 80, 40)
        cancel_local_rect = pygame.Rect(button_start_x_local + 80 + 20, button_y_local, 80, 40)
        
        self.draw_button(popup_surface, ok_local_rect, "OK", 
                        self.ok_button_hovered, self.ok_button_pressed)
        self.draw_button(popup_surface, cancel_local_rect, "Cancel", 
                        self.cancel_button_hovered, self.cancel_button_pressed)
        
        # Scale the popup for animation
        if self.popup_scale < 1.0:
            scaled_width = int(self.width * self.popup_scale)
            scaled_height = int(self.height * self.popup_scale)
            popup_surface = pygame.transform.scale(popup_surface, (scaled_width, scaled_height))
            
            # Adjust position for scaling
            scaled_x = self.x + (self.width - scaled_width) // 2
            scaled_y = self.y + (self.height - scaled_height) // 2
        else:
            scaled_x, scaled_y = self.x, self.y
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Draw the popup
        surface.blit(popup_surface, (scaled_x, scaled_y))