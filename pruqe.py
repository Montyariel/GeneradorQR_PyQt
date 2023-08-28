import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMenu, QAction
from PyQt6.QtGui import QPixmap, QFont, QCursor, QIcon
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation
import sqlite3
import datetime
import qrcode

class PantallaInicio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(360, 640)  # Tamaño fijo de la ventana

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Logo en la parte superior pegado al borde superior
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("C:/Users/ariel/generadorQr/qrcodes/logo/logomapsa.png")  # Ruta a tu imagen de logo
        logo_pixmap = logo_pixmap.scaledToHeight(200)  # Altura deseada del logo
        logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # Campo de entrada para Código
        self.campo_codigo = QLineEdit(self)
        self.campo_codigo.setPlaceholderText("Ingrese Código")
        layout.addWidget(self.campo_codigo, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Campo de entrada para Descripción de Material
        self.campo_descripcion = QLineEdit(self)
        self.campo_descripcion.setPlaceholderText("Descripción de Material")
        layout.addWidget(self.campo_descripcion, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Campo de entrada para Peso
        self.campo_peso = QLineEdit(self)
        self.campo_peso.setPlaceholderText("Ingrese Peso")
        layout.addWidget(self.campo_peso, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Campo de entrada para Cantidad
        self.campo_cantidad = QLineEdit(self)
        self.campo_cantidad.setPlaceholderText("Ingrese Cantidad")
        layout.addWidget(self.campo_cantidad, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Personalizar botones
        self.boton_guardar = QPushButton("Guardar", self)
        self.estilo_boton(self.boton_guardar, "#2196F3")  # Azul
        layout.addWidget(self.boton_guardar, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.boton_qr = QPushButton("Generar QR", self)
        self.estilo_boton(self.boton_qr, "#2196F3")  # Azul
        layout.addWidget(self.boton_qr, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.boton_siguiente = QPushButton("Siguiente", self)
        self.estilo_boton(self.boton_siguiente, "#2196F3")  # Azul
        layout.addWidget(self.boton_siguiente, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Agregar botón de configuración para cambiar el tema
        self.boton_configuracion = QPushButton(self)
        self.boton_configuracion.setIcon(QIcon("C:/Users/ariel/generadorQr/qrcodes/config.png"))
        self.estilo_boton(self.boton_configuracion, "transparent")  # Sin fondo ni borde
        self.boton_configuracion.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(self.boton_configuracion, alignment=Qt.AlignmentFlag.AlignRight)

        self.boton_configuracion.clicked.connect(self.mostrar_menu_configuracion)

        # Conectar botones a funciones
        self.boton_guardar.clicked.connect(self.mostrar_datos)
        self.boton_qr.clicked.connect(self.generar_qr)
        self.boton_siguiente.clicked.connect(self.limpiar_campos)

        # Sección inferior oculta
        self.seccion_inferior = QWidget(self)
        self.seccion_inferior.hide()
        self.layout_seccion_inferior = QVBoxLayout(self.seccion_inferior)

        self.qr_label = QLabel(self)
        self.layout_seccion_inferior.addWidget(self.qr_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.tabla_datos = QTableWidget(self)
        self.tabla_datos.setColumnCount(4)
        self.tabla_datos.setHorizontalHeaderLabels(["Código", "Descripción", "Peso", "Cantidad"])
        self.layout_seccion_inferior.addWidget(self.tabla_datos, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.seccion_inferior)

        # Animación de deslizamiento
        self.animation = QPropertyAnimation(self.seccion_inferior, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(QRect(0, 320, 360, 320))
        self.animation.setEndValue(QRect(0, 0, 720, 640))  # Amplía el ancho de la pantalla

        # Tema actual (claro por defecto)
        self.tema_oscuro = False

    def estilo_boton(self, boton, color):
        boton.setStyleSheet(
            f"background-color: {color}; color: white; border: none; "
            "padding: 10px 20px; text-align: center; text-decoration: none; "
            "display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;"
        )

    def mostrar_datos(self):
        # Mostrar la sección inferior con animación
        if not self.seccion_inferior.isVisible():
            self.animation.start()
            self.seccion_inferior.show()

            # Aquí deberías agregar el código para mostrar el código QR en el QLabel qr_label
            # Puedes cargar la imagen del código QR y configurarla en qr_label

    def generar_qr(self):
        # Aquí va el código para generar el código QR y guardarlo en una ubicación específica
        # Luego, puedes usar la ubicación del archivo generado para mostrarlo en qr_label en la función mostrar_datos
        pass

    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.campo_codigo.clear()
        self.campo_descripcion.clear()
        self.campo_peso.clear()
        self.campo_cantidad.clear()

    def mostrar_menu_configuracion(self):
        menu = QMenu(self)

        tema_dia = QAction("Modo Día", self)
        tema_noche = QAction("Modo Noche", self)

        menu.addAction(tema_dia)
        menu.addAction(tema_noche)

        tema_dia.triggered.connect(self.activar_modo_dia)
        tema_noche.triggered.connect(self.activar_modo_noche)

        menu.exec_(self.boton_configuracion.mapToGlobal(self.boton_configuracion.rect().bottomRight()))

    def activar_modo_dia(self):
        self.setStyleSheet("")  # Eliminar cualquier hoja de estilo
        self.tema_oscuro = False

    def activar_modo_noche(self):
        self.setStyleSheet("background-color: #333; color: white;")  # Establecer estilo oscuro
        self.tema_oscuro = True

def main():
    app = QApplication(sys.argv)
    ventana = PantallaInicio()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
