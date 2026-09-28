import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class DocumentRequest(BaseModel):
    document_type: str
    party1_name: str
    party2_name: str
    purpose: str
    date: str

@app.get("/")
def home():
    return {"message": "LegalEase API is running"}

@app.post("/generate")
def generate(request: DocumentRequest):

    prompt = f"""
    Create a professional draft of a {request.document_type}.

    Details:
    Party 1: {request.party1_name}
    Party 2: {request.party2_name}
    Purpose: {request.purpose}
    Date: {request.date}

    Use the provided details in the document.
    Include the important sections normally required for this type of document.
    Use clear and professional language.
    Add a disclaimer that this is a general draft and not legal advice.
    """

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return {
        "document_type": request.document_type,
        "document": response.text
    }