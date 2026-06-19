import streamlit as st

from utils.audio_processor import process_audio_from_youtube
from core.transcriber import transcribe_chunks

# Summary Imports
try:
    from core.summarizer import (
        split_transcript,
        summarize_chunks,
        combine_summaries
    )
    SUMMARY_AVAILABLE = True
except Exception as e:
    print(e)
    SUMMARY_AVAILABLE = False

# MCQ Imports
try:
    from core.mcq_generator import generate_mcqs
    MCQ_AVAILABLE = True
except Exception as e:
    print(e)
    MCQ_AVAILABLE = False


st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide"
)

# Sidebar
with st.sidebar:

    st.title("🎥 AI Video Assistant")

    st.success("🟢 System Ready")

    st.markdown("### AI Models")

    st.info("🎤 Whisper Small")
    st.info("🧠 Mistral Small")

    st.markdown("---")

    st.markdown("""
### Features

✅ YouTube Download

✅ Speech-to-Text

✅ AI Summary

✅ Quiz Generation

✅ Transcript Export

✅ Summary Export

✅ Quiz Export
""")

youtube_url = st.text_input(
    "Enter YouTube URL"
)

# =========================
# TRANSCRIPT
# =========================

if st.button("Generate Transcript"):

    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL."
        )

    else:

        try:

            status = st.empty()

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

            st.session_state[
                "transcript"
            ] = transcript

            status.success(
                "Transcript generated successfully!"
            )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )
search_term = st.text_input(
    "🔍 Search Transcript"
)

if (
    search_term
    and "transcript" in st.session_state
):

    if search_term.lower() in st.session_state[
        "transcript"
    ].lower():

        st.success(
            f"Found '{search_term}'"
        )

    else:

        st.warning(
            f"'{search_term}' not found"
        )
tab1, tab2, tab3 = st.tabs(
    [
        "📄 Transcript",
        "📝 Summary",
        "📚 Quiz"
    ]
)
# Display Transcript

if "transcript" in st.session_state:

    st.subheader(
        "📄 Transcript"
    )

    st.text_area(
        "Transcript",
        st.session_state[
            "transcript"
        ],
        height=400
    )

    st.download_button(
        label="⬇ Download Transcript",
        data=st.session_state[
            "transcript"
        ],
        file_name="transcript.txt",
        mime="text/plain"
    )
if "transcript" in st.session_state:

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Words",
            len(
                st.session_state[
                    "transcript"
                ].split()
            )
        )

    with col2:
        st.metric(
            "Status",
            "Complete"
        )

# =========================
# SUMMARY
# =========================

if (
    "transcript" in st.session_state
    and SUMMARY_AVAILABLE
):

    if st.button(
        "Generate Summary"
    ):

        try:

            with st.spinner(
                "Generating Summary..."
            ):

                chunks = split_transcript(
                    st.session_state[
                        "transcript"
                    ]
                )

                chunk_summaries = summarize_chunks(
                    chunks
                )

                final_summary = combine_summaries(
                    chunk_summaries
                )

                st.session_state[
                    "summary"
                ] = final_summary

        except Exception as e:

            st.error(
                f"Summary Error: {str(e)}"
            )

# Display Summary

if "summary" in st.session_state:

    st.subheader(
        "📝 AI Summary"
    )

    st.write(
        st.session_state[
            "summary"
        ]
    )

    st.download_button(
        label="⬇ Download Summary",
        data=st.session_state[
            "summary"
        ],
        file_name="summary.txt",
        mime="text/plain"
    )

# =========================
# MCQs
# =========================

if (
    "transcript" in st.session_state
    and MCQ_AVAILABLE
):

    if st.button(
        "Generate MCQs"
    ):

        try:

            with st.spinner(
                "Generating MCQs..."
            ):

                mcqs = generate_mcqs(
                    st.session_state[
                        "transcript"
                    ]
                )

                st.session_state[
                    "mcqs"
                ] = mcqs

        except Exception as e:

            st.error(
                f"MCQ Error: {str(e)}"
            )

# Display MCQs

if "mcqs" in st.session_state:

    st.subheader(
        "📚 Generated Quiz"
    )

    st.text_area(
        "Quiz",
        st.session_state[
            "mcqs"
        ],
        height=500
    )

    st.download_button(
        label="⬇ Download Quiz",
        data=st.session_state[
            "mcqs"
        ],
        file_name="quiz.txt",
        mime="text/plain"
    )

# Footer

st.markdown("---")

st.markdown("""
Built with:

• Whisper AI

• yt-dlp

• FFmpeg

• Mistral AI

• Python

• Streamlit
""")