class PlantasMedicinalesApp {
    constructor() {
        this.plantas = [];
        this.selectedPlant = null;
        this.currentUsos = [];
        this.editingUsage = null;
        
        this.initElements();
        this.initEventListeners();
        this.loadPlantas();
    }

    initElements() {
        this.searchInput = document.getElementById('pmPlantSearch');
        this.plantsGrid = document.getElementById('pmPlantsGrid');
        this.plantDetailsSection = document.getElementById('pmPlantDetailsSection');
        this.selectedPlantInfo = document.getElementById('pmSelectedPlantInfo');
        this.usageList = document.getElementById('pmUsageList');
        this.usageLoading = document.getElementById('pmUsageLoading');
        this.usageModal = document.getElementById('pmUsageModal');
        this.usageForm = document.getElementById('pmUsageForm');
        this.modalTitle = document.getElementById('pmModalTitle');
        this.addUsageBtn = document.getElementById('pmAddUsageBtn');
        this.closeModalBtn = document.getElementById('pmCloseModal');
        this.cancelBtn = document.getElementById('pmCancelBtn');
        this.saveBtn = document.getElementById('pmSaveBtn');
    }

    initEventListeners() {
        // Búsqueda
        this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        this.searchInput.addEventListener('focus', (e) => this.handleSearch(e.target.value));

        // Modal
        this.addUsageBtn.addEventListener('click', () => this.openModal());
        this.closeModalBtn.addEventListener('click', () => this.closeModalHandler());
        this.cancelBtn.addEventListener('click', () => this.closeModalHandler());
        this.usageForm.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Cerrar modal al hacer clic en el overlay
        this.usageModal.addEventListener('click', (e) => {
            if (e.target === this.usageModal) {
                this.closeModalHandler();
            }
        });

        // Cerrar modal con tecla Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.usageModal.style.display === 'flex') {
                this.closeModalHandler();
            }
        });
    }

    async loadPlantas() {
        // Mostrar loading
        document.getElementById('pmPlantsLoading').style.display = 'flex';
        this.plantsGrid.style.display = 'none';
        
        try {
            const response = await fetch('/api/plantas');
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            this.plantas = await response.json();
            this.displayPlantas(this.plantas);
        } catch (error) {
            console.error('Error cargando plantas:', error);
            this.showError('Error al cargar las plantas');
            // Ocultar loading aunque haya error
            document.getElementById('pmPlantsLoading').style.display = 'none';
        }
    }

    displayPlantas(plantas) {
        this.plantsGrid.innerHTML = '';
        
        // Ocultar loading y mostrar grid
        document.getElementById('pmPlantsLoading').style.display = 'none';
        this.plantsGrid.style.display = 'grid';
        
        // Actualizar contador
        document.getElementById('pmPlantsCount').textContent = plantas.length + ' plantas';
        
        plantas.forEach(planta => {
            const card = document.createElement('div');
            card.className = 'pm-plant-card';
            card.dataset.plantId = planta.idPlanta;
            
            card.innerHTML = `
                <div class="pm-plant-card-content">
                    <h4 class="pm-plant-scientific-name">${planta.nombreCientifico}</h4>
                    <p class="pm-plant-family">${planta.nomFamilia || 'Familia no especificada'}</p>
                    <p class="pm-plant-common-names">${planta.nombresComunes || 'Sin nombres comunes'}</p>
                </div>
            `;
            
            card.addEventListener('click', () => this.selectPlant(planta));
            this.plantsGrid.appendChild(card);
        });
    }

    handleSearch(query) {
        query = query.toLowerCase().trim();
        
        if (query.length < 2) {
            this.displayPlantas(this.plantas);
            return;
        }

        const filtered = this.plantas.filter(planta => 
            planta.nombreCientifico.toLowerCase().includes(query) ||
            (planta.nombresComunes && planta.nombresComunes.toLowerCase().includes(query)) ||
            (planta.nomFamilia && planta.nomFamilia.toLowerCase().includes(query))
        );

        this.displayPlantas(filtered);
    }

    async selectPlant(planta) {
        // Remover selección anterior
        document.querySelectorAll('.pm-plant-card').forEach(card => {
            card.classList.remove('pm-selected');
        });
        
        // Seleccionar nueva planta
        const selectedCard = document.querySelector(`[data-plant-id="${planta.idPlanta}"]`);
        if (selectedCard) {
            selectedCard.classList.add('pm-selected');
        }
        
        this.selectedPlant = planta;
        this.searchInput.value = planta.nombreCientifico;
        
        this.displaySelectedPlantInfo();
        this.plantDetailsSection.style.display = 'block';
        
        await this.loadUsos(planta.idPlanta);
    }

    displaySelectedPlantInfo() {
        this.selectedPlantInfo.innerHTML = `
            <div class="pm-plant-info-grid">
                <div class="pm-info-item">
                    <span class="pm-info-label">Nombre Científico:</span>
                    <span class="pm-info-value">${this.selectedPlant.nombreCientifico}</span>
                </div>
                <div class="pm-info-item">
                    <span class="pm-info-label">Familia:</span>
                    <span class="pm-info-value">${this.selectedPlant.nomFamilia || 'No especificada'}</span>
                </div>
                <div class="pm-info-item">
                    <span class="pm-info-label">Nombres Comunes:</span>
                    <span class="pm-info-value">${this.selectedPlant.nombresComunes || 'No registrados'}</span>
                </div>
            </div>
        `;
    }

    async loadUsos(plantId) {
        this.usageLoading.style.display = 'block';
        this.usageList.innerHTML = '';
        
        try {
            const response = await fetch(`/api/usos/${plantId}`);
            this.currentUsos = await response.json();
            this.displayUsos();
        } catch (error) {
            console.error('Error cargando usos:', error);
            this.showError('Error al cargar los usos');
        } finally {
            this.usageLoading.style.display = 'none';
        }
    }

    displayUsos() {
        if (this.currentUsos.length === 0) {
            this.usageList.innerHTML = `
                <div class="pm-empty-state">
                    <p>No hay usos registrados para esta planta.</p>
                    <p>Haz clic en "Agregar Nuevo Uso" para registrar un uso medicinal.</p>
                </div>
            `;
            return;
        }

        this.usageList.innerHTML = '';
        this.currentUsos.forEach((uso, index) => {
            const usoElement = document.createElement('div');
            usoElement.className = 'pm-usage-item';
            
            usoElement.innerHTML = `
                <div class="pm-usage-header">
                    <h4 class="pm-usage-part">${uso.parte || 'Parte no especificada'}</h4>
                    <div class="pm-usage-actions">
                        <button class="btn btn-warning pm-btn-edit" data-index="${index}">Editar</button>
                        <button class="btn btn-danger pm-btn-delete" data-index="${index}">Eliminar</button>
                    </div>
                </div>
                <div class="pm-usage-content">
                    <div class="pm-usage-field">
                        <strong>Uso Medicinal:</strong>
                        <p>${uso.uso || 'No especificado'}</p>
                    </div>
                    <div class="pm-usage-field">
                        <strong>Contraindicaciones:</strong>
                        <p>${uso.contraIndicaciones || 'No especificadas'}</p>
                    </div>
                    <div class="pm-usage-field">
                        <strong>Preparación:</strong>
                        <p>${uso.preparacion || 'No especificada'}</p>
                    </div>
                </div>
            `;

            this.usageList.appendChild(usoElement);
        });

        // Agregar eventos para editar y eliminar
        this.usageList.querySelectorAll('.pm-btn-edit').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.target.dataset.index);
                this.openModal(this.currentUsos[index], index);
            });
        });

        this.usageList.querySelectorAll('.pm-btn-delete').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.target.dataset.index);
                this.deleteUsage(index);
            });
        });
    }

    openModal(usage = null, index = null) {
        this.editingUsage = usage ? { ...usage, index } : null;
        
        if (usage) {
            this.modalTitle.textContent = 'Editar Uso';
            document.getElementById('pmUsagePart').value = usage.parte || '';
            document.getElementById('pmUsageUse').value = usage.uso || '';
            document.getElementById('pmUsageContraindications').value = usage.contraIndicaciones || '';
            document.getElementById('pmUsagePreparation').value = usage.preparacion || '';
        } else {
            this.modalTitle.textContent = 'Agregar Nuevo Uso';
            this.usageForm.reset();
        }
        
        this.usageModal.style.display = 'flex';
        // Prevenir scroll del body cuando el modal está abierto
        document.body.style.overflow = 'hidden';
    }

    // Renombré el método para evitar conflictos
    closeModalHandler() {
        this.usageModal.style.display = 'none';
        this.usageForm.reset();
        this.editingUsage = null;
        // Restaurar scroll del body
        document.body.style.overflow = '';
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.usageForm);
        const data = {
            parte: formData.get('parte').trim(),
            uso: formData.get('uso').trim(),
            contraIndicaciones: formData.get('contraIndicaciones').trim(),
            preparacion: formData.get('preparacion').trim(),
            fk_plantas: this.selectedPlant.idPlanta
        };

        // Validar campos
        if (!data.parte || !data.uso || !data.contraIndicaciones || !data.preparacion) {
            this.showError('Todos los campos son obligatorios');
            return;
        }

        try {
            let response;
            if (this.editingUsage) {
                // Actualizar uso existente
                response = await fetch(`/api/usos/${this.editingUsage.idUsos}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
            } else {
                // Crear nuevo uso
                response = await fetch('/api/usos', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
            }

            if (response.ok) {
                this.showSuccess(this.editingUsage ? 'Uso actualizado correctamente' : 'Uso agregado correctamente');
                this.closeModalHandler();
                await this.loadUsos(this.selectedPlant.idPlanta);
            } else {
                const error = await response.json();
                this.showError(error.error || 'Error al guardar el uso');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Error de conexión');
        }
    }

    async deleteUsage(index) {
        const uso = this.currentUsos[index];
        
        if (!confirm(`¿Estás seguro de que deseas eliminar este uso de ${uso.parte}?`)) {
            return;
        }

        try {
            const response = await fetch(`/api/usos/${uso.idUsos}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                this.showSuccess('Uso eliminado correctamente');
                await this.loadUsos(this.selectedPlant.idPlanta);
            } else {
                const error = await response.json();
                this.showError(error.error || 'Error al eliminar el uso');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showError('Error de conexión');
        }
    }

    showError(message) {
        // Sistema básico de notificaciones con alert
        alert('Error: ' + message);
    }

    showSuccess(message) {
        // Sistema básico de notificaciones con alert
        alert('Éxito: ' + message);
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new PlantasMedicinalesApp();
});