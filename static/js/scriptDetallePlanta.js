// Obtener el ID de la planta desde el atributo data del body
const plantId = document.body.getAttribute('data-plant-id');

// Función para volver a la página anterior
function goBack() {
    window.location.href = '/';
}

// Función para mostrar los datos de la planta
function displayPlantData(data) {
    // Información básica
    document.getElementById('plantName').textContent = data.nombreCientifico || 'Nombre no disponible';
    document.getElementById('plantId').textContent = data.idPlanta || '-';
    document.getElementById('plantFamily').textContent = data.nomFamilia || '-';
    document.getElementById('commonNames').textContent = data.nombres_comunes || 'No registrados';
    document.getElementById('registeredBy').textContent =
        `${data.empleado_registro || 'No registrado'} (${data.cargo_empleado || 'Cargo no especificado'})`;

    // Imagen
    const plantImage = document.getElementById('plantImage');
    if (data.linkImagen) {
        plantImage.src = data.linkImagen;
        plantImage.alt = `Imagen de ${data.nombreCientifico}`;
    } else {
        plantImage.src = 'https://via.placeholder.com/400x400/4a7c59/ffffff?text=Sin+Imagen';
        plantImage.alt = 'Imagen no disponible';
    }

    // Ecoregiones
    document.getElementById('ecoregions').textContent =
        data.ecoregiones || 'No se han registrado ecoregiones para esta planta.';

    // Usos medicinales
    const medicalUsesContainer = document.getElementById('medicalUses');
    if (data.usos_medicinales) {
        const uses = data.usos_medicinales.split(' | ');
        medicalUsesContainer.innerHTML = uses.map(use =>
            `<div class="usage-item">${use}</div>`
        ).join('');
    } else {
        medicalUsesContainer.innerHTML = '<p class="no-data">No se han registrado usos medicinales para esta planta.</p>';
    }

    // Saberes culturales
    const culturalContainer = document.getElementById('culturalKnowledge');
    if (data.saberes_culturales) {
        const knowledge = data.saberes_culturales.split(' | ');
        culturalContainer.innerHTML = knowledge.map(item =>
            `<p>${item}</p>`
        ).join('');
    } else {
        culturalContainer.innerHTML = '<p class="no-data">No se han registrado saberes culturales para esta planta.</p>';
    }

    // Aportes de expertos
    const expertContainer = document.getElementById('expertContributions');
    if (data.aportes_expertos) {
        const contributions = data.aportes_expertos.split(' | ');
        expertContainer.innerHTML = contributions.map(contrib =>
            `<div class="expert-contribution">${contrib}</div>`
        ).join('');
    } else {
        expertContainer.innerHTML = '<p class="no-data">No se han registrado aportes de expertos para esta planta.</p>';
    }
}

// Función para cargar los datos de la planta
function loadPlantData() {
    console.log('Cargando datos para planta ID:', plantId);
    
    // Verificar que plantId existe
    if (!plantId) {
        console.error('Plant ID no está definido');
        document.getElementById('loadingSection').innerHTML =
            '<p style="color: red;">Error: ID de planta no válido.</p>';
        return;
    }
    
    fetch(`/api/planta/${plantId}`)
        .then(response => {
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error('Planta no encontrada');
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data);
            displayPlantData(data);

            // Ocultar loading y mostrar contenido
            document.getElementById('loadingSection').style.display = 'none';
            document.getElementById('contentSection').style.display = 'grid';
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('loadingSection').innerHTML =
                '<p style="color: red;">Error al cargar la información de la planta.</p>';
        });
}

// Cargar los datos cuando la página esté lista
document.addEventListener('DOMContentLoaded', loadPlantData);