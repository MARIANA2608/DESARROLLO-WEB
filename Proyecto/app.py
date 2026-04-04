from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
from datetime import datetime
import os

# Forms
from forms.login_form import LoginForm
from forms.registro_form import RegistroForm
from forms.producto_form import ProductoForm
from forms.categoria_form import CategoriaForm
from forms.cliente_form import ClienteForm
from forms.pedido_form import PedidoForm
from forms.detalle_pedido_form import DetallePedidoForm

# Services
from services.usuario_service import registrar_usuario, obtener_usuario_por_email, obtener_usuario_por_id
from services.producto_service import listar_productos, insertar_producto, eliminar_producto, actualizar_producto, obtener_producto_por_id
from services.categoria_service import listar_categorias, insertar_categoria, eliminar_categoria, actualizar_categoria, obtener_categoria_por_id
from services.cliente_service import listar_clientes, insertar_cliente, eliminar_cliente, actualizar_cliente, obtener_cliente_por_id
from services.pedido_service import listar_pedidos, insertar_pedido, eliminar_pedido, obtener_pedido_por_id, actualizar_total_pedido
from services.detalle_pedido_service import listar_detalle, agregar_producto_a_pedido, eliminar_detalle


app = Flask(__name__)

# Mejor que la clave se pueda leer desde variables de entorno
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave_segura_restaurante_2026")


# ============================================================
#                   LOGIN MANAGER
# ============================================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para ingresar al sistema."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


# ============================================================
#              FUNCIÓN AUXILIAR PARA PDF
# ============================================================
def texto_pdf_seguro(texto):
    """
    Esta función evita errores cuando existen caracteres especiales
    que FPDF no soporta correctamente con latin-1.
    """
    if texto is None:
        return ""
    return str(texto).encode("latin-1", "replace").decode("latin-1")


# ============================================================
#                    MANEJO DE ERRORES
# ============================================================
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template("errores/404.html"), 404


@app.errorhandler(403)
def acceso_denegado(e):
    return render_template("errores/403.html"), 403


# ============================================================
#                    INICIO
# ============================================================
@app.route("/")
def inicio():
    return render_template("index.html")


# ============================================================
#                    REGISTRO
# ============================================================
@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        usuario_existente = obtener_usuario_por_email(form.email.data.strip())

        if usuario_existente:
            flash("Este correo ya está registrado.", "danger")
            return redirect(url_for("registro"))

        password_hash = generate_password_hash(form.password.data)
        registrar_usuario(
            form.nombre.data.strip(),
            form.email.data.strip(),
            password_hash
        )

        flash("Registro exitoso. Ahora inicia sesión.", "success")
        return redirect(url_for("login"))

    return render_template("auth/registro.html", form=form)


