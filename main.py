from datetime import datetime
from flask import Flask, flash, json, redirect, render_template, request, url_for, make_response


app = Flask(__name__)

app.secret_key = '332432fsdfsdsdfs'

# Registro de clientes
def registro(nombre, apellido, documento, direccion, telefono, email, password):
    with open('JSON/clientes.json') as archivo_clientes:
        data = json.load(archivo_clientes)
        data.append({
            'id': len(data) + 1,
            'nombre': nombre,
            'apellido': apellido,
            'documento': documento,
            'direccion': direccion,
            'telefono': telefono,
            'email': email,
            'password': password
        })
    with open('JSON/clientes.json', 'w') as archivo_clientes:
        json.dump(data, archivo_clientes)
        return True

# Logueo de clientes
def login(email, password):
    with open('JSON/clientes.json') as archivo_clientes:
        data = json.load(archivo_clientes)
        for cliente in data:
            if cliente['email'] == email and cliente['password'] == password:
                return True
    return False

# Obtener los libros
def libros():
    with open('JSON/libros.json') as archivo_libros:
        data = json.load(archivo_libros)
        return data

# Obtener datos del cliente
def cliente(email):
    with open('JSON/clientes.json') as archivo_clientes:
        data = json.load(archivo_clientes)
        for cliente in data:
            if cliente['email'] == email:
                return cliente
    return False

# Filtro de libros
def filtro_libros(tipo, texto):
    with open('JSON/libros.json') as archivo_libros:
        data = json.load(archivo_libros)
        libros_filtrados = []

        print(f"tipo: {tipo}, texto: {texto}")

        select = tipo.lower()
        
        for libro in data:
            if select == 'titulo':
                #debo saber si incluye alguna palabra del texto
                if libro['titulo'].lower().find(texto.lower()) != -1:
                    libros_filtrados.append(libro)
            elif select == 'genero':
                if libro['genero'].lower().find(texto.lower()) != -1:
                    libros_filtrados.append(libro)
            elif select == 'autor':
                if libro['autor'].lower().find(texto.lower()) != -1:
                    libros_filtrados.append(libro)
            elif select == 'editorial':
                if libro['editorial'].lower().find(texto.lower()) != -1:
                    libros_filtrados.append(libro)
        
        return libros_filtrados

# Ordenar por cantidad de libros
def ordenar_libros_cantidad():
    with open('JSON/libros.json') as archivo_libros:
        data = json.load(archivo_libros)
        data.sort(key=lambda x: x['cantidad_disponible'], reverse=True)
        print(data)
        return data

def ordenar_libros_publicacion():
    with open('JSON/libros.json') as archivo_libros:
        data = json.load(archivo_libros)
        data.sort(key=lambda x: x['fecha_publicacion'], reverse=True)
        return data

def sumo_resto_cantidad_disponible(id_libro, es_resta):
    with open('JSON/libros.json', 'r') as archivo_libros:
        data = json.load(archivo_libros)

    for libro in data:
        if libro['id_libro'] == id_libro:
            if es_resta:
                libro['cantidad_disponible'] -= 1
            else:
                libro['cantidad_disponible'] += 1
            break

    with open('JSON/libros.json', 'w') as archivo_libros:
        json.dump(data, archivo_libros, indent=4)

def hay_disponible(id_libro):
    with open('JSON/libros.json') as archivo_libros:
        data = json.load(archivo_libros)

    for libro in data:
        if libro['id_libro'] == id_libro:
            return libro['cantidad_disponible'] > 0
    return False

# Reserva de libros
def reservar(id_cliente, id_libro, fecha_prestamo, fecha_devolucion, estado_reserva):
    with open('JSON/reservas.json') as archivo_reservas:
        data = json.load(archivo_reservas)
        data.append({
            'reserva_id': len(data) + 1,
            'cliente_id': id_cliente,
            'libro_id': id_libro,
            'fecha_prestamo': fecha_prestamo,
            'fecha_devolucion': fecha_devolucion,
            'estado_reserva' : estado_reserva
        })

    sumo_resto_cantidad_disponible(id_libro, True)

    with open('JSON/reservas.json', 'w') as archivo_reservas:
        json.dump(data, archivo_reservas)
        return True

def es_libro_reservado_por_cliente(id_libro, id_cliente):
    libros_reservados = []

    with open('JSON/reservas.json') as archivo_reservas:
        reservas = json.load(archivo_reservas)
        for reserva in reservas:
            if reserva['cliente_id'] == id_cliente and reserva['estado_reserva'] == 1:
                libros_reservados.append(reserva['libro_id'])

    return id_libro in libros_reservados

def cambiar_estado_reserva(id_libro, id_cliente):
    with open('JSON/reservas.json') as archivo_reservas:
        reservas = json.load(archivo_reservas)
        for reserva in reservas:
            if (reserva['cliente_id'] == id_cliente and
                reserva['libro_id'] == id_libro and 
                reserva['estado_reserva'] == 1):
                reserva["estado_reserva"] = 2
                break 
    with open('JSON/reservas.json', 'w') as archivo_reservas:
        json.dump(reservas, archivo_reservas, indent=4)

# Obtener reservas
def obtener_reservas(email):
    with open('JSON/reservas.json') as archivo_reservas:
        data = json.load(archivo_reservas)
        reservas = []
        for reserva in data:
            if reserva['email'] == email:
                reservas.append(reserva)
        return reservas


def cerrar_sesion():
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('email', '', expires=0)
    return response

def cerrar_sesion():
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('email', '', expires=0)
    return response


###############################################ROUTES############################################
@app.route('/')
def hello():
    return render_template('index.html')

# Pantalla de Login
@app.route('/', methods=['POST'])
def funcion_login():
    email = str(request.form['email'])
    password = str(request.form['password'])

    if login(email, password):
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
        libro['es_cliente_reservado'] = es_libro_reservado_por_cliente(libro['id_libro'], data_cliente['id'])

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
    id_cliente = data_cliente['id']
    id_libro = int(request.form['id_libro'])
    fecha_prestamo = datetime.now().strftime("%Y-%m-%d")
    fecha_devolucion = str(request.form['fecha'])
    estado_reserva = 1

    if hay_disponible(id_libro) and reservar(id_cliente, id_libro, fecha_prestamo, fecha_devolucion, estado_reserva):
        return render_template('reserva_exitosa.html', fecha=fecha_devolucion)
    
@app.route('/devolucion_exitosa', methods=['POST'])
def devolucion_exitosa_template():
    data_cliente = cliente(request.cookies.get('email'))
    id_cliente = data_cliente['id']
    id_libro = int(request.form['id_libro'])

    sumo_resto_cantidad_disponible(id_libro, False)
    cambiar_estado_reserva(id_libro, id_cliente)

    return render_template('devolucion_exitosa.html')

@app.route('/admin')
def admin_template():
    email = request.cookies.get('email')
    data_cliente = cliente(email)
    data=libros()

    session = request.cookies.get('email')

    if session:
        response = make_response(render_template('libros.html', data=data, cliente=data_cliente))
        return response
    else:
        response = make_response(redirect(url_for('hello')))
        return response


if __name__ == '__main__':
    app.run(debug=True, port=5000)