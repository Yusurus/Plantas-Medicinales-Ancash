// Variables globales
const plantId = document.body.getAttribute('data-plant-id');
let imageGallery = [];

// Función para volver a la página anterior
function goBack() {
    window.location.href = '/';
}

// Función para cambiar la imagen principal
function changeMainImage(imageSrc, index) {
    // Actualizar imagen principal en la galería
    const mainImage = document.getElementById('mainImage');
    const mainImageInfo = document.getElementById('mainImageInfo');
    
    if (mainImage) {
        mainImage.src = imageSrc;
        mainImage.alt = `Imagen ${index + 1} de la planta`;
    }
    
    if (mainImageInfo) {
        mainImageInfo.src = imageSrc;
        mainImageInfo.alt = `Imagen ${index + 1} de la planta`;
    }
    
    // Actualizar estado activo de la galería
    document.querySelectorAll('.gallery-image').forEach((img, i) => {
        img.classList.toggle('active', i === index);
    });
}

// Función para cargar la galería de imágenes
function loadImageGallery() {
    fetch(`/api/planta/${plantId}/imagenes`)
        .then(response => response.json())
        .then(images => {
            imageGallery = images;
            const galleryContainer = document.getElementById('imageGallery');
            
            if (images && images.length > 0) {
                galleryContainer.innerHTML = images.map((img, index) => `
                    <div class="gallery-item">
                        <img src="${img.linkimagen}" 
                             alt="Imagen ${index + 1}" 
                             class="gallery-image ${index === 0 ? 'active' : ''}"
                             onclick="changeMainImage('${img.linkimagen}', ${index})"
                             title="Click para ver en grande"
                             onerror="this.src='https://via.placeholder.com/120x120/28a745/ffffff?text=Sin+Imagen'">
                    </div>
                `).join('');
                
                // Establecer la primera imagen como principal
                if (images.length > 0) {
                    const firstImage = images[0].linkimagen;
                    setMainImages(firstImage, 'Imagen principal de la planta');
                }
            } else {
                galleryContainer.innerHTML = '<div class="text-center p-3"><i class="bi bi-camera" style="font-size: 2rem;"></i><br>No hay imágenes adicionales disponibles</div>';
            }
        })
        .catch(error => {
            console.error('Error al cargar galería:', error);
            document.getElementById('imageGallery').innerHTML = '<div class="text-center p-3"><i class="bi bi-exclamation-triangle" style="font-size: 2rem;"></i><br>Error al cargar las imágenes</div>';
        });
}

// Función auxiliar para establecer las imágenes principales
function setMainImages(imageSrc, altText) {
    const mainImage = document.getElementById('mainImage');
    const mainImageInfo = document.getElementById('mainImageInfo');
    
    if (mainImage) {
        mainImage.src = imageSrc;
        mainImage.alt = altText;
        mainImage.onerror = function() {
            this.src = 'https://via.placeholder.com/400x400/28a745/ffffff?text=Sin+Imagen';
            this.alt = 'Imagen no disponible';
        };
    }
    
    if (mainImageInfo) {
        mainImageInfo.src = imageSrc;
        mainImageInfo.alt = altText;
        mainImageInfo.onerror = function() {
            this.src = 'https://via.placeholder.com/300x300/28a745/ffffff?text=Sin+Imagen';
            this.alt = 'Imagen no disponible';
        };
    }
}

