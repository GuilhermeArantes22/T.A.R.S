from google import genai
from dotenv import load_dotenv
import os
from defs import gravar_audio, exibir_quadrado, tars_speak
import asyncio
#load environment variables from .env file
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API")
GEMINI_INSTRUCTIONS = os.getenv("SYSTEM_PROMPT")


#api key for gemini api
API_KEY = genai.Client(api_key=GEMINI_KEY)


audio_path = gravar_audio()


assunto = API_KEY.files.upload(file=audio_path)



response = API_KEY.models.generate_content(
    model="gemini-2.5-flash", 
    contents=[assunto, "Responda à pergunta feita no áudio seguindo a risca suas instruções de sistema."],
    config={
        "system_instruction": GEMINI_INSTRUCTIONS
    }
)

exibir_quadrado(response.text)
asyncio.run(tars_speak(response.text))
if os.path.exists(audio_path):
    os.remove(audio_path)