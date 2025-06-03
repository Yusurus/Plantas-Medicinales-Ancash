const inputBusqueda = document.getElementById("inputBusqueda");
const tipoBusqueda = document.getElementById("tipoBusqueda");
const tarjetas = document.querySelectorAll(".planta");

inputBusqueda.addEventListener("input", filtrarPlantas);
tipoBusqueda.addEventListener("change", filtrarPlantas);

function filtrarPlantas() {
    const texto = inputBusqueda.value.toLowerCase().trim();
    const tipo = tipoBusqueda.value;

    tarjetas.forEach(card => {
        const nombreCientifico = card.dataset.nombrecientifico;
        const nombresComunes = card.dataset.nombres_comunes;
        const nomFamilia = card.dataset.nomfamilia;

        let visible = false;

        if (tipo === "todos") {
            visible = nombreCientifico.includes(texto) || nombresComunes.includes(texto) || nomFamilia.includes(texto);
        } else if (tipo === "nombreCientifico") {
            visible = nombreCientifico.includes(texto);
        } else if (tipo === "nombres_comunes") {
            visible = nombresComunes.includes(texto);
        } else if (tipo === "nomFamilia") {
            visible = nomFamilia.includes(texto);
        }

        card.style.display = visible ? "block" : "none";
    });
}
