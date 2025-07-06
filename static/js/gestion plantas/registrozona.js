class PlantManagement {
    constructor() {
        this.data = {
            plantaszona: [],
            regiones: [],
            provincias: [],
            ecoregiones: [],
            plantaSeleccionada: null
        };
        
        this.init();
    }

    // Inicialización principal
    async init() {
        await this.loadInitialData();
        this.setupEventListeners();
    }

    // Carga de datos inicial
    async loadInitialData() {
        try {
            await Promise.all([
                this.loadPlantas(),
                this.loadRegiones(),
                this.loadEcoregiones()
            ]);
        } catch (error) {
            console.error('Error en carga inicial:', error);
            this.showMessage('Error al cargar datos iniciales', 'danger');
        }
    }

    // Configuración de eventos
    setupEventListeners() {
        // Selección de planta
        document.getElementById('selectPlanta').addEventListener('change', (e) => {
            this.handlePlantSelection(e.target.value);
        });

        // Formularios
        this.setupFormListeners();
        
        // Filtros
        this.setupFilterListeners();
        
        // Modales
        this.setupModalListeners();
    }

    setupFormListeners() {
        const forms = {
            'formAgregarEcoregion': () => this.addEcoregionToPlant(),
            'formRegion': () => this.createRegion(),
            'formProvincia': () => this.createProvincia(),
            'formEcoregionProvincia': () => this.associateEcoregionProvincia()
        };

        Object.entries(forms).forEach(([formId, handler]) => {
            document.getElementById(formId).addEventListener('submit', (e) => {
                e.preventDefault();
                handler();
            });
        });
    }

    setupFilterListeners() {
        document.getElementById('filtroRegionProvincia').addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadProvinciasByRegion(e.target.value);
            }
        });

        document.getElementById('filtroProvinciaEcoregion').addEventListener('change', (e) => {
            if (e.target.value) {
                this.loadEcoregionesProvinciaGeografico(e.target.value);
            }
        });

        document.getElementById('regionEcoregion').addEventListener('change', (e) => {
            this.loadProvinciasByRegionForSelect(e.target.value, 'provinciaEcoregion');
        });
    }

    setupModalListeners() {
        document.getElementById('saveEdit').addEventListener('click', () => this.saveEdit());
        document.getElementById('confirmDelete').addEventListener('click', () => this.confirmDelete());
    }

    // === CARGA DE DATOS ===
    async loadPlantas() {
        try {
            const response = await fetch('/api/todas_plantas_zonas');
            this.data.plantaszona = await response.json();
            this.populatePlantSelect();
        } catch (error) {
            console.error('Error cargando plantas:', error);
            throw error;
        }
    }

    async loadRegiones() {
        try {
            const response = await fetch('/api/regiones');
            this.data.regiones = await response.json();
            this.populateRegionSelects();
            this.showRegionTable();
        } catch (error) {
            console.error('Error cargando regiones:', error);
            throw error;
        }
    }

    async loadEcoregiones() {
        try {
            const response = await fetch('/api/ecoregiones');
            this.data.ecoregiones = await response.json();
            this.populateEcoregionSelects();
        } catch (error) {
            console.error('Error cargando ecoregiones:', error);
            throw error;
        }
    }

    // === POBLACIÓN DE SELECTS ===
    populatePlantSelect() {
        const select = document.getElementById('selectPlanta');
        select.innerHTML = '<option value="">Seleccione una planta...</option>';
        
        this.data.plantaszona.forEach(planta => {
            const option = document.createElement('option');
            option.value = planta.idPlanta;
            option.textContent = `${planta.nombreCientifico} - ${planta.nombresComunes || 'Sin nombres comunes'}`;
            select.appendChild(option);
        });
    }

    populateRegionSelects() {
        const selectIds = ['regionProvincia', 'filtroRegionProvincia', 'regionEcoregion'];
        selectIds.forEach(id => this.populateSelect(id, this.data.regiones, 'idRegion', 'region', 'Seleccione una región...'));
    }

    populateEcoregionSelects() {
        const selectIds = ['ecoregionAsociar', 'selectEcoregion'];
        selectIds.forEach(id => this.populateSelect(id, this.data.ecoregiones, 'idecoregion', 'ecoregion', 'Seleccione una ecoregión...'));
    }

    populateSelect(selectId, data, valueField, textField, placeholder) {
        const select = document.getElementById(selectId);
        select.innerHTML = `<option value="">${placeholder}</option>`;
        
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valueField];
            option.textContent = item[textField];
            select.appendChild(option);
        });
    }

    // === MANEJO DE PLANTAS ===
    handlePlantSelection(plantaId) {
        if (plantaId) {
            this.data.plantaSeleccionada = this.data.plantaszona.find(p => p.idPlanta == plantaId);
            this.showPlantInfo(this.data.plantaSeleccionada);
            this.loadPlantEcoregiones(plantaId);
        } else {
            this.clearPlantInfo();
        }
    }

    showPlantInfo(planta) {
        const infoDiv = document.getElementById('infoPlanta');
        infoDiv.innerHTML = `
            <h6>${planta.nombreCientifico}</h6>
            <p><strong>Familia:</strong> ${planta.nomFamilia || 'No especificada'}</p>
            <p><strong>Nombres comunes:</strong> ${planta.nombresComunes || 'No especificados'}</p>
        `;
    }

    clearPlantInfo() {
        document.getElementById('infoPlanta').innerHTML = 'Seleccione una planta para ver su información';
        document.getElementById('tablaEcoregionesPlanta').querySelector('tbody').innerHTML = 
            '<tr><td colspan="3" class="text-center">Seleccione una planta</td></tr>';
    }

    async loadPlantEcoregiones(plantaId) {
        try {
            const response = await fetch(`/api/plantas/${plantaId}/ecoregiones`);
            const ecoregionesPlanta = await response.json();
            this.renderPlantEcoregionesTable(ecoregionesPlanta);
        } catch (error) {
            console.error('Error cargando ecoregiones de la planta:', error);
        }
    }

    renderPlantEcoregionesTable(ecoregiones) {
        const tbody = document.getElementById('tablaEcoregionesPlanta').querySelector('tbody');
        tbody.innerHTML = '';
        
        if (ecoregiones.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center">No tiene ecoregiones asociadas</td></tr>';
            return;
        }

        ecoregiones.forEach(eco => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${eco.ecoregion}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="plantManager.removeEcoregionFromPlant(${eco.idecoregion_planta})">
                        Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    // === MANEJO DE REGIONES Y PROVINCIAS ===
    async loadProvinciasByRegion(regionId) {
        try {
            const response = await fetch(`/api/regiones/${regionId}/provincias`);
            const provincias = await response.json();
            this.renderProvinciasTable(provincias, regionId);
        } catch (error) {
            console.error('Error cargando provincias:', error);
        }
    }

    renderProvinciasTable(provincias, regionId) {
        const tbody = document.getElementById('tablaProvincias').querySelector('tbody');
        tbody.innerHTML = '';
        
        if (provincias.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center">No hay provincias</td></tr>';
            return;
        }

        provincias.forEach(provincia => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${provincia.nombreProvincia}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="plantManager.editProvincia(${provincia.idprovincias}, '${provincia.nombreProvincia}', ${regionId})">
                        Editar
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="plantManager.deleteProvincia(${provincia.idprovincias})">
                        Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    showRegionTable() {
        const tbody = document.getElementById('tablaRegiones').querySelector('tbody');
        tbody.innerHTML = '';
        
        this.data.regiones.forEach(region => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${region.idRegion}</td>
                <td>${region.region}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="plantManager.editRegion(${region.idRegion}, '${region.region}')">
                        Editar
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="plantManager.deleteRegion(${region.idRegion})">
                        Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    async loadProvinciasByRegionForSelect(regionId, selectId) {
        if (!regionId) {
            document.getElementById(selectId).innerHTML = '<option value="">Seleccione una provincia...</option>';
            return;
        }
        
        try {
            const response = await fetch(`/api/regiones/${regionId}/provincias`);
            const provincias = await response.json();
            
            this.populateSelect(selectId, provincias, 'idprovincias', 'nombreProvincia', 'Seleccione una provincia...');
            
            if (selectId === 'provinciaEcoregion') {
                this.populateSelect('filtroProvinciaEcoregion', provincias, 'idprovincias', 'nombreProvincia', 'Seleccione una provincia para ver ecoregiones...');
            }
        } catch (error) {
            console.error('Error cargando provincias:', error);
        }
    }

    // === OPERACIONES CRUD ===
    async addEcoregionToPlant() {
        if (!this.data.plantaSeleccionada) {
            this.showMessage('Seleccione una planta primero', 'warning');
            return;
        }
        
        const ecoregionId = document.getElementById('selectEcoregion').value;
        if (!ecoregionId) {
            this.showMessage('Seleccione una ecoregión', 'warning');
            return;
        }
        
        try {
            const response = await this.apiRequest('/api/ecoregion-planta', 'POST', {
                idPlanta: this.data.plantaSeleccionada.idPlanta,
                idEcoregion: ecoregionId
            });
            
            if (response.ok) {
                this.showMessage('Ecoregión agregada exitosamente', 'success');
                this.loadPlantEcoregiones(this.data.plantaSeleccionada.idPlanta);
                document.getElementById('selectEcoregion').value = '';
            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error agregando ecoregión:', error);
            this.showMessage('Error al agregar la ecoregión', 'danger');
        }
    }

    async createRegion() {
        const nombre = document.getElementById('nombreRegion').value;
        
        try {
            const response = await this.apiRequest('/api/regiones', 'POST', { region: nombre });
            
            if (response.ok) {
                this.showMessage('Región creada exitosamente', 'success');
                document.getElementById('nombreRegion').value = '';
                await this.loadRegiones();
            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error creando región:', error);
            this.showMessage('Error al crear la región', 'danger');
        }
    }

    async createProvincia() {
        const regionId = document.getElementById('regionProvincia').value;
        const nombre = document.getElementById('nombreProvincia').value;
        
        try {
            const response = await this.apiRequest('/api/provincias', 'POST', {
                nombreProvincia: nombre,
                idRegion: regionId
            });
            
            if (response.ok) {
                this.showMessage('Provincia creada exitosamente', 'success');
                document.getElementById('nombreProvincia').value = '';
                document.getElementById('regionProvincia').value = '';
            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error creando provincia:', error);
            this.showMessage('Error al crear la provincia', 'danger');
        }
    }

    async associateEcoregionProvincia() {
        const provinciaId = document.getElementById('provinciaEcoregion').value;
        const ecoregionId = document.getElementById('ecoregionAsociar').value;

        if (!provinciaId || !ecoregionId) {
            this.showMessage('Seleccione una provincia y una ecoregión', 'warning');
            return;
        }

        try {
            const response = await this.apiRequest('/api/provincia-ecoregion', 'POST', {
                idProvincia: provinciaId,
                idEcoregion: ecoregionId
            });

            if (response.ok) {
                this.showMessage('Ecoregión asociada exitosamente', 'success');
                document.getElementById('formEcoregionProvincia').reset();

                // Si hay coincidencia con filtro, recargar tabla
                if (provinciaId === document.getElementById('filtroProvinciaEcoregion').value) {
                    this.loadEcoregionesProvinciaGeografico(provinciaId);
                }

            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error asociando ecoregión:', error);
            this.showMessage('Error al asociar la ecoregión', 'danger');
        }
    }

    // === OPERACIONES DE EDICIÓN Y ELIMINACIÓN ===
    editRegion(id, nombre) {
        this.setupEditModal('Editar Región', 'Nombre de la Región', nombre, id, 'region');
    }

    editProvincia(id, nombre, idRegion) {
        this.setupEditModal('Editar Provincia', 'Nombre de la Provincia', nombre, id, 'provincia');
        document.getElementById('regionProvincia').value = idRegion;
    }

    deleteRegion(id) {
        this.setupDeleteModal('¿Está seguro de que desea eliminar esta región?', id, 'region');
    }

    deleteProvincia(id) {
        this.setupDeleteModal('¿Está seguro de que desea eliminar esta provincia?', id, 'provincia');
    }

    setupEditModal(title, label, value, id, type) {
        document.getElementById('editModalTitle').textContent = title;
        document.getElementById('editLabel').textContent = label;
        document.getElementById('editInput').value = value;
        document.getElementById('editId').value = id;
        document.getElementById('editType').value = type;
        
        new bootstrap.Modal(document.getElementById('editModal')).show();
    }

    setupDeleteModal(message, id, type) {
        document.getElementById('deleteMessage').textContent = message;
        document.getElementById('deleteId').value = id;
        document.getElementById('deleteType').value = type;
        
        new bootstrap.Modal(document.getElementById('deleteModal')).show();
    }

    async saveEdit() {
        const id = document.getElementById('editId').value;
        const type = document.getElementById('editType').value;
        const value = document.getElementById('editInput').value;
        
        const handlers = {
            'region': () => this.updateRegion(id, value),
            'provincia': () => this.updateProvincia(id, value, document.getElementById('regionProvincia').value)
        };
        
        if (handlers[type]) {
            await handlers[type]();
        }
    }

    async updateRegion(id, value) {
        try {
            const response = await this.apiRequest(`/api/regiones/${id}`, 'PUT', { region: value });
            
            if (response.ok) {
                this.showMessage('Región actualizada exitosamente', 'success');
                bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
                await this.loadRegiones();
            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error actualizando región:', error);
            this.showMessage('Error al actualizar la región', 'danger');
        }
    }

    async updateProvincia(id, value, idRegion) {
        try {
            const response = await this.apiRequest(`/api/provincias/${id}`, 'PUT', {
                nombreProvincia: value,
                idRegion: idRegion
            });
            
            if (response.ok) {
                this.showMessage('Provincia actualizada exitosamente', 'success');
                bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
                const regionActual = document.getElementById('filtroRegionProvincia').value;
                if (regionActual) {
                    this.loadProvinciasByRegion(regionActual);
                }
            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error actualizando provincia:', error);
            this.showMessage('Error al actualizar la provincia', 'danger');
        }
    }

    async confirmDelete() {
        const id = document.getElementById('deleteId').value;
        const type = document.getElementById('deleteType').value;
        
        const handlers = {
            'region': () => this.deleteRegionConfirmed(id),
            'provincia': () => this.deleteProvinciaConfirmed(id)
        };
        
        if (handlers[type]) {
            await handlers[type]();
        }
    }

    async deleteRegionConfirmed(id) {
        try {
            const response = await this.apiRequest(`/api/regiones/${id}`, 'DELETE');
            
            if (response.ok) {
                this.showMessage('Región eliminada exitosamente', 'success');
                bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
                await this.loadRegiones();
            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error eliminando región:', error);
            this.showMessage('Error al eliminar la región', 'danger');
        }
    }

    async deleteProvinciaConfirmed(id) {
        try {
            const response = await this.apiRequest(`/api/provincias/${id}`, 'DELETE');
            
            if (response.ok) {
                this.showMessage('Provincia eliminada exitosamente', 'success');
                bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
                
                const regionActual = document.getElementById('filtroRegionProvincia').value;
                if (regionActual) {
                    this.loadProvinciasByRegion(regionActual);
                }
            } else {
                const result = await response.json();
                this.showMessage(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Error eliminando provincia:', error);
            this.showMessage('Error al eliminar la provincia', 'danger');
        }
    }

    // === FUNCIONES AUXILIARES ===
    async removeEcoregionFromPlant(id) {
        if (confirm('¿Está seguro de que desea eliminar esta asociación?')) {
            try {
                const response = await this.apiRequest(`/api/ecoregion-planta/eliminar/${id}`, 'DELETE');
                
                if (response.ok) {
                    this.showMessage('Asociación eliminada exitosamente', 'success');
                    this.loadPlantEcoregiones(this.data.plantaSeleccionada.idPlanta);
                } else {
                    const result = await response.json();
                    this.showMessage(`Error: ${result.error}`, 'danger');
                }
            } catch (error) {
                console.error('Error eliminando asociación:', error);
                this.showMessage('Error al eliminar la asociación', 'danger');
            }
        }
    }

    async loadEcoregionesProvinciaGeografico(provinciaId) {
        try {
            const response = await fetch(`/api/provincias/${provinciaId}/ecoregiones`);
            const ecoregiones = await response.json();
            this.renderEcoregionesGeograficoTable(ecoregiones);
        } catch (error) {
            console.error('Error cargando ecoregiones de la provincia:', error);
        }
    }

    renderEcoregionesGeograficoTable(ecoregiones) {
        const tbody = document.getElementById('tablaEcoregionesGeografico').querySelector('tbody');
        tbody.innerHTML = '';
        
        if (ecoregiones.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center">No hay ecoregiones asociadas</td></tr>';
            return;
        }

        ecoregiones.forEach(eco => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${eco.ecoregion}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="plantManager.removeProvinciaEcoregion(${eco.idprovincias}, ${eco.idecoregion})">
                        Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    async removeProvinciaEcoregion(provinciaId, ecoregionId) {
        if (confirm('¿Está seguro de que desea eliminar esta asociación?')) {
            try {
                const response = await this.apiRequest('/api/provincia-ecoregion', 'DELETE', {
                    idProvincia: provinciaId,
                    idEcoregion: ecoregionId
                });
                
                if (response.ok) {
                    this.showMessage('Asociación eliminada exitosamente', 'success');
                    this.loadEcoregionesProvinciaGeografico(provinciaId);
                } else {
                    const result = await response.json();
                    this.showMessage(`Error: ${result.error}`, 'danger');
                }
            } catch (error) {
                console.error('Error eliminando asociación:', error);
                this.showMessage('Error al eliminar la asociación', 'danger');
            }
        }
    }

    // === UTILIDADES ===
    async apiRequest(url, method = 'GET', data = null) {
        const config = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        return await fetch(url, config);
    }

    showMessage(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.plantManager = new PlantManagement();
});