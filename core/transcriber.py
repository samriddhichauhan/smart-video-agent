import whisper
import os

# Load model name from environment
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

# Global cached model
_model = None


def load_model():
    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL}...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Model loaded successfully!")

    return _model


def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:
    """
    Transcribes or translates a single audio chunk.
    """

    model = load_model()

    task = "translate" if translate else "transcribe"

    result = model.transcribe(
    chunk_path,
    task=task,
    fp16=False
)

    return result["text"]


def transcribe_chunks(chunks: list[str], translate: bool = False) -> str:
    """
    Transcribes multiple chunks and combines them.
    """

    full_transcription = ""

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}")

        try:
            text = transcribe_chunk(chunk, translate)

            full_transcription += text + "\n"

            print("Chunk transcription completed!")

        except Exception as e:
            print(f"Error transcribing {chunk}: {e}")

    return full_transcription.strip()