import logging
from groq import AsyncGroq
from core.config import settings
import base64

logger = logging.getLogger("cara.ai")
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

async def transcribe_audio_whisper(file_path: str) -> str:
    """Uses Groq Whisper to convert patient speech to text."""
    try:
        with open(file_path, "rb") as file:
            transcription = await client.audio.transcriptions.create(
                file=(file_path, file.read()),
                model="whisper-large-v3",
                response_format="text",
                language="en" # Future: map to patient's preferred_language
            )
            return transcription
    except Exception as e:
        logger.error(f"Whisper Transcription Error: {str(e)}")
        raise e

async def generate_llm_response(transcription: str, patient_context: dict) -> str:
    """Uses Llama 3 via Groq to formulate a contextual healthcare response."""
    # Strict prompt instructions to avoid medical diagnosis
    system_prompt = f"""
    You are DOSI, an elderly-friendly, emotionally supportive AI healthcare companion for CARA.
    Patient Profile: {patient_context}
    
    CRITICAL RULES:
    1. NEVER diagnose.
    2. NEVER change medication dosages.
    3. You CAN explain schedules, motivate adherence, and provide emotional support.
    4. Keep answers short, warm, and natural.
    """
    
    chat_completion = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcription}
        ],
        model="llama3-8b-8192",
        temperature=0.5,
        max_tokens=150
    )
    return chat_completion.choices[0].message.content

async def generate_wispr_voice(text: str) -> bytes:
    """
    Simulates Wispr API text-to-speech integration.
    In production, this streams the LLM text output into Wispr's TTS endpoint.
    """
    logger.info(f"Generating Wispr voice payload for: {text}")
    # Mocking byte stream for now
    return b"mock_audio_stream_bytes"
