let imagenSeleccionada = null;

function agregarImagen() {
    const url = document.getElementById("urlImagen").value.trim();
    const galeria = document.getElementById("galeria");

    if (url === "") {
        alert("Ingrese una URL de imagen");
        return;
    }

    // Quitar mensaje inicial
    const mensaje = document.querySelector(".mensaje");
    if (mensaje) {
        mensaje.remove();
    }

    const img = document.createElement("img");
    img.src = url;

    // Click para seleccionar imagen
    img.addEventListener("click", function () {
        seleccionarImagen(img);
    });

    // Error si la imagen no carga
    img.onerror = function () {
        alert("No se pudo cargar la imagen. Use una URL directa (.jpg, .png)");
        img.remove();
    };

    galeria.appendChild(img);
    document.getElementById("urlImagen").value = "";
}

function seleccionarImagen(img) {
    const imagenes = document.querySelectorAll("#galeria img");

    imagenes.forEach(i => i.classList.remove("seleccionada"));

    img.classList.add("seleccionada");
    imagenSeleccionada = img;
}

function eliminarImagen() {
    if (imagenSeleccionada) {
        imagenSeleccionada.remove();
        imagenSeleccionada = null;
    } else {
        alert("Seleccione una imagen primero");
    }
}
