const form = document.getElementById('plantForm');
const body = document.body;
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const dropZone = document.getElementById('drop-zone');
const imageInput = document.getElementById('image-input');
const fileNameDisplay = document.getElementById('file-name-display');
// const resultImagesContainer = document.getElementById('result-images');
const changeImageBtn = document.getElementById('change-image-btn');
const registerPlantBtn = document.getElementById('registerPlantBtn');
const noImagesMessageContainer = document.getElementById('noImagesMessageContainer'); // ¡AÑADE ESTA LÍNEA!

// --- NUEVAS CONSTANTES Y VARIABLES PARA EL CARRUSEL ---
const carouselImage = document.getElementById('carouselImage');
const prevImageBtn = document.getElementById('prevImageBtn');
const nextImageBtn = document.getElementById('nextImageBtn');
const imagePagination = document.getElementById('imagePagination')

let currentImageIndex = 0;
let plantimageUrls = [];

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
    // resultImagesContainer.innerHTML = '';
    noImagesMessageContainer.classList.add('hidden');

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

        if (data.is_logged_in) {
            registerPlantBtn.classList.remove('hidden')
        } else {
            registerPlantBtn.classList.add('hidden');
        }

        // Guardar datos de la planta en sessionStorage para poder registrarla
        sessionStorage.setItem('plantDataToRegister', JSON.stringify({
            scientificName: data.scientificName || '',
            commonNames: (data.commonNames && data.commonNames.length > 0) ? data.commonNames.join(', ') : '',
            family: data.family || '',
            genus: data.genus || '',
            imageUrls: (data.imageUrls && data.imageUrls.length > 0) ? data.imageUrls.join(', ') : ''
        }));

        registerPlantBtn.onclick = () => {
            sessionStorage.setItem('isFromIdentifier', 'true');
            window.location.href = '/registrar_planta';
        };

        document.getElementById('scientificName').textContent = data.scientificName || 'No disponible';
        document.getElementById('authorship').textContent = data.authorship || 'No disponible';
        document.getElementById('commonNames').textContent = (data.commonNames && data.commonNames.length > 0) ? data.commonNames.join(', ') : 'No disponible';
        document.getElementById('genus').textContent = data.genus || 'No disponible';
        document.getElementById('family').textContent = data.family || 'No disponible';
        document.getElementById('score').textContent = data.score ? parseFloat(data.score).toFixed(2) : 'N/A';

        plantImageUrls = data.imageUrls || []; // Asigna todas las URLs recibidas
        currentImageIndex = 0; // Reinicia el índice

        if (plantImageUrls.length > 0) {
            document.getElementById('image-carousel-container').classList.remove('hidden'); 
            carouselImage.classList.remove('hidden'); 

            showImage(currentImageIndex); 

            // Si hay más de una imagen, muestra los botones y la paginación
            if (plantImageUrls.length > 1) {
                prevImageBtn.classList.remove('hidden');
                nextImageBtn.classList.remove('hidden');
                imagePagination.classList.remove('hidden');
            } else {
                // Si solo hay una imagen, oculta los controles
                prevImageBtn.classList.add('hidden');
                nextImageBtn.classList.add('hidden');
                imagePagination.classList.add('hidden');
            }
        } else {
            // Si no hay imágenes, muestra un mensaje y oculta el carrusel
            document.getElementById('image-carousel-container').classList.add('hidden');
            noImagesMessageContainer.classList.remove('hidden');
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

// Función para mostrar la imagen actual
function showImage(index) {
    if (plantImageUrls.length === 0) {
        carouselImage.src = '';
        imagePagination.textContent = '';
        return;
    }

    currentImageIndex = (index + plantImageUrls.length) % plantImageUrls.length; 
    carouselImage.src = plantImageUrls[currentImageIndex];
    imagePagination.textContent = `${currentImageIndex + 1} de ${plantImageUrls.length}`;
}

// Función para la siguiente imagen
nextImageBtn.addEventListener('click', () => {
    showImage(currentImageIndex + 1);
});

// Función para la imagen anterior
prevImageBtn.addEventListener('click', () => {
    showImage(currentImageIndex - 1);
});