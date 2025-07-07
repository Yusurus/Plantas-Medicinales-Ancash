class ArchivacionesApp {
    constructor() {
        this.currentArchiver = null;
        this.archivers = {};
        
        this.initElements();
        this.initEventListeners();
        this.initArchivers();
    }

    initElements() {
        this.sectionButtons = {
            plantas: document.getElementById('btnArchivarPlantas'),
            zonas: document.getElementById('btnArchivarZonas'),
            saberes: document.getElementById('btnArchivarSaberes'),
            usos: document.getElementById('btnArchivarUsos')
        };

        this.sections = {
            plantas: document.getElementById('plantasArchivingSection'),
            zonas: document.getElementById('zonasArchivingSection'),
            saberes: document.getElementById('saberesArchivingSection'),
            usos: document.getElementById('usosArchivingSection')
        };

        this.confirmationModal = document.getElementById('confirmationModal');
        this.closeButton = document.querySelector('.close-button');
        this.confirmArchiveBtn = document.getElementById('confirmArchiveBtn');
        this.cancelArchiveBtn = document.getElementById('cancelArchiveBtn');
        this.itemNameToArchiveSpan = document.getElementById('itemNameToArchive');
    }

    initEventListeners() {
        // Botones de selección de sección
        this.sectionButtons.plantas.addEventListener('click', () => this.showSection('plantas'));
        this.sectionButtons.zonas.addEventListener('click', () => this.showSection('zonas'));
        this.sectionButtons.saberes.addEventListener('click', () => this.showSection('saberes'));
        this.sectionButtons.usos.addEventListener('click', () => this.showSection('usos'));

        // Modal events
        this.closeButton.addEventListener('click', () => this.closeModal());
        this.cancelArchiveBtn.addEventListener('click', () => this.closeModal());
        this.confirmArchiveBtn.addEventListener('click', () => this.confirmArchive());

        // Cerrar modal al hacer clic fuera
        window.addEventListener('click', (event) => {
            if (event.target === this.confirmationModal) {
                this.closeModal();
            }
        });

        // Cerrar modal con Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.confirmationModal.style.display === 'flex') {
                this.closeModal();
            }
        });
    }

    initArchivers() {
        this.archivers = {
            plantas: new Archiver(
                'plantas',
                'plantas-activas-list',
                'plantas-archivadas-list',
                'plantasSearchInput',
                '/api/archive_plant',
                '/api/plantas_activas',
                '/api/plantas_archivadas',
                'nombreCientifico',
                [
                    { key: 'nomFamilia', label: 'Familia' },
                    { key: 'nombres_comunes', label: 'Nombres Comunes' },
                    { key: 'linkImagen', label: 'Imagen' }
                ],
                'idPlanta'
            ),
            zonas: new Archiver(
                'zonas',
                'zonas-activas-list',
                'zonas-archivadas-list',
                'zonasSearchInput',
                '/api/archive_zona',
                '/api/zonas_activas',
                '/api/zonas_archivadas',
                'ecoregion',
                [
                    { key: 'nombreProvincia', label: 'Provincia' },
                    { key: 'region', label: 'Región' }
                ],
                'idZona'
            ),
            saberes: new Archiver(
                'saberes',
                'saberes-activas-list',
                'saberes-archivadas-list',
                'saberesSearchInput',
                '/api/archive_saber',
                '/api/saberes_culturales_activos',
                '/api/saberes_culturales_archivados',
                'descripcionSaber',
                [
                    { key: 'nombreCientifico', label: 'Planta Asociada' }
                ],
                'idSaberesCulturales'
            ),
            usos: new Archiver(
                'usos',
                'usos-activas-list',
                'usos-archivadas-list',
                'usosSearchInput',
                '/api/archive_uso',
                '/api/usos_medicinales_activos',
                '/api/usos_medicinales_archivados',
                'uso',
                [
                    { key: 'parte', label: 'Parte Usada' },
                    { key: 'nombreCientifico', label: 'Planta Asociada' },
                    { key: 'preparacion', label: 'Preparación' }
                ],
                'idUsos'
            )
        };
    }

    async showSection(sectionType) {
        // Ocultar todas las secciones
        Object.values(this.sections).forEach(sec => sec.classList.add('hidden'));
        
        // Mostrar la sección seleccionada
        this.sections[sectionType].classList.remove('hidden');
        
        // Establecer el archiver actual
        this.currentArchiver = this.archivers[sectionType];
        
        // Cargar datos
        await this.currentArchiver.loadItems();
    }

    closeModal() {
        this.confirmationModal.style.display = 'none';
        if (this.currentArchiver) {
            this.currentArchiver.currentItemToArchive = null;
        }
    }

    async confirmArchive() {
        if (this.currentArchiver && this.currentArchiver.currentItemToArchive) {
            await this.currentArchiver.archiveItem();
            this.closeModal();
        }
    }
}

