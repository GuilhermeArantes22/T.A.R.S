Esse e um projeto pessoal.

Esse e o TARS, um agente de IA inspirado no Jarvis do UCM.
Agora o backend pode rodar localmente com Ollama, sem depender da API do Gemini.

## LLM local

O arquivo `back-end/main.py` usa o Ollama com function calling para executar ferramentas locais, como `abrir_youtube_music`.

Variaveis esperadas no `back-end/.env`:

- `SYSTEM_PROMPT`
- `OLLAMA_HOST=http://localhost:11434`
- `OLLAMA_MODEL=llama3.2:3b`
- `ELEVENLABS_API`

## Modelo recomendado

Para PC mais fraco, o melhor ponto de partida aqui e `llama3.2:3b`.
Na biblioteca do Ollama, a familia `llama3.2` destaca suporte a tool use, e o tamanho de 3B costuma ser um bom equilibrio entre leveza e confiabilidade.

Se quiser algo ainda mais leve, teste `llama3.2:1b`, mas a confiabilidade no function calling tende a cair.

Para baixar o modelo:

```powershell
ollama pull llama3.2:3b
```

## Futuras adicoes

- Adicionar a interface grafica do TARS
- Adicionar leitura de PDF
- Melhorar o uso de tokens nas respostas
