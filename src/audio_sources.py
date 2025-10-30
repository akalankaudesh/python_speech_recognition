import speech_recognition as sr
from typing import Optional
import logging


class AudioSource:
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def get_audio(self) -> Optional[sr.AudioData]:
        raise NotImplementedError("Subclasses must implement get_audio()")


class MicrophoneSource(AudioSource):

    def __init__(self, device_index: Optional[int] = None):
        super().__init__()
        self.device_index = device_index
        self.microphone = sr.Microphone(device_index=device_index)
    
    def get_audio(self, duration: Optional[float] = None, 
                  phrase_time_limit: Optional[float] = None) -> Optional[sr.AudioData]:
        """Capture audio from microphone"""
        try:
            with self.microphone as source:
                print("Adjusting for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening... Speak now!")
                
                audio = self.recognizer.listen(
                    source,
                    timeout=duration,
                    phrase_time_limit=phrase_time_limit
                )
                return audio
        except Exception as e:
            logging.error(f"Error capturing audio: {e}")
            return None


class FileSource(AudioSource):

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
    
    def get_audio(self) -> Optional[sr.AudioData]:

        try:
            with sr.AudioFile(self.file_path) as source:
                audio = self.recognizer.record(source)
                return audio
        except Exception as e:
            logging.error(f"Error loading audio file: {e}")
            return None