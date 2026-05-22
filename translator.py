from utils.audio_processor import process_audio_from_youtube
from core.transcriber import transcribe_chunks


def translate_hindi_video():

    VIDEO_URL = input(
        "https://www.youtube.com/watch?v=dtqxANR_tiE&pp=ygURc2hvcnQgaGluZmkgdmlkZXA%3D"
    )

    print(
        "\nDownloading and processing audio...\n"
    )
    chunks = process_audio_from_youtube(
        VIDEO_URL
    )

    print(
        "\nTranslating Hindi → English...\n"
    )

    transcript = transcribe_chunks(
        chunks,
        translate=True
    )

    with open(
        "translated_output.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            transcript
        )

    print(
        "\nTranslation completed!"
    )

    print(
        "\nPreview:\n"
    )

    print(
        transcript[:1000]
    )


if __name__ == "__main__":
    translate_hindi_video()