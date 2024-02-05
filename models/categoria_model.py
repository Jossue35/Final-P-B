#from models.db_conector import DatabaseConnection
import psycopg2

class CategoriaModel:
    def __init__(self) -> None:
        #db = DatabaseConnection()
        self._conn = psycopg2.connect("dbname=proyecto_final user=postgres password=1234 host=localhost")
        self._cur = self._conn.cursor()

    def get_categoria(self):
        query = "SELECT * FROM categoria"
        self._cur.execute(query)
        return self._cur.fetchall()

    def create_categoria(self, nombre_categoria):
        query = "INSERT INTO categoria (nombre_categoria) VALUES (%s)"
        self._cur.execute(query, (nombre_categoria,))
        self._conn.commit()

    def get_categoria_by_id(self, categoria_id):
        try:
            query = "SELECT * FROM categoria WHERE id_categoria = %s"
            self._cur.execute(query, (categoria_id,))
            return self._cur.fetchone()
        except Exception as e:
            print(f"Error al obtener la categoria: {str(e)}")
            return None

    def update_categoria(self, id_categoria, nombre_categoria):
        try:
            query = "UPDATE categoria SET nombre_categoria=%s WHERE id_categoria=%s"
            self._cur.execute(query, (nombre_categoria, id_categoria))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False

    def delete_categoria(self, categoria_id):
        try:
            query = "DELETE FROM categoria WHERE id_categoria = %s"
            self._cur.execute(query, (categoria_id,))
            self._conn.commit()
            return True
        except Exception as e:
            print("Ocurrió un error: ", e)
            return False

    def close(self):
        self._cur.close()
        self._conn.commit()
        self._conn.close()

