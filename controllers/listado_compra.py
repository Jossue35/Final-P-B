from PyQt5.QtWidgets import  QTableWidgetItem, QTableWidget,QMainWindow, QLabel, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QIntValidator
from models import compras_model
from models.compras_model import CompraModel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QTableWidgetItem, QMessageBox, QPushButton, QVBoxLayout, QLabel
from PyQt5 import uic
import pathlib
from models.listado_compras_model import ListadoCompraModel
from controllers.categoria_form import CategoriaForm
from PyQt5.QtGui import QIcon

class ListadoCompraWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._listado_compra_model = ListadoCompraModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/compra.ui", self)

        botonCompra = self.findChild(QPushButton, 'buscar')
        botonCompra.clicked.connect(self.busqueda_compra)

        # Populate the QComboBox with id_compra values
        self.populate_cbox_id()

    def populate_cbox_id(self):
        # Clear existing items in the QComboBox
        cbxId = self.findChild(QComboBox, 'cbxId')
        cbxId.clear()

        # Get id_compra values from the model
        id_compras = self._listado_compra_model.get_compra()

        # Populate QComboBox with id_compra values
        for id_compra in id_compras:
            cbxId.addItem(str(id_compra[0]))  # Assuming id_compra is the first element in the tuple

    def busqueda_compra(self):
        # Retrieve selected id_compra from QComboBox
        cbxId = self.findChild(QComboBox, 'cbxId')
        selected_compra_id = cbxId.currentText()  # Use a different variable name

        # Clear existing items in the table
        self.tblcompra.setRowCount(0)

        # Check if compra is not None before populating the table
        if selected_compra_id:
            compra = self._listado_compra_model.get_compra_details(selected_compra_id)
            print(selected_compra_id)

            if compra:
                for row_num, compra_data in enumerate(compra):
                    self.tblcompra.insertRow(row_num)
                    for col_num, value in enumerate(compra_data):
                        item = QTableWidgetItem(str(value))
                        self.tblcompra.setItem(row_num, col_num, item)
