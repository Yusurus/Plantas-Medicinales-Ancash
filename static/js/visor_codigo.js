// Sistema de gestión de archivos para Flask
class FileSystemManager {
    constructor() {
        this.currentPath = '.';
        this.selectedFile = null;
        this.currentFileContent = null;
        this.treeData = null;
        this.treeContainer = document.getElementById('treeContainer');
        this.contentBody = document.getElementById('contentBody');
        this.contentHeader = document.getElementById('contentHeader');
        this.functionsList = document.getElementById('functionsList');
        this.treeSearch = document.getElementById('treeSearch');
        this.functionsSearch = document.getElementById('functionsSearch');
        
        this.init();
    }
    
    init() {
        this.loadFileTree();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Búsqueda en el árbol de archivos
        this.treeSearch.addEventListener('input', (e) => {
            this.filterTree(e.target.value);
        });
        
        // Búsqueda en funciones
        this.functionsSearch.addEventListener('input', (e) => {
            this.filterFunctions(e.target.value);
        });
    }
    
    async loadFileTree(path = '.') {
        try {
            this.showLoading(this.treeContainer);
            
            const response = await fetch(`/api/tree?path=${encodeURIComponent(path)}`);
            const data = await response.json();
            
            if (data.error) {
                this.showError(this.treeContainer, data.error);
                return;
            }
            
            // Guardar los datos del árbol
            this.treeData = data;
            console.log('Datos del árbol cargados:', this.treeData);
            
            this.renderTree(data);

            // Expandir automáticamente la carpeta raíz y cargar README
            setTimeout(() => {
                this.expandRootFolder();
                this.autoLoadReadme();
            }, 100); // Reducir el timeout
            
        } catch (error) {
            this.showError(this.treeContainer, 'Error al cargar el árbol de archivos');
            console.error('Error:', error);
        }
    }

    // Función mejorada para expandir la carpeta raíz
    expandRootFolder() {
        console.log('Intentando expandir carpeta raíz...');
        
        // Buscar el primer directorio en el árbol
        const rootDirectory = document.querySelector('.tree-item .tree-node.directory');
        if (rootDirectory) {
            console.log('Carpeta raíz encontrada:', rootDirectory);
            rootDirectory.click();
            console.log('Carpeta raíz expandida automáticamente');
        } else {
            console.log('No se encontró carpeta raíz para expandir');
        }
    }

    // Función mejorada para buscar README.md en los datos del árbol
    findReadmeInTree(node, currentPath = '') {
        console.log('Buscando README en nodo:', node);
        
        if (!node) return null;
        
        // Si es un array (raíz del árbol), buscar en cada elemento
        if (Array.isArray(node)) {
            console.log('Procesando array de nodos, cantidad:', node.length);
            for (const child of node) {
                const result = this.findReadmeInTree(child, currentPath);
                if (result) return result;
            }
            return null;
        }
        
        // Si es un archivo, verificar si es README
        if (node.type === 'file') {
            const fileName = node.name.toLowerCase();
            console.log('Verificando archivo:', fileName);
            
            if (fileName === 'readme.md' || 
                fileName === 'readme.markdown' || 
                fileName === 'readme.txt' ||
                fileName === 'readme.rst' ||
                fileName === 'readme') {
                console.log('README encontrado:', node.path);
                return node.path;
            }
        }
        
        // Si es un directorio, buscar en sus hijos
        if (node.type === 'directory' && node.children && node.children.length > 0) {
            console.log('Procesando directorio:', node.name, 'con', node.children.length, 'hijos');
            for (const child of node.children) {
                const result = this.findReadmeInTree(child, node.path);
                if (result) return result;
            }
        }
        
        return null;
    }

    // Función mejorada para cargar README automáticamente
    async autoLoadReadme() {
        console.log('Iniciando búsqueda automática de README...');
        console.log('Datos del árbol disponibles:', this.treeData);
        
        if (!this.treeData) {
            console.log('No hay datos del árbol disponibles para buscar README');
            return;
        }
        
        // Buscar README.md en el árbol
        const readmePath = this.findReadmeInTree(this.treeData);
        
        if (readmePath) {
            console.log('README encontrado en path:', readmePath);
            
            // Intentar múltiples estrategias para encontrar y hacer clic en el elemento
            this.loadReadmeFile(readmePath);
        } else {
            console.log('No se encontró README en el proyecto');
            // Mostrar mensaje de bienvenida por defecto
            this.showWelcomeMessage();
        }
    }

