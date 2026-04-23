from pathlib import Path
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.edge.options import Options



def abrir_youtube_music():
    """
    Inicia a rotina de boas-vindas do TARS. 
    Deve ser chamada sempre que o usuário disser que chegou, que está em casa 
    ou comandos similares de saudação de entrada."""
    



    options = Options()
    caminho_do_perfil = "C:\\Users\\guilh\\AppData\\Local\\Microsoft\\Edge\\User Data"
    edge_profile_name = "Profile 1"

    options.add_argument(f"user-data-dir={caminho_do_perfil}")
    options.add_argument(f"profile-directory={edge_profile_name}") 

    
    navegador = webdriver.Edge(options=options)
    
    try:
        navegador.get("https://music.youtube.com/watch?v=9vWNauaZAgg")
        time.sleep(1) 
        return "Protocolo de chegada ativado e música carregada."
    except Exception as e:
        return f"Falha ao abrir o navegador: {e}"

