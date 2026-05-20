from utils.audio_processor import process_audio_from_youtube
from core.transcriber import transcribe_chunks


def run_test():

    TEST_URL = (
        "https://www.youtube.com/watch?v=qYNweeDHiyU"
    )

    print("\n=== TEST STARTED ===\n")

    # Download + chunk audio
    chunks = process_audio_from_youtube(
        TEST_URL
    )

    print("\nGenerated Chunks:")

    for chunk in chunks:
        print(chunk)

    print("\nStarting Transcription...\n")

    transcript = transcribe_chunks(
        chunks
    )

    print("\nTranscript Preview:\n")

    print(transcript[:500])

    with open(
        "transcript_test.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(transcript)

    print(
        "\nTranscript saved as transcript_test.txt"
    )

    print("\n=== TEST COMPLETE ===")


if __name__ == "__main__":
    run_test()