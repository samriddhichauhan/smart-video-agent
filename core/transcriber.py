import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
_model=None

def load_model():
    global _model
    if _model is None:
        print(f"loading model....")
        _model = whisper.load_model(WHISPER_MODEL)
        print(f"model loaded successfully")
    return _model

def transcribe_chunk(chunk_path: str , translate: bool = False) -> str:
    model = load_model()
    result = model.transcribe(chunk_path)
    return result["text"]