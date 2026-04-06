import requests
from bs4 import BeautifulSoup
import os

# --- WEBHOOKS Y ROL ---
WH_ACTUALIZACIONES = "https://discord.com/api/webhooks/1490268181720465509/OYsQurlz2tjkL1lQa8xpnC5F6Bu_ZVMUJEDZ6GPLv7vJUF-fZA22oybsnD9vCfbMF4Ks"
WH_AVISOS = "https://discord.com/api/webhooks/1490268337798643833/B6v_h__IWjMf8dA4GSeiyfmRe1TZSNkm4XYmRReDQgTOwBaYwU1aYHBtNRNDd9-qeqOi"
WH_EVENTOS = "https://discord.com/api/webhooks/1490268471202680953/10316jlxpVEmzWWvhTi75k-Pm3KLo5U997pSyNgChK3YEfg6HRkBzBzoWd7lrOwfLNq3"
ROL_NOTICIAS = "<@&1483002893303808173>"

# --- ENLACES OFICIALES BDO SA ---
URL_ACTUALIZACIONES = "https://www.sa.playblackdesert.com/es-MX/News/Notice?boardType=2"
URL_AVISOS = "https://www.sa.playblackdesert.com/es-MX/News/Notice?boardType=1"
URL_EVENTOS = "https://www.sa.playblackdesert.com/es-MX/News/Notice?boardType=3"

def enviar_mensaje(url, mensaje):
    try:
        requests.post(url, json={"content": mensaje}, timeout=10)
    except:
        pass

def revisar_noticias(url_web, url_webhook, nombre_archivo, etiqueta):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        respuesta = requests.get(url_web, headers=headers, timeout=10)
        sopa = BeautifulSoup(respuesta.text, 'html.parser')
        
        primera_noticia = sopa.find('div', class_='box_list_area')
        if primera_noticia:
            enlace_tag = primera_noticia.find('a')
            if enlace_tag:
                titulo = enlace_tag.text.strip()
                enlace = enlace_tag['href']
                
                ultimo_guardado = ""
                if os.path.exists(nombre_archivo):
                    with open(nombre_archivo, "r", encoding="utf-8") as f:
                        ultimo_guardado = f.read().strip()
                
                if titulo != ultimo_guardado:
                    enviar_mensaje(url_webhook, f"{ROL_NOTICIAS}\n📢 **Nuevo {etiqueta} publicado:**\n**{titulo}**\nRevisa los detalles aquí: {enlace}")
                    # Guardamos el título para que no lo vuelva a enviar
                    with open(nombre_archivo, "w", encoding="utf-8") as f:
                        f.write(titulo)
    except:
        pass

if __name__ == "__main__":
    print("Buscando nuevas noticias en BDO SA...")
    revisar_noticias(URL_ACTUALIZACIONES, WH_ACTUALIZACIONES, "reg_act.txt", "Actualización")
    revisar_noticias(URL_AVISOS, WH_AVISOS, "reg_avi.txt", "Aviso")
    revisar_noticias(URL_EVENTOS, WH_EVENTOS, "reg_eve.txt", "Evento")
