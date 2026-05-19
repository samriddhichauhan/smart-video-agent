from utils.audio_processor import process_audio_from_youtube
from core.transcriber import transcribe_chunks

youtube_url = "https://youtu.be/63Kr3HFECHM?si=QW2l21lJxuFUxu7I"

print("Starting audio processing...\n")

chunks = process_audio_from_youtube(youtube_url)

print("\nStarting transcription...\n")

transcript = transcribe_chunks(chunks)

# Save transcript
with open("transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

print("\nTranscript saved successfully!")

print("\nFinal Transcript:\n")
print(transcript)