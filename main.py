from flask import Flask, render_template, request, Response, session, redirect, url_for
import flag
import requests
import os

from src.controllers.manga_controller import view_chapter_images, proxy_image, manga_details, manga_chapters
from src.controllers.main_controller import index

app = Flask(__name__, static_url_path='/static')
app.secret_key = os.urandom(24)  # Genera una clave secreta aleatoria


# Registrar las rutas
app.add_url_rule('/', view_func=index, methods=['GET', 'POST'])
app.add_url_rule('/manga/<manga_id>', view_func=manga_details)
app.add_url_rule('/manga/<manga_id>/chapters', view_func=manga_chapters)
app.add_url_rule('/manga/<manga_id>/chapter/<chapter_id>', view_func=view_chapter_images)
app.add_url_rule('/proxy-image', view_func=proxy_image)

@app.route('/informacion')
def informacion():
    return render_template('informacion.html')
if __name__ == '__main__':
    app.run(debug=True)