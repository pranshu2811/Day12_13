import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')

def get_bot_response(message: str) -> str:
    try:
        response = model.generate_content(message)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
