from PyQt5.QtWidgets import QDialog, QDateEdit, QTableWidgetItem, QTableWidget, QLabel,  QComboBox,  QLineEdit, QPushButton
from PyQt5.QtGui import QDoubleValidator
from models.compras_model import CompraModel
from PyQt5.QtCore import Qt
from PyQt5 import uic
import pathlib
from PyQt5.QtGui import QIcon, QPixmap

class ComprasWindow(QDialog):

    def __init__(self):
        super().__init__()
        self._compras_model = CompraModel()
        mod_path = pathlib.Path(__file__).parent.parent
        uic.loadUi(mod_path / "views/compras_window.ui", self)

        botonCompra = self.findChild(QPushButton, 'botonCompra')
        botonCompra.clicked.connect(self.realizar_compra)
        
        #ICONOS
        pixmap = QPixmap('logopng.png')
        pixmap = pixmap.scaledToWidth(231)  # Ajustar el ancho
        pixmap = pixmap.scaledToHeight(141)  # Ajustar la altura

        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setGeometry(390, 20, 231, 141)  # Establecer las dimensiones principal

        icon_path = "controllers/logopng.png"  # Reemplaza con la ruta real de tu icono
        self.setWindowIcon(QIcon(icon_path))

    def load_usuarios(self):
        usuarios = self._compras_model.get_usuario()
        print(usuarios)

        cbocompras = self.findChild(QComboBox, 'cbocompras')
        cbocompras.clear()

        for user_tuple in usuarios:
            user_string = ' '.join(map(str, user_tuple[1:]))
            cbocompras.addItem(user_string)

        for i, user_tuple in enumerate(usuarios):
            cbocompras.setItemData(i, user_tuple[0])  

    def realizar_compra(self):
        selected_user_id = self.findChild(QComboBox, 'cbocompras').currentData()
        selected_user_info = self.findChild(QComboBox, 'cbocompras').currentText()
        selected_date = self.findChild(QDateEdit, 'dateEdit').date().toString(Qt.ISODate)
        total_label = self.findChild(QLabel, 'total')

        product_info_list = []
        product_id_list = []
        total_value = 0.0

        table_widget = self.findChild(QTableWidget, 'tablacompras')
        for row in range(table_widget.rowCount()):
            try:
                id = int(table_widget.item(row, 0).text())
                nombre = table_widget.item(row, 1).text()
                precio = float(table_widget.item(row, 2).text())
                cantidad = float(table_widget.item(row, 3).text())
                unidades_lineedit = table_widget.cellWidget(row, 4)
                unidades = float(unidades_lineedit.text())

                
                total_product = precio * unidades
                total_value += total_product
                if unidades is not None and unidades != 0:
                    product_id_list.extend([id] * int(unidades))
                

                product_info_list.append("ID: {}, Producto: {}, Precio: {:.2f}, Cantidad: {:.2f}, Unidades: {:.2f}".format(id, nombre, precio, cantidad, unidades))
            except ValueError as e:
                print(f"Error processing row {row + 1}: {e}")

        total_label.setText(": {:.2f}".format(total_value))
        print(f"Compra realizada por: {selected_user_info} (ID: {selected_user_id}) en la fecha: {selected_date}")
        print("Productos:")
        for product_info in product_info_list:
            print(product_info)
        x = self._compras_model.insert_compra(selected_date,total_value,selected_user_id)
        for j in product_id_list:
            self._compras_model.insert_compra_producto(x,j)



    def load_productos(self):
        productos = self._compras_model.get_productos()
        print(productos)

        table_widget = self.findChild(QTableWidget, 'tablacompras')
        table_widget.setRowCount(0)

        for producto in productos:
            row_position = table_widget.rowCount()
            table_widget.insertRow(row_position)
            id_item = QTableWidgetItem(str(producto[0]))
            nombre_item = QTableWidgetItem(str(producto[1]))
            precio_item = QTableWidgetItem(str(producto[2]))
            cantidad_item = QTableWidgetItem(str(producto[3]))

            table_widget.setItem(row_position, 0, id_item)
            table_widget.setItem(row_position, 1, nombre_item)
            table_widget.setItem(row_position, 2, precio_item)
            table_widget.setItem(row_position, 3, cantidad_item)

            unidades_lineedit = QLineEdit()
            unidades_lineedit.setValidator(QDoubleValidator())

            table_widget.setCellWidget(row_position, 4, unidades_lineedit)

        