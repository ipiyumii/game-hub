"""
Color Styles and Constants for Snake and Ladder Game
"""

class GameStyles:
    """All color schemes and styling constants"""
    
    # Main color palette
    COLORS = {
        # Background colors
        'bg_main': '#1a1a2e',
        'bg_dark': '#16213e',
        'bg_light': '#0f3460',
        
        # Primary colors
        'primary': '#3498db',
        'secondary': '#9b59b6',
        'success': '#2ecc71',
        'danger': '#e74c3c',
        'warning': '#f39c12',
        'info': '#3498db',
        
        # Text colors
        'text_light': '#ecf0f1',
        'text_dark': '#2c3e50',
        'text_muted': '#95a5a6',
        
        # Cell colors
        'cell_light': '#ecf0f1',
        'cell_dark': '#bdc3c7',
        'cell_start': '#a8e6cf',
        'cell_end': '#ffd3b6',
        'cell_player': '#3498db',
        
        # Snake colors - realistic
        'snake_body': '#228B22',
        'snake_head': '#006400',
        'snake_pattern': '#90EE90',
        'snake_eye': '#FFD700',
        
        # Ladder colors - darker wooden
        'ladder_rail': '#5D4037',
        'ladder_rung': '#6D4C41',
        'ladder_shadow': '#3E2723',
        
        # Border colors
        'border_light': '#34495e',
        'border_dark': '#2c3e50',
        
        # Button colors
        'btn_primary': '#3498db',
        'btn_success': '#2ecc71',
        'btn_danger': '#e74c3c',
        'btn_warning': '#f39c12',
        'btn_hover': '#2980b9',
        
        # Dice colors
        'dice_bg': '#ffffff',
        'dice_dot': '#2c3e50',
        'dice_border': '#3498db',
    }
    
    # Font styles
    FONTS = {
        'title': ('Arial', 40, 'bold'),
        'subtitle': ('Arial', 18, 'bold'),
        'heading': ('Arial', 16, 'bold'),
        'normal': ('Arial', 12),
        'small': ('Arial', 10),
        'button': ('Arial', 14, 'bold'),
        'cell_number': ('Arial', 10, 'bold'),
        'dice': ('Arial', 24, 'bold'),
        'dice_value': ('Arial', 32, 'bold'),
        'choice': ('Arial', 18, 'bold'),
    }
    
    # Sizes
    SIZES = {
        'window_width': 1400,
        'window_height': 850,
        'min_cell_size': 40,
        'max_cell_size': 80,
        'padding': 20,
        'button_padding_x': 30,
        'button_padding_y': 10,
        'dice_size': 120,
    }
    
    @staticmethod
    def get_color(color_name):
        """Get color by name"""
        return GameStyles.COLORS.get(color_name, '#ffffff')
    
    @staticmethod
    def get_font(font_name):
        """Get font by name"""
        return GameStyles.FONTS.get(font_name, ('Arial', 12))
    
    @staticmethod
    def get_size(size_name):
        """Get size by name"""
        return GameStyles.SIZES.get(size_name, 20)