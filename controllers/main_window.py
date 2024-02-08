from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5 import uic
import pathlib
from PyQt5.QtGui import QPixmap, QIcon
from models.db_conector import DatabaseConnection


from controllers.cliente_window import ClienteWindow
from controllers.categoria_window import CategoriaWindow
from controllers.producto_window import ProductoWindow
from controllers.compras_window import ComprasWindow
from controllers.listado_compra import ListadoCompraWindow

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        root_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(root_path / "views/main_window.ui", self)

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(231)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(141)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(333, 70, 231, 141)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path))

        self.categoria_window = CategoriaWindow()
        self.pushButton.clicked.connect(self.abrir_ventana_categoria)

        self.producto_window = ProductoWindow()
        self.pushButton_3.clicked.connect(self.abrir_ventana_producto)

        self.cliente_window = ClienteWindow()
        self.pushButton_2.clicked.connect(self.abrir_ventana_cliente)

        self.compra_window = ComprasWindow()
        self.pushButton_4.clicked.connect(self.abrir_ventana_compras)

        self.listado_compra_window = ListadoCompraWindow()
        self.pushButton_5.clicked.connect(self.abrir_ventana_listado)


    def abrir_ventana_categoria(self):
        self.categoria_window.load_categoria()
        self.categoria_window.show()
        self.close()

    def abrir_ventana_producto(self):
        self.producto_window.load_producto()
        self.producto_window.show()
        self.close()

    def abrir_ventana_cliente(self):
        self.cliente_window.load_cliente()
        self.cliente_window.show()
        self.close()

    def abrir_ventana_compras(self):
        self.compra_window.load_usuarios()
        self.compra_window.load_productos()
        self.compra_window.show()
        self.close()

    def abrir_ventana_listado(self):
        self.listado_compra_window .show()
        self.close()

