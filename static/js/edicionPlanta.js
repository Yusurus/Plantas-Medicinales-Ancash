// edicion_planta.js
document.addEventListener('DOMContentLoaded', () => {
    // Comprobación inicial de si estamos en modo edición
    if (window.idPlantaParaEditar && window.datosPlantaDesdeServidor) {
        console.log('DEBUG: Modo edición detectado. idPlantaParaEditar:', window.idPlantaParaEditar);
        const planta = window.datosPlantaDesdeServidor;
        console.log('DEBUG: Datos de la planta recibidos para editar (window.datosPlantaDesdeServidor):', planta);

        const nombreCientificoInput = document.getElementById('nombreCientifico');
        const familiaSelect = document.getElementById('nomFamilia');
        const descMorfologicaInput = document.getElementById('descMorfologica'); 

        // --- Rellenar Nombre Científico ---
        console.log('DEBUG: Intentando rellenar Nombre Científico.');
        if (nombreCientificoInput) {
            nombreCientificoInput.value = planta.nombreCientifico || '';
            console.log('DEBUG: Nombre Científico establecido a:', nombreCientificoInput.value);
        } else {
            console.error('ERROR: Elemento con ID "nombreCientifico" no encontrado.');
        }

        // --- Rellenar Familia ---
        console.log('DEBUG: Intentando rellenar Familia.');
        if (familiaSelect) {
            console.log('DEBUG: Elemento familiaSelect encontrado.');
            // ¡CAMBIO AQUÍ! Usar 'nomFamilia' en lugar de 'fk_familiasplantas'
            console.log('DEBUG: Valor de familia en la planta (planta.nomFamilia):', planta.nomFamilia);
            
            // Loguea todas las opciones disponibles en el select para comparación
            console.log('DEBUG: Opciones disponibles en el select de Familia:');
            Array.from(familiaSelect.options).forEach(option => {
                console.log(`  - Valor: "${option.value}", Texto: "${option.textContent}"`);
            });

            if (planta.nomFamilia) { // Usar nomFamilia
                familiaSelect.value = planta.nomFamilia; // Usar nomFamilia
                // Verifica si el valor fue realmente seleccionado
                if (familiaSelect.value === planta.nomFamilia) { // Usar nomFamilia
                    console.log('DEBUG: Familia seleccionada correctamente:', familiaSelect.value);
                } else {
                    console.warn('ADVERTENCIA: No se pudo seleccionar el valor de la familia:', planta.nomFamilia, 'en el select. Posiblemente no existe esa opción o hay un problema de mayúsculas/minúsculas/espacios.');
                }
            } else {
                console.log('DEBUG: planta.nomFamilia está vacío o es nulo.');
            }
        } else {
            console.error('ERROR: Elemento con ID "nomFamilia" no encontrado.');
        }

        // --- Rellenar Nombres Comunes ---
        console.log('DEBUG: Intentando rellenar Nombres Comunes.');
        // ¡CAMBIO AQUÍ! Usar 'nombres_comunes' en lugar de 'nombresComunes'
        console.log('DEBUG: Valor de nombres_comunes en la planta:', planta.nombres_comunes);

        if (typeof nombresComunes === 'undefined') {
            console.error('ERROR: La variable global "nombresComunes" no está definida. Asegúrate de que script.js se cargue antes que edicion_planta.js.');
        } else if (planta.nombres_comunes) { // Usar nombres_comunes
            console.log('DEBUG: "nombresComunes" está definido y "planta.nombres_comunes" tiene valor.');
            nombresComunes.length = 0; // Limpiar el array global
            console.log('DEBUG: Array global "nombresComunes" limpiado.');

            const namesToSplit = typeof planta.nombres_comunes === 'string' ? planta.nombres_comunes : String(planta.nombres_comunes);
            
            // Usamos split(',') para ser más flexibles con el separador (sin espacio extra)
            namesToSplit.split(',').forEach(name => {
                const trimmedName = name.trim();
                if (trimmedName !== '') {
                    nombresComunes.push(trimmedName);
                    console.log('DEBUG: Nombre común añadido:', trimmedName);
                }
            });
            console.log('DEBUG: Array global "nombresComunes" después de llenar:', nombresComunes);

            if (typeof actualizarLista === 'function') {
                actualizarLista(); // Llamar a la función de script.js para actualizar la UI
                console.log('DEBUG: Se llamó a actualizarLista() para nombres comunes.');
            } else {
                console.error('ERROR: La función "actualizarLista()" no está definida. Asegúrate de que script.js se cargue antes que edicion_planta.js.');
            }
        } else {
            console.log('DEBUG: planta.nombres_comunes está vacío o es nulo. No se añadirán nombres comunes.');
        }

        // --- Rellenar Imágenes ---
        console.log('DEBUG: Intentando rellenar Imágenes.');
        // ¡CAMBIO AQUÍ! Usar 'Imagenes' en lugar de 'imagenes'
        console.log('DEBUG: Valor de Imagenes en la planta:', planta.Imagenes);

        if (typeof imagenes === 'undefined') {
            console.error('ERROR: La variable global "imagenes" no está definida. Asegúrate de que script.js se cargue antes que edicion_planta.js.');
        } else if (planta.Imagenes) { // Usar Imagenes
            console.log('DEBUG: "imagenes" está definido y "planta.Imagenes" tiene valor.');
            imagenes.length = 0; // Limpiar el array global
            console.log('DEBUG: Array global "imagenes" limpiado.');

            const urlsToSplit = typeof planta.Imagenes === 'string' ? planta.Imagenes : String(planta.Imagenes);

            // Usamos split(',') para ser más flexibles con el separador (sin espacio extra)
            urlsToSplit.split(',').forEach(url => {
                const trimmedUrl = url.trim();
                if (trimmedUrl !== '') {
                    imagenes.push(trimmedUrl);
                    console.log('DEBUG: URL de imagen añadida:', trimmedUrl);
                }
            });
            console.log('DEBUG: Array global "imagenes" después de llenar:', imagenes);

            if (typeof actualizarGaleria === 'function') {
                actualizarGaleria(); // Llamar a la función de script.js para actualizar la UI
                console.log('DEBUG: Se llamó a actualizarGaleria() para imágenes.');
            } else {
                console.error('ERROR: La función "actualizarGaleria()" no está definida. Asegúrate de que script.js se cargue antes que edicion_planta.js.');
            }
        } else {
            console.log('DEBUG: planta.Imagenes está vacío o es nulo. No se añadirán imágenes.');
        }

        // --- Rellenar Descripción Morfológica ---
        console.log('DEBUG: Intentando rellenar Descripción Morfológica.');
        // ¡Este ya estaba correcto! Solo confirmamos que la clave es 'descMorfologica'
        if (descMorfologicaInput) {
            descMorfologicaInput.value = planta.descMorfologica || '';
            console.log('DEBUG: Descripción Morfológica establecida a:', descMorfologicaInput.value);
        } else {
            console.error('ERROR: Elemento con ID "descMorfologica" no encontrado.');
        }
    } else {
        console.log('DEBUG: No estamos en modo edición o no hay datos de planta inyectados.');
    }
});