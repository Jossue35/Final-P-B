from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QPushButton,  QLabel
from PyQt5 import uic
import pathlib
from models.cliente_model import ClienteModel
from controllers.cliente_form import ClienteForm
from PyQt5.QtGui import  QPixmap, QIcon

class ClienteWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._cliente_model = ClienteModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/cliente.ui", self)
        self._new_cliente = ClienteForm()
        self.load_cliente()
        self.nuevoClienteAction.triggered.connect(lambda: self.create_cliente())
        self._new_cliente.cliente_saved.connect(self.load_cliente)

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(231)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(141)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(395, 40, 231, 141)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path)) 
    
    def load_cliente(self):
        cliente = self._cliente_model.get_cliente()
        self.tableWidget.setRowCount(len(cliente))

        for i, cliente_data in enumerate(cliente):
            id_usuario, cedula, nombre_usuario, apellido, correo, telefono, direccion = cliente_data
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(id_usuario)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(cedula)))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(nombre_usuario)))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(apellido)))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(correo))) 
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(telefono))) 
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(direccion))) 
            self.tableWidget.setRowHeight(i, 40)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("controllers/icone-black1"))  # Reemplaza "ruta_del_icono_editar.png" por la ruta de tu icono de edición
            edit_button.setStyleSheet("background-color: transparent; border: none;")  # Configuración para quitar fondo y borde
            edit_button.setIconSize(QSize(20, 20))
            edit_button.clicked.connect(self.edit_cliente)
            edit_button.setProperty("row", i)
            self.tableWidget.setCellWidget(i, 7, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("controllers/xicone-black"))  # Reemplaza "ruta_del_icono_eliminar.png" por la ruta de tu icono de eliminación
            delete_button.setStyleSheet("background-color: transparent; border: none;")
            delete_button.setIconSize(QSize(20, 20))
            delete_button.clicked.connect(self.delete_cliente)
            delete_button.setProperty("row", i)
            self.tableWidget.setCellWidget(i, 8, delete_button)
        
    def edit_cliente(self):
        sender = self.sender()
        row = sender.property("row")
        id_cliente = int(self.tableWidget.item(row, 0).text())
        self._new_cliente.load_cliente_data(id_cliente)
        self._new_cliente.show()

    def delete_cliente(self):
        sender = self.sender()
        row = sender.property("row")
        cliente_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, 'Eliminar Cliente', 'Vas eliminar el cliente, Estas seguro?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            success = self._cliente_model.delete_cliente(cliente_id)
            if success:
                QMessageBox.information(self, 'Éxito', 'Se ha eliminado el cliente.')
                self.load_cliente()
            else:
                QMessageBox.warning(self, 'Error', 'Error al eliminar el cliente.')

    def create_cliente(self):
        self._new_cliente.reset_form()
        self._new_cliente.show()

    def closeEvent(self, ev) -> None:
        self._cliente_model.close()
        return super().closeEvent(ev)