const form = document.getElementById('plantForm');
        const body = document.body;
        const loading = document.getElementById('loading');
        const errorDiv = document.getElementById('error');
        const dropZone = document.getElementById('drop-zone');
        const imageInput = document.getElementById('image-input');
        const fileNameDisplay = document.getElementById('file-name-display');
        const resultImagesContainer = document.getElementById('result-images');
        const changeImageBtn = document.getElementById('change-image-btn');

        dropZone.addEventListener('click', () => {
            imageInput.click();
        });

        // Event listener para el botón cambiar imagen
        changeImageBtn.addEventListener('click', () => {
            imageInput.click();
        });

        imageInput.addEventListener('change', (event) => {
            const file = event.target.files[0];
            const preview = document.getElementById('preview-image');
            if (file) {
                fileNameDisplay.textContent = `Archivo seleccionado: ${file.name}`;
                preview.src = URL.createObjectURL(file);
                preview.classList.remove('hidden');
                changeImageBtn.classList.remove('hidden'); // Mostrar botón cambiar imagen
                dropZone.classList.add('hidden'); // Ocultar zona de drop
            } else {
                fileNameDisplay.textContent = '';
                preview.classList.add('hidden');
                changeImageBtn.classList.add('hidden'); // Ocultar botón cambiar imagen
                dropZone.classList.remove('hidden'); // Mostrar zona de drop si no hay imagen
            }
        });

        // Eventos para drag and drop
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
            document.body.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
        });

        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            const preview = document.getElementById('preview-image');
            if (files.length > 0) {
                imageInput.files = files;
                fileNameDisplay.textContent = `Archivo seleccionado: ${files[0].name}`;
                preview.src = URL.createObjectURL(files[0]);
                preview.classList.remove('hidden');
                changeImageBtn.classList.remove('hidden'); // Mostrar botón cambiar imagen
                dropZone.classList.add('hidden'); // Ocultar zona de drop
            } else {
                fileNameDisplay.textContent = '';
                preview.classList.add('hidden');
                changeImageBtn.classList.add('hidden'); // Ocultar botón cambiar imagen
                dropZone.classList.remove('hidden'); // Mostrar si no hay imagen
            }
        }

        // Event listener para el formulario
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            body.classList.remove('results-active');
            loading.classList.remove('hidden');
            errorDiv.classList.add('hidden');
            const formData = new FormData(form);
            resultImagesContainer.innerHTML = '';

            try {
                const res = await fetch('/identify', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                loading.classList.add('hidden');

                if (!res.ok) {
                    throw new Error(data.error || 'No se encontraron coincidencias.');
                }

                document.getElementById('scientificName').textContent = data.scientificName || 'No disponible';
                document.getElementById('authorship').textContent = data.authorship || 'No disponible';
                document.getElementById('commonNames').textContent = (data.commonNames && data.commonNames.length > 0) ? data.commonNames.join(', ') : 'No disponible';
                document.getElementById('genus').textContent = data.genus || 'No disponible';
                document.getElementById('family').textContent = data.family || 'No disponible';
                document.getElementById('score').textContent = data.score ? parseFloat(data.score).toFixed(2) : 'N/A';

                if (data.imageUrls && data.imageUrls.length > 0) {
                    data.imageUrls.forEach(url => {
                        console.log("URL de imagen recibida:", url);
                        const img = document.createElement('img');
                        img.src = url;
                        img.alt = data.scientificName || 'Imagen de planta';
                        img.classList.add('w-50', 'h-50', 'object-cover', 'rounded-lg', 'shadow-md');
                        resultImagesContainer.appendChild(img);
                    });
                } else {
                    resultImagesContainer.innerHTML = '<p class="text-sm text-gray-500">No se encontraron imágenes relacionadas.</p>';
                }

                body.classList.add('results-active');
                document.getElementById('result-card').classList.remove('hidden'); // Mostrar resultado
            } catch (err) {
                loading.classList.add('hidden');
                errorDiv.textContent = err.message;
                errorDiv.classList.remove('hidden');
                body.classList.remove('results-active');
                document.getElementById('result-card').classList.add('hidden'); // Ocultar resultado en caso de error
            }
        });

        // Event listener para el botón "Volver al inicio"
        document.addEventListener("DOMContentLoaded", function () {
            const volverInicioBtn = document.getElementById("volverInicio");
            volverInicioBtn.addEventListener("click", function () {
                window.location.href = "/";
            });
        });