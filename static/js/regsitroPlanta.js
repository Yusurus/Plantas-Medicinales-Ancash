const imagenes = [];

    function agregarImagen() {
      const input = document.getElementById('imagen');
      const url = input.value.trim();

      // Validar que sea una URL de imagen
      if (!url.match(/\.(jpeg|jpg|png|gif|webp)$/i)) {
        alert('La URL no es una imagen válida.');
        return;
      }

      // Comprobar si se carga la imagen
      const img = new Image();
      img.onload = function () {
        // Evitar duplicados
        if (imagenes.includes(url)) {
          alert('La imagen ya fue añadida.');
          return;
        }

        imagenes.push(url);
        actualizarGaleria();
        input.value = '';
        input.focus();
      };
      img.onerror = function () {
        alert('No se pudo cargar la imagen desde la URL proporcionada.');
      };
      img.src = url;
    }

    function actualizarGaleria() {
      const contenedor = document.getElementById('contenedorImagenes');
      contenedor.innerHTML = '';

      imagenes.forEach((url, index) => {
        const div = document.createElement('div');
        div.style.position = 'relative';

        const img = document.createElement('img');
        img.src = url;
        img.style.width = '100px';
        img.style.height = '100px';
        img.style.objectFit = 'cover';
        img.style.border = '1px solid #ccc';
        img.classList.add('rounded');

        const btn = document.createElement('button');
        btn.textContent = '×';
        btn.type = 'button';
        btn.style.position = 'absolute';
        btn.style.top = '2px';
        btn.style.right = '2px';
        btn.className = 'btn btn-sm btn-danger';
        btn.onclick = () => {
          imagenes.splice(index, 1);
          actualizarGaleria();
        };

        div.appendChild(img);
        div.appendChild(btn);
        contenedor.appendChild(div);
      });

      // Guardar en campo oculto separado por comas
      document.getElementById('imagenesInput').value = imagenes.join(', ');
    }

//--------------------------------------------------------------------------------
const input = document.getElementById('imagen');
    const preview = document.getElementById('preview');

    input.addEventListener('input', () => {
      const url = input.value.trim();

      // Validar que la URL termine en una extensión de imagen
      if (url.match(/\.(jpeg|jpg|gif|png|webp)$/i)) {
        // Probar si la imagen se carga correctamente
        const img = new Image();
        img.onload = function () {
          preview.src = url;
          preview.style.display = 'block';
        };
        img.onerror = function () {
          preview.style.display = 'none';
        };
        img.src = url;
      } else {
        preview.style.display = 'none';
      }
    });

//--------------------------------------------------------------------------------

