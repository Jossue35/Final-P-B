from models.db_conector import DatabaseConnection

class CompraModel:
    def __init__(self) -> None:
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    def get_usuario(self):
        query = "SELECT id_usuario, nombre_usuario, apellido FROM usuario"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def get_productos(self):
        query = "SELECT id_producto, nombre_producto, precio, cantidad FROM producto"
        self._cur.execute(query)
        return self._cur.fetchall()
    
    def insert_compra(self, fecha_compra, precio_total, id_usuario_fk):
        query = """
        WITH inserted_compra AS (
          INSERT INTO compra (fecha_compra, precio_total, id_usuario_fk)
          VALUES (%s, %s, %s)
          RETURNING id_compra
        )
        SELECT id_compra FROM inserted_compra;
        """
        self._cur.execute(query, (fecha_compra,  precio_total, id_usuario_fk))
        id_compra = self._cur.fetchone()[0]
        self._conn.commit()
        return id_compra
    
    def insert_compra_producto(self, id_compra, id_producto):
        query = "INSERT INTO public.compra_producto (id_compra_fk, id_producto_fk) VALUES (%s, %s);"
        values = (id_compra, id_producto)
    
        try:
            self._cur.execute(query, values)
            self._conn.commit()
            print("Compra_Producto record inserted successfully")
        except Exception as e:
            self._conn.rollback()
            print(f"Error inserting Compra_Producto record: {e}")

    def close(self):
        self._cur.close()
        self._conn.close()