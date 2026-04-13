import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import textwrap
import edge_tts
import asyncio
import subprocess
import pyttsx3
import re

#def para gravar o microfone e salvar o arquivo de áudio
def gravar_audio(filename="pergunta.wav", segundos=5):
    fs = 44100  # Frequência de amostragem
    print("T.A.R.S: Ouvindo, senhor...")
    # Captura o áudio do microfone padrão
    gravacao = sd.rec(int(segundos * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Espera a gravação terminar
    write(filename, fs, gravacao)
    print("T.A.R.S: Processando áudio...")
    return filename




#teste de texto formatado
def exibir_quadrado(texto, largura=70):
    
    linhas = textwrap.wrap(texto, width=largura)
    
   
    print("┌" + "─" * (largura + 2) + "┐")
    
    for linha in linhas:
    
        print(f"│ {linha.ljust(largura)} │")
        

    print("└" + "─" * (largura + 2) + "┘")






#def pro tars falar 
async def tars_speak(texto):
    VOICE = "pt-BR-AntonioNeural"
    OUTPUT_FILE = "tars_voice.mp3"
    


    texto_limpo = texto.replace('*', '').replace('#', '').replace('`', '')
    


    communicate = edge_tts.Communicate(texto_limpo, VOICE, rate="+4%", pitch="-6Hz")
    await communicate.save(OUTPUT_FILE)
    


    try:
        if os.path.exists("ffplay.exe"):
            subprocess.run([
                "ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", OUTPUT_FILE
            ], check=True)
        else:
            print("\n[ERRO]: ffplay.exe não encontrado na pasta do projeto.")
    finally:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
