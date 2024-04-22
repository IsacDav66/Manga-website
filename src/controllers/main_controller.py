from flask import render_template, request, session, redirect, url_for

from src.models.manga_model import search_manga, get_recent_manga  # Importaciones locales
from src.utils.image_utils import get_cover_url  # Importación local

def index():
    #*Ruta principal para la búsqueda e indexado de mangas."""
    limit = 20  # Define 'limit' aquí, fuera de las ramas if/else

    if request.method == 'POST':
        query = request.form.get('query')
        session['search_query'] = query  # Almacenar la consulta de búsqueda en la sesión
        page = request.args.get('page', 1, type=int)
        offset = (page - 1) * limit
        search_response = search_manga(query, limit, offset)  # Obtener la respuesta de la búsqueda

        manga_with_cover = []
        if search_response:
            for manga in search_response['data']:
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

            total_manga = search_response['total']
            total_pages = (total_manga + limit - 1) // limit

        return render_template("index.html", 
                               manga_data=manga_with_cover,
                               page=page, 
                               total_pages=total_pages)


    else:
        # Eliminar la búsqueda almacenada si no hay un parámetro 'page'
        if 'search_query' in session and not request.args.get('page'):
            del session['search_query']

        if 'search_query' in session:  # Si hay una búsqueda almacenada en la sesión
            query = session['search_query']
            page = request.args.get('page', 1, type=int)
            offset = (page - 1) * limit
            search_response = search_manga(query, limit, offset)

            manga_with_cover = []
            if search_response:
                for manga in search_response['data']:
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

                total_manga = search_response['total']
                total_pages = (total_manga + limit - 1) // limit

            return render_template("index.html", 
                                   manga_data=manga_with_cover,
                                   page=page, 
                                   total_pages=total_pages)

        # Si no hay búsqueda, mostrar mangas recientes
        else:
            page = request.args.get('page', 1, type=int)  # Obtener número de página
            offset = (page - 1) * limit

            recent_manga_data = get_recent_manga(limit, offset)

            # Procesar datos de mangas recientes (similar a la búsqueda)
            recent_manga_with_cover = []
            if recent_manga_data:
                for manga in recent_manga_data['data']:
                    manga_id = manga['id']
                    cover_url = get_cover_url(manga_id)
                    if cover_url:
                        title = manga['attributes']['title'].get('en', 'No title available')
                        description = manga['attributes']['description'].get('en', 'No description available')
                        recent_manga_with_cover.append({
                            'title': title,
                            'description': description,
                            'cover_url': cover_url,
                            'manga_id': manga_id
                        })

                total_manga = recent_manga_data['total']
                total_pages = (total_manga + limit - 1) // limit

            return render_template("index.html", 
                                   manga_data=recent_manga_with_cover, 
                                   show_recent=True,
                                   page=page, 
                                   total_pages=total_pages)