    // Nueva función para cargar el archivo README
    async loadReadmeFile(readmePath) {
        console.log('Cargando README desde:', readmePath);
        
        try {
            // Estrategia 1: Buscar el elemento en el DOM y hacer clic
            const readmeElement = document.querySelector(`[data-path="${readmePath}"]`);
            if (readmeElement) {
                console.log('Elemento README encontrado en DOM, haciendo clic...');
                readmeElement.click();
                return;
            }
            
            // Estrategia 2: Cargar directamente usando la API
            console.log('Elemento no encontrado en DOM, cargando directamente...');
            
            // Extraer información del archivo
            const fileName = readmePath.split('/').pop();
            const extension = '.' + fileName.split('.').pop();
            
            // Cargar el archivo directamente
            await this.selectFile(readmePath, fileName, extension);
            
            // Buscar y marcar el elemento como seleccionado si existe
            setTimeout(() => {
                const readmeElement = document.querySelector(`[data-path="${readmePath}"]`);
                if (readmeElement) {
                    this.highlightSelectedFile(readmeElement);
                }
            }, 200);
            
            console.log('README cargado exitosamente');
            
        } catch (error) {
            console.error('Error al cargar README automáticamente:', error);
            this.showWelcomeMessage();
        }
    }

    // Función para mostrar mensaje de bienvenida
    showWelcomeMessage() {
        this.contentHeader.innerHTML = `
            <i class="bi bi-house-fill me-2"></i>Bienvenido al explorador de archivos
        `;
        
        this.contentBody.innerHTML = `
            <div class="welcome-message text-center py-5">
                <i class="bi bi-folder2-open display-4 text-white mb-3"></i>
                <h3 class="text-white">Explorador de Archivos</h3>
                <p class="text-white">Selecciona un archivo del árbol de navegación para ver su contenido</p>
                <small class="text-white">
                    <i class="bi bi-info-circle me-1"></i>
                    Los archivos README.md se cargan automáticamente si están disponibles
                </small>
            </div>
        `;
        
        this.functionsList.innerHTML = `
            <div class="welcome-message">
                <p><i class="bi bi-info-circle text-info me-2"></i>Las funciones aparecerán aquí cuando selecciones un archivo de código</p>
            </div>
        `;
    }
    
    renderTree(node, container = this.treeContainer) {
        if (container === this.treeContainer) {
            container.innerHTML = '';
        }
        
        const element = this.createTreeElement(node);
        container.appendChild(element);
    }
    
    createTreeElement(node) {
        const div = document.createElement('div');
        div.className = 'tree-item';
        
        if (node.type === 'directory') {
            div.innerHTML = `
                <div class="tree-node directory" data-path="${node.path}">
                    <i class="bi bi-folder-fill text-success me-2"></i>
                    <span>${node.name}</span>
                    <i class="bi bi-chevron-right ms-auto toggle-icon"></i>
                </div>
                <div class="tree-children" style="display: none;"></div>
            `;
            
            const nodeElement = div.querySelector('.tree-node');
            const childrenContainer = div.querySelector('.tree-children');
            const toggleIcon = div.querySelector('.toggle-icon');
            
            nodeElement.addEventListener('click', () => {
                const isExpanded = childrenContainer.style.display !== 'none';
                
                if (isExpanded) {
                    childrenContainer.style.display = 'none';
                    toggleIcon.className = 'bi bi-chevron-right ms-auto toggle-icon';
                } else {
                    childrenContainer.style.display = 'block';
                    toggleIcon.className = 'bi bi-chevron-down ms-auto toggle-icon';
                    
                    // Renderizar hijos si no se han renderizado
                    if (childrenContainer.children.length === 0 && node.children) {
                        node.children.forEach(child => {
                            const childElement = this.createTreeElement(child);
                            childrenContainer.appendChild(childElement);
                        });
                    }
                }
            });
        } else {
            const iconClass = this.getFileIcon(node.extension);
            div.innerHTML = `
                <div class="tree-node file" data-path="${node.path}" data-extension="${node.extension}">
                    <i class="${iconClass} me-2"></i>
                    <span>${node.name}</span>
                </div>
            `;
            
            const nodeElement = div.querySelector('.tree-node');
            nodeElement.addEventListener('click', () => {
                this.selectFile(node.path, node.name, node.extension);
                this.highlightSelectedFile(nodeElement);
            });
        }
        
        return div;
    }
    
