let plantas = [];
let plantaSeleccionada = null;
let saberEditando = null;

// Cargar plantas al iniciar
async function cargarPlantas() {
    try {
        const response = await fetch('/api/plantas');
        plantas = await response.json();
        mostrarPlantas(plantas);
    } catch (error) {
        console.error('Error al cargar plantas:', error);
        alert('Error al cargar las plantas');
    }
}

// Mostrar plantas en cards
function mostrarPlantas(plantasAMostrar) {
    const grid = document.getElementById('plantasGrid');
    const noResults = document.getElementById('noResults');
    
    if (plantasAMostrar.length === 0) {
        grid.innerHTML = '';
        noResults.style.display = 'block';
        return;
    }
    
    noResults.style.display = 'none';
    
    grid.innerHTML = plantasAMostrar.map(planta => `
        <div class="planta-card" onclick="seleccionarPlanta(${planta.idPlanta})">
            <div class="planta-nombre-cientifico">${planta.nombreCientifico}</div>
            <div class="planta-familia">Familia: ${planta.nomFamilia || 'Sin especificar'}</div>
            <div class="planta-nombres-comunes">
                <strong>Nombres comunes:</strong><br>
                ${planta.nombresComunes || 'Sin nombres comunes registrados'}
            </div>
        </div>
    `).join('');
}

// Filtrar plantas
function filtrarPlantas(termino) {
    const plantasFiltradas = plantas.filter(planta => {
        const texto = `${planta.nombreCientifico} ${planta.nomFamilia || ''} ${planta.nombresComunes || ''}`.toLowerCase();
        return texto.includes(termino.toLowerCase());
    });
    mostrarPlantas(plantasFiltradas);
}

// Seleccionar planta
async function seleccionarPlanta(plantaId) {
    // Remover selección anterior
    document.querySelectorAll('.planta-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Marcar nueva selección
    event.target.closest('.planta-card').classList.add('selected');
    
    plantaSeleccionada = plantas.find(p => p.idPlanta === plantaId);
    
    // Mostrar sección de saberes
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('saberesContent').style.display = 'block';
    document.getElementById('plantaSeleccionada').textContent = plantaSeleccionada.nombreCientifico;
    
    // Cargar saberes
    await cargarSaberes(plantaId);
}

// Cargar saberes de una planta
async function cargarSaberes(plantaId) {
    try {
        const response = await fetch(`/api/saberes/${plantaId}`);
        const saberes = await response.json();
        mostrarSaberes(saberes);
    } catch (error) {
        console.error('Error al cargar saberes:', error);
        alert('Error al cargar los saberes');
    }
}

// Mostrar saberes
function mostrarSaberes(saberes) {
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
                <button class="btn btn-edit" onclick="editarSaber(${saber.idSaberes}, '${saber.descripcionSaber.replace(/'/g, "\\'")}')">
                    ✏️ Editar
                </button>
                <button class="btn btn-delete" onclick="eliminarSaber(${saber.idSaberes})">
                    🗑️ Eliminar
                </button>
            </div>
        </div>
    `).join('');
}

// Abrir modal para agregar
function abrirModalAgregar() {
    saberEditando = null;
    document.getElementById('modalTitle').textContent = 'Agregar Saber Cultural';
    document.getElementById('descripcionSaber').value = '';
    document.getElementById('btnGuardar').textContent = 'Guardar';
    document.getElementById('saberModal').style.display = 'block';
}

// Editar saber
function editarSaber(id, descripcion) {
    saberEditando = id;
    document.getElementById('modalTitle').textContent = 'Editar Saber Cultural';
    document.getElementById('descripcionSaber').value = descripcion;
    document.getElementById('btnGuardar').textContent = 'Actualizar';
    document.getElementById('saberModal').style.display = 'block';
}

// Cerrar modal
function cerrarModal() {
    document.getElementById('saberModal').style.display = 'none';
    saberEditando = null;
}

// Eliminar saber
async function eliminarSaber(id) {
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
            await cargarSaberes(plantaSeleccionada.idPlanta);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al eliminar el saber');
    }
}

// Event listeners
document.getElementById('searchInput').addEventListener('input', (e) => {
    filtrarPlantas(e.target.value);
});

document.getElementById('saberForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const descripcion = document.getElementById('descripcionSaber').value.trim();
    
    if (!descripcion) {
        alert('La descripción es requerida');
        return;
    }
    
    try {
        const url = saberEditando ? `/api/saberes/${saberEditando}` : '/api/saberes';
        const method = saberEditando ? 'PUT' : 'POST';
        
        const body = saberEditando ? 
            { descripcionSaber: descripcion } :
            { descripcionSaber: descripcion, fk_plantas: plantaSeleccionada.idPlanta };
        
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
            cerrarModal();
            await cargarSaberes(plantaSeleccionada.idPlanta);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al guardar el saber');
    }
});

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('saberModal');
    if (event.target === modal) {
        cerrarModal();
    }
}

// Inicializar aplicación
cargarPlantas();