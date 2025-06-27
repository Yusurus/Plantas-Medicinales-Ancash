document.addEventListener('DOMContentLoaded', () => {
    if (window.idPlantaParaEditar && window.datosPlantaDesdeServidor) {
        const planta = window.datosPlantaDesdeServidor;

        const nombreCientificoInput = document.getElementById('nombreCientifico');
        const familiaSelect = document.getElementById('nomFamilia');
        const descMorfologicaInput = document.getElementById('descMorfologica'); 

        if (nombreCientificoInput) {
            nombreCientificoInput.value = planta.nombreCientifico || '';
        }

        if (familiaSelect && planta.nomFamilia) {
            familiaSelect.value = planta.nomFamilia;
        }

        if (typeof nombresComunes !== 'undefined' && planta.nombres_comunes) {
            nombresComunes.length = 0;
            planta.nombres_comunes.split(',').forEach(name => {
                const trimmedName = name.trim();
                if (trimmedName !== '') {
                    nombresComunes.push(trimmedName);
                }
            });

            if (typeof actualizarLista === 'function') {
                actualizarLista();
            }
        }

        if (typeof imagenes !== 'undefined' && planta.Imagenes) {
            imagenes.length = 0;
            planta.Imagenes.split(',').forEach(url => {
                const trimmedUrl = url.trim();
                if (trimmedUrl !== '') {
                    imagenes.push(trimmedUrl);
                }
            });

            if (typeof actualizarGaleria === 'function') {
                actualizarGaleria();
            }
        }

        if (descMorfologicaInput) {
            descMorfologicaInput.value = planta.descMorfologica || '';
        }
    }
});
