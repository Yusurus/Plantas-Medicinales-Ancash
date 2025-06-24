document.addEventListener('DOMContentLoaded', function() {
    let currentPlantId = null;
    let searchTimeout = null;
    
    // Elementos DOM
    const searchInput = document.getElementById('searchPlant');
    const clearSearchBtn = document.getElementById('clearSearch');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const plantsList = document.getElementById('plantsList');
    const noResults = document.getElementById('noResults');
    const step1 = document.getElementById('step1');
    const step2 = document.getElementById('step2');
    const selectedPlantInfo = document.getElementById('selectedPlantInfo');
    const regionSelect = document.getElementById('region');
    const zoneForm = document.getElementById('zoneForm');
    const cancelBtn = document.getElementById('cancelBtn');
    const selectedPlantIdInput = document.getElementById('selectedPlantId');
    
    // Cargar plantas iniciales y regiones
    loadPlants();
    loadRegions();
    
    // Event listeners
    searchInput.addEventListener('input', handleSearch);
    clearSearchBtn.addEventListener('click', clearSearch);
    cancelBtn.addEventListener('click', goBackToStep1);
    zoneForm.addEventListener('submit', handleZoneFormSubmit);
    
    function handleSearch() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = searchInput.value.trim();
            loadPlants(query);
        }, 300);
    }
    
    function clearSearch() {
        searchInput.value = '';
        loadPlants();
    }
    
    function showLoading() {
        loadingSpinner.style.display = 'block';
        plantsList.style.display = 'none';
        noResults.style.display = 'none';
    }
    
    function hideLoading() {
        loadingSpinner.style.display = 'none';
    }
    
    function loadPlants(searchQuery = '') {
        showLoading();
        
        let url = '/buscar_plantas';
        if (searchQuery) {
            url += `?q=${encodeURIComponent(searchQuery)}`;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                hideLoading();
                
                if (data.success) {
                    displayPlants(data.plantas);
                } else {
                    showError('Error al cargar plantas: ' + data.error);
                }
            })
            .catch(error => {
                hideLoading();
                console.error('Error:', error);
                showError('Error de conexión al cargar plantas');
            });
    }
    
    function displayPlants(plantas) {
        plantsList.innerHTML = '';
        
        if (plantas.length === 0) {
            plantsList.style.display = 'none';
            noResults.style.display = 'block';
            return;
        }
        
        plantsList.style.display = 'flex';      // Agregar esta línea
        plantsList.style.flexWrap = 'wrap';     // Agregar esta línea
        noResults.style.display = 'none';
        
        plantas.forEach(planta => {
            const plantCard = createPlantCard(planta);
            plantsList.appendChild(plantCard);
        });
    }
    
    function createPlantCard(planta) {
        const col = document.createElement('div');
        col.className = 'col-plant mb-3';
        
        col.innerHTML = `
            <div class="card h-100 plant-card" data-plant-id="${planta.idPlanta}" style="cursor: pointer;">
                <div class="card-body">
                    <h6 class="card-title text-success">${planta.nombreCientifico}</h6>
                    <p class="card-text">
                        <small class="text-muted">
                            <i class="bi bi-collection"></i> ${planta.nomFamilia || 'Familia no especificada'}
                        </small>
                    </p>
                    <p class="card-text">
                        <small>
                            <i class="bi bi-chat-square-text"></i> 
                            ${planta.nombres_comunes || 'Sin nombres comunes'}
                        </small>
                    </p>
                </div>
                <div class="card-footer bg-success text-white">
                    <small>
                        <i class="bi bi-cursor-fill"></i> Clic para seleccionar
                    </small>
                </div>
            </div>
        `;
        
        // Event listener para seleccionar planta
        col.querySelector('.plant-card').addEventListener('click', () => {
            selectPlant(planta.idPlanta);
        });
        
        return col;
    }
    
    function selectPlant(plantId) {
        currentPlantId = plantId;
        selectedPlantIdInput.value = plantId;
        
        // Cargar información detallada de la planta
        fetch(`/obtener_info_planta/${plantId}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    displaySelectedPlantInfo(data.planta);
                    showStep2();
                } else {
                    showError('Error al cargar información de la planta');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('Error de conexión');
            });
    }
    
    function displaySelectedPlantInfo(planta) {
        selectedPlantInfo.innerHTML = `
            <div class="alert alert-info">
                <h6 class="alert-heading">
                    <i class="bi bi-info-circle"></i> Planta Seleccionada
                </h6>
                <p class="mb-1"><strong>Nombre científico:</strong> ${planta.nombreCientifico}</p>
                <p class="mb-1"><strong>Familia:</strong> ${planta.nomFamilia || 'No especificada'}</p>
                <p class="mb-0"><strong>Nombres comunes:</strong> ${planta.nombres_comunes || 'Ninguno registrado'}</p>
                
                ${planta.zonas_existentes && planta.zonas_existentes.length > 0 ? `
                    <hr>
                    <p class="mb-1"><strong>Zonas ya registradas:</strong></p>
                    <ul class="mb-0">
                        ${planta.zonas_existentes.map(zona => `
                            <li>${zona.region} - ${zona.ecoregion} 
                                ${zona.nombreComun ? `(${zona.nombreComun})` : ''}
                            </li>
                        `).join('')}
                    </ul>
                ` : ''}
            </div>
        `;
    }
    
    function showStep2() {
        step1.style.display = 'none';
        step2.style.display = 'block';
    }
    
    function goBackToStep1() {
        step2.style.display = 'none';
        step1.style.display = 'block';
        currentPlantId = null;
        selectedPlantIdInput.value = '';
        zoneForm.reset();
    }
    
    function loadRegions() {
        fetch('/obtener_regiones')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    regionSelect.innerHTML = '<option value="">Seleccionar región...</option>';
                    data.regiones.forEach(region => {
                        const option = document.createElement('option');
                        option.value = region.idRegion;
                        option.textContent = region.region;
                        regionSelect.appendChild(option);
                    });
                } else {
                    showError('Error al cargar regiones');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError('Error de conexión al cargar regiones');
            });
    }
    
    function handleZoneFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(zoneForm);
        const data = {
            planta_id: parseInt(selectedPlantIdInput.value),
            region_id: parseInt(formData.get('region')),
            ecoregion: formData.get('ecoregion'),
            nombre_comun: formData.get('nombreComun')
        };
        
        const saveBtn = document.getElementById('saveZoneBtn');
        const originalText = saveBtn.innerHTML;
        saveBtn.innerHTML = '<i class="bi bi-hourglass-split"></i> Guardando...';
        saveBtn.disabled = true;
        
        fetch('/guardar_zona', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccess('Zona agregada exitosamente');
                setTimeout(() => {
                    goBackToStep1();
                    loadPlants(); // Recargar lista de plantas
                }, 1500);
            } else {
                showError('Error al guardar: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error de conexión al guardar');
        })
        .finally(() => {
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        });
    }
    
    function showError(message) {
        // Crear y mostrar alerta de error
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            <i class="bi bi-exclamation-triangle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insertar al inicio del card-body
        const cardBody = document.querySelector('.card-body');
        cardBody.insertBefore(alert, cardBody.firstChild);
        
        // Auto-ocultar después de 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
    
    function showSuccess(message) {
        // Crear y mostrar alerta de éxito
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.innerHTML = `
            <i class="bi bi-check-circle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insertar al inicio del card-body
        const cardBody = document.querySelector('.card-body');
        cardBody.insertBefore(alert, cardBody.firstChild);
        
        // Auto-ocultar después de 3 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 3000);
    }
});