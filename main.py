from datetime import datetime
from utils import *
from flask import Flask, flash, json, redirect, render_template, request, url_for, make_response


app = Flask(__name__)

app.secret_key = '332432fsdfsdsdfs'

@app.route('/')
def hello():
    return render_template('index.html')

# Pantalla de Login
@app.route('/', methods=['POST'])
def funcion_login():
    email = str(request.form['email'])
    password = str(request.form['password'])

    if login(email, password):
        if email == "admin@biblioteca.com":
            response = make_response(redirect(url_for('admin')))
        else:
            response = make_response(redirect(url_for('libros_template')))
        response.set_cookie('email', email)
        return response
    else:
        flash('Nombre de usuario o contraseña incorrectos.')
        return redirect(url_for('hello'))
    
# Pantalla de Registro
@app.route('/registro',)
def registro_template():
    return render_template('registro.html')

@app.route('/registro', methods=['POST'])
def funcion_registro():
    nombre = str(request.form['nombre'])
    apellido = str(request.form['apellido'])
    documento = str(request.form['documento'])
    direccion = str(request.form['direccion'])
    telefono = str(request.form['telefono'])
    email = str(request.form['email'])
    password = str(request.form['password'])
    if registro(nombre, apellido, documento, direccion, telefono, email, password):
        flash('Registro exitoso!')
        return redirect(url_for('hello'))
    else:
        flash('Error en el registro.')
        return redirect(url_for('registro_template'))

#Pantalla de Libros
@app.route('/libros')
def libros_template():
    session = request.cookies.get('email')
    data_cliente = cliente(session)
    data=libros()

    for libro in data:
        libro['es_cliente_reservado'] = es_libro_reservado_por_cliente(libro['id_libro'], data_cliente['id_cliente'])

    if session:
        response = make_response(render_template('libros.html', data=data, cliente=data_cliente))
        return response
    else:
        response = make_response(redirect(url_for('hello')))
        return response
  
  
@app.route('/libros', methods=['POST'])
def filtro_libros_template():
    email = request.cookies.get('email')
    print(f"email: {email}")
    data_cliente = cliente(email)
    tipo = str(request.form['tipo'])
    texto = str(request.form['texto'])
    data = filtro_libros(tipo, texto)
    return render_template('libros.html', data=data, cliente=data_cliente)

# Ordenar por cantidad de libros
@app.route('/ordenar', methods=['POST'])
def ordenar_template():
    orden = request.form['ordenar']
    print(f"orden: {orden}")
    email = request.cookies.get('email')
    data_cliente = cliente(email)
    data = []
    if(orden == 'cantidad'):
        data = ordenar_libros_cantidad()
    else:
        data = ordenar_libros_publicacion()
    return render_template('libros.html', data=data, cliente=data_cliente)

# Cerrar sesion
@app.route('/cerrar_sesion')
def cerrar_sesion_template():
    return cerrar_sesion()

@app.route('/reserva_libro', methods=['POST'])
def reserva_template():
    id_libro = str(request.form['id_libro'])
    email_cliente = request.cookies.get('email')
    data_cliente = cliente(email_cliente)
    return render_template('reservar.html', cliente=data_cliente, id_libro=id_libro)

@app.route('/reserva_exitosa', methods=['POST'])
def reserva_exitosa_template():
    data_cliente = cliente(request.cookies.get('email'))
    id_cliente = data_cliente['id_cliente']
    id_libro = int(request.form['id_libro'])
    fecha_prestamo = datetime.now().strftime("%Y-%m-%d")
    fecha_devolucion = str(request.form['fecha'])
    estado_reserva = 1

    if hay_disponible(id_libro) and reservar(id_cliente, id_libro, fecha_prestamo, fecha_devolucion, estado_reserva):
        return render_template('reserva_exitosa.html', fecha=fecha_devolucion)
    
@app.route('/devolucion_exitosa', methods=['POST'])
def devolucion_exitosa_template():
    data_cliente = cliente(request.cookies.get('email'))
    id_cliente = data_cliente['id_cliente']
    id_libro = int(request.form['id_libro'])

    sumo_resto_cantidad_disponible(id_libro, False)
    cambiar_estado_reserva(id_libro, id_cliente)

    return render_template('devolucion_exitosa.html')

@app.route('/admin')
def admin():
    email = request.cookies.get('email')

    if email == "admin@biblioteca.com":

        all_reservas = reservas()
        for reserva in all_reservas:
            data_cliente = cliente(None, reserva["cliente_id"])
            data_libro = libros(reserva["libro_id"])

            reserva["libro_nombre"] = data_libro["titulo"]
            reserva["cantidad_disponible"] = data_libro["cantidad_disponible"]
            reserva["cliente_nombre"] = data_cliente["nombre"] + " " + data_cliente["apellido"]

        response = make_response(render_template('admin/reportes.html', reservas = all_reservas))
        return response
    else:
        response = make_response(render_template('admin/acceso_restringido.html'))
        return response
    
@app.route('/seccion_libros')
def seccion_libros():
    email = request.cookies.get('email')

    if email == "admin@biblioteca.com":
        data_libros = libros()
        return make_response(render_template('admin/seccion_libros.html', data = data_libros))
    else:
        return make_response(render_template('admin/acceso_restringido.html'))
    
@app.route('/admin_libros')
def admin_libros():
    email = request.cookies.get('email')

    if email == "admin@biblioteca.com":
        accion = request.args.get('accion')
        libro_id = request.args.get('libro_id')

        if accion == 'eliminar':
            eliminar_libro(int(libro_id))
            return render_template('admin/satisfactorio.html', accion="eliminacion")
        elif accion == 'editar':
            data_libro = libros(int(libro_id))
            return render_template('admin/edicion_libro.html', libro=data_libro)
        else:
            return render_template('admin/registro_libro.html')
    else:
        return make_response(render_template('admin/acceso_restringido.html'))
    
@app.route('/crear_editar_libro', methods=['POST'])
def crear_editar_libro():
    email = request.cookies.get('email')

    if email == "admin@biblioteca.com":
        id_libro = str(request.form['id_libro'])
        autor = str(request.form['autor'])
        cantidad_disponible = str(request.form['cantidad_disponible'])
        editorial = str(request.form['editorial'])
        fecha_publicacion = str(request.form['fecha_publicacion'])
        genero = str(request.form['genero'])
        picture = str(request.form['picture'])
        publicacion = str(request.form['publicacion'])
        titulo = str(request.form['titulo'])

        if id_libro == "":
            registro_edicion_libro(autor, cantidad_disponible, editorial, fecha_publicacion, genero, picture, publicacion, titulo)
            return make_response(render_template('admin/satisfactorio.html', accion="creacion"))
        else:
            registro_edicion_libro(autor, cantidad_disponible, editorial, fecha_publicacion, genero, picture, publicacion, titulo, int(id_libro))
            return make_response(render_template('admin/satisfactorio.html', accion="edicion"))
    else:
        return make_response(render_template('admin/acceso_restringido.html'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)