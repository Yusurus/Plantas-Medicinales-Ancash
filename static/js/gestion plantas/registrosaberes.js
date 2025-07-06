// Módulo para gestión de saberes culturales
const SaberesModule = (function() {
    // Variables privadas del módulo
    let plantasSaberes = [];
    let plantaSeleccionadaSaberes = null;
    let saberEditando = null;

    // Función privada para cargar plantas
    async function cargarPlantasSaberes() {
        try {
            const response = await fetch('/api/plantas');
            plantasSaberes = await response.json();
            mostrarPlantasSaberes(plantasSaberes);
        } catch (error) {
            console.error('Error al cargar plantas:', error);
            alert('Error al cargar las plantas');
        }
    }

    // Función privada para mostrar plantas en cards
    function mostrarPlantasSaberes(plantasAMostrar) {
        const grid = document.getElementById('plantasGrid');
        const noResults = document.getElementById('noResults');
        
        if (plantasAMostrar.length === 0) {
            grid.innerHTML = '';
            noResults.style.display = 'block';
            return;
        }
        
        noResults.style.display = 'none';
        
        grid.innerHTML = plantasAMostrar.map(planta => `
            <div class="planta-card" onclick="SaberesModule.seleccionarPlanta(${planta.idPlanta})">
                <div class="planta-nombre-cientifico">${planta.nombreCientifico}</div>
                <div class="planta-familia">Familia: ${planta.nomFamilia || 'Sin especificar'}</div>
                <div class="planta-nombres-comunes">
                    <strong>Nombres comunes:</strong><br>
                    ${planta.nombresComunes || 'Sin nombres comunes registrados'}
                </div>
            </div>
        `).join('');
    }

    // Función privada para filtrar plantas
    function filtrarPlantasSaberes(termino) {
        const plantasFiltradas = plantasSaberes.filter(planta => {
            const texto = `${planta.nombreCientifico} ${planta.nomFamilia || ''} ${planta.nombresComunes || ''}`.toLowerCase();
            return texto.includes(termino.toLowerCase());
        });
        mostrarPlantasSaberes(plantasFiltradas);
    }

    // Función privada para cargar saberes de una planta
    async function cargarSaberesPlanta(plantaId) {
        try {
            const response = await fetch(`/api/saberes/${plantaId}`);
            const saberes = await response.json();
            mostrarSaberesList(saberes);
        } catch (error) {
            console.error('Error al cargar saberes:', error);
            alert('Error al cargar los saberes');
        }
    }

    // Función privada para mostrar saberes
    function mostrarSaberesList(saberes) {
        const lista = document.getElementById('saberesList');
        
        if (saberes.length === 0) {
            lista.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📚</div>
                    <h3>Sin saberes registrados</h3>
                    <p>Esta planta aún no tiene saberes culturales registrados</p>
                </div>
            `;
            return;
        }
        
        lista.innerHTML = saberes.map(saber => `
            <div class="saber-item">
                <div class="saber-description">${saber.descripcionSaber}</div>
                <div class="saber-actions">
                    <button class="btn btn-edit" onclick="SaberesModule.editarSaber(${saber.idSaberes}, '${saber.descripcionSaber.replace(/'/g, "\\'")}')">
                        ✏️ Editar
                    </button>
                    <button class="btn btn-delete" onclick="SaberesModule.eliminarSaber(${saber.idSaberes})">
                        🗑️ Eliminar
                    </button>
                </div>
            </div>
        `).join('');
    }

    // Función privada para guardar/actualizar saber
    async function guardarSaber(descripcion) {
        try {
            const url = saberEditando ? `/api/saberes/${saberEditando}` : '/api/saberes';
            const method = saberEditando ? 'PUT' : 'POST';
            
            const body = saberEditando ? 
                { descripcionSaber: descripcion } :
                { descripcionSaber: descripcion, fk_plantas: plantaSeleccionadaSaberes.idPlanta };
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert(saberEditando ? 'Saber actualizado exitosamente' : 'Saber agregado exitosamente');
                cerrarModalSaber();
                await cargarSaberesPlanta(plantaSeleccionadaSaberes.idPlanta);
            } else {
                alert('Error: ' + result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al guardar el saber');
        }
    }

    // Función privada para cerrar modal
    function cerrarModalSaber() {
        document.getElementById('saberModal').style.display = 'none';
        saberEditando = null;
    }

    // Funciones públicas del módulo
    return {
        // Inicializar el módulo
        init: function() {
            cargarPlantasSaberes();
            this.initEventListeners();
        },

        // Inicializar event listeners
        initEventListeners: function() {
            // Buscador de plantas
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.addEventListener('input', (e) => {
                    filtrarPlantasSaberes(e.target.value);
                });
            }

            // Formulario de saber
            const saberForm = document.getElementById('saberForm');
            if (saberForm) {
                saberForm.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    
                    const descripcion = document.getElementById('descripcionSaber').value.trim();
                    
                    if (!descripcion) {
                        alert('La descripción es requerida');
                        return;
                    }
                    
                    await guardarSaber(descripcion);
                });
            }

            // Cerrar modal al hacer clic fuera
            window.addEventListener('click', (event) => {
                const modal = document.getElementById('saberModal');
                if (event.target === modal) {
                    cerrarModalSaber();
                }
            });
        },

        // Seleccionar planta
        seleccionarPlanta: async function(plantaId) {
            // Remover selección anterior
            document.querySelectorAll('.planta-card').forEach(card => {
                card.classList.remove('selected');
            });
            
            // Marcar nueva selección
            event.target.closest('.planta-card').classList.add('selected');
            
            plantaSeleccionadaSaberes = plantasSaberes.find(p => p.idPlanta === plantaId);
            
            // Mostrar sección de saberes
            const emptyState = document.getElementById('emptyState');
            const saberesContent = document.getElementById('saberesContent');
            const plantaSeleccionadaElement = document.getElementById('plantaSeleccionada');
            
            if (emptyState) emptyState.style.display = 'none';
            if (saberesContent) saberesContent.style.display = 'block';
            if (plantaSeleccionadaElement) plantaSeleccionadaElement.textContent = plantaSeleccionadaSaberes.nombreCientifico;
            
            // Cargar saberes
            await cargarSaberesPlanta(plantaId);
        },

        // Abrir modal para agregar
        abrirModalAgregar: function() {
            saberEditando = null;
            document.getElementById('modalTitle').textContent = 'Agregar Saber Cultural';
            document.getElementById('descripcionSaber').value = '';
            document.getElementById('btnGuardar').textContent = 'Guardar';
            document.getElementById('saberModal').style.display = 'block';
        },

        // Editar saber
        editarSaber: function(id, descripcion) {
            saberEditando = id;
            document.getElementById('modalTitle').textContent = 'Editar Saber Cultural';
            document.getElementById('descripcionSaber').value = descripcion;
            document.getElementById('btnGuardar').textContent = 'Actualizar';
            document.getElementById('saberModal').style.display = 'block';
        },

        // Cerrar modal
        cerrarModal: function() {
            cerrarModalSaber();
        },

        // Eliminar saber
        eliminarSaber: async function(id) {
            if (!confirm('¿Estás seguro de que deseas eliminar este saber cultural?')) {
                return;
            }
            
            try {
                const response = await fetch(`/api/saberes/${id}`, {
                    method: 'DELETE'
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('Saber eliminado exitosamente');
                    await cargarSaberesPlanta(plantaSeleccionadaSaberes.idPlanta);
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al eliminar el saber');
            }
        }
    };
})();

// Inicializar el módulo cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Solo inicializar si estamos en la página de saberes
    if (document.getElementById('plantasGrid') && document.getElementById('saberesList')) {
        SaberesModule.init();
    }
});