import sys
sys.path.insert(0, '..')

from src import VoiceRecognitionSystem, GoogleRecognitionEngine, LanguageCode


def main():
    print("Audio File Recognition Example")
    print("=" * 50)
    
    engine = GoogleRecognitionEngine()
    vr_system = VoiceRecognitionSystem(engine)
    
    # Specify your audio file path
    audio_file = "D:\SoundTrack\sample_audio.wav"
    
    print(f"\nRecognizing speech from: {audio_file}")
    result = vr_system.recognize_from_file(audio_file)
    
    if result.success:
        print(f"✓ Recognized text: {result.text}")
        print(f"  Language: {result.language}")
    else:
        print(f"✗ Error: {result.error_message}")


if __name__ == "__main__":
    main()