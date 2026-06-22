let rol = "admin";

function cambiarRol(tipo) {

    rol = tipo;

    document.getElementById("btnAdmin")
        .classList.remove("active");

    document.getElementById("btnCliente")
        .classList.remove("active");

    if (tipo === "admin") {

        document.getElementById("btnAdmin")
            .classList.add("active");

        document.getElementById("camposCliente")
            .style.display = "none";

    } else {

        document.getElementById("btnCliente")
            .classList.add("active");

        document.getElementById("camposCliente")
            .style.display = "block";
    }
}

window.onload = function () {

    document.getElementById("camposCliente")
        .style.display = "none";
}

function login(event) {

    event.preventDefault();

    let correo =
        document.getElementById("correo").value;

    let password =
        document.getElementById("password").value;

    if (
        rol === "admin" &&
        correo === "admin@gmail.com" &&
        password === "rosas"
    ) {
        window.location.href = "admin.html";
        return;
    }

    if (
        rol === "cliente" &&
        correo === "cliente@gama.com" &&
        password === "123"
    ) {
        window.location.href = "cliente.html";
        return;
    }

    alert("Correo o contraseña incorrectos");
}