// Función para mostrar los datos de la planta
function displayPlantData(data) {
    // Información del header
    document.getElementById('plantName').textContent = data.nombreCientifico || 'Nombre no disponible';
    document.getElementById('plantFamily').innerHTML = `<i class="bi bi-flower1"></i> Familia: ${data.nomFamilia || 'No especificada'}`;
    
    // Información básica
    document.getElementById('plantId').textContent = data.idPlanta || '-';
    document.getElementById('plantFamilyInfo').textContent = data.nomFamilia || '-';
    document.getElementById('scientificName').textContent = data.nombreCientifico || '-';
    
    // Nombres comunes
    const commonNamesEl = document.getElementById('commonNames');
    if (data.nombres_comunes) {
        const names = data.nombres_comunes.split(',').map(name => name.trim());
        commonNamesEl.innerHTML = names.map(name => `<span class="badge bg-success me-1">${name}</span>`).join(' ');
    } else {
        commonNamesEl.innerHTML = '<span class="text-muted">No registrados</span>';
    }
    
    document.getElementById('registeredBy').textContent =
        `${data.empleado_registro || 'No registrado'} (${data.cargo_empleado || 'Cargo no especificado'})`;

    // Imagen principal con manejo de errores mejorado
    if (data.linkImagen) {
        setMainImages(data.linkImagen, `Imagen de ${data.nombreCientifico}`);
    } else {
        setMainImages(
            'https://via.placeholder.com/400x400/28a745/ffffff?text=Sin+Imagen',
            'Imagen no disponible'
        );
    }

    // Datos morfológicos
    const morfologiaEl = document.getElementById('datos_morfo');
    if (data.datos_morfologicos && data.datos_morfologicos.trim()) {
        morfologiaEl.innerHTML = data.datos_morfologicos;
    } else {
        morfologiaEl.innerHTML = '<div class="text-muted">No se han registrado datos morfológicos para esta planta.</div>';
    }

    // Ecoregiones
    const ecoregionesEl = document.getElementById('ecoregions');
    if (data.ecoregiones && data.ecoregiones.trim()) {
        ecoregionesEl.innerHTML = data.ecoregiones;
    } else {
        ecoregionesEl.innerHTML = '<div class="text-muted">No se han registrado ecoregiones para esta planta.</div>';
    }

    // Usos medicinales - con diferentes colores
    const medicalUsesContainer = document.getElementById('medicalUses');
    if (data.usos_medicinales && data.usos_medicinales.trim()) {
        const uses = data.usos_medicinales.split(' | ').filter(use => use.trim());
        const colors = ['success', 'info', 'warning', 'secondary', 'primary'];
        medicalUsesContainer.innerHTML = uses.map((use, index) => {
            const colorClass = colors[index % colors.length];
            return `<div class="alert alert-${colorClass} mb-2">
                <i class="bi bi-capsule"></i> ${use.trim()}
            </div>`;
        }).join('');
    } else {
        medicalUsesContainer.innerHTML = '<div class="text-muted">No se han registrado usos medicinales para esta planta.</div>';
    }

    // Saberes culturales - con color azul claro
    const culturalContainer = document.getElementById('saberes_culturales');
    if (data.saberes_culturales && data.saberes_culturales.trim()) {
        const knowledge = data.saberes_culturales.split(' | ').filter(item => item.trim());
        culturalContainer.innerHTML = knowledge.map(item =>
            `<div class="alert alert-info mb-2">
                <i class="bi bi-book-half"></i> ${item.trim()}
            </div>`
        ).join('');
    } else {
        culturalContainer.innerHTML = '<div class="text-muted">No se han registrado saberes culturales para esta planta.</div>';
    }

    // Aportes de expertos - con color amarillento
    const expertContainer = document.getElementById('expertContributions');
    if (data.aportes_expertos && data.aportes_expertos.trim()) {
        const contributions = data.aportes_expertos.split(' | ').filter(contrib => contrib.trim());
        expertContainer.innerHTML = contributions.map(contrib =>
            `<div class="alert alert-warning mb-2">
                <i class="bi bi-person-check"></i> ${contrib.trim()}
            </div>`
        ).join('');
    } else {
        expertContainer.innerHTML = '<div class="text-muted">No se han registrado aportes de expertos para esta planta.</div>';
    }
}

// Función para cargar los datos de la planta
function loadPlantData() {
    console.log('Cargando datos para planta ID:', plantId);
    
    if (!plantId) {
        console.error('Plant ID no está definido');
        document.getElementById('loadingSection').innerHTML =
            '<div class="text-center"><i class="bi bi-exclamation-triangle" style="font-size: 3rem;"></i><p class="mt-3">Error: ID de planta no válido.</p></div>';
        return;
    }
    
    fetch(`/api/planta/${plantId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);
            displayPlantData(data);
            loadImageGallery();
            
            // Ocultar loading y mostrar contenido
            document.getElementById('loadingSection').style.display = 'none';
            document.getElementById('contentSection').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loadingSection').innerHTML =
                `<div class="text-center">
                    <i class="bi bi-exclamation-triangle" style="font-size: 3rem;"></i>
                    <p class="mt-3">Error al cargar la información de la planta.</p>
                    <p class="text-muted">${error.message}</p>
                </div>`;
        });
}

// Cargar los datos cuando la página esté lista
document.addEventListener('DOMContentLoaded', loadPlantData);