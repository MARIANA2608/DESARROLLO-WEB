// ===== ALERTA PERSONALIZADA =====
document.getElementById("btnAlerta").addEventListener("click", function () {
    alert("¡Gracias por visitar esta página interactiva hecha con Bootstrap y JavaScript!");
});

// ===== VALIDACIÓN DEL FORMULARIO =====
document.getElementById("formContacto").addEventListener("submit", function (e) {
    e.preventDefault();

    let nombre = document.getElementById("nombre").value.trim();
    let correo = document.getElementById("correo").value.trim();
    let mensaje = document.getElementById("mensaje").value.trim();

    let valido = true;

    // Limpiar errores
    document.getElementById("errorNombre").textContent = "";
    document.getElementById("errorCorreo").textContent = "";
    document.getElementById("errorMensaje").textContent = "";

    if (nombre === "") {
        document.getElementById("errorNombre").textContent = "El nombre es obligatorio.";
        valido = false;
    }

    if (correo === "") {
        document.getElementById("errorCorreo").textContent = "El correo es obligatorio.";
        valido = false;
    }

    if (mensaje === "") {
        document.getElementById("errorMensaje").textContent = "El mensaje no puede estar vacío.";
        valido = false;
    }

    if (valido) {
        alert("Formulario enviado correctamente. ¡Gracias por contactarnos!");
        this.reset();
    }
});
