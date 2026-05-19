import yt_dlp
import os
import subprocess

DOWNLOAD_DIR = "downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

FFMPEG_PATH = r"C:\Users\samri\Downloads\ffmpeg-8.1.1-essentials_build\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"

FFMPEG_BIN = r"C:\Users\samri\Downloads\ffmpeg-8.1.1-essentials_build\ffmpeg-8.1.1-essentials_build\bin"


def download_audio_from_youtube(url: str) -> str:

    output_template = os.path.join(
        DOWNLOAD_DIR,
        "%(title)s.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",

        "outtmpl": output_template,

        "ffmpeg_location": FFMPEG_BIN,

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],

        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info_dict = ydl.extract_info(
            url,
            download=True
        )

        audio_file_path = ydl.prepare_filename(
            info_dict
        )

        audio_file_path = (
            audio_file_path
            .replace(".webm", ".mp3")
            .replace(".m4a", ".mp3")
        )

        return audio_file_path


def convert_to_wav(input_path: str) -> str:

    output_path = (
        os.path.splitext(input_path)[0]
        + ".wav"
    )

    command = [
        FFMPEG_PATH,
        "-i",
        input_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        output_path,
        "-y"
    ]

    subprocess.run(command)

    return output_path


def chunk_audio(
    input_path: str,
    chunk_length_minutes: int = 10
) -> list:

    chunk_length_seconds = (
        chunk_length_minutes * 60
    )

    output_folder = (
        os.path.splitext(input_path)[0]
        + "_chunks"
    )

    os.makedirs(output_folder, exist_ok=True)

    output_pattern = os.path.join(
        output_folder,
        "chunk_%03d.wav"
    )

    command = [
        FFMPEG_PATH,
        "-i",
        input_path,
        "-f",
        "segment",
        "-segment_time",
        str(chunk_length_seconds),
        "-c",
        "copy",
        output_pattern,
        "-y"
    ]

    subprocess.run(command)

    chunk_files = [
        os.path.join(output_folder, file)
        for file in os.listdir(output_folder)
        if file.endswith(".wav")
    ]

    return chunk_files


def process_audio_from_youtube(url: str) -> list:

    if (
        url.startswith("http://")
        or url.startswith("https://")
    ):

        print("Detecting YouTube URL")

        audio_path = download_audio_from_youtube(
            url
        )

        wav_path = convert_to_wav(
            audio_path
        )

    else:

        print("Local audio file detected")

        wav_path = convert_to_wav(
            url
        )

    print("Chunking audio")

    chunks = chunk_audio(wav_path)

    print(
        f"Audio ready - {len(chunks)} chunks generated"
    )

    return chunks


if __name__ == "__main__":

    youtube_url = (
        "https://youtu.be/63Kr3HFECHM?si=QW2l21lJxuFUxu7I"
    )

    chunks = process_audio_from_youtube(
        youtube_url
    )

    print("\nGenerated Chunks:\n")

    for chunk in chunks:
        print(chunk)