# ============================================================
#                    LOGIN
# ============================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = obtener_usuario_por_email(form.email.data.strip())

        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash("Bienvenido al sistema.", "success")

            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("inicio"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("auth/login.html", form=form)


# ============================================================
#                    LOGOUT
# ============================================================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))


# ============================================================
#                    CRUD CATEGORIAS
# ============================================================
@app.route("/categorias")
@login_required
def categorias_listar():
    categorias = listar_categorias()
    return render_template("categorias/listar.html", categorias=categorias)


@app.route("/categorias/nuevo", methods=["GET", "POST"])
@login_required
def categoria_nuevo():
    form = CategoriaForm()

    if form.validate_on_submit():
        insertar_categoria(form.nombre_categoria.data.strip())
        flash("Categoría registrada correctamente.", "success")
        return redirect(url_for("categorias_listar"))

    return render_template("categorias/formulario.html", form=form, titulo="Nueva Categoría")


@app.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
def categoria_editar(id):
    categoria = obtener_categoria_por_id(id)

    if not categoria:
        flash("Categoría no encontrada.", "danger")
        return redirect(url_for("categorias_listar"))

    form = CategoriaForm()

    # Cargar datos manualmente (para evitar errores si categoria es diccionario)
    if request.method == "GET":
        form.nombre_categoria.data = categoria["nombre_categoria"]

    if form.validate_on_submit():
        actualizar_categoria(id, form.nombre_categoria.data.strip())
        flash("Categoría actualizada correctamente.", "warning")
        return redirect(url_for("categorias_listar"))

    return render_template("categorias/formulario.html", form=form, titulo="Editar Categoría")


@app.route("/categorias/eliminar/<int:id>", methods=["POST"])
@login_required
def categoria_eliminar(id):
    eliminado = eliminar_categoria(id)

    if not eliminado:
        flash("No se puede eliminar porque tiene productos relacionados.", "danger")
        return redirect(url_for("categorias_listar"))

    flash("Categoría eliminada correctamente.", "info")
    return redirect(url_for("categorias_listar"))


# ============================================================
#                    CRUD CLIENTES
# ============================================================
@app.route("/clientes")
@login_required
def clientes_listar():
    clientes = listar_clientes()
    return render_template("clientes/listar.html", clientes=clientes)


@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def cliente_nuevo():
    form = ClienteForm()

    if form.validate_on_submit():
        insertar_cliente(
            form.nombres.data.strip(),
            form.cedula.data.strip(),
            form.telefono.data.strip(),
            form.direccion.data.strip()
        )

        flash("Cliente registrado correctamente.", "success")
        return redirect(url_for("clientes_listar"))

    return render_template("clientes/formulario.html", form=form, titulo="Nuevo Cliente")


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def cliente_editar(id):
    cliente = obtener_cliente_por_id(id)

    if not cliente:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for("clientes_listar"))

    form = ClienteForm()

    if request.method == "GET":
        form.nombres.data = cliente["nombres"]
        form.cedula.data = cliente["cedula"]
        form.telefono.data = cliente["telefono"]
        form.direccion.data = cliente["direccion"]

    if form.validate_on_submit():
        actualizar_cliente(
            id,
            form.nombres.data.strip(),
            form.cedula.data.strip(),
            form.telefono.data.strip(),
            form.direccion.data.strip()
        )

        flash("Cliente actualizado correctamente.", "warning")
        return redirect(url_for("clientes_listar"))

    return render_template("clientes/formulario.html", form=form, titulo="Editar Cliente")


@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def cliente_eliminar(id):
    eliminado = eliminar_cliente(id)

    if not eliminado:
        flash("No se puede eliminar porque el cliente tiene pedidos registrados.", "danger")
        return redirect(url_for("clientes_listar"))

    flash("Cliente eliminado correctamente.", "info")
    return redirect(url_for("clientes_listar"))


# ============================================================
#                    CRUD PRODUCTOS
# ============================================================
@app.route("/productos")
@login_required
def productos_listar():
    productos = listar_productos()
    return render_template("productos/listar.html", productos=productos)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def producto_nuevo():
    form = ProductoForm()

    categorias = listar_categorias()

    # Validación importante
    if len(categorias) == 0:
        flash("Primero debes registrar una categoría antes de crear productos.", "warning")
        return redirect(url_for("categoria_nuevo"))

    form.id_categoria.choices = [(c["id_categoria"], c["nombre_categoria"]) for c in categorias]

    if form.validate_on_submit():
        insertar_producto(
            form.nombre.data.strip(),
            form.descripcion.data.strip(),
            float(form.precio.data),
            int(form.stock.data),
            int(form.id_categoria.data)
        )

        flash("Producto registrado correctamente.", "success")
        return redirect(url_for("productos_listar"))

    return render_template("productos/formulario.html", form=form, titulo="Nuevo Producto")


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def producto_editar(id):
    producto = obtener_producto_por_id(id)

    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("productos_listar"))

    form = ProductoForm()

    categorias = listar_categorias()

    if len(categorias) == 0:
        flash("No existen categorías registradas. Registra una categoría primero.", "warning")
        return redirect(url_for("categoria_nuevo"))

    form.id_categoria.choices = [(c["id_categoria"], c["nombre_categoria"]) for c in categorias]

    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]
        form.id_categoria.data = producto["id_categoria"]

    if form.validate_on_submit():
        actualizar_producto(
            id,
            form.nombre.data.strip(),
            form.descripcion.data.strip(),
            float(form.precio.data),
            int(form.stock.data),
            int(form.id_categoria.data)
        )

        flash("Producto actualizado correctamente.", "warning")
        return redirect(url_for("productos_listar"))

    return render_template("productos/formulario.html", form=form, titulo="Editar Producto")


