import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Optional
import speech_recognition as sr

from ..constants import LanguageCode
from ..main import VoiceRecognitionSystem
from ..recognition_engines import GoogleRecognitionEngine
from .styles import GUIStyles
from .widgets import StatusBar, TextDisplayWidget, ControlPanel, HistoryPanel


class VoiceRecognitionGUI:
    """Main GUI Application for Voice Recognition"""
    
    def __init__(
        self, 
        root: tk.Tk, 
        recognition_system: Optional[VoiceRecognitionSystem] = None
    ):
        self.root = root
        self.root.title("Multilingual Voice Recognition System")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Initialize recognition system
        if recognition_system is None:
            engine = GoogleRecognitionEngine()
            recognition_system = VoiceRecognitionSystem(engine)
        
        self.vr_system = recognition_system
        
        # Recognition state
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.continuous_mode = False
        
        # Language mapping
        self.language_map = self._create_language_map()
        
        # Setup GUI
        GUIStyles.setup_styles()
        self._create_gui()
        self._adjust_for_noise()
    
    def _create_language_map(self):
        """Create language name to code mapping"""
        return {
            "English (US)": LanguageCode.ENGLISH_US,
            "English (UK)": LanguageCode.ENGLISH_UK,
            "Spanish": LanguageCode.SPANISH,
            "French": LanguageCode.FRENCH,
            "German": LanguageCode.GERMAN,
            "Italian": LanguageCode.ITALIAN,
            "Portuguese": LanguageCode.PORTUGUESE,
            "Russian": LanguageCode.RUSSIAN,
            "Japanese": LanguageCode.JAPANESE,
            "Chinese (Mandarin)": LanguageCode.CHINESE_MANDARIN,
            "Korean": LanguageCode.KOREAN,
            "Arabic": LanguageCode.ARABIC,
            "Hindi": LanguageCode.HINDI,
            "Dutch": LanguageCode.DUTCH,
            "Polish": LanguageCode.POLISH,
            "Turkish": LanguageCode.TURKISH,
            "Swedish": LanguageCode.SWEDISH,
            "Danish": LanguageCode.DANISH,
            "Norwegian": LanguageCode.NORWEGIAN,
            "Finnish": LanguageCode.FINNISH,
        }
    
    def _create_gui(self):
        """Create all GUI components"""
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_container,
            text="🎤 Voice Recognition System",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Control Panel
        self.control_panel = ControlPanel(
            main_container,
            self.language_map,
            self.start_listening,
            self.stop_listening,
            self.toggle_continuous_mode
        )
        self.control_panel.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Status Bar
        self.status_bar = StatusBar(main_container)
        self.status_bar.grid(row=2, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Text Display
        self.text_display = TextDisplayWidget(main_container)
        self.text_display.grid(
            row=3, column=0, pady=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S)
        )
        
        # History Panel
        self.history_panel = HistoryPanel(main_container)
        self.history_panel.grid(row=4, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Bottom Buttons
        self._create_bottom_buttons(main_container)
    
    def _create_bottom_buttons(self, parent):
        """Create bottom action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(
            button_frame, 
            text="Clear Text", 
            command=self.clear_text
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="Clear History", 
            command=self.clear_history
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="Save to File", 
            command=self.save_to_file
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="Copy Text", 
            command=self.copy_text
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="Export History", 
            command=self.export_system_history
        ).pack(side=tk.LEFT)
    
    def _adjust_for_noise(self):
        """Adjust for ambient noise in background thread"""
        self.status_bar.update_status("Adjusting for ambient noise...")
        
        def adjust():
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.status_bar.update_status("Ready to listen...")
            except Exception as e:
                self.status_bar.update_status(f"Error: {str(e)}", 'error')
        
        thread = threading.Thread(target=adjust, daemon=True)
        thread.start()
    
    def toggle_continuous_mode(self):
        """Toggle continuous listening mode"""
        self.continuous_mode = self.control_panel.get_continuous_mode()
        if self.continuous_mode and self.is_listening:
            self.status_bar.update_status(
                "Continuous mode enabled - keep speaking..."
            )
    
    def start_listening(self):
        """Start listening for speech"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.control_panel.enable_stop()
        self.status_bar.set_indicator_color('red')
        self.status_bar.update_status("Listening... Speak now!")
        
        thread = threading.Thread(target=self._listen_thread, daemon=True)
        thread.start()
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        self.continuous_mode = False
        self.control_panel.set_continuous_mode(False)
        self.control_panel.enable_start()
        self.status_bar.set_indicator_color('gray')
        self.status_bar.update_status("Stopped listening.")
    
    def _listen_thread(self):
        """Background thread for listening"""
        while self.is_listening:
            try:
                selected_language_name = self.control_panel.get_selected_language()
                language_code = self.language_map[selected_language_name]
                
                with self.microphone as source:
                    audio = self.recognizer.listen(
                        source, timeout=5, phrase_time_limit=10
                    )
                
                self.status_bar.update_status("Recognizing...")
                self.status_bar.set_indicator_color('yellow')
                
                # Use the recognition system
                text = self.recognizer.recognize_google(
                    audio, language=language_code.value
                )
                
                # Display result
                self.root.after(
                    0, self._display_recognition, 
                    text, selected_language_name
                )
                
                if not self.continuous_mode:
                    self.root.after(0, self.stop_listening)
                else:
                    self.status_bar.set_indicator_color('red')
                    self.status_bar.update_status("Listening... Speak now!")
                    
            except sr.WaitTimeoutError:
                if not self.continuous_mode:
                    self.root.after(
                        0, self.status_bar.update_status, 
                        "No speech detected.", 'error'
                    )
                    self.root.after(0, self.stop_listening)
            except sr.UnknownValueError:
                self.root.after(
                    0, self._display_error, "Could not understand audio"
                )
                if not self.continuous_mode:
                    self.root.after(0, self.stop_listening)
            except sr.RequestError as e:
                self.root.after(0, self._display_error, f"API Error: {str(e)}")
                self.root.after(0, self.stop_listening)
            except Exception as e:
                self.root.after(0, self._display_error, f"Error: {str(e)}")
                self.root.after(0, self.stop_listening)
    
    def _display_recognition(self, text: str, language: str):
        """Display recognized text"""
        self.text_display.add_recognition(text, language)
        self.history_panel.add_entry(text)
        self.status_bar.update_status(
            f"Recognized: {text[:30]}...", 'success'
        )
        self.status_bar.set_indicator_color('green')
    
    def _display_error(self, error_message: str):
        """Display error message"""
        self.text_display.add_error(error_message)
        self.status_bar.update_status(error_message, 'error')
    
    def clear_text(self):
        """Clear text display"""
        if messagebox.askyesno("Clear Text", "Clear all recognized text?"):
            self.text_display.clear()
            self.status_bar.update_status("Text cleared.")
    
    def clear_history(self):
        """Clear recognition history"""
        if messagebox.askyesno("Clear History", "Clear recognition history?"):
            self.history_panel.clear()
            self.status_bar.update_status("History cleared.")
    
    def save_to_file(self):
        """Save recognized text to file"""
        text_content = self.text_display.get_text()
        
        if not text_content:
            messagebox.showwarning("No Content", "There is no text to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                messagebox.showinfo("Success", f"Text saved to {file_path}")
                self.status_bar.update_status(
                    f"Saved to {file_path}", 'success'
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def copy_text(self):
        """Copy text to clipboard"""
        text_content = self.text_display.get_text()
        
        if not text_content:
            messagebox.showwarning("No Content", "There is no text to copy.")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(text_content)
        messagebox.showinfo("Copied", "Text copied to clipboard!")
        self.status_bar.update_status("Text copied to clipboard.", 'success')
    
    def export_system_history(self):
        """Export VoiceRecognitionSystem history to JSON"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.vr_system.export_history(file_path)
                messagebox.showinfo("Success", f"History exported to {file_path}")
                self.status_bar.update_status(
                    f"History exported to {file_path}", 'success'
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}")


def launch_gui():
    """Launch the GUI application"""
    root = tk.Tk()
    app = VoiceRecognitionGUI(root)
    root.mainloop()