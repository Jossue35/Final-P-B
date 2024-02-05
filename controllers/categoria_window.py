from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QLabel
from PyQt5 import uic
import pathlib
from models.categoria_model import CategoriaModel
from controllers.categoria_form import CategoriaForm
from PyQt5.QtGui import QCloseEvent, QPixmap, QIcon


class CategoriaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._categoria_model = CategoriaModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/categoria.ui", self)
        self._new_categoria = CategoriaForm()
        self.load_categoria()
        self.nuevaCategoriaAction.triggered.connect(lambda: self.create_categoria())
        self._new_categoria.categoria_saved.connect(self.load_categoria)

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(231)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(141)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(333, 70, 231, 141)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path))

    def load_categoria(self):
        categoria = self._categoria_model.get_categoria()
        self.tableWidget.setRowCount(len(categoria))

        for i, categoria_data in enumerate(categoria):
            id_categoria, nombre_categoria = categoria_data
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(id_categoria)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(nombre_categoria))) 
            self.tableWidget.setRowHeight(i, 40)

            edit_button = QPushButton()
            edit_button.setIcon(QIcon("controllers/icone-black1"))  # Reemplaza "ruta_del_icono_editar.png" por la ruta de tu icono de edición
            edit_button.setStyleSheet("background-color: transparent; border: none;")  # Configuración para quitar fondo y borde
            edit_button.setIconSize(QSize(20, 20))
            edit_button.clicked.connect(self.edit_categoria)
            edit_button.setProperty("row", i)
            self.tableWidget.setCellWidget(i, 2, edit_button)

            delete_button = QPushButton()
            delete_button.setIcon(QIcon("controllers/xicone-black"))  # Reemplaza "ruta_del_icono_eliminar.png" por la ruta de tu icono de eliminación
            delete_button.setStyleSheet("background-color: transparent; border: none;")
            delete_button.setIconSize(QSize(20, 20))
            delete_button.clicked.connect(self.delete_categoria)
            delete_button.setProperty("row", i)
            self.tableWidget.setCellWidget(i, 3, delete_button)

    def edit_categoria(self):
        sender = self.sender()
        row = sender.property("row")
        id_categoria = int(self.tableWidget.item(row, 0).text())
        self._new_categoria.load_categoria_data(id_categoria)
        self._new_categoria.show()

    def delete_categoria(self):
        sender = self.sender()
        row = sender.property("row")
        categoria_id = self.tableWidget.item(row, 0).text()

       
        reply = QMessageBox.question(self, 'Eliminar Estudiante', 'Vas eliminar la categoria, Estas seguro?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            
            success = self._categoria_model.delete_categoria(categoria_id)
            if success:
                QMessageBox.information(self, 'Éxito', 'Se ha eliminado la categoria.')
                self.load_categoria()
            else:
                QMessageBox.warning(self, 'Error', 'Error al eliminar la categoria.')

    def create_categoria(self):
        self._new_categoria.reset_form()
        self._new_categoria.show()
    

    def closeEvent(self, ev) -> None:
        self._categoria_model.close()
        return super().closeEvent(ev)