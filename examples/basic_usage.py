import sys
sys.path.insert(0, '..')

from src import VoiceRecognitionSystem, GoogleRecognitionEngine, LanguageCode


def main():
    print("Basic Voice Recognition Example")
    print("=" * 50)
    
    # Initialize system
    engine = GoogleRecognitionEngine()
    vr_system = VoiceRecognitionSystem(engine)
    
    # Recognize from microphone
    print("\nSpeak something in English...")
    result = vr_system.recognize_from_microphone()
    
    if result.success:
        print(f"✓ You said: {result.text}")
    else:
        print(f"✗ Error: {result.error_message}")


if __name__ == "__main__":
    main()