# Multilingual Voice Recognition System
Python voice recognition system supporting 20+ international languages.

## Features

- 🎤 Real-time microphone recognition
- 📁 Audio file recognition (WAV, AIFF, FLAC)
- 🌍 Support for 20+ languages
- 📊 Recognition history tracking
- 💾 JSON export functionality
- 🔌 Extensible architecture
- 📝 Comprehensive logging

## Supported Languages

English (US/UK), Spanish, French, German, Italian, Portuguese, Russian, Japanese, Chinese (Mandarin), Korean, Arabic, Hindi, Dutch, Polish, Turkish, Swedish, Danish, Norwegian, Finnish, and more!

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Step 1: Clone or Download

Download this project and navigate to the directory.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note for macOS users:**
```bash
brew install portaudio
pip install pyaudio
```

**Note for Linux users:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Step 3: Install Package
```bash
pip install -e .
```

## Quick Start
```python
from src import VoiceRecognitionSystem, GoogleRecognitionEngine, LanguageCode

# Initialize the system
engine = GoogleRecognitionEngine()
vr_system = VoiceRecognitionSystem(engine)

# Recognize from microphone
result = vr_system.recognize_from_microphone()
print(f"You said: {result.text}")

# Recognize in Spanish
result = vr_system.recognize_from_microphone(language=LanguageCode.SPANISH)
print(f"Dijiste: {result.text}")

# Recognize from file
result = vr_system.recognize_from_file("audio.wav")
print(f"File content: {result.text}")
```

## Examples

Run the examples:
```bash
# Basic usage
python examples/basic_usage.py

# Multilingual demo
python examples/multilingual_demo.py

# File recognition
python examples/file_recognition.py

#Gui
python examples/gui_app.py

![GUI App Screenshot](https://github.com/user-attachments/assets/5343a573-66bd-48de-a3e7-d6a24ee8c36d)

```

## API Reference

### VoiceRecognitionSystem

Main class for voice recognition operations.

**Methods:**
- `recognize_from_microphone(language=None, duration=None)` - Recognize from microphone
- `recognize_from_file(file_path, language=None)` - Recognize from audio file
- `get_history()` - Get recognition history
- `export_history(file_path)` - Export history to JSON
- `set_language(language)` - Set default language
- `list_available_languages()` - List all supported languages
- `list_microphones()` - List available microphone devices

### RecognitionResult

Data class containing recognition results.

**Attributes:**
- `text` - Recognized text
- `language` - Language code used
- `confidence` - Confidence score (if available)
- `timestamp` - Recognition timestamp
- `success` - Success status
- `error_message` - Error message (if failed)

## Troubleshooting

### PyAudio Installation Issues

**Windows:**
Download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install:
```bash
pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### Microphone Permission Issues

Make sure to grant microphone permissions to your terminal/IDE in system settings.
