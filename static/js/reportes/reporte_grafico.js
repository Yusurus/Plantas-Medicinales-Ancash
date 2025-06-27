let chartFamiliasInstance;
let chartRegionesInstance;
// Cargar datos al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    cargarResumenGeneral();
    cargarGraficoFamilias();
    cargarGraficoRegiones();
});

// Función para cargar el resumen general
async function cargarResumenGeneral() {
    try {
        const response = await fetch('/api/reportes/resumen-general');
        const data = await response.json();
        
        document.getElementById('totalPlantas').textContent = data.total_plantas;
        document.getElementById('totalFamilias').textContent = data.total_familias;
        document.getElementById('totalSaberes').textContent = data.total_saberes;
        document.getElementById('totalUsos').textContent = data.total_usos;
        document.getElementById('totalRegiones').textContent = data.total_regiones;
    } catch (error) {
        console.error('Error al cargar resumen general:', error);
    }
}

// Función para cargar gráfico de familias
async function cargarGraficoFamilias() {
    try {
        const response = await fetch('/api/reportes/plantas-por-familia');
        const data = await response.json();
        
        const ctx = document.getElementById('chartFamilias').getContext('2d');

        if (chartFamiliasInstance) {
            chartFamiliasInstance.destroy();
        }

        chartFamiliasInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.map(item => item.familia),
                datasets: [{
                    data: data.map(item => item.cantidad_plantas),
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF',
                        '#4BC0C0', '#FF6384'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const clickedElementIndex = elements[0].index;
                        const label = chartFamiliasInstance.data.labels[clickedElementIndex];
                        mostrarPlantasEnModal('familia', label);
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error al cargar gráfico de familias:', error);
    }
}

// Función para cargar gráfico de regiones
async function cargarGraficoRegiones() {
    try {
        const response = await fetch('/api/reportes/plantas-por-region');
        const data = await response.json();
        
        const ctx = document.getElementById('chartRegiones').getContext('2d');

        if (chartRegionesInstance) {
            chartRegionesInstance.destroy();
        }
        chartRegionesInstance  = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.region),
                datasets: [{
                    label: 'Número de Plantas',
                    data: data.map(item => item.cantidad_plantas),
                    backgroundColor: '#667eea',
                    borderColor: '#764ba2',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                onClick: (event, elements) => {
                    if (elements.length > 0) {
                        const clickedElementIndex = elements[0].index;
                        const label = chartRegionesInstance.data.labels[clickedElementIndex];
                        mostrarPlantasEnModal('region', label);
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error al cargar gráfico de regiones:', error);
    }
}

async function mostrarPlantasEnModal(tipo, valor) {
    const modalTitle = document.getElementById('plantasModalLabel');
    const plantasGrid = document.getElementById('plantasGrid');
    const modalLoading = document.getElementById('modalLoading');
    const modalNoResults = document.getElementById('modalNoResults');

    plantasGrid.innerHTML = '';
    modalLoading.classList.remove('d-none');
    modalNoResults.classList.add('d-none');

    modalTitle.textContent = `Plantas de ${valor} (${tipo === 'familia' ? 'Familia' : 'Región'})`;
    const plantasModal = new bootstrap.Modal(document.getElementById('plantasModal'));
    plantasModal.show();

    try {
        const response = await fetch(`/api/reportes/plantas-detalles?tipo=${tipo}&valor=${encodeURIComponent(valor)}`);
        const plantas = await response.json();

        modalLoading.classList.add('d-none');

        if (plantas.length > 0) {
            plantas.forEach(planta => {
                const plantCard = document.createElement('div');
                plantCard.classList.add('plant-card');

                const imageUrl = planta.linkImagen;

                let commonNamesHtml = '';
                if (planta.nombres_comunes) {
                    const commonNamesArray = planta.nombres_comunes.split(', ');
                    commonNamesHtml = `<div class="common-names-badges">` +
                                    commonNamesArray.map(name => 
                                        `<span class="badge bg-secondary common-names-badge">${name}</span>`
                                    ).join('') +
                                    `</div>`;
                }

                plantCard.innerHTML = `
                    <img src="${imageUrl}" class="plant-card-img" alt="${planta.nombreCientifico}">
                    <div class="plant-card-body">
                        <h6 class="scientific-name">${planta.nombreCientifico}</h6>
                        ${commonNamesHtml}
                    </div>
                    <a href="/detalles/${planta.idPlanta}" class="btn-ver-detalles mt-2">
                    <i class="bi bi-eye"></i>
                    </a>
                    <div style="height: 0.8em;"></div>
                </div>
                `;
                plantasGrid.appendChild(plantCard);
            });
        } else {
            modalNoResults.classList.remove('d-none');
        }

    } catch (error) {
        console.error('Error al obtener detalles de plantas:', error);
        plantasGrid.innerHTML = '<p class="text-danger">Error al cargar las plantas.</p>'; // Mensaje de error en el grid
        modalLoading.classList.add('d-none');
    }
}