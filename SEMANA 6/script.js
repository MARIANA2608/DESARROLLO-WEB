const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const password = document.getElementById("password");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");
const btnEnviar = document.getElementById("btnEnviar");

function validarFormulario() {
    let valido = true;

    // Nombre
    if (nombre.value.length < 3) {
        errorNombre.textContent = "Debe tener al menos 3 caracteres";
        nombre.className = "invalido";
        valido = false;
    } else {
        errorNombre.textContent = "";
        nombre.className = "valido";
    }

    // Correo
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexCorreo.test(correo.value)) {
        errorCorreo.textContent = "Correo no válido";
        correo.className = "invalido";
        valido = false;
    } else {
        errorCorreo.textContent = "";
        correo.className = "valido";
    }

    // Contraseña
    const regexPassword = /^(?=.*\d)(?=.*[\W_]).{8,}$/;
    if (!regexPassword.test(password.value)) {
        errorPassword.textContent = "Mínimo 8 caracteres, un número y un símbolo";
        password.className = "invalido";
        valido = false;
    } else {
        errorPassword.textContent = "";
        password.className = "valido";
    }

    // Confirmación
    if (password.value !== confirmar.value || confirmar.value === "") {
        errorConfirmar.textContent = "Las contraseñas no coinciden";
        confirmar.className = "invalido";
        valido = false;
    } else {
        errorConfirmar.textContent = "";
        confirmar.className = "valido";
    }

    // Edad
    if (edad.value < 18) {
        errorEdad.textContent = "Debe ser mayor o igual a 18 años";
        edad.className = "invalido";
        valido = false;
    } else {
        errorEdad.textContent = "";
        edad.className = "valido";
    }

    btnEnviar.disabled = !valido;
}

// Eventos en tiempo real
[nombre, correo, password, confirmar, edad].forEach(input => {
    input.addEventListener("input", validarFormulario);
});

// Envío
document.getElementById("formulario").addEventListener("submit", function(e) {
    e.preventDefault();
    alert("Formulario validado correctamente ✅");
});
