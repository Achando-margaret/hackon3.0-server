# backend/ai_service.py
import os
from google.generativeai import GenerativeModel, configure

configure(api_key=os.getenv("GEMINI_API_KEY"))

model = GenerativeModel("gemini-pro")

def generate_text(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("AI generation error:", e)
        return "Error generating response"