    getFileIcon(extension) {
        const icons = {
            '.py': 'bi bi-file-code-fill text-primary',
            '.css': 'bi bi-file-code-fill text-info',
            '.js': 'bi bi-file-code-fill text-warning',
            '.html': 'bi bi-file-code-fill text-danger',
            '.htm': 'bi bi-file-code-fill text-info',
            '.md': 'bi bi-file-text-fill text-primary',
            '.markdown': 'bi bi-file-text-fill text-primary',
            '.txt': 'bi bi-file-text-fill text-secondary',
            '.rst': 'bi bi-file-text-fill text-info'
        };
        
        return icons[extension] || 'bi bi-file-fill';
    }
    
    highlightSelectedFile(element) {
        // Remover selección anterior
        document.querySelectorAll('.tree-node.selected').forEach(node => {
            node.classList.remove('selected');
        });
        
        // Agregar selección actual
        element.classList.add('selected');
    }
    
    async selectFile(filePath, fileName, extension) {
        console.log('Seleccionando archivo:', filePath);
        
        this.selectedFile = { path: filePath, name: fileName, extension: extension };
        
        // Actualizar header
        this.contentHeader.innerHTML = `
            <i class="${this.getFileIcon(extension)} me-2"></i>${fileName}
        `;
        
        // Cargar contenido del archivo
        await this.loadFileContent(filePath);
        
        // Cargar funciones del archivo (solo para archivos de código)
        if (this.isCodeFile(extension)) {
            await this.loadFileFunctions(filePath);
        } else {
            this.functionsList.innerHTML = `
                <div class="welcome-message">
                    <p><i class="bi bi-info-circle text-info me-2"></i>Este tipo de archivo no contiene funciones analizables</p>
                </div>
            `;
        }
    }
    
    // Nueva función para verificar si es un archivo de código
    isCodeFile(extension) {
        const codeExtensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go'];
        return codeExtensions.includes(extension);
    }
    
    async loadFileContent(filePath) {
        try {
            this.showLoading(this.contentBody);
            
            const response = await fetch(`/api/file/${encodeURIComponent(filePath)}`);
            const data = await response.json();
            
            if (data.error) {
                this.showError(this.contentBody, data.error);
                return;
            }
            
            this.currentFileContent = data;
            this.renderFileContent(data);
        } catch (error) {
            this.showError(this.contentBody, 'Error al cargar el contenido del archivo');
            console.error('Error:', error);
        }
    }
    
    renderFileContent(data) {
        if (data.type === 'markdown') {
            this.contentBody.innerHTML = `
                <div class="markdown-content">
                    ${data.content}
                </div>
            `;
        } else if (data.type === 'code') {
            // Mostrar el contenido resaltado que ya viene con números de línea
            this.contentBody.innerHTML = `
                <style>${data.css}</style>
                <div class="code-content">
                    ${data.content}
                </div>
            `;
        } else {
            // Para otros tipos de archivos, mostrar como texto plano
            this.contentBody.innerHTML = `
                <div class="text-content">
                    <pre><code>${data.content}</code></pre>
                </div>
            `;
        }
    }
    
