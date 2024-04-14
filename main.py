from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__, static_url_path='/static')
external_URL = []
#===========================================================================================================================

#!                           Funciones para obtener detalles y capítulos de un manga

#===========================================================================================================================


def get_manga_details(manga_id):
    #*Obtiene los detalles de un manga utilizando su ID."""
    url = f"https://api.mangadex.org/manga/{manga_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_manga_chapters(manga_id):
    #*Obtiene los capítulos de un manga utilizando su ID."""
    url = f"https://api.mangadex.org/manga/{manga_id}/feed"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def search_manga(query):
    #*Realiza una búsqueda de mangas utilizando el título."""
    base_url = "https://api.mangadex.org"
    search_url = f"{base_url}/manga"
    params = {'title': query}
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    return None
# Ruta principal para la búsqueda e indexado de mangas

def get_cover_filename(manga_id):
    #*Obtiene el nombre del archivo de la portada de un manga."""
    url = f"https://api.mangadex.org/cover?limit=1&manga%5B%5D={manga_id}&order%5BcreatedAt%5D=asc"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["result"] == "ok" and data["total"] > 0:
            return data["data"][0]["attributes"]["fileName"]
    return None

#===========================================================================================================================

#!                                      PROXYS DEl PROYECTO

#===========================================================================================================================




def get_cover_url(manga_id):
    #*Obtiene la URL de la portada de un manga."""
    filename = get_cover_filename(manga_id)
    if filename:
        # Construir la URL de la imagen original en Mangadex
        original_image_url = f"https://uploads.mangadex.org/covers/{manga_id}/{filename}"
        # Devolver la URL de la imagen a través del proxy
        return f"/proxy-image?url={original_image_url}"
    return None


def get_chapter_image_urls(chapter_id):
    #*"Obtiene las URLs de las imágenes de un capítulo."""
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    response = requests.get(url)
    if response.status_code == 200:
        chapter_data = response.json()
        image_urls = []
        for page in chapter_data['chapter']['data']:
            image_urls.append(f"/proxy-image?url={chapter_data['baseUrl']}/data/{chapter_data['chapter']['hash']}/{page}")
        return image_urls
    return None


@app.route('/manga/<manga_id>/chapter/<chapter_id>')
def view_chapter_images(manga_id, chapter_id):
    print("ID DEL CAPITULO: ", chapter_id)
    print("ID DEL MANGA: ", manga_id)
    chapter_image_urls = get_chapter_image_urls(chapter_id)
    if chapter_image_urls:
        return render_template("chapter_images.html", chapter_image_urls=chapter_image_urls)
    else:
        chapter_info = get_manga_chapters(manga_id)
        #print(chapter_info) info del manga completo
        if chapter_info.get("result") == "ok" and chapter_info.get("response") == "collection":
            chapters_data = chapter_info.get("data")
            for chapter in chapters_data:
                if chapter.get("id") == chapter_id:
                    attributes = chapter.get("attributes")
                    if attributes.get("externalUrl") is not None:
                        print("URL EXTERNA",attributes.get("externalUrl"))
                        external_url = attributes.get("externalUrl")
                        return render_template("pruebaifra.html", external_url=external_url)
                    else:
                        return "Chapter images not found and no external URL available."
        return "Chapter information not available."



@app.route('/proxy-image')
def proxy_image():
    #*Ruta para obtener imágenes a través de un proxy."""
    # Obtener la URL de la imagen original
    image_url = request.args.get('url')
    # Realizar una solicitud a la URL de la imagen original en Mangadex
    response = requests.get(image_url, stream=True)
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Devolver la respuesta de la imagen con los encabezados correctos
        return Response(response.content, content_type=response.headers['content-type'])
    else:
        # Enviar un mensaje de error si la solicitud falla
        return 'Error al recuperar la imagen', 500

#===========================================================================================================================

#!                             FUNCIONES UTILIZANDO LAS FUNCIONES ENDPOINT

#===========================================================================================================================


@app.route('/', methods=['GET', 'POST'])
def index():
    #*Ruta principal para la búsqueda e indexado de mangas."""
    if request.method == 'POST':
        query = request.form.get('query')
        manga_data = search_manga(query)
        manga_with_cover = []
        if manga_data:
            for manga in manga_data:
                manga_id = manga['id']
                cover_url = get_cover_url(manga_id)
                if cover_url:
                    title = manga['attributes']['title'].get('en', 'No title available')
                    description = manga['attributes']['description'].get('en', 'No description available')
                    manga_with_cover.append({
                        'title': title,
                        'description': description,
                        'cover_url': cover_url,
                        'manga_id': manga_id
                    })
        return render_template("index.html", manga_data=manga_with_cover)
    else:
        return render_template("index.html")


# Rutas para detalles y capítulos de un manga

@app.route('/manga/<manga_id>')
def manga_details(manga_id):
    #*Ruta para mostrar los detalles de un manga."""
    manga_details = get_manga_details(manga_id)
    if manga_details:
        return render_template("manga_details.html", manga_details=manga_details)
    else:
        return "Manga details not found."

@app.route('/manga/<manga_id>/chapters')
def manga_chapters(manga_id):
    # Ruta para mostrar los capítulos de un manga
    print("AA")
    print(manga_id)
    manga_chapters = get_manga_chapters(manga_id)
    
    
    # Inicializar la lista external_URL
    global external_URL 
    
    
    # Ahora external_URL es una lista que contiene los capítulos y sus enlaces externos
    print(external_URL)
            
        

    if manga_chapters:
        return render_template("manga_chapters.html", manga_id=manga_id, manga_chapters=manga_chapters)
    else:
        return "Manga chapters not found."

# Funciones para buscar mangas y obtener detalles de la portada



# Ruta para ver las imágenes de un capítulo


if __name__ == '__main__':
    app.run(debug=True)
