import os

from selenium import webdriver
from selenium.webdriver.edge.options import Options

_NAVEGADOR_MUSIC = None


def abrir_youtube_music():
    """
    Abre o YouTube Music para a rotina de chegada.

    Use apenas quando o usuario disser que chegou, ou algo similar.
    """

    options = Options()
    caminho_do_perfil = os.getenv(
        "PROFILE_PATH",
        "C:\\Users\\guilh\\AppData\\Local\\Microsoft\\Edge\\User Data",
    )
    edge_profile_name = os.getenv("EDGE_PROFILE_NAME", "Profile 1")
    youtube_music_url = os.getenv(
        "YOUTUBE_MUSIC_URL",
        "https://music.youtube.com/watch?v=9vWNauaZAgg",
    )

    options.add_argument(f"user-data-dir={caminho_do_perfil}")
    options.add_argument(f"profile-directory={edge_profile_name}")

    global _NAVEGADOR_MUSIC

    navegador = webdriver.Edge(options=options)
    navegador.get(youtube_music_url)
    _NAVEGADOR_MUSIC = navegador
    return "YouTube Music aberto e reproduzindo."
