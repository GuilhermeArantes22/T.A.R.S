# from google.cloud import texttospeech

# client = texttospeech.TextToSpeechClient()

# # Configuração do texto
# synthesis_input = texttospeech.SynthesisInput(text="Olá! Como posso ajudar você hoje?")

# # Seleção da voz (ex: Português do Brasil)
# voice = texttospeech.VoiceSelectionParams(
#     language_code="pt-BR", name="pt-BR-Wavenet-A"
# )

# # Configuração do arquivo de saída
# audio_config = texttospeech.AudioConfig(
#     audio_encoding=texttospeech.AudioEncoding.MP3
# )

# response = client.synthesize_speech(
#     input=synthesis_input, voice=voice, audio_config=audio_config
# )

# with open("output.mp3", "wb") as out:
#     out.write(response.audio_content)

from google import genai


for m in genai.list_models():
    if 'gemma' in m.name:
        print(m.name)