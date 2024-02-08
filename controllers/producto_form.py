import typing
import pathlib
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5 import  uic
from PyQt5.QtCore import  pyqtSignal
from models.producto_model import ProductoModel
from PyQt5.QtGui import  QPixmap, QIcon

class ProductoForm(QWidget):
    producto_saved = pyqtSignal()
    def __init__(self):
        super().__init__()
        self._productoHandler = ProductoModel()
        self.producto_id = None
        mod_path= pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/producto_form.ui", self)
        self.saveButton.clicked.connect(lambda: self.save_producto())
        self.cancelButton.clicked.connect(lambda: self.close())

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(81)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(41)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(450, 245, 81, 41)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path))

    def save_producto(self):
        if self.producto_id:
            self._productoHandler.update_producto(
                self.producto_id,
                self.nameTextField.text(),
                self.precioTextField.text(),
                self.cantidadTextField.text()
            )
        
        else:
            self._productoHandler.create_producto(
                self.nameTextField.text(),
                self.precioTextField.text(),
                self.cantidadTextField.text()
            )
        self.producto_saved.emit()
        self.close()

    def load_producto_data(self, producto_id):
        self.producto_id = producto_id
        producto_data = self._productoHandler.get_producto_by_id(producto_id)
        if producto_data:
            self.nameTextField.setText(producto_data[1]),
            self.precioTextField.setText(str(producto_data[2])),
            self.cantidadTextField.setText(str(producto_data[3]))
    
    def reset_form(self):
        self.nameTextField.setText("")
        self.precioTextField.setText("")
        self.cantidadTextField.setText("")