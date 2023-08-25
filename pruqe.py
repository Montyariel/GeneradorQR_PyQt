import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QGraphicsLineItem, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QMessageBox
from PyQt6.QtGui import QPixmap, QFont, QPen, QColor
from PyQt6.QtCore import Qt, QTimer
import sqlite3
import datetime
import qrcode

class PantallaInicio(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pantalla de Inicio")
        self.setFixedSize(360, 640)  # Establecer tamaño fijo de la ventana

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Logo en la parte superior centrado horizontalmente
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("C:/Users/ariel/generadorQr/qrcodes/logo/logomapsa.png")  # Ruta a tu imagen de logo
        logo_pixmap = logo_pixmap.scaledToHeight(200)  # Altura deseada del logo
        logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignHCenter)

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

        # Ajustar la longitud de los campos
        self.campo_codigo.setMinimumWidth(300)
        self.campo_descripcion.setMinimumWidth(300)
        self.campo_peso.setMinimumWidth(300)
        self.campo_cantidad.setMinimumWidth(300)

        # Botón de guardar con estilo personalizado
        self.boton_guardar = QPushButton("Guardar")
        self.boton_guardar.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        layout.addWidget(self.boton_guardar, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Botón de generar QR con estilo personalizado
        self.boton_qr = QPushButton("Generar QR")
        self.boton_qr.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        layout.addWidget(self.boton_qr, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Botón de siguiente
        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setStyleSheet("background-color: #2196F3; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        layout.addWidget(self.boton_siguiente, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Conectar el botón de guardar a la función
        self.boton_guardar.clicked.connect(self.guardar_datos)

        # Conectar el botón de generar QR a la función
        self.boton_qr.clicked.connect(self.generar_qr)

        # Conectar el botón de siguiente a la función
        self.boton_siguiente.clicked.connect(self.limpiar_campos)

        # Leyenda de error en campos vacíos
        self.mensaje_error = QLabel("")
        self.mensaje_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensaje_error.setStyleSheet("color: black; font-weight: bold;")

        # Leyenda de éxito en guardar
        self.mensaje_exito = QLabel("")
        self.mensaje_exito.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mensaje_exito.setStyleSheet("color: green; font-weight: bold;")

        layout.addWidget(self.mensaje_error, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.mensaje_exito, alignment=Qt.AlignmentFlag.AlignCenter)

        # Inicializar gráficos para las líneas de mensajes
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)

        # Timer para animar las líneas de mensaje
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animar_lineas_mensaje)

        # Variables de posición para animar las líneas de mensaje
        self.linea_x = 0
        self.linea_y = 20

        # Bandera para controlar la animación
        self.animando = False

        # Crear la tabla si no existe
        self.crear_tabla()

    def crear_tabla(self):
        try:
            conn = sqlite3.connect("movimientos.db")
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movimientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo TEXT,
                    descripcion TEXT,
                    peso REAL,
                    cantidad INTEGER,
                    fecha_hora TEXT,
                    usuario TEXT,
                    sector TEXT
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            self.mostrar_mensaje(f"Error al crear la tabla: {e}", is_error=True)

    def guardar_datos(self):
        codigo = self.campo_codigo.text()
        descripcion = self.campo_descripcion.text()
        peso = self.campo_peso.text()
        cantidad = self.campo_cantidad.text()

        if codigo and descripcion and peso and cantidad:
            try:
                conn = sqlite3.connect("movimientos.db")
                cursor = conn.cursor()

                fecha_hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("INSERT INTO movimientos (codigo, descripcion, peso, cantidad, fecha_hora, usuario, sector) VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (codigo, descripcion, peso, cantidad, fecha_hora_actual, "NombreUsuario", "Sector"))

                conn.commit()
                conn.close()

                self.mostrar_mensaje("Guardado exitoso", is_error=False)
            except Exception as e:
                self.mostrar_mensaje(f"Error al guardar los datos: {e}", is_error=True)
        else:
            self.mostrar_mensaje("Faltan completar algunos campos.", is_error=True)

    def mostrar_mensaje(self, mensaje, is_error=False):
        if is_error:
            self.mensaje_error.setStyleSheet("color: red; font-weight: bold;")
            self.mensaje_error.setText(mensaje)
            self.animar_lineas_mensaje()
        else:
            self.mensaje_exito.setStyleSheet("color: green; font-weight: bold;")
            self.mensaje_exito.setText(mensaje)
            self.animar_lineas_mensaje()

    def animar_lineas_mensaje(self):
        if not self.animando:
            self.animando = True
            self.linea_x = 0
            self.timer.start(100)

    def generar_qr(self):
        codigo = self.campo_codigo.text()
        descripcion = self.campo_descripcion.text()
        peso = self.campo_peso.text()
        cantidad = self.campo_cantidad.text()

        if codigo and descripcion and peso and cantidad:
            try:
                unique_code = f"{codigo}_{descripcion}_{peso}_{cantidad}"
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(unique_code)
                qr.make(fit=True)

                qr_image = qr.make_image(fill_color="black", back_color="white")
                qr_image_path = f"qrcodes/{unique_code}.png"
                qr_image.save(qr_image_path)

                self.mostrar_mensaje("Código QR generado.", is_error=False)
            except Exception as e:
                self.mostrar_mensaje(f"Error al generar el código QR: {e}", is_error=True)
        else:
            self.mostrar_mensaje("Faltan completar algunos campos.", is_error=True)

    def limpiar_campos(self):
        self.campo_codigo.clear()
        self.campo_descripcion.clear()
        self.campo_peso.clear()
        self.campo_cantidad.clear()
        self.mostrar_mensaje("", is_error=False)

def main():
    app = QApplication(sys.argv)
    ventana = PantallaInicio()
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

