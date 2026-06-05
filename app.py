import streamlit as st

from utils.audio_processor import process_audio_from_youtube
from core.transcriber import transcribe_chunks

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥"
)

st.title("🎥 AI Video Assistant")

youtube_url = st.text_input(
    "Enter YouTube URL"
)

if st.button("Generate Transcript"):

    if youtube_url:

        with st.spinner("Processing video..."):

            chunks = process_audio_from_youtube(
                youtube_url
            )

            transcript = transcribe_chunks(
                chunks
            )

        st.success(
            "Transcription Complete!"
        )

        st.subheader("Transcript")

        st.text_area(
            "Transcript",
            transcript,
            height=400
        )

        with open(
            "transcript.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(transcript)

    else:
        st.warning(
            "Please enter a YouTube URL"
        )