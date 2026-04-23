from google import genai
from dotenv import load_dotenv
import os
from defs_de_resposta import gravar_audio, exibir_quadrado, tars_speak, transcrever_audio
import asyncio
from elevenlabs import play, save, Voice, VoiceSettings
from elevenlabs.client import ElevenLabs
from web_actions import abrir_youtube_music



#load environment variables from .env file
load_dotenv()
ELEVENLABS_API = os.getenv("ELEVENLABS_API")
GEMINI_KEY = os.getenv("GEMINI_API")
GEMINI_INSTRUCTIONS = os.getenv("SYSTEM_PROMPT")


#api key for gemini api
API_KEY = genai.Client(api_key=GEMINI_KEY)
#apikey for elevenlabs
API_KEY_ELEVEN = ElevenLabs(api_key=ELEVENLABS_API)






tools_list = [abrir_youtube_music]


audio_path = gravar_audio()

texto_audio = transcrever_audio(audio_path)
exibir_quadrado(f"Transcrição: {texto_audio}", largura=80)



response = API_KEY.models.generate_content(
    model="gemini-2.5-flash",
    contents=texto_audio,
    config={
        "system_instruction": GEMINI_INSTRUCTIONS,
        "tools": tools_list,  
        "automatic_function_calling": {"disable": False} 
    }
)


texto_final = response.text

exibir_quadrado(texto_final)
asyncio.run(tars_speak(texto_final))


if os.path.exists(audio_path):
    os.remove(audio_path)