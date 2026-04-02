from flask import Flask, render_template, redirect, url_for, flash, make_response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF

from forms.login_form import LoginForm
from forms.registro_form import RegistroForm
from forms.producto_form import ProductoForm
from forms.categoria_form import CategoriaForm
from forms.cliente_form import ClienteForm
from forms.pedido_form import PedidoForm
from forms.detalle_pedido_form import DetallePedidoForm

from services.usuario_service import registrar_usuario, obtener_usuario_por_email, obtener_usuario_por_id
from services.producto_service import listar_productos, insertar_producto, eliminar_producto, actualizar_producto, obtener_producto_por_id
from services.categoria_service import listar_categorias, insertar_categoria, eliminar_categoria, actualizar_categoria, obtener_categoria_por_id
from services.cliente_service import listar_clientes, insertar_cliente, eliminar_cliente, actualizar_cliente, obtener_cliente_por_id
from services.pedido_service import listar_pedidos, insertar_pedido, eliminar_pedido, obtener_pedido_por_id, actualizar_total_pedido
from services.detalle_pedido_service import listar_detalle, agregar_producto_a_pedido, eliminar_detalle


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave_segura_2026"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


@app.route("/")
def inicio():
    return render_template("index.html")


# ---------------- REGISTRO ----------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        usuario_existente = obtener_usuario_por_email(form.email.data)

        if usuario_existente:
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("registro"))

        password_hash = generate_password_hash(form.password.data)
        registrar_usuario(form.nombre.data, form.email.data, password_hash)

        flash("Registro exitoso. Ahora inicia sesión.", "success")
        return redirect(url_for("login"))

    return render_template("auth/registro.html", form=form)


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = obtener_usuario_por_email(form.email.data)

        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash("Bienvenido al sistema.", "success")

            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("inicio"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("auth/login.html", form=form)


# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))


# ---------------- CATEGORIAS CRUD ----------------
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

    return render_template("categorias/formulario.html", form=form)


@app.route("/categorias/editar/<int:id>", methods=["GET", "POST"])
@login_required
def categoria_editar(id):
    categoria = obtener_categoria_por_id(id)

    if not categoria:
        flash("Categoría no encontrada.", "danger")
        return redirect(url_for("categorias_listar"))

    form = CategoriaForm(data=categoria)

    if form.validate_on_submit():
        actualizar_categoria(id, form.nombre_categoria.data.strip())
        flash("Categoría actualizada.", "warning")
        return redirect(url_for("categorias_listar"))

    return render_template("categorias/formulario.html", form=form, categoria=categoria)


@app.route("/categorias/eliminar/<int:id>", methods=["POST"])
@login_required
def categoria_eliminar(id):
    eliminar_categoria(id)
    flash("Categoría eliminada.", "info")
    return redirect(url_for("categorias_listar"))


# ---------------- CLIENTES CRUD ----------------
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

    return render_template("clientes/formulario.html", form=form)


@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
@login_required
def cliente_editar(id):
    cliente = obtener_cliente_por_id(id)

    if not cliente:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for("clientes_listar"))

    form = ClienteForm(data=cliente)

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

    return render_template("clientes/formulario.html", form=form, cliente=cliente)


@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def cliente_eliminar(id):
    eliminar_cliente(id)
    flash("Cliente eliminado.", "info")
    return redirect(url_for("clientes_listar"))


# ---------------- PRODUCTOS CRUD ----------------
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

    return render_template("productos/formulario.html", form=form)


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def producto_editar(id):
    producto = obtener_producto_por_id(id)

    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("productos_listar"))

    form = ProductoForm(data=producto)

    categorias = listar_categorias()
    form.id_categoria.choices = [(c["id_categoria"], c["nombre_categoria"]) for c in categorias]

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

    return render_template("productos/formulario.html", form=form, producto=producto)


@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def producto_eliminar(id):
    eliminar_producto(id)
    flash("Producto eliminado.", "info")
    return redirect(url_for("productos_listar"))


# ---------------- PEDIDOS CRUD ----------------
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
    form.id_cliente.choices = [(c["id_cliente"], c["nombres"]) for c in clientes]

    if form.validate_on_submit():
        pedido_id = insertar_pedido(form.id_cliente.data)
        flash("Pedido creado. Ahora agrega productos.", "success")
        return redirect(url_for("pedido_detalle", id=pedido_id))

    return render_template("pedidos/formulario.html", form=form)


@app.route("/pedidos/detalle/<int:id>", methods=["GET", "POST"])
@login_required
def pedido_detalle(id):
    pedido = obtener_pedido_por_id(id)
    detalles = listar_detalle(id)

    form = DetallePedidoForm()

    productos = listar_productos()
    form.id_producto.choices = [(p["id_producto"], p["nombre"]) for p in productos]

    if form.validate_on_submit():
        agregar_producto_a_pedido(id, form.id_producto.data, form.cantidad.data)
        actualizar_total_pedido(id)
        flash("Producto agregado al pedido.", "success")
        return redirect(url_for("pedido_detalle", id=id))

    return render_template("pedidos/detalle.html", pedido=pedido, detalles=detalles, form=form)


@app.route("/pedidos/eliminar_detalle/<int:id_detalle>/<int:id_pedido>", methods=["POST"])
@login_required
def pedido_eliminar_detalle(id_detalle, id_pedido):
    eliminar_detalle(id_detalle)
    actualizar_total_pedido(id_pedido)
    flash("Detalle eliminado.", "info")
    return redirect(url_for("pedido_detalle", id=id_pedido))


@app.route("/pedidos/eliminar/<int:id>", methods=["POST"])
@login_required
def pedido_eliminar(id):
    eliminar_pedido(id)
    flash("Pedido eliminado.", "danger")
    return redirect(url_for("pedidos_listar"))


# ---------------- PDF PRODUCTOS ----------------
@app.route("/exportar/pdf")
@login_required
def exportar_pdf():
    productos = listar_productos()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "REPORTE DE PRODUCTOS - RESTAURANTE", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, f"Generado por: {current_user.nombre}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(15, 10, "ID", 1)
    pdf.cell(60, 10, "Nombre", 1)
    pdf.cell(50, 10, "Categoria", 1)
    pdf.cell(30, 10, "Precio", 1)
    pdf.cell(20, 10, "Stock", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 9)

    for p in productos:
        pdf.cell(15, 10, str(p["id_producto"]), 1)
        pdf.cell(60, 10, str(p["nombre"])[:25], 1)
        pdf.cell(50, 10, str(p["nombre_categoria"])[:20], 1)
        pdf.cell(30, 10, f"${p['precio']}", 1)
        pdf.cell(20, 10, str(p["stock"]), 1)
        pdf.ln()

    response = make_response(pdf.output(dest="S").encode("latin-1"))
    response.headers.set("Content-Disposition", "attachment", filename="reporte_productos.pdf")
    response.headers.set("Content-Type", "application/pdf")
    return response


if __name__ == "__main__":
    app.run(debug=True)