from flask import json, redirect, url_for, make_response

# Registro de clientes
def registro(nombre, apellido, documento, direccion, telefono, email, password):
    with open('JSON/clientes.json', encoding='utf-8') as archivo_clientes:
        data = json.load(archivo_clientes)
        data.append({
            'id_cliente': len(data) + 1,
            'nombre': nombre,
            'apellido': apellido,
            'documento': documento,
            'direccion': direccion,
            'telefono': telefono,
            'email': email,
            'password': password
        })
    with open('JSON/clientes.json', 'w', encoding='utf-8') as archivo_clientes:
        json.dump(data, archivo_clientes)
        return True

# Logueo de clientes
def login(email, password):
    with open('JSON/clientes.json', encoding='utf-8') as archivo_clientes:
        data = json.load(archivo_clientes)
        for cliente in data:
            if cliente['email'] == email and cliente['password'] == password:
                return True
    return False

# Obtener los libros
def libros(libro_id=None):
    with open('JSON/libros.json', encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)
        if libro_id is not None:
            for libro in data:
                if libro['id_libro'] == libro_id:
                    return libro
            return None
        else:
            return data
        
# Obtener los usuarios
def usuarios():
    with open('JSON/clientes.json', encoding='utf-8') as archivo_clientes:
        data = json.load(archivo_clientes)
        return data

# Obtener datos del cliente
def cliente(email, cliente_id=None):
    with open('JSON/clientes.json', encoding='utf-8') as archivo_clientes:
        data = json.load(archivo_clientes)
        if email is not None:
            for cliente in data:
                if cliente['email'] == email:
                    return cliente
            return None
        elif cliente_id is not None:
            for cliente in data:
                if cliente['id_cliente'] == cliente_id:
                    return cliente
            return None
        else:
            return data

def reservas():
    with open('JSON/reservas.json', encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)
        return data

# Filtro de libros
def filtro_libros(tipo, texto):
    with open('JSON/libros.json', encoding='utf-8') as archivo_libros:
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
    with open('JSON/libros.json', encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)
        data.sort(key=lambda x: x['cantidad_disponible'], reverse=True)
        print(data)
        return data

def ordenar_libros_publicacion():
    with open('JSON/libros.json', encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)
        data.sort(key=lambda x: x['fecha_publicacion'], reverse=True)
        return data

def sumo_resto_cantidad_disponible(id_libro, es_resta):
    with open('JSON/libros.json', 'r', encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)

    for libro in data:
        if libro['id_libro'] == id_libro:
            if es_resta:
                libro['cantidad_disponible'] -= 1
            else:
                libro['cantidad_disponible'] += 1
            break

    with open('JSON/libros.json', 'w', encoding='utf-8') as archivo_libros:
        json.dump(data, archivo_libros, indent=4)

def hay_disponible(id_libro):
    with open('JSON/libros.json', encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)

    for libro in data:
        if libro['id_libro'] == id_libro:
            return libro['cantidad_disponible'] > 0
    return False

# Reserva de libros
def reservar(id_cliente, id_libro, fecha_prestamo, fecha_devolucion, estado_reserva):
    with open('JSON/reservas.json', encoding='utf-8') as archivo_reservas:
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

    with open('JSON/reservas.json', 'w', encoding='utf-8') as archivo_reservas:
        json.dump(data, archivo_reservas)
        return True

def es_libro_reservado_por_cliente(id_libro, id_cliente):
    libros_reservados = []

    with open('JSON/reservas.json', encoding='utf-8') as archivo_reservas:
        reservas = json.load(archivo_reservas)
        for reserva in reservas:
            if reserva['cliente_id'] == id_cliente and reserva['estado_reserva'] == 1:
                libros_reservados.append(reserva['libro_id'])

    return id_libro in libros_reservados

def cambiar_estado_reserva(id_libro, id_cliente):
    with open('JSON/reservas.json', encoding='utf-8') as archivo_reservas:
        reservas = json.load(archivo_reservas)
        for reserva in reservas:
            if (reserva['cliente_id'] == id_cliente and
                reserva['libro_id'] == id_libro and 
                reserva['estado_reserva'] == 1):
                reserva["estado_reserva"] = 2
                break 
    with open('JSON/reservas.json', 'w', encoding='utf-8') as archivo_reservas:
        json.dump(reservas, archivo_reservas, indent=4)

# Obtener reservas
def obtener_reservas(email):
    with open('JSON/reservas.json', encoding='utf-8') as archivo_reservas:
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

def registro_edicion_libro(autor, cantidad_disponible, editorial, fecha_publicacion, genero, picture, publicacion, titulo, id_libro=None):
    with open('JSON/libros.json',encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)
        if id_libro is None:
            data.append({
            "id_libro": len(data) + 1,
            "autor": autor,
            "cantidad_disponible": int(cantidad_disponible),
            "editorial": editorial,
            "fecha_publicacion": fecha_publicacion,
            "genero": genero,
            "picture": picture,
            "publicacion": int(publicacion),
            "titulo": titulo
            })
        else:
            for libro in data:
                if libro['id_libro'] == id_libro:
                    libro['autor'] = autor
                    libro['cantidad_disponible'] = int(cantidad_disponible)
                    libro['editorial'] = editorial
                    libro['fecha_publicacion'] = fecha_publicacion
                    libro['genero'] = genero
                    libro['picture'] = picture
                    libro['publicacion'] = int(publicacion)
                    libro['titulo'] = titulo
                    break
    
        with open('JSON/libros.json', 'w', encoding='utf-8') as archivo_libros:
            json.dump(data, archivo_libros,ensure_ascii=False, indent=4)
            return True
    
def eliminar_libro(id_libro):
    with open('JSON/libros.json', encoding='utf-8') as archivo_libros:
        data = json.load(archivo_libros)
        nuevos_libros = []
        for libro in data:
            if libro['id_libro'] != id_libro:
                nuevos_libros.append(libro)

    with open('JSON/libros.json', 'w', encoding='utf-8') as archivo_libros:
        json.dump(nuevos_libros, archivo_libros, indent=4)
        return True