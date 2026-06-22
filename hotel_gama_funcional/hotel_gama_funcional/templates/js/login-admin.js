function loginAdmin(event){
    event.preventDefault();

    let correo = document.getElementById("correo").value;
    let password = document.getElementById("password").value;

    if(correo === "admin@gmail.com" && password === "rosas"){
        window.location.href = "admin.html";
    }else{
        alert("Correo o contraseña incorrectos");
    }
}