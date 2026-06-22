from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_response(user_message: str, user_context: dict):
    system_context = f"""
You are a friendly fitness assistant for NeuroFit AI app.

User's fitness data:
- Age: {user_context.get('age')}
- BMI: {user_context.get('bmi')}
- TDEE: {user_context.get('tdee')}
- Goal: {user_context.get('goal')}
- Activity Level: {user_context.get('activity_level')}

Answer the user's question based on this data. Keep responses short, friendly and motivating. Use emojis occasionally.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_context},
            {"role": "user", "content": user_message}
        ]
    )

    return response.choices[0].message.content