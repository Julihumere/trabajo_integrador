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

# Reserva de libros
def reservar(libro):
    email = request.cookies.get('email')
    with open('JSON/reservas.json') as archivo_reservas:
        data = json.load(archivo_reservas)
        data.append({
            'id': len(data) + 1,
            'email': email,
            'libro': libro
        })
    with open('JSON/reservas.json', 'w') as archivo_reservas:
        json.dump(data, archivo_reservas)
        return True

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
    id_cliente = str(request.form['id_cliente'])
    email = request.cookies.get('email')
    data_cliente = cliente(email)
    return render_template('reservar.html', cliente=data_cliente, id_libro=id_libro, id_cliente=id_cliente)



if __name__ == '__main__':
    app.run(debug=True, port=5000)