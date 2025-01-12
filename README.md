# Resumen del Proyecto: Explorador de Mangas con API de MangaDex


![image](https://github.com/user-attachments/assets/497fe8fe-0ffd-4bcf-81cd-ac33f86e6ce0)


Este proyecto es una aplicación web desarrollada con Python y Flask, diseñada para permitir a los usuarios explorar y leer mangas utilizando la API de MangaDex. La aplicación proporciona funcionalidades de búsqueda, listado de mangas recientes, visualización de detalles y lectura de capítulos.

**Características Principales:**

1.  **Navegación y Búsqueda:**
    *   **Página Principal:** Muestra una lista de mangas recientes con la opción de paginación.
    *   **Búsqueda de Mangas:** Permite a los usuarios buscar mangas por título, con resultados paginados.
    *   **Almacenamiento de Búsqueda:** La última búsqueda se guarda en la sesión del usuario para facilitar la navegación.
    *    **Listado de Mangas:** Los resultados de búsqueda y mangas recientes se muestran en una cuadrícula con sus portadas.
2.  **Detalles del Manga:**
    *   **Página de Detalles:** Muestra la información detallada de un manga seleccionado.
    *    **Lista de Capítulos:** Presenta una lista de capítulos de cada manga, agrupados por volumen cuando están disponibles, mostrando el número de capítulo, título y la bandera del idioma de traducción, con enlaces a las páginas de lectura.
    *   **Gestión de Idiomas:** Utiliza un mapeo personalizado para mostrar la abreviatura correcta de los idiomas y el emoji correspondiente a la bandera.
        *   **Agrupamiento de capítulos:** Los capítulos se agrupan por volumen y número de capítulo, con opciones para mostrar u ocultar el contenido de cada grupo.

3.  **Visualización de Capítulos:**
    *   **Lectura de Capítulos:** Permite a los usuarios leer los capítulos de un manga, mostrando las imágenes de cada página con botones de navegación.
     *   **URLs Externas:** Si el capítulo tiene una URL externa, se muestra una vista con un iframe que apunta a dicha url.
    *   **Navegación de Capítulos:** Incluye un campo para navegar a un capítulo específico, así como botones para ir al anterior o al siguiente capítulo.
    *   **Atajos de teclado:** Se pueden usar las flechas del teclado para la navegación de los capítulos.
    *    **Proxy de Imágenes:** Las imágenes de los capítulos y portadas se cargan a través de un proxy para evitar problemas de CORS.

4.  **Interfaz de Usuario:**
    *   **Diseño Responsivo:** La interfaz es adaptable a diferentes tamaños de pantalla.
    *   **Estilos Personalizados:** Se utilizan CSS para personalizar la apariencia de la aplicación.
    *   **Componentes Interactivos:** Incluye botones, campos de texto y switch para la gestión de la vista.
    *   **Control de Vista de Títulos:** Un switch para mostrar u ocultar los títulos de los mangas.

**Tecnologías Utilizadas:**

*   **Python:** Lenguaje de programación principal.
*   **Flask:** Framework web para construir la aplicación.
*   **Requests:** Librería para realizar peticiones HTTP a la API de MangaDex.
*   **HTML, CSS, JavaScript:** Para la interfaz de usuario.
*  **Flag:** Librería para mostrar emojis de banderas según el código de idioma.

**Propósito:**

La aplicación proporciona una manera fácil y agradable para que los usuarios descubran y lean mangas a través de la API de MangaDex, ofreciendo una experiencia de lectura en línea fluida y organizada.

**Para un Trabajo:**

Este proyecto es un buen ejemplo de una aplicación web que interactúa con una API externa y presenta datos de forma organizada y fácil de usar. Muestra habilidades en el desarrollo web, manejo de APIs, diseño responsive, y la implementación de funcionalidades interactivas con JavaScript. Este trabajo se enfoca en la funcionalidad y en demostrar las habilidades en programación web.


![image](https://github.com/user-attachments/assets/86926fc3-7e7b-40b7-acff-a3f4e320e599)    ![image](https://github.com/user-attachments/assets/69590d6f-8afb-4e76-bc0f-16ae6265ae91)    ![image](https://github.com/user-attachments/assets/07fe3952-5095-46d5-8457-58dbfce83b9e)    ![image](https://github.com/user-attachments/assets/c11f2bf0-794e-4c5f-b34b-885172c7c0d4)

