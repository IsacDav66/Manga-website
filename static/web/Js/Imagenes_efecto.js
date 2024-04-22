        const images = document.querySelectorAll('img');

            images.forEach(image => {
                image.addEventListener('load', () => {
                    image.style.opacity = 1;
                });
            });