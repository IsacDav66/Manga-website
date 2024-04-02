from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__)

# Add functions to retrieve manga details and chapters

def get_manga_details(manga_id):
    url = f"https://api.mangadex.org/manga/{manga_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_manga_chapters(manga_id):
    url = f"https://api.mangadex.org/manga/{manga_id}/feed"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Modify the index route to include manga details and chapters

@app.route('/', methods=['GET', 'POST'])
def index():
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

# Add routes for manga details and chapters

@app.route('/manga/<manga_id>')
def manga_details(manga_id):
    manga_details = get_manga_details(manga_id)
    if manga_details:
        return render_template("manga_details.html", manga_details=manga_details)
    else:
        return "Manga details not found."

@app.route('/manga/<manga_id>/chapters')
def manga_chapters(manga_id):
    manga_chapters = get_manga_chapters(manga_id)
    if manga_chapters:
        return render_template("manga_chapters.html", manga_chapters=manga_chapters)
    else:
        return "Manga chapters not found."




def search_manga(query):
    base_url = "https://api.mangadex.org"
    search_url = f"{base_url}/manga"
    params = {'title': query}
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['data']
    return None

def get_cover_filename(manga_id):
    url = f"https://api.mangadex.org/cover?limit=1&manga%5B%5D={manga_id}&order%5BcreatedAt%5D=asc"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["result"] == "ok" and data["total"] > 0:
            return data["data"][0]["attributes"]["fileName"]
    return None


def get_cover_url(manga_id):
    filename = get_cover_filename(manga_id)
    if filename:
        # Construir la URL de la imagen original en Mangadex
        original_image_url = f"https://uploads.mangadex.org/covers/{manga_id}/{filename}"
        # Devolver la URL de la imagen a través del proxy
        return f"/proxy-image?url={original_image_url}"
    return None

@app.route('/proxy-image')
def proxy_image():
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


@app.route('/chapter/<chapter_id>')
def view_chapter_images(chapter_id):
    chapter_image_urls = get_chapter_image_urls(chapter_id)
    if chapter_image_urls:
        return render_template("chapter_images.html", chapter_image_urls=chapter_image_urls)
    else:
        return "Chapter images not found."

    
def get_chapter_image_urls(chapter_id):
    url = f"https://api.mangadex.org/at-home/server/{chapter_id}"
    response = requests.get(url)
    if response.status_code == 200:
        chapter_data = response.json()
        image_urls = []
        for page in chapter_data['chapter']['data']:
            image_urls.append(f"/proxy-image?url={chapter_data['baseUrl']}/data/{chapter_data['chapter']['hash']}/{page}")
        return image_urls
    return None

if __name__ == '__main__':
    app.run(debug=True)
