import sys
sys.path.insert(0, '..')

from src.gui import VoiceRecognitionGUI
from src import VoiceRecognitionSystem, GoogleRecognitionEngine
import tkinter as tk


def main():
    # Create recognition system
    engine = GoogleRecognitionEngine()
    vr_system = VoiceRecognitionSystem(engine)
    
    # Create and launch GUI
    root = tk.Tk()
    app = VoiceRecognitionGUI(root, vr_system)
    root.mainloop()


if __name__ == "__main__":
    main()