from PyQt5.QtWidgets import  QTableWidgetItem, QMainWindow, QLabel, QTableWidgetItem, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow,  QTableWidgetItem,  QPushButton
from PyQt5 import uic
import pathlib
from models.listado_compras_model import ListadoCompraModel
from controllers.categoria_form import CategoriaForm
from PyQt5.QtGui import QIcon, QPixmap

class ListadoCompraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._listado_compra_model = ListadoCompraModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/compra.ui", self)

        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(231)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(141)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(410, 40, 231, 141)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  
        self.setWindowIcon(QIcon(icon_path))

        botonCompra = self.findChild(QPushButton, 'buscar')
        botonCompra.clicked.connect(self.busqueda_compra)

        self.populate_cbox_id()

    def populate_cbox_id(self):
       
        cbxId = self.findChild(QComboBox, 'cbxId')
        cbxId.clear()

       
        id_compras = self._listado_compra_model.get_compra()
        for id_compra in id_compras:
            cbxId.addItem(str(id_compra[0]))  

    def busqueda_compra(self):
        cbxId = self.findChild(QComboBox, 'cbxId')
        selected_compra_id = cbxId.currentText() 
        self.tblcompra.setRowCount(0)

        if selected_compra_id:
            compra = self._listado_compra_model.get_compra_details(selected_compra_id)
            print(selected_compra_id)

            if compra:
                for row_num, compra_data in enumerate(compra):
                    self.tblcompra.insertRow(row_num)
                    for col_num, value in enumerate(compra_data):
                        item = QTableWidgetItem(str(value))
                        self.tblcompra.setItem(row_num, col_num, item)