    // Función mejorada para saltar a una línea específica
    jumpToLine(lineNumber) {
        console.log(`Intentando saltar a la línea: ${lineNumber}`);
        
        // Estrategia múltiple para encontrar la línea
        let targetLine = null;
        
        // Estrategia 1: Buscar por clase .lineno (Pygments estándar)
        const lineElements = document.querySelectorAll('.lineno');
        lineElements.forEach(lineEl => {
            if (parseInt(lineEl.textContent.trim()) === parseInt(lineNumber)) {
                targetLine = lineEl.closest('tr') || lineEl.parentElement;
                console.log('Línea encontrada con estrategia 1 (.lineno)');
            }
        });
        
        // Estrategia 2: Buscar por data-line-number
        if (!targetLine) {
            const dataLineElements = document.querySelectorAll('[data-line-number]');
            dataLineElements.forEach(lineEl => {
                if (parseInt(lineEl.getAttribute('data-line-number')) === parseInt(lineNumber)) {
                    targetLine = lineEl;
                    console.log('Línea encontrada con estrategia 2 (data-line-number)');
                }
            });
        }
        
        // Estrategia 3: Buscar por ID (algunas implementaciones usan line-X)
        if (!targetLine) {
            const lineById = document.getElementById(`line-${lineNumber}`);
            if (lineById) {
                targetLine = lineById;
                console.log('Línea encontrada con estrategia 3 (ID)');
            }
        }
        
        // Estrategia 4: Buscar en estructura de tabla (Pygments tabla)
        if (!targetLine) {
            const tableRows = document.querySelectorAll('.codehilite tr, .highlight tr, .code-content tr');
            tableRows.forEach((row, index) => {
                const lineNumCell = row.querySelector('td:first-child');
                if (lineNumCell && parseInt(lineNumCell.textContent.trim()) === parseInt(lineNumber)) {
                    targetLine = row;
                    console.log('Línea encontrada con estrategia 4 (tabla)');
                }
            });
        }
        
        // Estrategia 5: Buscar por posición aproximada (si no hay números de línea explícitos)
        if (!targetLine) {
            const codeLines = document.querySelectorAll('.code-content pre > code > span, .code-content pre > span, .codehilite pre > span');
            if (codeLines.length > 0 && lineNumber <= codeLines.length) {
                targetLine = codeLines[lineNumber - 1];
                console.log('Línea encontrada con estrategia 5 (posición aproximada)');
            }
        }
        
        // Estrategia 6: Buscar líneas en estructura simple
        if (!targetLine) {
            const allLines = document.querySelectorAll('.code-line, .line');
            if (allLines.length > 0 && lineNumber <= allLines.length) {
                targetLine = allLines[lineNumber - 1];
                console.log('Línea encontrada con estrategia 6 (líneas simples)');
            }
        }
        
        if (targetLine) {
            console.log('Línea objetivo encontrada:', targetLine);
            
            // Remover highlight anterior
            document.querySelectorAll('.highlighted-line').forEach(el => {
                el.classList.remove('highlighted-line');
            });
            
            // Aplicar highlight a la línea objetivo
            targetLine.classList.add('highlighted-line');
            
            // Scroll suave hacia la línea
            targetLine.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'nearest'
            });
            
            // Remover highlight después de 3 segundos
            setTimeout(() => {
                targetLine.classList.remove('highlighted-line');
            }, 3000);
            
