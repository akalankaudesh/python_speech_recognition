import speech_recognition as sr
from typing import Optional, Tuple


class RecognitionEngine:

    def recognize(self, audio: sr.AudioData, language: str) -> Tuple[str, Optional[float]]:
       
        raise NotImplementedError("Subclasses must implement recognize()")


class GoogleRecognitionEngine(RecognitionEngine):

    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.recognizer = sr.Recognizer()
    
    def recognize(self, audio: sr.AudioData, language: str) -> Tuple[str, Optional[float]]:
        
        try:
            if self.api_key:
                text = self.recognizer.recognize_google(
                    audio, 
                    key=self.api_key, 
                    language=language,
                    show_all=False
                )
            else:
                text = self.recognizer.recognize_google(
                    audio, 
                    language=language,
                    show_all=False
                )
            return text, None
        except sr.UnknownValueError:
            raise ValueError("Could not understand audio")
        except sr.RequestError as e:
            raise ConnectionError(f"API request error: {e}")


class SphinxRecognitionEngine(RecognitionEngine):
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def recognize(self, audio: sr.AudioData, language: str) -> Tuple[str, Optional[float]]:

        try:
            text = self.recognizer.recognize_sphinx(audio, language=language)
            return text, None
        except sr.UnknownValueError:
            raise ValueError("Could not understand audio")
        except sr.RequestError as e:
            raise ConnectionError(f"Sphinx error: {e}")