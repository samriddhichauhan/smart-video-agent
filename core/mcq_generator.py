from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
import os

def get_llm():

    api_key = os.getenv(
        "MISTRAL_API_KEY"
    )

    print(
        "API KEY FOUND:",
        api_key is not None
    )

    return ChatMistralAI(
        model="mistral-small-latest",
        mistral_api_key=api_key,
        temperature=0
    )

def generate_mcqs(transcript):

    llm = get_llm()

    prompt = f"""
You are an expert teacher.

Generate 10 multiple-choice questions from the transcript.

Format:

Question:
A)
B)
C)
D)

Correct Answer:

Transcript:

{transcript}
"""

    response = llm.invoke(
        prompt
    )

    return response.content