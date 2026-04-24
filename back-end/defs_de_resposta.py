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
import elevenlabs
from elevenlabs.types.voice_settings import VoiceSettings
from faster_whisper import WhisperModel


def _get_env_float(name, default):
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default

#def para gravar o microfone e salvar o arquivo de áudio
def gravar_audio(filename="pergunta.wav", threshold=0.0030, silence_duration=1.0):
    filename = os.getenv("TARS_INPUT_AUDIO_FILE", filename)
    threshold = _get_env_float("AUDIO_THRESHOLD", threshold)
    silence_duration = _get_env_float("AUDIO_SILENCE_DURATION", silence_duration)

    fs = 44100
    chunk_size = 1024
    audio_data = []

    print("T.A.R.S: Ouvindo...")

    silence_chunks = 0
    max_silence_chunks = int(silence_duration * fs / chunk_size)
    falando = False

    with sd.InputStream(samplerate=fs, channels=1, dtype='float32') as stream:
        # calibrar ruído de fundo nos primeiros 0,5 segundos
        ambient_levels = []
        for _ in range(5):
            data, _ = stream.read(chunk_size)
            ambient_levels.append(np.sqrt(np.mean(np.square(data))))
        ambient_threshold = max(np.mean(ambient_levels) * 3, threshold)
        threshold = max(threshold, ambient_threshold)
        print(f"T.A.R.S: Threshold ajustado para {threshold:.4f}")

        while True:
            data, _ = stream.read(chunk_size)
            audio_data.append(data.copy())

            volume = np.sqrt(np.mean(np.square(data)))

            if volume > threshold:
                if not falando:
                    print("T.A.R.S: Detectei voz...")
                    falando = True
                silence_chunks = 0
            elif falando:
                silence_chunks += 1

            if falando and silence_chunks >= max_silence_chunks:
                print("T.A.R.S: Entendido, processando...")
                break

    audio_full = np.concatenate(audio_data, axis=0)
    audio_int16 = (audio_full * 32767).astype(np.int16)
    write(filename, fs, audio_int16)
    return filename


def transcrever_audio(filename="pergunta.wav", model_size_or_path="small", device="cpu", compute_type="int8", language="pt"):
    """Transcreve localmente o áudio usando Whisper via faster-whisper."""
    filename = os.getenv("TARS_INPUT_AUDIO_FILE", filename)
    model_size_or_path = os.getenv("WHISPER_MODEL", model_size_or_path)
    device = os.getenv("WHISPER_DEVICE", device)
    compute_type = os.getenv("WHISPER_COMPUTE_TYPE", compute_type)
    language = os.getenv("WHISPER_LANGUAGE", language)
    model = WhisperModel(model_size_or_path, device=device, compute_type=compute_type)
    segments, info = model.transcribe(filename, beam_size=5, vad_filter=True, language=language)
    texto = " ".join(segment.text for segment in segments).strip()
    print(f"T.A.R.S: Transcrição concluída ({info.language})")
    return texto


#teste de texto formatado
def exibir_quadrado(texto, largura=70):
    
    linhas = textwrap.wrap(texto, width=largura)
    
   
    print("┌" + "─" * (largura + 2) + "┐")
    
    for linha in linhas:
    
        print(f"│ {linha.ljust(largura)} │")
        

    print("└" + "─" * (largura + 2) + "┘")






def _resolve_voice_id(client, voice_name):
    if not voice_name:
        return None

    try:
        # Pega todas as vozes disponíveis para a sua API Key
        response = client.voices.get_all()
        
        # A resposta da ElevenLabs geralmente vem em um atributo chamado 'voices'
        voices = getattr(response, "voices", [])
        
        # 1. Tenta busca exata (Case Insensitive)
        for v in voices:
            if v.name.lower() == voice_name.lower():
                return v.voice_id
        
        # 2. Tenta busca parcial (se você digitar só "Sandro")
        for v in voices:
            if voice_name.lower() in v.name.lower():
                return v.voice_id

        # 3. Se não achou nada, mas a lista não está vazia, usa a primeira da lista
        if voices:
            print(f"Voz '{voice_name}' não encontrada. Usando a primeira disponível: {voices[0].name}")
            return voices[0].voice_id

    except Exception as e:
        print(f"Erro ao resolver voz: {e}")
    
    # Se tudo falhar, retorna o próprio voice_name 
    # (pode ser que você tenha passado o ID direto como string)
    return voice_name

async def tars_speak(
    texto,
    voice_name="Teste",
    output_file="tars_voice.mp3",
    output_format="mp3_22050_32",
    model_id="eleven_multilingual_v2",
    stability=0.35,
    similarity_boost=0.45,
    style=0.55,
    delay_before_playback=0,
):
    api_key = os.getenv("ELEVENLABS_API")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API não configurada")

    voice_name = os.getenv("TARS_DEFAULT_VOICE_NAME", voice_name)
    output_file = os.getenv("TARS_OUTPUT_FILE", output_file)
    output_format = os.getenv("ELEVENLABS_OUTPUT_FORMAT", output_format)
    model_id = os.getenv("ELEVENLABS_MODEL_ID", model_id)
    stability = _get_env_float("ELEVENLABS_STABILITY", stability)
    similarity_boost = _get_env_float("ELEVENLABS_SIMILARITY_BOOST", similarity_boost)
    style = _get_env_float("ELEVENLABS_STYLE", style)

    texto = str(texto).strip()
    if not texto:
        print("T.A.R.S: Texto vazio. Nada para falar.")
        return

    client = elevenlabs.ElevenLabs(api_key=api_key)
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "6EgjYphdzo2yW69NjS3h")

    voice_settings = VoiceSettings(
        stability=stability,
        similarity_boost=similarity_boost,
        style=style,
    )

    print(f"T.A.R.S: Gerando áudio para a voz '{voice_name}' ({voice_id})...")
    audio_stream = client.text_to_speech.convert(
        voice_id,
        text=texto,
        output_format=output_format,
        model_id=model_id,
        voice_settings=voice_settings,
    )

    elevenlabs.save(audio_stream, output_file)
    print(f"T.A.R.S: Áudio salvo em '{output_file}'")

    if delay_before_playback > 0:
        print(f"T.A.R.S: Aguardando {delay_before_playback} segundo(s) antes de falar...")
        await asyncio.sleep(delay_before_playback)

    if os.path.exists("ffplay.exe"):
        await asyncio.to_thread(
            subprocess.run,
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", output_file],
            check=True,
        )
    else:
        print("T.A.R.S: ffplay.exe não encontrado. O arquivo está salvo, mas não será reproduzido automaticamente.")