const nombresComunes = [];

    function agregarNombreComun() {
      const input = document.getElementById('nombreComunInput');
      const nombre = input.value.trim();
      if (nombre !== '') {
        nombresComunes.push(nombre);
        actualizarLista();
        input.value = '';
        input.focus();
      }
    }

    function actualizarLista() {
      const lista = document.getElementById('listaNombresComunes');
      lista.innerHTML = '';
      nombresComunes.forEach((nombre, index) => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.textContent = nombre;

        const btn = document.createElement('button');
        btn.className = 'btn btn-sm btn-danger';
        btn.textContent = 'Eliminar';
        btn.onclick = () => {
          nombresComunes.splice(index, 1);
          actualizarLista();
        };

        li.appendChild(btn);
        lista.appendChild(li);
      });

      document.getElementById('nombresComunesInput').value = nombresComunes.join(', ');
    }

    // Validación de formulario con Bootstrap
    (() => {
      'use strict'
      const form = document.getElementById('plantaForm');
      form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
        // Asegurar el campo oculto esté actualizado
        document.getElementById('nombresComunesInput').value = nombresComunes.join(', ');
        document.getElementById('imagenesInput').value = imagenes.join(', ');

      }, false);
    })();


    // Buscar nombre científico en PlantNet
    const buscarPlantnetBtn = document.getElementById('buscarPlantnetBtn');
    const nombreCientificoInput = document.getElementById('nombreCientifico');
    const loadingPlantnet = document.getElementById('loadingPlantnet');
    const errorPlantnet = document.getElementById('errorPlantnet');

    buscarPlantnetBtn.addEventListener('click', async () => {
      const scientificName = nombreCientificoInput.value.trim();

      if (!scientificName) {
        alert('Por favor, ingrese un nombre científico para buscar en PlantNet.');
        return;
      }

      loadingPlantnet.classList.remove('d-none');
      errorPlantnet.classList.add('d-none');
      errorPlantnet.textContent = '';

      try {
        const encodedScientificName = encodeURIComponent(scientificName);
        const response = await fetch(`/buscar_nombre?scientific_name=${encodedScientificName}`);
        const data = await response.json();
        console.log("Datos recibidos de PlantNet:", data);


        if (!response.ok) {
          throw new Error(data.message || 'Error desconocido al buscar en PlantNet.');
        }

        if (data.family) {
          const familiaSelect = document.getElementById('nomFamilia');
          let foundFamily = false;

          for (let i = 0; i < familiaSelect.options.length; i++) {
            if (familiaSelect.options[i].value === data.family) {
              familiaSelect.value = data.family;
              foundFamily = true;
              break;
            }
          }

          if (!foundFamily) {
            console.log(">> No se encontró la familia, registrando: ", data.family); // ✅ Confirmación en consola

            fetch('/registrar_familia', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ nombreFamilia: data.family })
            })
              .then(response => response.json())
              .then(result => {
                console.log(">> Resultado del registro:", result); // ✅ Ver si la respuesta vino bien

                if (result.success) {
                  const option = document.createElement('option');
                  option.value = data.family;
                  option.textContent = data.family;
                  familiaSelect.appendChild(option);
                  familiaSelect.value = data.family;
                } else {
                  alert('No se pudo registrar la familia: ' + result.message);
                }
              })
              .catch(error => {
                console.error('Error registrando la familia:', error); // ✅ Ver errores de red u otros
              });
          }
        }

        nombresComunes.length = 0;
        if (data.commonNames && data.commonNames.length > 0) {
          data.commonNames.forEach(name => nombresComunes.push(name));
        }
        actualizarLista();

        imagenes.length = 0;
        if (data.imageUrls && data.imageUrls.length > 0) {
          data.imageUrls.forEach(url => imagenes.push(url));
        }
        actualizarGaleria();

      } catch (error) {
        errorPlantnet.textContent = error.message;
        errorPlantnet.classList.remove('d-none');
      } finally {
        loadingPlantnet.classList.add('d-none');
      }
    });

    // Pre-llenar campos si hay datos en sessionStorage
    document.addEventListener('DOMContentLoaded', () => {
      const plantDataString = sessionStorage.getItem('plantDataToRegister');
      const isFromIdentifier = sessionStorage.getItem('isFromIdentifier');

      if (plantDataString && isFromIdentifier === 'true') {
        try {
          const plantData = JSON.parse(plantDataString);

          const nombreCientificoInput = document.getElementById('nombreCientifico');
          console.log(plantData);
          if (nombreCientificoInput) {
            nombreCientificoInput.value = plantData.scientificName || '';
            nombreCientificoInput.classList.add('is-valid');
          }
          /// buscarPlantnetBtn.click();
          /*const nomFamiliaSelect = document.getElementById('nomFamilia');
          if (nomFamiliaSelect && plantData.family) {
            for (let i = 0; i < nomFamiliaSelect.options.length; i++) {
              if (nomFamiliaSelect.options[i].value === plantData.family) {
                nomFamiliaSelect.value = plantData.family;
                break;
              }
            }
          }*/
          if (plantData.family) {
            const familiaSelect = document.getElementById('nomFamilia');
            let foundFamily = false;

            for (let i = 0; i < familiaSelect.options.length; i++) {
              if (familiaSelect.options[i].value === plantData.family) {
                familiaSelect.value = plantData.family;
                foundFamily = true;
                break;
              }
            }

            if (!foundFamily) {
              console.log(">> No se encontró la familia, registrando: ", plantData.family); // ✅ Confirmación en consola

              fetch('/registrar_familia', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nombreFamilia: plantData.family })
              })
                .then(response => response.json())
                .then(result => {
                  console.log(">> Resultado del registro:", result); // ✅ Ver si la respuesta vino bien

                  if (result.success) {
                    const option = document.createElement('option');
                    option.value = plantData.family;
                    option.textContent = plantData.family;
                    familiaSelect.appendChild(option);
                    familiaSelect.value = plantData.family;
                  } else {
                    alert('No se pudo registrar la familia: ' + result.message);
                  }
                })
                .catch(error => {
                  console.error('Error registrando la familia:', error); // ✅ Ver errores de red u otros
                });
            }
          }
          if (plantData.commonNames) {
            nombresComunes.length = 0;
            plantData.commonNames.split(', ').forEach(name => {
              if (name.trim() !== '') {
                nombresComunes.push(name.trim());
              }
            });
            actualizarLista();
          }

          if (plantData.imageUrls) {
            imagenes.length = 0;
            plantData.imageUrls.split(', ').forEach(url => {
              if (url.trim() !== '') {
                imagenes.push(url.trim());
              }
            });
            actualizarGaleria();
          }
        } catch (e) {
          console.error("Error al parsear o pre-llenar datos de planta desde sessionStorage:", e);
        }
      }
      sessionStorage.removeItem('plantDataToRegister');
      sessionStorage.removeItem('isFromIdentifier');
    });