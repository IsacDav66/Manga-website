from flask import render_template, Response,request
import requests

def view_chapter_images(manga_id, chapter_id):
    from src.utils.image_utils import get_chapter_image_urls  # Importación local
    from src.models.manga_model import get_manga_chapters
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


def manga_details(manga_id):
    """Muestra los detalles de un manga."""
    from src.models.manga_model import get_manga_details  # Importación local

    manga_details = get_manga_details(manga_id)
    if manga_details:
        return render_template("manga_details.html", manga_details=manga_details)
    else:
        return "Manga details not found."

import re

def manga_chapters(manga_id):
    """Muestra los capítulos de un manga."""
    from src.models.manga_model import get_manga_chapters  # Importación local
    from src.utils.general_utils import get_flag_emoji  # Importación local
    from itertools import groupby  # Importar groupby

    print("Capitulos cargando")
    print("Manga ID: ", manga_id)
    manga_chapters = get_manga_chapters(manga_id)

    if manga_chapters:
        custom_abbr_mapping = {
            "EN": "GB",
            "ES": "ES",
            "AR": "SA",
            "MS": "MY"
        }
        chapters_with_volume = []
        chapters_without_volume = []
        for chapter_data in manga_chapters['data']:
            chapter = chapter_data['attributes']
            chapter['id'] = chapter_data['id']
            translated_language = chapter.get('translatedLanguage', '')
            print(chapter)

            if translated_language:
                translated_language_upper = translated_language.split('-')[0].upper()
                if translated_language_upper in custom_abbr_mapping:
                    translated_language = custom_abbr_mapping[translated_language_upper]
                    # Obtener el emoji de la bandera utilizando la abreviatura ajustada
                    flag_emoji = get_flag_emoji(translated_language)
                    chapter['flag_emoji'] = flag_emoji
                    print("CHAPTER:", chapter['flag_emoji'])
                else:
                    chapter['flag_emoji'] = ""

            # Separar capítulos con y sin volumen
            if chapter.get('volume'):
                cleaned_volume = re.sub(r'\D', '', chapter['volume'])  # Eliminar todos los caracteres que no sean dígitos
                chapter['volume'] = cleaned_volume
                cleaned_chapter = re.sub(r'\D', '', chapter['chapter'])  # Eliminar todos los caracteres que no sean dígitos
                chapter['chapter'] = cleaned_chapter
                chapters_with_volume.append(chapter)
            else:
                chapters_without_volume.append(chapter)

        # Ordenar y agrupar capítulos con volumen
        chapters_with_volume.sort(key=lambda chapter: (int(float(chapter['volume'])), int(float(chapter['chapter']))), reverse=True)
        grouped_chapters = []
        for volume, chapters in groupby(chapters_with_volume, key=lambda chapter: chapter['volume']):
            volume_group = {
                'volume': volume,
                'chapter_groups': []  # Lista para subgrupos por página
            }
            for chapter_number, page_chapters in groupby(chapters, key=lambda chapter: chapter['chapter']):
                volume_group['chapter_groups'].append({
                    'chapter_number': chapter_number,
                    'chapters': list(page_chapters)
                })
            grouped_chapters.append(volume_group)

        chapters_without_volume.sort(key=lambda chapter: int(float(chapter['chapter'])), reverse=True)
        grouped_chapters_without_volume = []
        for chapter_number, chapters in groupby(chapters_without_volume, key=lambda chapter: chapter['chapter']):
            grouped_chapters_without_volume.append({
                'chapter_number': chapter_number,
                'chapters': list(chapters)
            })

        # Pasar los datos actualizados a la plantilla
        return render_template("manga_chapters.html", manga_id=manga_id,
                            grouped_chapters=grouped_chapters,
                            grouped_chapters_without_volume=grouped_chapters_without_volume,  # Pasar la nueva estructura
                            get_flag_emoji=get_flag_emoji,
                            custom_abbr_mapping=custom_abbr_mapping)
    else:
        return "Manga chapters not found."
