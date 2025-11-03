import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Callable, Dict
from datetime import datetime


class StatusBar(ttk.Frame):
    """Custom status bar with indicator"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.status_label = ttk.Label(
            self,
            text="Ready to listen...",
            style='Status.TLabel'
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Listening indicator
        self.indicator = tk.Canvas(
            self, 
            width=15, 
            height=15, 
            bg='white', 
            highlightthickness=0
        )
        self.indicator.pack(side=tk.RIGHT, padx=(10, 0))
        self.indicator_circle = self.indicator.create_oval(
            2, 2, 13, 13, 
            fill='gray', 
            outline=''
        )
    
    def update_status(self, message: str, status_type: str = 'normal'):
        """Update status message with appropriate style"""
        style_map = {
            'normal': 'Status.TLabel',
            'success': 'Success.TLabel',
            'error': 'Error.TLabel'
        }
        self.status_label.config(
            text=message, 
            style=style_map.get(status_type, 'Status.TLabel')
        )
    
    def set_indicator_color(self, color: str):
        """Set the color of the listening indicator"""
        self.indicator.itemconfig(self.indicator_circle, fill=color)


class TextDisplayWidget(ttk.LabelFrame):
    """Custom text display widget with formatting"""
    
    def __init__(self, parent, title: str = "Recognized Text"):
        super().__init__(parent, text=title, padding="10")
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Create scrolled text widget
        self.text_widget = scrolledtext.ScrolledText(
            self,
            wrap=tk.WORD,
            font=('Arial', 12),
            height=15,
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        self.text_widget.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags
        self._setup_tags()
    
    def _setup_tags(self):
        """Setup text formatting tags"""
        self.text_widget.tag_configure(
            'timestamp', 
            foreground='#95a5a6', 
            font=('Arial', 9)
        )
        self.text_widget.tag_configure(
            'language', 
            foreground='#3498db', 
            font=('Arial', 9, 'italic')
        )
        self.text_widget.tag_configure(
            'text', 
            foreground='#2c3e50', 
            font=('Arial', 12)
        )
        self.text_widget.tag_configure(
            'error', 
            foreground='#e74c3c', 
            font=('Arial', 10, 'italic')
        )
    
    def add_recognition(self, text: str, language: str):
        """Add recognized text with formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_widget.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.text_widget.insert(tk.END, f"({language}) ", 'language')
        self.text_widget.insert(tk.END, f"{text}\n\n", 'text')
        self.text_widget.see(tk.END)
    
    def add_error(self, error_message: str):
        """Add error message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.text_widget.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.text_widget.insert(tk.END, f"❌ {error_message}\n\n", 'error')
        self.text_widget.see(tk.END)
    
    def get_text(self) -> str:
        """Get all text content"""
        return self.text_widget.get(1.0, tk.END).strip()
    
    def clear(self):
        """Clear all text"""
        self.text_widget.delete(1.0, tk.END)


class ControlPanel(ttk.LabelFrame):
    """Control panel with language selection and buttons"""
    
    def __init__(
        self, 
        parent, 
        language_map: Dict[str, any], 
        on_start: Callable, 
        on_stop: Callable, 
        on_continuous_toggle: Callable
    ):
        super().__init__(parent, text="Controls", padding="10")
        
        self.language_map = language_map
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_continuous_toggle = on_continuous_toggle
        
        self.columnconfigure(1, weight=1)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create control panel widgets"""
        # Language selection
        ttk.Label(self, text="Language:").grid(
            row=0, column=0, padx=(0, 10), sticky=tk.W
        )
        
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(
            self,
            textvariable=self.language_var,
            values=list(self.language_map.keys()),
            state='readonly',
            width=20
        )
        self.language_combo.grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10)
        )
        self.language_combo.current(0)
        
        # Continuous mode checkbox
        self.continuous_var = tk.BooleanVar(value=False)
        self.continuous_check = ttk.Checkbutton(
            self,
            text="Continuous Mode",
            variable=self.continuous_var,
            command=self.on_continuous_toggle
        )
        self.continuous_check.grid(row=0, column=2, padx=(0, 10))
        
        # Start button
        self.start_button = ttk.Button(
            self,
            text="🎙️ Start Listening",
            command=self.on_start,
            style='Start.TButton',
            width=20
        )
        self.start_button.grid(row=0, column=3, padx=(0, 5))
        
        # Stop button
        self.stop_button = ttk.Button(
            self,
            text="⏹️ Stop",
            command=self.on_stop,
            style='Stop.TButton',
            width=15,
            state='disabled'
        )
        self.stop_button.grid(row=0, column=4)
    
    def get_selected_language(self) -> str:
        """Get currently selected language"""
        return self.language_var.get()
    
    def get_continuous_mode(self) -> bool:
        """Get continuous mode state"""
        return self.continuous_var.get()
    
    def set_continuous_mode(self, value: bool):
        """Set continuous mode state"""
        self.continuous_var.set(value)
    
    def enable_start(self):
        """Enable start button and disable stop button"""
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
    
    def enable_stop(self):
        """Enable stop button and disable start button"""
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')


class HistoryPanel(ttk.LabelFrame):
    """Recognition history panel"""
    
    def __init__(self, parent, title: str = "Recognition History"):
        super().__init__(parent, text=title, padding="10")
        
        self.columnconfigure(0, weight=1)
        
        # History listbox
        self.listbox = tk.Listbox(
            self,
            height=5,
            font=('Arial', 9),
            bg='#ecf0f1'
        )
        self.listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self, 
            orient=tk.VERTICAL, 
            command=self.listbox.yview
        )
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.listbox.config(yscrollcommand=scrollbar.set)
    
    def add_entry(self, text: str):
        """Add entry to history"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        display_text = text[:50] + ('...' if len(text) > 50 else '')
        entry = f"{timestamp} - {display_text}"
        self.listbox.insert(0, entry)
    
    def clear(self):
        """Clear all history"""
        self.listbox.delete(0, tk.END)