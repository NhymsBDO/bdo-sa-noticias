import requests
from bs4 import BeautifulSoup
import os

# --- WEBHOOKS DESDE LA BÓVEDA SECRETA ---
WH_ACTUALIZACIONES = os.environ.get("WH_ACTUALIZACIONES")
WH_AVISOS = os.environ.get("WH_AVISOS")
WH_EVENTOS = os.environ.get("WH_EVENTOS")
ROL_NOTICIAS = "<@&1483002893303808173>"

# --- ENLACES OFICIALES BDO SA ---
URL_ACTUALIZACIONES = "https://www.sa.playblackdesert.com/es-MX/News/Notice?boardType=2"
URL_AVISOS = "https://www.sa.playblackdesert.com/es-MX/News/Notice?boardType=1"
URL_EVENTOS = "https://www.sa.playblackdesert.com/es-MX/News/Notice?boardType=3"

def enviar_mensaje(url, mensaje):
    try:
        if url:
            requests.post(url, json={"content": mensaje}, timeout=10)
    except Exception as e:
        print(f"Error enviando a Discord: {e}")

def revisar_noticias(url_web, url_webhook, nombre_archivo, etiqueta):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        print(f"\n--- Revisando {etiqueta} ---")
        respuesta = requests.get(url_web, headers=headers, timeout=10)
        print(f"Código de respuesta de la página: {respuesta.status_code}")
        
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        primera_noticia = sopa.find('div', class_='box_list_area')
        if primera_noticia:
            enlace_tag = primera_noticia.find('a')
            if enlace_tag:
                titulo = enlace_tag.text.strip()
                enlace = enlace_tag['href']
                print(f"Noticia encontrada con éxito: {titulo}")
                
                ultimo_guardado = ""
                if os.path.exists(nombre_archivo):
                    with open(nombre_archivo, "r", encoding="utf-8") as f:
                        ultimo_guardado = f.read().strip()
                
                if titulo != ultimo_guardado:
                    print("¡Es una noticia nueva! Enviando a Discord...")
                    enviar_mensaje(url_webhook, f"{ROL_NOTICIAS}\n📢 **Nuevo {etiqueta} publicado:**\n**{titulo}**\nRevisa los detalles aquí: {enlace}")
                    with open(nombre_archivo, "w", encoding="utf-8") as f:
                        f.write(titulo)
                else:
                    print("La noticia es la misma de la última vez. No se envía.")
        else:
            print("ERROR: La página cargó, pero no se encontró el formato de la noticia (Pearl Abyss cambió la web o nos bloqueó).")
            
    except Exception as e:
        print(f"ERROR FATAL al intentar leer {etiqueta}: {e}")

if __name__ == "__main__":
    print("Iniciando Modo Diagnóstico...")
    revisar_noticias(URL_ACTUALIZACIONES, WH_ACTUALIZACIONES, "reg_act.txt", "Actualización")
    revisar_noticias(URL_AVISOS, WH_AVISOS, "reg_avi.txt", "Aviso")
    revisar_noticias(URL_EVENTOS, WH_EVENTOS, "reg_eve.txt", "Evento")
