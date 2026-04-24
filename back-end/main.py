from pathlib import Path
from dotenv import load_dotenv
import os
import asyncio
import json
import re
from ollama import Client, RequestError, ResponseError
from defs_de_resposta import gravar_audio, exibir_quadrado, tars_speak, transcrever_audio
from web_actions import abrir_youtube_music


ENV_PATH = Path(__file__).with_name(".env")
load_dotenv(ENV_PATH)

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

OLLAMA_CLIENT = Client(host=OLLAMA_HOST)
AVAILABLE_TOOLS = {
    "abrir_youtube_music": abrir_youtube_music,
}
TOOLS_LIST = [
    {
        "type": "function",
        "function": {
            "name": "abrir_youtube_music",
            "description": (
                "Abre o YouTube Music para a rotina de chegada do usuario. "
                "Use apenas quando o usuario disser que chegou, que esta em casa ou algo similar. "
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    }
]


def normalizar_texto(texto):
    return re.sub(r"\s+", " ", (texto or "").strip().lower())


def ferramentas_ativas_para_texto(texto_usuario):
    texto = normalizar_texto(texto_usuario)
    gatilhos = (
        "cheguei",
        "estou em casa",
        "to em casa",
        "acabei de chegar",
        "voltei para casa",
    )
    return TOOLS_LIST if any(gatilho in texto for gatilho in gatilhos) else []


def deve_acionar_rotina_chegada(texto_usuario):
    return bool(ferramentas_ativas_para_texto(texto_usuario))


def executar_ferramenta(tool_name, tool_args=None):
    tool_args = normalizar_argumentos_tool_call(tool_args)
    tool_fn = AVAILABLE_TOOLS.get(tool_name)

    if not tool_fn:
        return f"Ferramenta '{tool_name}' nao esta disponivel."

    try:
        return str(tool_fn(**tool_args))
    except TypeError as exc:
        return f"Erro de argumentos ao executar '{tool_name}': {exc}"
    except Exception as exc:
        return f"Erro ao executar '{tool_name}': {exc}"


def normalizar_argumentos_tool_call(argumentos):
    if argumentos is None:
        return {}

    if isinstance(argumentos, str):
        argumentos = argumentos.strip()
        if not argumentos or argumentos in {"null", "<nil>"}:
            return {}

        try:
            argumentos = json.loads(argumentos)
        except json.JSONDecodeError:
            return {}

    return argumentos if isinstance(argumentos, dict) else {}


def extrair_tool_call_de_texto(texto):
    if not texto:
        return None

    decoder = json.JSONDecoder()
    for match in re.finditer(r"\{", texto):
        try:
            payload, _ = decoder.raw_decode(texto[match.start() :])
        except json.JSONDecodeError:
            continue

        nome = payload.get("name")
        if nome not in AVAILABLE_TOOLS:
            continue

        argumentos = normalizar_argumentos_tool_call(
            payload.get("arguments", payload.get("parameters"))
        )
        return nome, argumentos

    for tool_name in AVAILABLE_TOOLS:
        if tool_name in texto:
            return tool_name, {}

    return None


def extrair_tool_calls_da_resposta(message):
    tool_calls = list(message.tool_calls or [])
    if tool_calls:
        return tool_calls

    tool_call_textual = extrair_tool_call_de_texto(message.content or "")
    if not tool_call_textual:
        return []

    tool_name, tool_args = tool_call_textual
    return [{"function": {"name": tool_name, "arguments": tool_args}}]


def gerar_resposta_llm(texto_usuario):
    messages = []
    tools = ferramentas_ativas_para_texto(texto_usuario)

    if deve_acionar_rotina_chegada(texto_usuario):
        tool_result = executar_ferramenta("abrir_youtube_music")
        if "falha" in normalizar_texto(tool_result) or "erro" in normalizar_texto(tool_result):
            return tool_result
        return f"Bem-vindo de volta, senhor. {tool_result}"

    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

    messages.append({"role": "user", "content": texto_usuario})

    for _ in range(4):
        response = OLLAMA_CLIENT.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=tools,
        )

        assistant_message = response.message.model_dump(exclude_none=True)
        messages.append(assistant_message)
        tool_calls = extrair_tool_calls_da_resposta(response.message)

        if not tool_calls:
            return (assistant_message.get("content") or "").strip()

        for tool_call in tool_calls:
            function_call = getattr(tool_call, "function", None) or tool_call.get("function", {})
            tool_name = getattr(function_call, "name", None) or function_call.get("name")
            tool_args = normalizar_argumentos_tool_call(
                getattr(function_call, "arguments", None) or function_call.get("arguments")
            )
            tool_result = executar_ferramenta(tool_name, tool_args)

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": str(tool_result),
                }
            )

    return "Cheguei ao limite de chamadas de ferramenta e nao consegui concluir a resposta."


def main():
    audio_path = gravar_audio()

    texto_audio = transcrever_audio(audio_path)
    exibir_quadrado(f"Transcricao: {texto_audio}", largura=80)
    delay_fala = 2 if deve_acionar_rotina_chegada(texto_audio) else 0

    try:
        texto_final = gerar_resposta_llm(texto_audio)
    except (RequestError, ResponseError, ConnectionError) as exc:
        texto_final = (
            "Nao consegui falar com o Ollama. "
            f"Confirme se ele esta aberto e se o modelo '{OLLAMA_MODEL}' foi baixado. "
            f"Detalhe: {exc}"
        )

    exibir_quadrado(texto_final)
    asyncio.run(tars_speak(texto_final, delay_before_playback=delay_fala))

    if delay_fala > 0:
        import time
        time.sleep(10)
        
    if os.path.exists(audio_path):
        os.remove(audio_path)


if __name__ == "__main__":
    main()
