import os
from typing import List, Optional
from groq import Groq

# Initialize Groq client
# client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are Dosi, a friendly medication adherence companion for CARA.
You help patients understand their health journey and stay motivated.
STRICT RULES:
- Never provide specific medical advice or diagnose
- Never tell patients to change dosage
- Always encourage them to consult their doctor for medical questions
- Keep responses short (2-3 sentences max)
- Be warm, encouraging, like a supportive friend
"""

def get_dosi_response(message: str, history: List[dict], provider: str = "groq"):
    if provider == "groq":
        model = "llama-4-scout" # Latest high-speed model from Groq
        # chat_completion = client.chat.completions.create(
        #     messages=[
        #         {"role": "system", "content": SYSTEM_PROMPT},
        #         *history,
        #         {"role": "user", "content": message},
        #     ],
        #     model=model,
        # )
        # return chat_completion.choices[0].message.content
        return f"Hi, I'm Dosi (running on {model})! I'm here to help you stay healthy with lightning speed."
    
    return "Hi, I'm Dosi! I'm here to help you stay on track."

def generate_weekly_insight(stats: dict):
    return "Your adherence is at 95%! Dosi is very happy with your progress."
