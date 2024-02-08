from models.db_conector import DatabaseConnection

class ListadoCompraModel:
    def __init__(self) -> None:
        db = DatabaseConnection()
        self._conn = db.connection
        self._cur = db.cursor

    def close(self):
        self._cur.close()
        self._conn.close()

    def get_compra(self):
        query = "SELECT id_compra FROM compra"
        self._cur.execute(query)
        return self._cur.fetchall()

    def get_compra_details(self, id_compra):
        query = """
            SELECT c.id_compra, c.fecha_compra, c.precio_total,
                   p.nombre_producto, SUM(p.precio) AS total_precio
            FROM compra c
            INNER JOIN compra_producto cp ON c.id_compra = cp.id_compra_fk
            INNER JOIN producto p ON cp.id_producto_fk = p.id_producto
            WHERE c.id_compra = %s
            GROUP BY c.id_compra, c.fecha_compra, c.recibo, c.precio_total, p.nombre_producto;
        """
        self._cur.execute(query, (id_compra,))
        return self._cur.fetchall()