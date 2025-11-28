from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import datetime
from config import DATABASE
from models import get_db_connection, init_schema, seed_usuarios
from forms import LoginForm, ProductoFiltroForm, ProductoForm, AlmacenFiltroForm, AlmacenForm
from utils import md5, require_login, can_edit_productos, can_edit_almacenes

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Inicialización de la base de datos y usuarios al arrancar
with app.app_context():
    init_schema()
    seed_usuarios(
        admin_pw_md5=md5('admin23'),
        prod_pw_md5=md5('productos 19'),
        almac_pw_md5=md5('almacenes 11')
    )

# ------------------- LOGIN -------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        pw = md5(form.password.data)
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (nombre, pw)).fetchone()
        if user:
            session.clear()
            session['usuario'] = user['nombre']
            session['rol'] = user['rol']
            conn.execute("UPDATE usuarios SET fecha_hora_ultimo_inicio=? WHERE nombre=?", (datetime.now().isoformat(' '), nombre))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        conn.close()
        flash('Credenciales inválidas', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------- HOME -------------------
@app.route('/home')
def home():
    if not require_login(session):
        return redirect(url_for('login'))
    return render_template('home.html', usuario=session['usuario'], rol=session['rol'])

# ------------------- PRODUCTOS -------------------
@app.route('/productos', methods=['GET', 'POST'])
def productos():
    if not require_login(session):
        return redirect(url_for('login'))
    conn = get_db_connection()
    almacenes = conn.execute("SELECT id, nombre FROM almacenes").fetchall()
    form = ProductoFiltroForm()
    form.almacen.choices = [(0, 'Todos')] + [(a['id'], a['nombre']) for a in almacenes]

    query = """SELECT p.id, p.nombre, p.precio, p.cantidad, p.departamento, p.almacen,
               a.nombre AS almacen_nombre, p.fecha_hora_creacion, p.fecha_hora_ultima_modificacion,
               p.ultimo_usuario_en_modificar
               FROM productos p LEFT JOIN almacenes a ON a.id = p.almacen WHERE 1=1"""
    params = []

    if request.method == 'POST' and form.validate():
        if form.id.data:
            query += " AND p.id = ?"; params.append(form.id.data)
        if form.nombre.data:
            query += " AND p.nombre LIKE ?"; params.append(f"%{form.nombre.data.strip()}%")
        if form.precio_min.data is not None:
            query += " AND p.precio >= ?"; params.append(float(form.precio_min.data))
        if form.precio_max.data is not None:
            query += " AND p.precio <= ?"; params.append(float(form.precio_max.data))
        if form.cantidad_min.data is not None:
            query += " AND p.cantidad >= ?"; params.append(int(form.cantidad_min.data))
        if form.cantidad_max.data is not None:
            query += " AND p.cantidad <= ?"; params.append(int(form.cantidad_max.data))
        if form.departamento.data:
            query += " AND p.departamento LIKE ?"; params.append(f"%{form.departamento.data.strip()}%")
        if form.almacen.data and int(form.almacen.data) != 0:
            query += " AND p.almacen = ?"; params.append(int(form.almacen.data))
        if form.usuario_modificacion.data:
            query += " AND p.ultimo_usuario_en_modificar LIKE ?"
            params.append(f"%{form.usuario_modificacion.data.strip()}%")
        if form.filtro_modificaciones.data == 'ultimos':
            query += " AND p.fecha_hora_ultima_modificacion IS NOT NULL"
            query += " ORDER BY p.fecha_hora_ultima_modificacion DESC"

    productos = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('productos.html', productos=productos, form=form, puede_editar=can_edit_productos(session['rol']))


@app.route('/productos/agregar', methods=['GET', 'POST'])
def producto_agregar():
    if not require_login(session): return redirect(url_for('login'))
    if not can_edit_productos(session['rol']): return redirect(url_for('productos'))

    conn = get_db_connection()
    almacenes = conn.execute("SELECT id, nombre FROM almacenes").fetchall()
    form = ProductoForm()
    form.almacen.choices = [(a['id'], a['nombre']) for a in almacenes]

    if form.validate_on_submit():
        conn.execute("""
            INSERT INTO productos (nombre, precio, cantidad, departamento, almacen,
            fecha_hora_creacion, fecha_hora_ultima_modificacion, ultimo_usuario_en_modificar)
            VALUES (?,?,?,?,?,?,?,?)
        """, (
            form.nombre.data.strip(),
            float(form.precio.data),
            int(form.cantidad.data),
            form.departamento.data.strip(),
            int(form.almacen.data),
            datetime.now().isoformat(' '),
            datetime.now().isoformat(' '),
            session['usuario']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))

    conn.close()
    return render_template('producto_form.html', form=form, modo='Agregar')

@app.route('/productos/modificar/<int:pid>', methods=['GET', 'POST'])
def producto_modificar(pid):
    if not require_login(session):
        return redirect(url_for('login'))
    if not can_edit_productos(session['rol']):
        return redirect(url_for('productos'))

    conn = get_db_connection()
    producto = conn.execute("SELECT * FROM productos WHERE id=?", (pid,)).fetchone()
    if not producto:
        conn.close()
        return redirect(url_for('productos'))

    almacenes = conn.execute("SELECT id, nombre FROM almacenes").fetchall()
    form = ProductoForm()
    form.almacen.choices = [(a['id'], a['nombre']) for a in almacenes]

    if form.validate_on_submit():
        conn.execute("""
            UPDATE productos 
            SET nombre=?, precio=?, cantidad=?, departamento=?, almacen=?, 
                fecha_hora_ultima_modificacion=?, ultimo_usuario_en_modificar=?
            WHERE id=?
        """, (
            form.nombre.data.strip(),
            float(form.precio.data),
            int(form.cantidad.data),
            form.departamento.data.strip(),
            int(form.almacen.data),
            datetime.now().isoformat(' '),
            session['usuario'], #usuario que modificó
            pid
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('productos'))

    form.nombre.data = producto['nombre']
    form.precio.data = producto['precio']
    form.cantidad.data = producto['cantidad']
    form.departamento.data = producto['departamento']
    form.almacen.data = producto['almacen']
    conn.close()
    return render_template('producto_form.html', form=form, modo='Modificar')


@app.route('/productos/eliminar/<int:pid>', methods=['POST'])
def producto_eliminar(pid):
    if not require_login(session): return redirect(url_for('login'))
    if not can_edit_productos(session['rol']): return redirect(url_for('productos'))
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

# ------------------- ALMACENES -------------------
@app.route('/almacenes', methods=['GET', 'POST'])
def almacenes():
    if not require_login(session):
        return redirect(url_for('login'))
    conn = get_db_connection()
    form = AlmacenFiltroForm()
    query = """SELECT id, nombre, fecha_hora_creacion, fecha_hora_ultima_modificacion, ultimo_usuario_en_modificar
               FROM almacenes WHERE 1=1"""
    params = []

    if request.method == 'POST' and form.validate():
        if form.id.data:
            query += " AND id = ?"; params.append(form.id.data)
        if form.nombre.data:
            query += " AND nombre LIKE ?"; params.append(f"%{form.nombre.data.strip()}%")
        if form.usuario_modificacion.data:
            query += " AND ultimo_usuario_en_modificar LIKE ?"
            params.append(f"%{form.usuario_modificacion.data.strip()}%")
        if form.filtro_modificaciones.data == 'ultimos':
            query += " AND fecha_hora_ultima_modificacion IS NOT NULL"
            query += " ORDER BY fecha_hora_ultima_modificacion DESC"

    data = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('almacenes.html', almacenes=data, form=form, puede_editar=can_edit_almacenes(session['rol']))

@app.route('/almacenes/agregar', methods=['GET', 'POST'])
def almacen_agregar():
    if not require_login(session):
        return redirect(url_for('login'))
    if not can_edit_almacenes(session['rol']):
        return redirect(url_for('almacenes'))

    form = AlmacenForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO almacenes (nombre, fecha_hora_creacion, fecha_hora_ultima_modificacion, ultimo_usuario_en_modificar)
            VALUES (?,?,?,?)
        """, (
            form.nombre.data.strip(),
            datetime.now().isoformat(' '),
            datetime.now().isoformat(' '),
            session['usuario']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('almacenes'))

    return render_template('almacenes.html', crear=True, form=form)

@app.route('/almacenes/modificar/<int:aid>', methods=['GET', 'POST'])
def almacen_modificar(aid):
    if not require_login(session):
        return redirect(url_for('login'))
    if not can_edit_almacenes(session['rol']):
        return redirect(url_for('almacenes'))

    conn = get_db_connection()
    almacen = conn.execute("SELECT * FROM almacenes WHERE id=?", (aid,)).fetchone()
    if not almacen:
        conn.close()
        return redirect(url_for('almacenes'))

    form = AlmacenForm()
    if form.validate_on_submit():
        conn.execute("""
            UPDATE almacenes 
            SET nombre=?, fecha_hora_ultima_modificacion=?, ultimo_usuario_en_modificar=?
            WHERE id=?
        """, (
            form.nombre.data.strip(),
            datetime.now().isoformat(' '),
            session['usuario'], #usuario que modificó
            aid
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('almacenes'))

    form.nombre.data = almacen['nombre']
    conn.close()
    return render_template('almacen_form.html', form=form, modo='Modificar')

@app.route('/almacenes/eliminar/<int:aid>', methods=['POST'])
def almacen_eliminar(aid):
    if not require_login(session):
        return redirect(url_for('login'))
    if not can_edit_almacenes(session['rol']):
        return redirect(url_for('almacenes'))

    conn = get_db_connection()
    conn.execute("DELETE FROM almacenes WHERE id=?", (aid,))
    conn.commit()
    conn.close()
    return redirect(url_for('almacenes'))


if __name__ == '__main__':
    app.run(debug=True)
