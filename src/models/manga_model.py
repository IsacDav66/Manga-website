import requests

def get_manga_details(manga_id):
    """Obtiene los detalles de un manga utilizando su ID."""
    url = f"https://api.mangadex.org/manga/{manga_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_manga_chapters(manga_id):
    """Obtiene los capítulos de un manga utilizando su ID."""
    url = f"https://api.mangadex.org/manga/{manga_id}/feed"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def search_manga(query, limit=20, offset=0):
    """Realiza una búsqueda de mangas utilizando el título y paginación."""
    offset = min(offset, 9980)  # Limitar el offset a un máximo de 9980
    base_url = "https://api.mangadex.org"
    search_url = f"{base_url}/manga"
    params = {
        'title': query,
        'limit': limit,
        'offset': offset
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        return response.json()  # Devolver la respuesta JSON completa
    return None

def get_cover_filename(manga_id):
    """Obtiene el nombre del archivo de la portada de un manga."""
    url = f"https://api.mangadex.org/cover?limit=1&manga%5B%5D={manga_id}&order%5BcreatedAt%5D=asc"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["result"] == "ok" and data["total"] > 0:
            return data["data"][0]["attributes"]["fileName"]
    return None

def get_recent_manga(limit=20, offset=0):
    """Obtiene una lista de mangas recientes de Mangadex con paginación y límite de offset."""
    offset = min(offset, 9980)  # Limitar el offset a un máximo de 9980

    url = "https://api.mangadex.org/manga"
    params = {
        'limit': limit,
        'offset': offset,
        'order[latestUploadedChapter]': 'desc'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()  # Devolver la respuesta JSON completa
    return []