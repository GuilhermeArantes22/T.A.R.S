import asyncio
import edge_tts
import os
import subprocess

async def testar_voz(texto, nome_voz):
    print(f"Testando a voz: {nome_voz}")
    output = "teste.mp3"
    
    # Gera o áudio localmente
    communicate = edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+5%", pitch="-7Hz")
    await communicate.save(output)
    
    # Toca o áudio (usando aquele comando de PowerShell que funcionou para você)
    path = os.path.abspath(output)
    play_script = f"""
    $MediaPlayer = New-Object System.Windows.Media.MediaPlayer
    $MediaPlayer.Open('{path}')
    while ($MediaPlayer.NaturalDuration.HasTimeSpan -eq $false) {{ Start-Sleep -Milliseconds 50 }}
    $Duration = $MediaPlayer.NaturalDuration.TimeSpan.TotalSeconds
    $MediaPlayer.Play()
    Start-Sleep -Seconds $Duration
    """
    subprocess.run(["powershell", "-Command", f"Add-Type -AssemblyName PresentationCore; {play_script}"], capture_output=True)
    
    os.remove(output)

# Lista de vozes para você ouvir
vozes = ["pt-BR-AntonioNeural"]
mensagem = "AAAAA"

for voz in vozes:
    asyncio.run(testar_voz(mensagem, voz))