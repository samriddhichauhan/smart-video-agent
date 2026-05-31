from langchain_mistralai import ChatMistralAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)

import os

def get_llm():
    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
def split_transcript(transcript:str)->list[str]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(transcript)

def summarize_chunks(transcript_chunks:list[str])->list[str]:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that summarizes meeting transcripts."),
        ("human", "Summarize the following transcript chunk:\n{chunk}")
    ])
    output_parser = StrOutputParser()
    summarize_chunk = RunnableLambda(lambda chunk: output_parser.parse(prompt.format_messages(chunk=chunk), llm))
    return [summarize_chunk.run(chunk) for chunk in transcript_chunks]    