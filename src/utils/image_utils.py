from flask import render_template, Response,request
import requests
def get_cover_url(manga_id):
    """Obtiene la URL de la portada de un manga."""
    from src.models.manga_model import get_cover_filename  # Importación local

    filename = get_cover_filename(manga_id)
    if filename:
        # Construir la URL de la imagen original en Mangadex
        original_image_url = f"https://uploads.mangadex.org/covers/{manga_id}/{filename}"
        # Devolver la URL de la imagen a través del proxy
        return f"/proxy-image?url={original_image_url}"
    return None

def get_chapter_image_urls(chapter_id):
    """Obtiene las URLs de las imágenes de un capítulo."""
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    response = requests.get(url)
    if response.status_code == 200:
        chapter_data = response.json()
        image_urls = []
        for page in chapter_data['chapter']['data']:
            image_urls.append(f"/proxy-image?url={chapter_data['baseUrl']}/data/{chapter_data['chapter']['hash']}/{page}")
        return image_urls
    return None