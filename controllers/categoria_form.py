import typing
import pathlib
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5 import  uic
from PyQt5.QtCore import  pyqtSignal
from models.categoria_model import CategoriaModel
from PyQt5.QtGui import  QPixmap, QIcon

class CategoriaForm(QWidget):
    categoria_saved = pyqtSignal()
    def __init__(self):
        super().__init__()
        self._categoriaHandler = CategoriaModel()
        self.categoria_id = None
        mod_path= pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/categoria_form.ui", self)
        self.saveButton.clicked.connect(lambda: self.save_categoria())
        self.cancelButton.clicked.connect(lambda: self.close())

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(81)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(41)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(450, 245, 81, 41)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path))
    
    def save_categoria(self):
        if self.categoria_id:
            self._categoriaHandler.update_categoria(
                self.categoria_id,
                self.nombreCategoriaTextField.text()
            )
        
        else:
            self._categoriaHandler.create_categoria(
                self.nombreCategoriaTextField.text()
            )
        self.categoria_saved.emit()
        self.close()

    def load_categoria_data(self, categoria_id):
        self.categoria_id = categoria_id
        categoria_data = self._categoriaHandler.get_categoria_by_id(categoria_id)
        if categoria_data:
            self.nombreCategoriaTextField.setText(categoria_data[1])

    def reset_form(self):
        self.nombreCategoriaTextField.setText("")
        self.categoria_id = None
