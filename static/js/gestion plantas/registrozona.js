// Variables globales
    let plantaszona = [];
    let regiones = [];
    let provincias = [];
    let ecoregiones = [];
    let plantaSeleccionada = null;

    // Inicializar la aplicación
    document.addEventListener('DOMContentLoaded', function() {
        cargarPlantas();
        cargarRegiones();
        cargarEcoregiones();
        inicializarEventos();
    });

    // Eventos principales
    function inicializarEventos() {
        // Evento para seleccionar planta
        document.getElementById('selectPlanta').addEventListener('change', function() {
            const plantaId = this.value;
            if (plantaId) {
                plantaSeleccionada = plantaszona.find(p => p.idPlanta == plantaId);
                mostrarInfoPlanta(plantaSeleccionada);
                cargarEcoregionesPlanta(plantaId);
            } else {
                limpiarInfoPlanta();
            }
        });

        // Formulario agregar ecoregión a planta
        document.getElementById('formAgregarEcoregion').addEventListener('submit', function(e) {
            e.preventDefault();
            agregarEcoregionPlanta();
        });

        // Formulario crear región
        document.getElementById('formRegion').addEventListener('submit', function(e) {
            e.preventDefault();
            crearRegion();
        });

        // Formulario crear provincia
        document.getElementById('formProvincia').addEventListener('submit', function(e) {
            e.preventDefault();
            crearProvincia();
        });

        // Formulario asociar ecoregión a provincia
        document.getElementById('formEcoregionProvincia').addEventListener('submit', function(e) {
            e.preventDefault();
            asociarEcoregionProvincia();
        });

        // Filtros
        document.getElementById('filtroRegionProvincia').addEventListener('change', function() {
            if (this.value) {
                cargarProvinciasPorRegion(this.value);
            }
        });

        document.getElementById('filtroProvinciaEcoregion').addEventListener('change', function() {
            if (this.value) {
                cargarEcoregionesProvinciaGeografico(this.value);
            }
        });

        // Eventos para cascada de selects
        document.getElementById('regionEcoregion').addEventListener('change', function() {
            cargarProvinciasPorRegionSelect(this.value, 'provinciaEcoregion');
        });

        // Eventos de modales
        document.getElementById('saveEdit').addEventListener('click', guardarEdicion);
        document.getElementById('confirmDelete').addEventListener('click', confirmarEliminacion);
    }

    // Funciones de carga de datos
    async function cargarPlantas() {
        try {
            const response = await fetch('/api/todas_plantas_zonas');
            plantaszona = await response.json();
            
            const select = document.getElementById('selectPlanta');
            select.innerHTML = '<option value="">Seleccione una planta...</option>';
            
            plantaszona.forEach(planta => {
                const option = document.createElement('option');
                option.value = planta.idPlanta;
                option.textContent = `${planta.nombreCientifico} - ${planta.nombresComunes || 'Sin nombres comunes'}`;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Error cargando plantas:', error);
            alert('Error al cargar las plantas');
        }
    }

    async function cargarRegiones() {
        try {
            const response = await fetch('/api/regiones');
            regiones = await response.json();
            
            // Llenar select de regiones en formulario de provincia
            llenarSelectRegiones('regionProvincia');
            llenarSelectRegiones('filtroRegionProvincia');
            llenarSelectRegiones('regionEcoregion');
            
            // Llenar tabla de regiones
            mostrarTablaRegiones();
            
        } catch (error) {
            console.error('Error cargando regiones:', error);
            alert('Error al cargar las regiones');
        }
    }

    async function cargarEcoregiones() {
        try {
            const response = await fetch('/api/ecoregiones');
            ecoregiones = await response.json();
            
            // Llenar select de regiones en formulario de provincia
            llenarSelectEcoregiones('ecoregionAsociar');
            llenarSelectEcoregiones('selectEcoregion');
            
        } catch (error) {
            console.error('Error cargando ecorregiones:', error);
            alert('Error al cargar las ecrregiones');
        }
    }

    // Funciones auxiliares para llenar selects
    function llenarSelectRegiones(selectId) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Seleccione una región...</option>';
        
        regiones.forEach(region => {
            const option = document.createElement('option');
            option.value = region.idRegion;
            option.textContent = region.region;
            select.appendChild(option);
        });
    }

    function llenarSelectEcoregiones(selectId) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Seleccione una ecoregión...</option>';
        
        ecoregiones.forEach(ecoregion => {
            const option = document.createElement('option');
            option.value = ecoregion.idecoregion;
            option.textContent = ecoregion.ecoregion;
            select.appendChild(option);
        });
    }

    // Funciones para mostrar información
    function mostrarInfoPlanta(planta) {
        const infoDiv = document.getElementById('infoPlanta');
        infoDiv.innerHTML = `
            <h6>${planta.nombreCientifico}</h6>
            <p><strong>Familia:</strong> ${planta.nomFamilia || 'No especificada'}</p>
            <p><strong>Nombres comunes:</strong> ${planta.nombresComunes || 'No especificados'}</p>
        `;
    }

    function limpiarInfoPlanta() {
        document.getElementById('infoPlanta').innerHTML = 'Seleccione una planta para ver su información';
        document.getElementById('tablaEcoregionesPlanta').querySelector('tbody').innerHTML = 
            '<tr><td colspan="3" class="text-center">Seleccione una planta</td></tr>';
    }

    // Funciones para cargar datos específicos
    async function cargarEcoregionesPlanta(plantaId) {
        try {
            const response = await fetch(`/api/plantas/${plantaId}/ecoregiones`);
            const ecoregionesPlanta = await response.json();
            
            const tbody = document.getElementById('tablaEcoregionesPlanta').querySelector('tbody');
            tbody.innerHTML = '';
            
            if (ecoregionesPlanta.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center">No tiene ecoregiones asociadas</td></tr>';
            } else {
                ecoregionesPlanta.forEach(eco => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${eco.ecoregion}</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="eliminarEcoregionPlanta(${eco.idecoregion_planta})">
                                Eliminar
                            </button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Error cargando ecoregiones de la planta:', error);
        }
    }

    async function cargarProvinciasPorRegion(regionId) {
        try {
            const response = await fetch(`/api/regiones/${regionId}/provincias`);
            const provincias = await response.json();
            
            const tbody = document.getElementById('tablaProvincias').querySelector('tbody');
            tbody.innerHTML = '';
            
            if (provincias.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center">No hay provincias</td></tr>';
            } else {
                provincias.forEach(provincia => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${provincia.idProvincia}</td>
                        <td>${provincia.nombreProvincia}</td>
                        <td>
                            <button class="btn btn-sm btn-warning" onclick="editarProvincia(${provincia.idProvincia}, '${provincia.nombreProvincia}')">
                                Editar
                            </button>
                            <button class="btn btn-sm btn-danger" onclick="eliminarProvincia(${provincia.idProvincia})">
                                Eliminar
                            </button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Error cargando provincias:', error);
        }
    }

    function mostrarTablaRegiones() {
        const tbody = document.getElementById('tablaRegiones').querySelector('tbody');
        tbody.innerHTML = '';
        
        regiones.forEach(region => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${region.idRegion}</td>
                <td>${region.region}</td>
                <td>
                    <button class="btn btn-sm btn-warning" onclick="editarRegion(${region.idRegion}, '${region.region}')">
                        Editar
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="eliminarRegion(${region.idRegion})">
                        Eliminar
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });
    }

    // Funciones CRUD
    async function agregarEcoregionPlanta() {
        if (!plantaSeleccionada) {
            alert('Seleccione una planta primero');
            return;
        }
        
        const ecoregionId = document.getElementById('selectEcoregion').value;
        if (!ecoregionId) {
            alert('Seleccione una ecoregión');
            return;
        }
        
        try {
            const response = await fetch('/api/ecoregion-planta', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idPlanta: plantaSeleccionada.idPlanta,
                    idEcoregion: ecoregionId
                })
            });
            
            const result = await response.json();
            if (response.ok) {
                alert('Ecoregión agregada exitosamente');
                cargarEcoregionesPlanta(plantaSeleccionada.idPlanta);
                document.getElementById('selectEcoregion').value = '';
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error agregando ecoregión:', error);
            alert('Error al agregar la ecoregión');
        }
    }

    async function crearRegion() {
        const nombre = document.getElementById('nombreRegion').value;
        
        try {
            const response = await fetch('/api/regiones', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    region: nombre
                })
            });
            
            const result = await response.json();
            if (response.ok) {
                alert('Región creada exitosamente');
                document.getElementById('nombreRegion').value = '';
                cargarRegiones();
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error creando región:', error);
            alert('Error al crear la región');
        }
    }

    async function crearProvincia() {
        const regionId = document.getElementById('regionProvincia').value;
        const nombre = document.getElementById('nombreProvincia').value;
        
        try {
            const response = await fetch('/api/provincias', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    nombreProvincia: nombre,
                    idRegion: regionId
                })
            });
            
            const result = await response.json();
            if (response.ok) {
                alert('Provincia creada exitosamente');
                document.getElementById('nombreProvincia').value = '';
                document.getElementById('regionProvincia').value = '';
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error creando provincia:', error);
            alert('Error al crear la provincia');
        }
    }

    // Funciones de edición y eliminación
    function editarRegion(id, nombre) {
        document.getElementById('editModalTitle').textContent = 'Editar Región';
        document.getElementById('editLabel').textContent = 'Nombre de la Región';
        document.getElementById('editInput').value = nombre;
        document.getElementById('editId').value = id;
        document.getElementById('editType').value = 'region';
        
        new bootstrap.Modal(document.getElementById('editModal')).show();
    }

    function eliminarRegion(id) {
        document.getElementById('deleteMessage').textContent = '¿Está seguro de que desea eliminar esta región?';
        document.getElementById('deleteId').value = id;
        document.getElementById('deleteType').value = 'region';
        
        new bootstrap.Modal(document.getElementById('deleteModal')).show();
    }

    async function eliminarEcoregionPlanta(id) {
        if (confirm('¿Está seguro de que desea eliminar esta asociación?')) {
            try {
                const response = await fetch(`/api/ecoregion-planta/eliminar/${id}`, {
                    method: 'DELETE'
                });                
                
                const result = await response.json();
                if (response.ok) {
                    alert('Asociación eliminada exitosamente');
                    cargarEcoregionesPlanta(plantaSeleccionada.idPlanta);
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error eliminando asociación:', error);
                alert('Error al eliminar la asociación');
            }
        }
    }

    async function guardarEdicion() {
        const id = document.getElementById('editId').value;
        const tipo = document.getElementById('editType').value;
        const valor = document.getElementById('editInput').value;
        
        if (tipo === 'region') {
            try {
                const response = await fetch(`/api/regiones/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        region: valor
                    })
                });
                
                const result = await response.json();
                if (response.ok) {
                    alert('Región actualizada exitosamente');
                    bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
                    cargarRegiones();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error actualizando región:', error);
                alert('Error al actualizar la región');
            }
        }
    }

    async function confirmarEliminacion() {
        const id = document.getElementById('deleteId').value;
        const tipo = document.getElementById('deleteType').value;
        
        if (tipo === 'region') {
            try {
                const response = await fetch(`/api/regiones/${id}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                if (response.ok) {
                    alert('Región eliminada exitosamente');
                    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
                    cargarRegiones();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error eliminando región:', error);
                alert('Error al eliminar la región');
            }
        }
    }

    // Funciones adicionales para provincias
    function editarProvincia(id, nombre) {
        document.getElementById('editModalTitle').textContent = 'Editar Provincia';
        document.getElementById('editLabel').textContent = 'Nombre de la Provincia';
        document.getElementById('editInput').value = nombre;
        document.getElementById('editId').value = id;
        document.getElementById('editType').value = 'provincia';
        
        new bootstrap.Modal(document.getElementById('editModal')).show();
    }

    function eliminarProvincia(id) {
        document.getElementById('deleteMessage').textContent = '¿Está seguro de que desea eliminar esta provincia?';
        document.getElementById('deleteId').value = id;
        document.getElementById('deleteType').value = 'provincia';
        
        new bootstrap.Modal(document.getElementById('deleteModal')).show();
    }

    async function cargarProvinciasPorRegionSelect(regionId, selectId) {
        if (!regionId) {
            document.getElementById(selectId).innerHTML = '<option value="">Seleccione una provincia...</option>';
            return;
        }
        
        try {
            const response = await fetch(`/api/regiones/${regionId}/provincias`);
            const provincias = await response.json();
            
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Seleccione una provincia...</option>';
            
            provincias.forEach(provincia => {
                const option = document.createElement('option');
                option.value = provincia.idprovincias;
                option.textContent = provincia.nombreProvincia;
                select.appendChild(option);
            });
            
            // También llenar el filtro de provincias para ecoregiones
            if (selectId === 'provinciaEcoregion') {
                const filtroSelect = document.getElementById('filtroProvinciaEcoregion');
                filtroSelect.innerHTML = '<option value="">Seleccione una provincia para ver ecoregiones...</option>';
                
                provincias.forEach(provincia => {
                    const option = document.createElement('option');
                    option.value = provincia.idprovincias;
                    option.textContent = provincia.nombreProvincia;
                    filtroSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error cargando provincias:', error);
        }
    }

    async function asociarEcoregionProvincia() {
        const provinciaId = document.getElementById('provinciaEcoregion').value;
        const ecoregionId = document.getElementById('ecoregionAsociar').value;
        
        if (!provinciaId || !ecoregionId) {
            alert('Seleccione una provincia y una ecoregión');
            return;
        }
        
        try {
            const response = await fetch('/api/provincia-ecoregion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    idProvincia: provinciaId,
                    idEcoregion: ecoregionId
                })
            });
            
            const result = await response.json();
            if (response.ok) {
                alert('Ecoregión asociada exitosamente');
                document.getElementById('formEcoregionProvincia').reset();
                inicializarEventos();
                cargarEcoregionesProvinciaGeografico(provinciaId);
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error asociando ecoregión:', error);
            alert('Error al asociar la ecoregión');
        }
    }

    async function cargarEcoregionesProvinciaGeografico(provinciaId) {
        try {
            const response = await fetch(`/api/provincias/${provinciaId}/ecoregiones`);
            const ecoregiones = await response.json();
            
            const tbody = document.getElementById('tablaEcoregionesGeografico').querySelector('tbody');
            tbody.innerHTML = '';
            
            if (ecoregiones.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center">No hay ecoregiones asociadas</td></tr>';
            } else {
                ecoregiones.forEach(eco => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${eco.ecoregion}</td>
                        <td>
                            <button class="btn btn-sm btn-danger" onclick="eliminarProvinciaEcoregion(${eco.idprovincias}, ${eco.idecoregion})">
                                Eliminar
                            </button>
                        </td>
                    `;
                    console.log("Provincia recibida:", eco.idecoregion,eco.ecoregion, eco.idprovincias, eco.idRegion);
                    tbody.appendChild(row);
                });
            }
        } catch (error) {
            console.error('Error cargando ecoregiones de la provincia:', error);
        }
    }

    async function eliminarProvinciaEcoregion(provinciaId, ecoregionId) {
        if (confirm('¿Está seguro de que desea eliminar esta asociación?')) {
            try {
                const response = await fetch('/api/provincia-ecoregion', {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        idProvincia: provinciaId,
                        idEcoregion: ecoregionId
                    })
                });
                
                const result = await response.json();
                if (response.ok) {
                    alert('Asociación eliminada exitosamente');
                    cargarEcoregionesProvinciaGeografico(provinciaId);
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error eliminando asociación:', error);
                alert('Error al eliminar la asociación');
            }
        }
    }

    // Mejorar la función de guardar edición para manejar provincias
    async function guardarEdicionMejorada() {
        const id = document.getElementById('editId').value;
        const tipo = document.getElementById('editType').value;
        const valor = document.getElementById('editInput').value;
        
        if (tipo === 'region') {
            try {
                const response = await fetch(`/api/regiones/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        region: valor
                    })
                });
                
                const result = await response.json();
                if (response.ok) {
                    alert('Región actualizada exitosamente');
                    bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
                    cargarRegiones();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error actualizando región:', error);
                alert('Error al actualizar la región');
            }
        } else if (tipo === 'provincia') {
            // Para provincias necesitamos el ID de la región también
            // Esto requeriría modificar el modal para incluir la región
            alert('Función de edición de provincia en desarrollo');
        }
    }

    // Mejorar la función de confirmación de eliminación
    async function confirmarEliminacionMejorada() {
        const id = document.getElementById('deleteId').value;
        const tipo = document.getElementById('deleteType').value;
        
        if (tipo === 'region') {
            try {
                const response = await fetch(`/api/regiones/${id}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                if (response.ok) {
                    alert('Región eliminada exitosamente');
                    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
                    cargarRegiones();
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error eliminando región:', error);
                alert('Error al eliminar la región');
            }
        } else if (tipo === 'provincia') {
            try {
                const response = await fetch(`/api/provincias/${id}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                if (response.ok) {
                    alert('Provincia eliminada exitosamente');
                    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
                    // Recargar la tabla de provincias si está visible
                    const regionActual = document.getElementById('filtroRegionProvincia').value;
                    if (regionActual) {
                        cargarProvinciasPorRegion(regionActual);
                    }
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error eliminando provincia:', error);
                alert('Error al eliminar la provincia');
            }
        }
    }

    // Reemplazar las funciones anteriores con las mejoradas
    document.getElementById('saveEdit').removeEventListener('click', guardarEdicion);
    document.getElementById('confirmDelete').removeEventListener('click', confirmarEliminacion);
    document.getElementById('saveEdit').addEventListener('click', guardarEdicionMejorada);
    document.getElementById('confirmDelete').addEventListener('click', confirmarEliminacionMejorada);

    // Función para mostrar mensajes de estado
    function mostrarMensaje(mensaje, tipo = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${tipo} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
        
        // Auto-cerrar después de 5 segundos
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }