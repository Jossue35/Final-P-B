import typing
import pathlib
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5 import  uic
from PyQt5.QtCore import  pyqtSignal
from models.cliente_model import ClienteModel
from PyQt5.QtGui import  QPixmap, QIcon

class ClienteForm(QWidget):
    cliente_saved = pyqtSignal()
    def __init__(self):
        super().__init__()
        self._clienteHandler = ClienteModel()
        self.cliente_id = None
        mod_path= pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/cliente_form.ui", self)
        self.saveButton.clicked.connect(lambda: self.save_cliente())
        self.cancelButton.clicked.connect(lambda: self.close())

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(81)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(41)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(790, 360, 81, 41)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path))

    def save_cliente(self):
        if self.cliente_id:
            self._clienteHandler.update_cliente(
                self.cliente_id,
                self.cedulaTextField.text(),
                self.nombreTextField.text(),
                self.apellidoTextField.text(),
                self.correoTextField.text(),
                self.telefonoTextField.text(),
                self.direccionTextField.text()
            )
        else:
            self._clienteHandler.create_cliente(
                self.cedulaTextField.text(),
                self.nombreTextField.text(),
                self.apellidoTextField.text(),
                self.correoTextField.text(),
                self.telefonoTextField.text(),
                self.direccionTextField.text()
            )
        self.cliente_saved.emit()
        self.close()

    def load_cliente_data(self, cliente_id):
        self.cliente_id = cliente_id
        cliente_data = self._clienteHandler.get_cliente_by_id(cliente_id)
        if cliente_data:
                self.cedulaTextField.setText((cliente_data[1])),
                self.nombreTextField.setText(cliente_data[2]),
                self.apellidoTextField.setText(cliente_data[3]),
                self.correoTextField.setText(cliente_data[4]),
                self.telefonoTextField.setText(str(cliente_data[5])),
                self.direccionTextField.setText(cliente_data[6])
    def reset_form(self):
        self.cedulaTextField.setText(""),
        self.nombreTextField.setText(""),
        self.apellidoTextField.setText(""),
        self.correoTextField.setText(""),
        self.telefonoTextField.setText(""),
        self.direccionTextField.setText("")