@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def producto_eliminar(id):
    producto = obtener_producto_por_id(id)

    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("productos_listar"))

    eliminado = eliminar_producto(id)

    if not eliminado:
        flash("No se puede eliminar porque este producto ya está en pedidos.", "danger")
        return redirect(url_for("productos_listar"))

    flash("Producto eliminado correctamente.", "info")
    return redirect(url_for("productos_listar"))


# ============================================================
#                    CRUD PEDIDOS (FACTURA)
# ============================================================
@app.route("/pedidos")
@login_required
def pedidos_listar():
    pedidos = listar_pedidos()
    return render_template("pedidos/listar.html", pedidos=pedidos)


@app.route("/pedidos/nuevo", methods=["GET", "POST"])
@login_required
def pedido_nuevo():
    form = PedidoForm()

    clientes = listar_clientes()

    if len(clientes) == 0:
        flash("Primero debes registrar un cliente antes de crear pedidos.", "warning")
        return redirect(url_for("cliente_nuevo"))

    form.id_cliente.choices = [(c["id_cliente"], c["nombres"]) for c in clientes]

    if form.validate_on_submit():
        pedido_id = insertar_pedido(form.id_cliente.data)
        flash("Pedido creado. Ahora agrega productos.", "success")
        return redirect(url_for("pedido_detalle", id=pedido_id))

    return render_template("pedidos/formulario.html", form=form, titulo="Nuevo Pedido")


@app.route("/pedidos/detalle/<int:id>", methods=["GET", "POST"])
@login_required
def pedido_detalle(id):
    pedido = obtener_pedido_por_id(id)

    if not pedido:
        flash("Pedido no encontrado.", "danger")
        return redirect(url_for("pedidos_listar"))

    detalles = listar_detalle(id)
    form = DetallePedidoForm()

    productos = listar_productos()

    if len(productos) == 0:
        flash("No hay productos registrados. Registra productos antes de agregar al pedido.", "warning")
        return redirect(url_for("producto_nuevo"))

    form.id_producto.choices = [(p["id_producto"], f"{p['nombre']} - ${p['precio']}") for p in productos]

    if form.validate_on_submit():
        ok, mensaje = agregar_producto_a_pedido(id, form.id_producto.data, form.cantidad.data)

        if ok:
            actualizar_total_pedido(id)
            flash(mensaje, "success")
        else:
            flash(mensaje, "danger")

        return redirect(url_for("pedido_detalle", id=id))

    return render_template("pedidos/detalle.html", pedido=pedido, detalles=detalles, form=form)


@app.route("/pedidos/eliminar_detalle/<int:id_detalle>/<int:id_pedido>", methods=["POST"])
@login_required
def pedido_eliminar_detalle(id_detalle, id_pedido):
    eliminado = eliminar_detalle(id_detalle)

    if eliminado:
        actualizar_total_pedido(id_pedido)
        flash("Producto eliminado del pedido.", "info")
    else:
        flash("No se pudo eliminar el detalle.", "danger")

    return redirect(url_for("pedido_detalle", id=id_pedido))


@app.route("/pedidos/eliminar/<int:id>", methods=["POST"])
@login_required
def pedido_eliminar(id):
    pedido = obtener_pedido_por_id(id)

    if not pedido:
        flash("Pedido no encontrado.", "danger")
        return redirect(url_for("pedidos_listar"))

    eliminar_pedido(id)
    flash("Pedido eliminado correctamente.", "danger")
    return redirect(url_for("pedidos_listar"))


