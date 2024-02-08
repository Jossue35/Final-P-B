from PyQt5.QtCore import  QSize
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton,  QLabel
from PyQt5 import uic
import pathlib
from models.producto_model import ProductoModel
from controllers.producto_form import ProductoForm
from PyQt5.QtGui import  QPixmap, QIcon

class ProductoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._producto_model = ProductoModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/producto.ui", self)
        self._new_producto = ProductoForm()
        self.load_producto()
        self.nuevoProductoAction.triggered.connect(lambda: self.create_producto())
        self._new_producto.producto_saved.connect(self.load_producto)

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(231)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(141)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(395, 40, 231, 141)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path))

    def load_producto(self):
        producto = self._producto_model.get_producto()
        self.tableWidget.setRowCount(len(producto))
        
        for i, producto_data in enumerate(producto):
            id_producto, nombre_producto, nombre_categoria, precio, cantidad = producto_data[:5]
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(id_producto)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(nombre_producto)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(nombre_categoria)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(precio))) 
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(cantidad))) 
            self.tableWidget.setRowHeight(i, 40)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("controllers/icone-black1"))  # Reemplaza "ruta_del_icono_editar.png" por la ruta de tu icono de edición
            edit_button.setStyleSheet("background-color: transparent; border: none;")  # Configuración para quitar fondo y borde
            edit_button.setIconSize(QSize(20, 20))
            edit_button.clicked.connect(self.edit_producto)
            edit_button.setProperty("row", i)
            self.tableWidget.setCellWidget(i, 5, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("controllers/xicone-black"))  # Reemplaza "ruta_del_icono_eliminar.png" por la ruta de tu icono de eliminación
            delete_button.setStyleSheet("background-color: transparent; border: none;")
            delete_button.setIconSize(QSize(20, 20))
            delete_button.clicked.connect(self.delete_producto)
            delete_button.setProperty("row", i)
            self.tableWidget.setCellWidget(i, 6, delete_button)
    
    def edit_producto(self):
        sender = self.sender()
        row = sender.property("row")
        id_producto = int(self.tableWidget.item(row, 0).text())
        self._new_producto.load_producto_data(id_producto)
        self._new_producto.show()

    def delete_producto(self):
        sender = self.sender()
        row = sender.property("row")
        producto_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, 'Eliminar Producto', 'Vas eliminar el producto, Estas seguro?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            success = self._producto_model.delete_producto(producto_id)
            if success:
                QMessageBox.information(self, 'Éxito', 'Se ha eliminado el producto.')
                self.load_producto()
            else:
                QMessageBox.warning(self, 'Error', 'Error al eliminar el producto.')

    def create_producto(self):
        self._new_producto.reset_form()
        self._new_producto.show()

    def closeEvent(self, ev) -> None:
        self._producto_model.close()
        return super().closeEvent(ev)