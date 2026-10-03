import os
import google.generativeai as genai
from core.config import settings

genai.configure(api_key=settings.AI_API_KEY)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, prompt: str, user_role: str, context_data: str = "") -> str:
        system_prompt = f"You are a Freelance Marketplace AI Assistant. The user is a {user_role}. Do not invent data. Be helpful."
        full_prompt = f"{system_prompt}\n\nMarketplace Data Context:\n{context_data}\n\nUser Question:\n{prompt}"
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"

ai_service = AIService()