class Archiver {
    constructor(type, activeListId, archivedListId, searchInputId, archiveEndpoint, activeEndpoint, archivedEndpoint, itemNameKey, displayKeys, idKey) {
        this.type = type;
        this.activeListContainer = document.getElementById(activeListId);
        this.archivedListContainer = document.getElementById(archivedListId);
        this.searchInput = document.getElementById(searchInputId);
        this.archiveEndpoint = archiveEndpoint;
        this.activeEndpoint = activeEndpoint;
        this.archivedEndpoint = archivedEndpoint;
        this.itemNameKey = itemNameKey;
        this.displayKeys = displayKeys;
        this.idKey = idKey;
        this.currentItemToArchive = null;
        this.allActiveItems = [];
        this.allArchivedItems = [];
        this.motivoInput = document.getElementById('motivoArchivacion');

        if (this.searchInput) {
            this.searchInput.addEventListener('input', () => this.filterItems());
        }
    }

    async archiveItem() {
        if (!this.currentItemToArchive) return;

        try {
            const motivo = this.motivoInput?.value || 'Sin motivo especificado';

            const response = await fetch(`${this.archiveEndpoint}/${this.currentItemToArchive.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ motivo })
            });

            if (response.ok) {
                this.showSuccess(`${this.currentItemToArchive.name} ha sido archivado correctamente`);
                await this.loadItems();
                this.searchInput.value = '';
                this.motivoInput.value = '';
            } else {
                const error = await response.json();
                this.showError(error.error || 'Error al archivar el elemento');
            }
        } catch (error) {
            console.error('Error archivando elemento:', error);
            this.showError('Error de conexión');
        }
    }

    async loadItems() {
        try {
            // Mostrar loading
            this.showLoading(true);
            
            // Cargar elementos activos y archivados en paralelo
            const [activeResponse, archivedResponse] = await Promise.all([
                fetch(this.activeEndpoint),
                fetch(this.archivedEndpoint)
            ]);

            if (!activeResponse.ok || !archivedResponse.ok) {
                throw new Error('Error al cargar los datos');
            }

            this.allActiveItems = await activeResponse.json();
            this.allArchivedItems = await archivedResponse.json();

            // Renderizar elementos
            this.renderItemCards(this.allActiveItems, this.activeListContainer, 'active');
            this.renderItemCards(this.allArchivedItems, this.archivedListContainer, 'archived');

        } catch (error) {
            console.error('Error cargando elementos:', error);
            this.showError('Error al cargar los elementos');
        } finally {
            this.showLoading(false);
        }
    }

    showLoading(show) {
        const activeSpinner = this.activeListContainer.querySelector('.loading-spinner');
        const archivedSpinner = this.archivedListContainer.querySelector('.loading-spinner');
        
        if (activeSpinner) activeSpinner.style.display = show ? 'block' : 'none';
        if (archivedSpinner) archivedSpinner.style.display = show ? 'block' : 'none';
    }

    filterItems() {
        const searchTerm = this.searchInput.value.toLowerCase();

        const filteredActiveItems = this.allActiveItems.filter(item => {
            const nameMatch = item[this.itemNameKey] && item[this.itemNameKey].toLowerCase().includes(searchTerm);
            const fieldsMatch = this.displayKeys.some(keyInfo =>
                item[keyInfo.key] && String(item[keyInfo.key]).toLowerCase().includes(searchTerm)
            );
            return nameMatch || fieldsMatch;
        });

        const filteredArchivedItems = this.allArchivedItems.filter(item => {
            const nameMatch = item[this.itemNameKey] && item[this.itemNameKey].toLowerCase().includes(searchTerm);
            const fieldsMatch = this.displayKeys.some(keyInfo =>
                item[keyInfo.key] && String(item[keyInfo.key]).toLowerCase().includes(searchTerm)
            );
            return nameMatch || fieldsMatch;
        });

        this.renderItemCards(filteredActiveItems, this.activeListContainer, 'active');
        this.renderItemCards(filteredArchivedItems, this.archivedListContainer, 'archived');
    }

    renderItemCards(items, container, statusType) {
        // Limpiar contenedor pero mantener spinner
        const spinner = container.querySelector('.loading-spinner');
        container.innerHTML = '';
        if (spinner) container.appendChild(spinner);

        if (items.length === 0) {
            const emptyMessage = document.createElement('p');
            emptyMessage.textContent = `No hay ${this.type} ${statusType === 'active' ? 'activos' : 'archivados'} que coincidan con la búsqueda.`;
            emptyMessage.className = 'empty-message';
            container.appendChild(emptyMessage);
            return;
        }

        items.forEach(item => {
            const itemCard = document.createElement('div');
            itemCard.classList.add('item-card');
            itemCard.dataset.itemId = item[this.idKey];
            itemCard.dataset.itemName = item[this.itemNameKey];

            let cardContent = `<h5>${item[this.itemNameKey] || 'Sin nombre'}</h5>`;

            this.displayKeys.forEach(keyInfo => {
                if (item[keyInfo.key]) {
                    if (keyInfo.key === 'linkImagen') {
                        const imageUrl = item[keyInfo.key] || 'placeholder_image.jpg';
                        cardContent += `<img src="${imageUrl}" alt="${item[this.itemNameKey]}" style="width:100px; height:auto; margin-top: 10px; border-radius: 5px;">`;
                    } else {
                        cardContent += `<p><strong>${keyInfo.label}:</strong> ${item[keyInfo.key]}</p>`;
                    }
                }
            });

            itemCard.innerHTML = cardContent;

            // Solo elementos activos pueden ser archivados
            if (statusType === 'active') {
                itemCard.classList.add('clickable');
                itemCard.addEventListener('click', () => {
                    this.currentItemToArchive = {
                        id: item[this.idKey],
                        name: item[this.itemNameKey]
                    };
                    document.getElementById('itemNameToArchive').textContent = item[this.itemNameKey];
                    document.getElementById('confirmationModal').style.display = 'flex';
                });
            }

            container.appendChild(itemCard);
        });
    }

    async archiveItem() {
        if (!this.currentItemToArchive) return;

        try {
            const response = await fetch(`${this.archiveEndpoint}/${this.currentItemToArchive.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                this.showSuccess(`${this.currentItemToArchive.name} ha sido archivado correctamente`);
                // Recargar datos
                await this.loadItems();
                // Limpiar búsqueda
                this.searchInput.value = '';
            } else {
                const error = await response.json();
                this.showError(error.error || 'Error al archivar el elemento');
            }
        } catch (error) {
            console.error('Error archivando elemento:', error);
            this.showError('Error de conexión');
        }
    }

    showError(message) {
        alert('Error: ' + message);
    }

    showSuccess(message) {
        alert('Éxito: ' + message);
    }
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    new ArchivacionesApp();
});