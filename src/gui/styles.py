from tkinter import ttk


class GUIStyles:
    """Centralized style management for the GUI"""
    
    # Color scheme
    COLORS = {
        'primary': '#3498db',
        'success': '#27ae60',
        'danger': '#e74c3c',
        'warning': '#f39c12',
        'info': '#2c3e50',
        'light': '#ecf0f1',
        'dark': '#2c3e50',
        'gray': '#95a5a6',
        'background': '#f8f9fa',
    }
    
    # Font configurations
    FONTS = {
        'title': ('Arial', 16, 'bold'),
        'subtitle': ('Arial', 12, 'bold'),
        'normal': ('Arial', 10),
        'small': ('Arial', 9),
        'text_display': ('Arial', 12),
    }
    
    @staticmethod
    def setup_styles():
        """Setup all custom styles for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Title styles
        style.configure(
            'Title.TLabel',
            font=GUIStyles.FONTS['title'],
            foreground=GUIStyles.COLORS['info']
        )
        
        # Status styles
        style.configure(
            'Status.TLabel',
            font=GUIStyles.FONTS['normal'],
            foreground=GUIStyles.COLORS['gray']
        )
        
        style.configure(
            'Success.TLabel',
            font=GUIStyles.FONTS['normal'],
            foreground=GUIStyles.COLORS['success']
        )
        
        style.configure(
            'Error.TLabel',
            font=GUIStyles.FONTS['normal'],
            foreground=GUIStyles.COLORS['danger']
        )
        
        # Button styles
        style.configure(
            'Start.TButton',
            font=GUIStyles.FONTS['subtitle']
        )
        
        style.configure(
            'Stop.TButton',
            font=GUIStyles.FONTS['subtitle']
        )
        
        return style