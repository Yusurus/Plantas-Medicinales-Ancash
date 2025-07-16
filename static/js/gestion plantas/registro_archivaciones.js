document.addEventListener('DOMContentLoaded', () => {
  const activeContainer = document.getElementById('active-plants-container');
  const activeCount = document.getElementById('active-plants-count');
  const searchInput = document.getElementById('plantSearchInput');
  const placeholder = document.getElementById('placeholder-message');
  const detailsContainer = document.getElementById('selected-plant-details-container');

  const modal1 = document.getElementById('confirmation-modal');
  const modal2 = document.getElementById('second-confirmation-modal');
  const modal3 = document.getElementById('third-confirmation-modal');

  const cancel1 = document.getElementById('cancel-archive');
  const confirm1 = document.getElementById('confirm-archive');

  const cancel2 = document.getElementById('cancel-final-archive');
  const confirm2 = document.getElementById('confirm-final-archive');

  const cancel3 = document.getElementById('cancel-third-archive');
  const confirm3 = document.getElementById('confirm-third-archive');

  const inputReason = document.getElementById('archive-reason');
  const inputPhrase = document.getElementById('third-confirmation-input');
  const requiredPhrase = document.getElementById('required-confirmation-text');
  const errorPhrase = document.getElementById('third-confirmation-error');
  const itemNameSpan = document.getElementById('item-name-to-archive');

  const tabActivos = document.getElementById('tab-activos');
  const tabArchivados = document.getElementById('tab-archivados');

  let allPlants = [];
  let selectedPlant = null;
  let currentArchive = { type: '', id: null, name: '' };

  function toggleModal(modal, show) {
    modal.classList.toggle('hidden', !show);
    modal.classList.toggle('active', show);
  }

  function createPlantCard(plant) {
    const card = document.createElement('div');
    card.className = 'bg-white p-4 shadow rounded-lg cursor-pointer hover:bg-green-100';
    card.setAttribute('data-nombre', plant.nombreCientifico.toLowerCase());
    card.setAttribute('data-familia', plant.nomFamilia.toLowerCase());
    card.setAttribute('data-comun', (plant.nombres_comunes || '').toLowerCase());
    card.innerHTML = `
      <h4 class="font-semibold text-lg text-green-800">${plant.nombreCientifico}</h4>
      <p class="text-sm text-gray-600">Familia: ${plant.nomFamilia}</p>
      <p class="text-sm text-gray-500">${plant.nombres_comunes || ''}</p>
    `;
    card.addEventListener('click', () => {
      selectedPlant = plant;
      loadPlantDetails(plant);
    });
    return card;
  }

  async function fetchPlantasActivas() {
    try {
      const res = await fetch('/api/plantas_activas');
      const data = await res.json();
      allPlants = data;
      renderPlantas(data);
    } catch (err) {
      console.error('Error cargando plantas:', err);
    }
  }

  function renderPlantas(plantas) {
    activeContainer.innerHTML = '';
    if (plantas.length === 0) {
      activeContainer.innerHTML = '<p class="text-gray-500">No hay plantas activas</p>';
    } else {
      plantas.forEach(p => activeContainer.appendChild(createPlantCard(p)));
    }
    activeCount.textContent = `${plantas.length} plantas`;
  }

  if (searchInput) {
    searchInput.addEventListener('input', e => {
      const value = e.target.value.toLowerCase();
      const cards = activeContainer.querySelectorAll('.bg-white');
      cards.forEach(card => {
        const match = card.dataset.nombre.includes(value) ||
                      card.dataset.familia.includes(value) ||
                      card.dataset.comun.includes(value);
        card.style.display = match ? 'block' : 'none';
      });
    });
  }

  async function loadPlantDetails(plant) {
    placeholder.classList.add('hidden');
    detailsContainer.innerHTML = '<p class="text-sm text-gray-500">Cargando detalles...</p>';

    try {
      const res = await fetch(`/api/plantas/${plant.idPlanta}/detalles`);
      const data = await res.json();
      renderDetallesPlanta(plant, data);
    } catch (err) {
      detailsContainer.innerHTML = '<p class="text-red-500">Error al cargar detalles.</p>';
    }
  }

  function renderDetallesPlanta(plant, detalles) {
    function renderItems(items, type, mostrarBoton = true) {
      return items.map(item => {
        let label = '';
        let id = '';
        let name = '';
        if (type === 'zona') {
          label = item.ecoregion;
          id = item.idZona;
          name = item.ecoregion;
        } else if (type === 'saber') {
          label = item.descripcionSaber;
          id = item.idSaberesCulturales;
          name = item.descripcionSaber;
        } else if (type === 'uso') {
          label = `${item.uso}: ${item.parte} - ${item.preparacion}`;
          id = item.idUsos;
          name = item.uso;
        }
        return `
          <div class="detail-item">
            <div class="detail-label">${label}</div>
            ${mostrarBoton ? `<button class="pm-btn pm-btn-save" data-type="${type}" data-id="${id}" data-name="${name}">Archivar ${type.charAt(0).toUpperCase() + type.slice(1)}</button>` : ''}
          </div>`;
      }).join('');
    }

    const zonas = renderItems(detalles.zonas, 'zona');
    const saberes = renderItems(detalles.saberes, 'saber');
    const usos = renderItems(detalles.usos, 'uso');

    detailsContainer.innerHTML = `
      <div class="mb-4">
        <h4 class="text-lg font-semibold text-green-800">Detalles de ${plant.nombreCientifico}</h4>
        <p class="text-sm text-gray-700">Familia: ${plant.nomFamilia} | Nombres Comunes: ${plant.nombres_comunes || '—'}</p>
      </div>
      <div class="mb-4" id="tab-panel-activos">
        <h5 class="font-semibold">Zonas</h5>
        ${zonas || '<p class="text-sm text-gray-400">No hay zonas</p>'}
        <h5 class="font-semibold mt-4">Saberes Culturales</h5>
        ${saberes || '<p class="text-sm text-gray-400">No hay saberes</p>'}
        <h5 class="font-semibold mt-4">Usos Medicinales</h5>
        ${usos || '<p class="text-sm text-gray-400">No hay usos</p>'}
        <div class="mt-6 text-center">
          <button id="btn-archive-plant" class="pm-btn pm-btn-save">Archivar Planta Completa</button>
        </div>
      </div>
      <div class="mb-4 hidden" id="tab-panel-archivados">
        <p class="text-sm text-gray-400">Cargando elementos archivados...</p>
      </div>
    `;

    document.querySelectorAll('[data-type]').forEach(btn => {
      btn.addEventListener('click', () => {
        currentArchive = {
          type: btn.dataset.type,
          id: btn.dataset.id,
          name: btn.dataset.name
        };
        itemNameSpan.textContent = currentArchive.name;
        inputReason.value = '';
        toggleModal(modal1, true);
      });
    });

    document.getElementById('btn-archive-plant').addEventListener('click', () => {
      currentArchive = {
        type: 'planta',
        id: plant.idPlanta,
        name: plant.nombreCientifico
      };
      requiredPhrase.textContent = `ARCHIVAR PLANTA ${plant.nombreCientifico}`;
      inputPhrase.value = '';
      errorPhrase.classList.add('hidden');
      toggleModal(modal3, true);
    });

    tabActivos.addEventListener('click', () => {
      tabActivos.classList.add('active-tab');
      tabArchivados.classList.remove('active-tab');
      document.getElementById('tab-panel-activos').classList.remove('hidden');
      document.getElementById('tab-panel-archivados').classList.add('hidden');
    });

    tabArchivados.addEventListener('click', async () => {
      tabArchivados.classList.add('active-tab');
      tabActivos.classList.remove('active-tab');
      document.getElementById('tab-panel-activos').classList.add('hidden');
      const archivadosPanel = document.getElementById('tab-panel-archivados');
      archivadosPanel.classList.remove('hidden');

      try {
        const res = await fetch(`/api/plantas/${plant.idPlanta}/archivados`);
        const data = await res.json();

        archivadosPanel.innerHTML = `
          <div class="mb-4">
            <h5 class="font-semibold">Zonas Archivadas</h5>
            ${renderItems(data.zonas, 'zona', false) || '<p class="text-sm text-gray-400">No hay zonas archivadas</p>'}
            <h5 class="font-semibold mt-4">Saberes Archivados</h5>
            ${renderItems(data.saberes, 'saber', false) || '<p class="text-sm text-gray-400">No hay saberes archivados</p>'}
            <h5 class="font-semibold mt-4">Usos Archivados</h5>
            ${renderItems(data.usos, 'uso', false) || '<p class="text-sm text-gray-400">No hay usos archivados</p>'}
          </div>
        `;
      } catch (err) {
        archivadosPanel.innerHTML = '<p class="text-red-500">Error al cargar archivados.</p>';
      }
    });
  }

  confirm3.addEventListener('click', () => {
    const expected = requiredPhrase.textContent.trim();
    const typed = inputPhrase.value.trim();
    if (typed !== expected) {
      errorPhrase.classList.remove('hidden');
      return;
    }
    errorPhrase.classList.add('hidden');
    toggleModal(modal3, false);
    itemNameSpan.textContent = currentArchive.name;
    inputReason.value = '';
    toggleModal(modal1, true);
  });

  cancel1.addEventListener('click', () => toggleModal(modal1, false));
  cancel2.addEventListener('click', () => toggleModal(modal2, false));
  cancel3.addEventListener('click', () => toggleModal(modal3, false));

  confirm1.addEventListener('click', () => {
    toggleModal(modal1, false);
    toggleModal(modal2, true);
  });

  confirm2.addEventListener('click', async () => {
    const motivo = inputReason.value.trim();
    toggleModal(modal2, false);

    let endpoint = '';
    switch (currentArchive.type) {
      case 'zona': endpoint = `/api/archive_zona/${currentArchive.id}`; break;
      case 'saber': endpoint = `/api/archive_saber/${currentArchive.id}`; break;
      case 'uso': endpoint = `/api/archive_uso/${currentArchive.id}`; break;
      case 'planta': endpoint = `/api/archive_plant/${currentArchive.id}`; break;
    }

    try {
      await fetch(endpoint, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ motivo })
      });
      if (currentArchive.type === 'planta') {
        detailsContainer.innerHTML = `
          <p id="placeholder-message" class="text-gray-500 text-center py-10">
            Seleccione una planta activa para ver sus detalles y opciones de archivación.
          </p>
        `;
        selectedPlant = null;
        searchInput.value = "";
        fetchPlantasActivas();
      } else {
        const archivedElement = document.querySelector(
          `[data-type="${currentArchive.type}"][data-id="${currentArchive.id}"]`
        );
        if (archivedElement && archivedElement.closest('.detail-item')) {
          archivedElement.closest('.detail-item').remove();
        }
      }
    } catch (err) {
      console.error('Error al archivar:', err);
    }
  });

  fetchPlantasActivas();
});
