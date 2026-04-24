# TARS

Projeto pessoal de assistente de voz inspirado no TARS e no Jarvis.

Hoje o foco do projeto esta no backend local: o usuario fala, o audio e transcrito, o modelo responde via Ollama e o sistema pode executar a rotina de chegada abrindo o YouTube Music.

## O que o projeto faz hoje

- Grava audio pelo microfone
- Transcreve fala localmente com `faster-whisper`
- Envia o texto para um modelo rodando no `Ollama`
- Executa tool calling para acionar ferramentas locais
- Gera a resposta em voz com `ElevenLabs`
- Reproduz o audio com `ffplay.exe`

## Estrutura atual

```text
TARS/
|-- back-end/
|   |-- main.py
|   |-- defs_de_resposta.py
|   |-- web_actions.py
|   `-- testedevoz.py
|-- front_end/
|   `-- main.html
|-- ffplay.exe
`-- README.md
```

## Backend

O fluxo principal esta em `back-end/main.py`.

Componentes importantes:

- `main.py`: orquestra gravacao, transcricao, chamada ao Ollama, execucao de ferramentas e resposta final
- `defs_de_resposta.py`: captura audio, transcreve com Whisper e sintetiza voz
- `web_actions.py`: contem a ferramenta `abrir_youtube_music`

## Ferramenta disponivel

No estado atual, a ferramenta registrada e:

- `abrir_youtube_music`: usada quando o usuario diz algo como "cheguei" ou "estou em casa"

Nesse caso, o sistema abre o Microsoft Edge com o perfil configurado e carrega a URL definida para o YouTube Music.

## Requisitos

Antes de rodar, voce precisa ter:

- Python instalado
- `Ollama` em execucao local
- O modelo escolhido baixado no Ollama
- `ffplay.exe` disponivel na raiz do projeto
- Microsoft Edge e WebDriver compativeis com o Selenium
- Chave da ElevenLabs para sintese de voz

Bibliotecas usadas no codigo:

- `python-dotenv`
- `ollama`
- `sounddevice`
- `numpy`
- `scipy`
- `edge-tts`
- `pyttsx3`
- `elevenlabs`
- `faster-whisper`
- `selenium`

## Variaveis de ambiente

Crie o arquivo `back-end/.env` com as variaveis que fizerem sentido para o seu ambiente.

Minimo recomendado:

```env
SYSTEM_PROMPT=Voce e o TARS...
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
ELEVENLABS_API=sua_chave_aqui
```

Variaveis usadas pelo projeto:

```env
SYSTEM_PROMPT=
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

ELEVENLABS_API=
ELEVENLABS_VOICE_ID=6EgjYphdzo2yW69NjS3h
ELEVENLABS_OUTPUT_FORMAT=mp3_22050_32
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
ELEVENLABS_STABILITY=0.35
ELEVENLABS_SIMILARITY_BOOST=0.45
ELEVENLABS_STYLE=0.55

TARS_DEFAULT_VOICE_NAME=Teste
TARS_OUTPUT_FILE=tars_voice.mp3
TARS_INPUT_AUDIO_FILE=pergunta.wav

WHISPER_MODEL=small
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
WHISPER_LANGUAGE=pt

AUDIO_THRESHOLD=0.0030
AUDIO_SILENCE_DURATION=1.0

PROFILE_PATH=C:\Users\guilh\AppData\Local\Microsoft\Edge\User Data
EDGE_PROFILE_NAME=Profile 1
YOUTUBE_MUSIC_URL=https://music.youtube.com/watch?v=9vWNauaZAgg
```

## Modelo recomendado

Para maquinas mais simples, `llama3.2:3b` e um bom ponto de partida.

Para baixar:

```powershell
ollama pull llama3.2:3b
```

Se quiser algo ainda mais leve, voce pode testar `llama3.2:1b`, com a troca de velocidade por menor confiabilidade em tool calling.

## Como executar

Com o Ollama aberto e o ambiente configurado:

```powershell
cd back-end
python main.py
```

O programa vai:

1. ouvir o microfone
2. transcrever sua fala
3. gerar uma resposta com o modelo local
4. falar a resposta em audio

## Frontend

A pasta `front_end/` ja existe, mas `front_end/main.html` ainda esta vazio. Hoje a interface principal do projeto continua sendo o fluxo por voz no backend.

## Proximos passos sugeridos

- criar uma interface grafica para acompanhar transcricao e resposta
- adicionar mais ferramentas locais alem do YouTube Music
- organizar dependencias em um `requirements.txt`
- melhorar tratamento de erros e configuracao inicial
