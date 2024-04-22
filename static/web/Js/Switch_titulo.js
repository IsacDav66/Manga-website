const titleSwitch = document.getElementById('title-switch');
            const titulosManga = document.querySelectorAll('.titulo-manga');

            // Función para actualizar la visibilidad de los títulos
            function updateTitulosVisibility() {
                if (titleSwitch.checked) {
                    titulosManga.forEach(titulo => titulo.style.display = 'block');
                } else {
                    titulosManga.forEach(titulo => titulo.style.display = 'none');
                }
            }

            // Cargar el estado del interruptor del almacenamiento local al cargar la página
            window.addEventListener('load', () => {
                    const storedState = localStorage.getItem('titleSwitchState');
                    const isSwitchOn = storedState && storedState === 'on'; // Verifica si el valor no es null
                titleSwitch.checked = isSwitchOn;
                updateTitulosVisibility();
            });

            // Guardar el estado del interruptor en el almacenamiento local al cambiar
            titleSwitch.addEventListener('change', () => {
                localStorage.setItem('titleSwitchState', titleSwitch.checked ? 'on' : 'off');
                updateTitulosVisibility();
            });