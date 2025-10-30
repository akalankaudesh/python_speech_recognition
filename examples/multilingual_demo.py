import sys
sys.path.insert(0, '..')

from src import VoiceRecognitionSystem, GoogleRecognitionEngine, LanguageCode


def main():
    print("Multilingual Voice Recognition Demo")
    print("=" * 50)
    
    engine = GoogleRecognitionEngine()
    vr_system = VoiceRecognitionSystem(engine)
    
    languages = [
        (LanguageCode.ENGLISH_US, "English"),
        (LanguageCode.SPANISH, "Spanish"),
        (LanguageCode.FRENCH, "French"),
    ]
    
    for lang_code, lang_name in languages:
        print(f"\n--- {lang_name} Recognition ---")
        print(f"Speak something in {lang_name}...")
        
        result = vr_system.recognize_from_microphone(language=lang_code)
        
        if result.success:
            print(f"✓ Recognized: {result.text}")
        else:
            print(f"✗ Error: {result.error_message}")
    
    # Export history
    vr_system.export_history("multilingual_history.json")
    print("\nHistory exported to multilingual_history.json")


if __name__ == "__main__":
    main()