# ============================================================
#                    PDF FACTURA
# ============================================================
@app.route("/pedidos/factura/<int:id_pedido>")
@login_required
def generar_factura_pdf(id_pedido):
    pedido = obtener_pedido_por_id(id_pedido)
    detalles = listar_detalle(id_pedido)

    if not pedido:
        flash("Pedido no encontrado.", "danger")
        return redirect(url_for("pedidos_listar"))

    if len(detalles) == 0:
        flash("No se puede generar factura porque el pedido está vacío.", "danger")
        return redirect(url_for("pedido_detalle", id=id_pedido))

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, texto_pdf_seguro("FACTURA - RESTAURANTE"), ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", "", 12)

    pdf.cell(0, 8, texto_pdf_seguro(f"Factura Nro: {pedido['id_pedido']}"), ln=True)
    pdf.cell(0, 8, texto_pdf_seguro(f"Cliente: {pedido['nombres']}"), ln=True)

    fecha = pedido["fecha"]
    if isinstance(fecha, datetime):
        fecha_str = fecha.strftime("%d/%m/%Y %H:%M")
    else:
        fecha_str = str(fecha)

    pdf.cell(0, 8, texto_pdf_seguro(f"Fecha: {fecha_str}"), ln=True)
    pdf.cell(0, 8, texto_pdf_seguro(f"Generado por: {current_user.nombre}"), ln=True)

    pdf.ln(10)

    # Tabla
    pdf.set_font("Arial", "B", 11)
    pdf.cell(70, 10, texto_pdf_seguro("Producto"), 1)
    pdf.cell(30, 10, texto_pdf_seguro("Precio"), 1)
    pdf.cell(25, 10, texto_pdf_seguro("Cant."), 1)
    pdf.cell(30, 10, texto_pdf_seguro("Subtotal"), 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)

    for d in detalles:
        pdf.cell(70, 10, texto_pdf_seguro(str(d["nombre"])[:30]), 1)
        pdf.cell(30, 10, texto_pdf_seguro(f"${d['precio']}"), 1)
        pdf.cell(25, 10, texto_pdf_seguro(str(d["cantidad"])), 1)
        pdf.cell(30, 10, texto_pdf_seguro(f"${d['subtotal']}"), 1)
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, texto_pdf_seguro(f"TOTAL A PAGAR: ${pedido['total']}"), ln=True, align="R")

    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    pdf.multi_cell(0, 8, texto_pdf_seguro("Gracias por su compra. Vuelva pronto al Restaurante."))

    response = make_response(pdf.output(dest="S").encode("latin-1"))
    response.headers.set("Content-Disposition", "attachment", filename=f"factura_pedido_{id_pedido}.pdf")
    response.headers.set("Content-Type", "application/pdf")
    return response


# ============================================================
#                    PDF PRODUCTOS REPORTE
# ============================================================
@app.route("/productos/reporte_pdf")
@login_required
def exportar_pdf_productos():
    productos = listar_productos()

    if len(productos) == 0:
        flash("No hay productos registrados para exportar.", "warning")
        return redirect(url_for("productos_listar"))

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, texto_pdf_seguro("REPORTE DE PRODUCTOS - RESTAURANTE"), ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, texto_pdf_seguro(f"Generado por: {current_user.nombre}"), ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(15, 10, texto_pdf_seguro("ID"), 1)
    pdf.cell(60, 10, texto_pdf_seguro("Nombre"), 1)
    pdf.cell(50, 10, texto_pdf_seguro("Categoria"), 1)
    pdf.cell(30, 10, texto_pdf_seguro("Precio"), 1)
    pdf.cell(20, 10, texto_pdf_seguro("Stock"), 1)
    pdf.ln()

    pdf.set_font("Arial", "", 9)

    for p in productos:
        pdf.cell(15, 10, texto_pdf_seguro(str(p["id_producto"])), 1)
        pdf.cell(60, 10, texto_pdf_seguro(str(p["nombre"])[:25]), 1)
        pdf.cell(50, 10, texto_pdf_seguro(str(p["nombre_categoria"])[:20]), 1)
        pdf.cell(30, 10, texto_pdf_seguro(f"${p['precio']}"), 1)
        pdf.cell(20, 10, texto_pdf_seguro(str(p["stock"])), 1)
        pdf.ln()

    response = make_response(pdf.output(dest="S").encode("latin-1"))
    response.headers.set("Content-Disposition", "attachment", filename="reporte_productos.pdf")
    response.headers.set("Content-Type", "application/pdf")
    return response


# ============================================================
#                    EJECUCIÓN
# ============================================================
if __name__ == "__main__":
    app.run(debug=True)