            console.log(`Saltado exitosamente a la línea ${lineNumber}`);
        } else {
            console.warn(`No se pudo encontrar la línea ${lineNumber}`);
            
            // Fallback: mostrar mensaje de error temporal
            const errorMsg = document.createElement('div');
            errorMsg.className = 'alert alert-warning';
            errorMsg.style.position = 'fixed';
            errorMsg.style.top = '20px';
            errorMsg.style.right = '20px';
            errorMsg.style.zIndex = '9999';
            errorMsg.innerHTML = `
                <i class="bi bi-exclamation-triangle me-2"></i>
                No se pudo encontrar la línea ${lineNumber}
            `;
            
            document.body.appendChild(errorMsg);
            
            setTimeout(() => {
                errorMsg.remove();
            }, 3000);
        }
    }
    
    async loadFileFunctions(filePath) {
        try {
            const response = await fetch(`/api/functions/${encodeURIComponent(filePath)}`);
            const functions = await response.json();
            
            this.renderFunctions(functions);
        } catch (error) {
            this.showError(this.functionsList, 'Error al cargar las funciones');
            console.error('Error:', error);
        }
    }
    
    renderFunctions(functions) {
        if (!functions || functions.length === 0) {
            this.functionsList.innerHTML = `
                <div class="welcome-message">
                    <p><i class="bi bi-info-circle text-info me-2"></i>No se encontraron funciones en este archivo</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        functions.forEach(func => {
            if (func.error) {
                html += `
                    <div class="function-item error">
                        <i class="bi bi-exclamation-triangle text-danger me-2"></i>
                        <span>${func.error}</span>
                    </div>
                `;
                return;
            }
            
            const icon = this.getFunctionIcon(func.type);
            const privacy = func.is_private ? '<i class="bi bi-lock-fill text-muted ms-1" title="Privada"></i>' : '';
            
            if (func.type === 'class') {
                html += `
                    <div class="function-item class-item">
                        <div class="function-header" onclick="this.parentElement.classList.toggle('expanded')">
                            <i class="${icon} me-2"></i>
                            <span class="function-name">${func.name}</span>
                            ${privacy}
                            <button class="jump-to-line ms-auto me-2" onclick="event.stopPropagation(); window.fileSystemManager.jumpToLine(${func.line})" title="Ir a línea ${func.line}">
                                <i class="bi bi-arrow-up-right-circle"></i> L${func.line}
                            </button>
                            <i class="bi bi-chevron-down toggle-icon"></i>
                        </div>
                        ${func.docstring ? `<div class="function-doc">${func.docstring}</div>` : ''}
                        <div class="class-methods">
                            ${func.methods.map(method => `
                                <div class="method-item" onclick="window.fileSystemManager.jumpToLine(${method.line})">
                                    <i class="bi bi-arrow-return-right me-2"></i>
                                    <span class="method-name">${method.name}</span>
                                    <span class="method-params">(${method.params.join(', ')})</span>
                                    ${method.is_private ? '<i class="bi bi-lock-fill text-muted ms-1" title="Privado"></i>' : ''}
                                    <button class="jump-to-line ms-auto" onclick="event.stopPropagation(); window.fileSystemManager.jumpToLine(${method.line})" title="Ir a línea ${method.line}">
                                        <i class="bi bi-arrow-up-right-circle"></i> L${method.line}
                                    </button>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            } else {
                const params = func.params ? `(${func.params.join(', ')})` : '';
                html += `
                    <div class="function-item" onclick="window.fileSystemManager.jumpToLine(${func.line})">
                        <div style="display: flex; align-items: center;">
                            <i class="${icon} me-2"></i>
                            <span class="function-name">${func.name}</span>
                            <span class="function-params">${params}</span>
                            ${privacy}
                            <button class="jump-to-line ms-auto" onclick="event.stopPropagation(); window.fileSystemManager.jumpToLine(${func.line})" title="Ir a línea ${func.line}">
                                <i class="bi bi-arrow-up-right-circle"></i> L${func.line}
                            </button>
                        </div>
                        ${func.docstring ? `<div class="function-doc">${func.docstring}</div>` : ''}
                    </div>
                `;
            }
        });
        
        this.functionsList.innerHTML = html;
    }
    
    getFunctionIcon(type) {
        const icons = {
            'function': 'bi bi-gear-fill',
            'class': 'bi bi-box-fill',
            'javascript_function': 'bi bi-braces',
            'javascript_arrow_function': 'bi bi-arrow-right-circle'
        };
        
        return icons[type] || 'bi bi-code';
    }
    
    filterTree(query) {
        const treeItems = document.querySelectorAll('.tree-node');
        query = query.toLowerCase();
        
        treeItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            const matches = text.includes(query);
            
            item.style.display = matches || query === '' ? 'flex' : 'none';
            
            // Expandir padres si hay coincidencias
            if (matches && query !== '') {
                let parent = item.closest('.tree-children');
                while (parent) {
                    parent.style.display = 'block';
                    const toggleIcon = parent.previousElementSibling?.querySelector('.toggle-icon');
                    if (toggleIcon) {
                        toggleIcon.className = 'bi bi-chevron-down ms-auto toggle-icon';
                    }
                    parent = parent.parentElement.closest('.tree-children');
                }
            }
        });
    }
    
    filterFunctions(query) {
        const functionItems = document.querySelectorAll('.function-item');
        query = query.toLowerCase();
        
        functionItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            const matches = text.includes(query);
            item.style.display = matches || query === '' ? 'block' : 'none';
        });
    }
    
    showLoading(container) {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                Cargando...
            </div>
        `;
    }
    
    showError(container, message) {
        container.innerHTML = `
            <div class="error-message">
                <i class="bi bi-exclamation-triangle text-danger me-2"></i>
                ${message}
            </div>
        `;
    }
    
    // Método para configurar archivos a ignorar
    async configureIgnored(ignoredFiles = [], ignoredDirs = []) {
        try {
            const response = await fetch('/api/configure', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ignored_files: ignoredFiles,
                    ignored_dirs: ignoredDirs
                })
            });
            
            const result = await response.json();
            console.log('Configuración actualizada:', result);
            
            // Recargar el árbol
            this.loadFileTree();
        } catch (error) {
            console.error('Error al configurar archivos ignorados:', error);
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.fileSystemManager = new FileSystemManager();
});