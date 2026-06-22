function mostrarSeccion(id, boton) {
    let secciones = document.querySelectorAll(".seccion");
    let botones = document.querySelectorAll(".tab");

    secciones.forEach(seccion => {
        seccion.classList.remove("activa");
    });

    botones.forEach(btn => {
        btn.classList.remove("active");
    });

    document.getElementById(id).classList.add("activa");
    boton.classList.add("active");
}

