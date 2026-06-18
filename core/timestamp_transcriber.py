import whisper

model = whisper.load_model("small")

def transcribe_with_timestamps(audio_file):

    result = model.transcribe(
        audio_file,
        fp16=False
    )

    transcript = ""

    for segment in result["segments"]:

        start = int(segment["start"])

        mins = start // 60
        secs = start % 60

        transcript += (
            f"[{mins:02d}:{secs:02d}] "
            f"{segment['text']}\n"
        )

    return transcript