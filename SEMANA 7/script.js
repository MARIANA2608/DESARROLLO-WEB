// Arreglo inicial de productos
const productos = [
    {
        nombre: "Botella reutilizable",
        precio: 8.50,
        descripcion: "Ideal para reducir el uso de plástico."
    },
    {
        nombre: "Bolsa ecológica",
        precio: 3.00,
        descripcion: "Reutilizable y resistente para compras."
    },
    {
        nombre: "Cepillo de bambú",
        precio: 2.75,
        descripcion: "Alternativa sostenible para el cuidado personal."
    }
];

// Referencia al elemento <ul>
const lista = document.getElementById("listaProductos");

// Función que renderiza los productos en la lista
function mostrarProductos() {
    // Limpia la lista antes de volver a cargarla
    lista.innerHTML = "";

    productos.forEach(producto => {
        const item = document.createElement("li");

        item.textContent = `${producto.nombre} - $${producto.precio} | ${producto.descripcion}`;

        lista.appendChild(item);
    });
}

// Evento que se ejecuta al cargar la página
document.addEventListener("DOMContentLoaded", mostrarProductos);

// Botón para agregar un nuevo producto
const botonAgregar = document.getElementById("btnAgregar");

botonAgregar.addEventListener("click", () => {
    const nuevoProducto = {
        nombre: "Producto nuevo",
        precio: 1.99,
        descripcion: "Este producto fue agregado dinámicamente."
    };

    productos.push(nuevoProducto);
    mostrarProductos();
});
