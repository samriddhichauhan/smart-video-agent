from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0
    )


def split_transcript(transcript: str) -> list[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_text(transcript)


def summarize_chunks(chunks: list[str]) -> list[str]:

    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert note-taking assistant."
        ),
        (
            "human",
            "Summarize this transcript chunk:\n\n{chunk}"
        )
    ])

    chain = prompt | llm | StrOutputParser()

    summaries = []

    for chunk in chunks:

        print("Summarizing chunk...")

        summary = chain.invoke({
            "chunk": chunk
        })

        summaries.append(summary)

    return summaries


def combine_summaries(chunk_summaries: list[str]) -> str:

    llm = get_llm()

    combined_text = "\n\n".join(
        chunk_summaries
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an expert summarizer.

            Combine all chunk summaries into:

            1. Executive Summary
            2. Key Points
            3. Important Concepts
            4. Final Conclusion
            """
        ),
        (
            "human",
            "{summary_text}"
        )
    ])

    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "summary_text": combined_text
    })


def summarize_transcript_file(
    transcript_file: str
):

    with open(
        transcript_file,
        "r",
        encoding="utf-8"
    ) as file:

        transcript = file.read()

    print("Splitting transcript...")

    chunks = split_transcript(
        transcript
    )

    print(
        f"Created {len(chunks)} chunks"
    )

    chunk_summaries = summarize_chunks(
        chunks
    )

    final_summary = combine_summaries(
        chunk_summaries
    )

    with open(
        "summary.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(final_summary)

    print("\n===== FINAL SUMMARY =====\n")

    print(final_summary)

    print(
        "\nSummary saved as summary.txt"
    )


if __name__ == "__main__":

    summarize_transcript_file(
        "transcript_test.txt"
    )