from models.db_conector import DatabaseConnection

class ProductoModel:
    def __init__(self) -> None:
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur  = db.cursor

    def get_producto(self):
        query = """SELECT p.id_producto, p.nombre_producto, c.nombre_categoria, p.precio, p.cantidad
                FROM producto p
                INNER JOIN categoria c ON p.id_categoria2 = c.id_categoria;"""
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def create_producto(self, nombre_producto, precio, cantidad):
        query = "INSERT INTO producto (nombre_producto, precio, cantidad) \
            VALUES(%s, %s, %s)"
        self._cur.execute(query, (nombre_producto, precio, cantidad))
        self._conn.commit()

    def get_producto_by_id(self, producto_id):
        try:
            query = "SELECT * FROM producto WHERE id_producto = %s"
            self._cur.execute(query,(producto_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener el producto: {str(e)}")
            return None
        
    def update_producto(self, id_producto, nombre_producto, precio, cantidad):
        try:
            query = "UPDATE producto SET nombre_producto=%s, precio=%s, cantidad=%s \
                WHERE id_producto=%s"
            self._cur.execute(query, (nombre_producto, precio, cantidad, id_producto))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False
        
    def delete_producto(self, producto_id):
        try:
            query = "DELETE FROM producto WHERE id_producto = %s"
            self._cur.execute(query, (producto_id,))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrio un error: ",e)
            return False
        
    def close(self):
        self._cur.close()
        self._conn.close()