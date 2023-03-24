from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

# Conectar a la base de datos
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='red5g'
)

# Ruta para agregar un nuevo usuario a la base de datos red5g.
@app.route('/registro', methods=['POST'])
def registro():
    #Se debe agregar la cabecera de autenticacion headers.
    key_app = request.headers.get('AUTH', '')
    #Consulta key.
    sql = f"SELECT * FROM parametro where credencial = '{key_app}';"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        #Recepcion de datos.
        data = request.get_json()
        nombrecompleto = data['nombrecompleto']
        correo = data['correo']
        passw = data['passw']
        direccion = data['direccion']
        telefono = data['telefono']
        fecha_nacimiento = data['fecha_nacimiento']
        
        #Registro en tabla usuarios de red5g.
        sql1 = f"INSERT INTO registro_usuarios (nombre_completo, correo, passw, direccion, telefono, fecha_nacimiento) VALUES ('{nombrecompleto}','{correo}','{passw}','{direccion}','{telefono}','{fecha_nacimiento}');"
        #Registro en tabla login_usuario. (LAST_INSERT_ID(), me toma el id de la tabla regristro_usuarios y me lo anexa en tabla login_usuario).
        sql2 = f"INSERT INTO login_usuario (id_usuario, correo, passw) VALUES (LAST_INSERT_ID(),'{correo}','{passw}');"
        
        #Envio de consultas
        cursor.execute(sql1)
        cursor.execute(sql2)
        connection.commit()
        cursor.close()
        return jsonify({'Mensaje': 'Registro exitoso'})
    return jsonify({'Mensaje': 'Error key_app en Headers'})

"""---"""

# Ruta login de usuarios previamente registrados.
@app.route('/login', methods=['POST'])
def login():
    #Se debe agregar la cabecera de autenticacion headers.
    key_app = request.headers.get('AUTH', '')
    #Consulta key.
    sql = f"SELECT * FROM parametro where credencial = '{key_app}';"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    
    if result:
        #Recepcion de datos
        data = request.get_json()
        correo = data['correo']
        passw = data['passw']
        #Consulta.
        sql = f"SELECT * FROM login_usuario where correo = '{correo}' and passw = '{passw}';"
        #Envio de consulta.
        cursor.execute(sql)
        result2 = cursor.fetchall()
        print(result2)
        if result2:
            cursor.close()
            return jsonify({"Bienvenid@":correo})
        return jsonify({"Mesaje":"Las credenciales no existen"})
    return jsonify({'Mensaje': 'Error key_app en Headers'})

"""---"""

# Ruta para actualizar un registro en la base de datos red5g.
@app.route('/update', methods=['PUT'])
def update():
    #Se debe agregar la cabecera de autenticacion headers.
    key_app = request.headers.get('AUTH', '')
    #Consulta key.
    sql = f"SELECT * FROM parametro where credencial = '{key_app}';"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        data = request.get_json()
        new_value = data['new_value']
        old_value = data['old_value']
        cursor = connection.cursor()
        sql = "UPDATE table_name SET column1 = %s WHERE column2 = %s"
        val = (new_value, old_value)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        return jsonify({'status': 'success'})

# Ruta para eliminar un registro de la base de datos
@app.route('/delete', methods=['DELETE'])
def delete():
    data = request.get_json()
    value_to_delete = data['value_to_delete']
    cursor = connection.cursor()
    sql = "DELETE FROM table_name WHERE column1 = %s"
    val = (value_to_delete,)
    cursor.execute(sql, val)
    connection.commit()
    cursor.close()
    return jsonify({'status': 'success'})

# Ruta para consultar todos los registros de la base de datos
@app.route('/get', methods=['GET'])
def get():
    cursor = connection.cursor()
    sql = "SELECT * FROM table_name"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)