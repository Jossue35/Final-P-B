from models.db_conector import DatabaseConnection

class ClienteModel:
    def __init__(self) -> None:
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur  = db.cursor

    def get_cliente(self):
        query = "SELECT id_usuario, cedula, nombre_usuario, apellido, correo, telefono, direccion \
            FROM usuario"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def create_cliente(self, cedula, nombre_usuario, apellido, correo, telefono, direccion):
        query = "INSERT INTO usuario(cedula, nombre_usuario, apellido, correo, telefono, direccion )\
            VALUES (%s, %s, %s, %s, %s, %s)"
        self._cur.execute(query, (cedula, nombre_usuario, apellido, correo, telefono, direccion))
        self._conn.commit()

    def get_cliente_by_id(self, cliente_id):
        try:
            query = "SELECT * FROM usuario WHERE id_usuario = %s"
            self._cur.execute(query, (cliente_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener el cliente: {str(e)}")
            return None
        
    def update_cliente(self, id_usuario,  cedula, nombre_usuario, apellido, correo, telefono, direccion):
        try:
            query = "UPDATE usuario SET cedula=%s, nombre_usuario=%s, apellido=%s, correo=%s, telefono=%s, direccion=%s WHERE id_usuario=%s"
            self._cur.execute(query, (cedula, nombre_usuario, apellido, correo, telefono, direccion, id_usuario))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False
        
    def delete_cliente(self, cliente_id):
        try:
            query = "DELETE FROM usuario WHERE id_usuario = %s"
            self._cur.execute(query, (cliente_id,))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrio un error: ",e)
            return False
        
    def close(self):
        self._cur.close()
        self._conn.close()

        
