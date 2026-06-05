import streamlit as st

from utils.audio_processor import process_audio_from_youtube
from core.transcriber import transcribe_chunks
from core.summarizer import (
    split_transcript,
    summarize_chunks,
    combine_summaries
)

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("🎥 AI Video Assistant")

    st.markdown("""
    ### Features

    ✅ YouTube Audio Download

    ✅ Whisper Transcription

    ✅ Hindi Translation

    ✅ AI Summarization

    ✅ Download Transcript

    ✅ Download Summary
    """)

# Main UI
st.title("🎥 AI Video Assistant")

youtube_url = st.text_input(
    "Enter YouTube URL"
)

if st.button("Generate Transcript"):

    if youtube_url:

        status = st.empty()

        try:

            status.info(
                "Downloading and processing audio..."
            )

            chunks = process_audio_from_youtube(
                youtube_url
            )

            status.info(
                "Generating transcript..."
            )

            transcript = transcribe_chunks(
                chunks
            )

            status.success(
                "Transcription Complete!"
            )

            st.subheader("Transcript")

            st.text_area(
                "Transcript",
                transcript,
                height=400
            )

            st.download_button(
                "⬇ Download Transcript",
                transcript,
                file_name="transcript.txt"
            )

            # Save transcript for summary
            st.session_state["transcript"] = transcript

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

    else:

        st.warning(
            "Please enter a YouTube URL"
        )

# Summary Section
if "transcript" in st.session_state:

    if st.button("Generate Summary"):

        try:

            with st.spinner(
                "Generating AI Summary..."
            ):

                transcript = st.session_state[
                    "transcript"
                ]

                chunks = split_transcript(
                    transcript
                )

                chunk_summaries = summarize_chunks(
                    chunks
                )

                final_summary = combine_summaries(
                    chunk_summaries
                )

            st.success(
                "Summary Generated!"
            )

            st.subheader(
                "AI Summary"
            )

            st.write(
                final_summary
            )

            st.download_button(
                "⬇ Download Summary",
                final_summary,
                file_name="summary.txt"
            )

        except Exception as e:

            st.error(
                f"Summary Error: {str(e)}"
            )