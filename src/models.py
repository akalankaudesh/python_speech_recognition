from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime
import json


@dataclass
class RecognitionResult:

    text: str
    language: str
    confidence: Optional[float]
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "language": self.language,
            "confidence": self.confidence,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "error_message": self.error_message
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)