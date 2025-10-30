from typing import Optional, List, Dict
from datetime import datetime
import logging
import json
import speech_recognition as sr

from .constants import LanguageCode
from .models import RecognitionResult
from .audio_sources import AudioSource, MicrophoneSource, FileSource
from .recognition_engines import RecognitionEngine


class VoiceRecognitionSystem:
   
    def __init__(self, 
                 engine: RecognitionEngine,
                 default_language: LanguageCode = LanguageCode.ENGLISH_US):
        self.engine = engine
        self.default_language = default_language
        self.history: List[RecognitionResult] = []
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def recognize_from_source(self, 
                            audio_source: AudioSource,
                            language: Optional[LanguageCode] = None) -> RecognitionResult:
        """Recognize speech from an audio source"""
        if language is None:
            language = self.default_language
        
        lang_code = language.value
        
        try:
            audio = audio_source.get_audio()
            if audio is None:
                result = RecognitionResult(
                    text="",
                    language=lang_code,
                    confidence=None,
                    timestamp=datetime.now(),
                    success=False,
                    error_message="Failed to capture audio"
                )
                self.history.append(result)
                return result
            
            text, confidence = self.engine.recognize(audio, lang_code)
            
            result = RecognitionResult(
                text=text,
                language=lang_code,
                confidence=confidence,
                timestamp=datetime.now(),
                success=True
            )
            
            self.logger.info(f"Recognition successful: {text}")
            self.history.append(result)
            return result
            
        except ValueError as e:
            result = RecognitionResult(
                text="",
                language=lang_code,
                confidence=None,
                timestamp=datetime.now(),
                success=False,
                error_message=str(e)
            )
            self.logger.warning(f"Recognition failed: {e}")
            self.history.append(result)
            return result
            
        except ConnectionError as e:
            result = RecognitionResult(
                text="",
                language=lang_code,
                confidence=None,
                timestamp=datetime.now(),
                success=False,
                error_message=str(e)
            )
            self.logger.error(f"Connection error: {e}")
            self.history.append(result)
            return result
    
    def recognize_from_microphone(self, 
                                 language: Optional[LanguageCode] = None,
                                 duration: Optional[float] = None) -> RecognitionResult:
        mic_source = MicrophoneSource()
        return self.recognize_from_source(mic_source, language)
    
    def recognize_from_file(self, 
                           file_path: str,
                           language: Optional[LanguageCode] = None) -> RecognitionResult:
        file_source = FileSource(file_path)
        return self.recognize_from_source(file_source, language)
    
    def get_history(self) -> List[RecognitionResult]:
      
        return self.history
    
    def clear_history(self):
   
        self.history.clear()
        self.logger.info("History cleared")
    
    def export_history(self, file_path: str):

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                history_dict = [result.to_dict() for result in self.history]
                json.dump(history_dict, f, indent=2, ensure_ascii=False)
            self.logger.info(f"History exported to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to export history: {e}")
    
    def set_language(self, language: LanguageCode):
        self.default_language = language
        self.logger.info(f"Default language set to {language.value}")
    
    @staticmethod
    def list_available_languages() -> List[str]:
        return [lang.value for lang in LanguageCode]
    
    @staticmethod
    def list_microphones() -> Dict[int, str]:
        mic_list = {}
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            mic_list[index] = name
        return mic_list