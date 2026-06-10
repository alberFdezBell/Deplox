import sys
import os
import json
import requests
import subprocess
import zipfile
import shutil
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton,
    QListWidget, QListWidgetItem,
    QLabel, QMessageBox, QFileDialog
)

from PySide6.QtCore import Qt

CONFIG_FILE = "config.json"
DOWNLOAD_FOLDER = "downloads"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"apps": []}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"apps": []}


class Installer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IT Installer")
        self.setMinimumSize(600, 400)

        self.data = load_config()

        self.init_ui()
        self.load()

    def init_ui(self):
        w = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Selecciona apps"))

        self.list = QListWidget()
        self.list.setSelectionMode(QListWidget.NoSelection)

        layout.addWidget(self.list)

        btn = QPushButton("Instalar")
        btn.clicked.connect(self.run)

        layout.addWidget(btn)

        w.setLayout(layout)
        self.setCentralWidget(w)

    def load(self):
        self.list.clear()

        for app in self.data.get("apps", []):
            item = QListWidgetItem(app["name"])

            # ✅ FIX PySide6 (antes: 0 → ERROR)
            item.setCheckState(Qt.CheckState.Unchecked)

            item.setData(1000, app)
            self.list.addItem(item)

    def download(self, url, path):
        r = requests.get(url, stream=True)
        r.raise_for_status()

        with open(path, "wb") as f:
            for c in r.iter_content(chunk_size=1024):
                if c:
                    f.write(c)

    def run(self):
        selected_apps = []
        
        for i in range(self.list.count()):
            item = self.list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                app = item.data(1000)
                selected_apps.append(app)

        if not selected_apps:
            QMessageBox.warning(self, "Aviso", "Selecciona al menos una app")
            return

        # Obtener carpeta de descargas del usuario
        downloads_folder = str(Path.home() / "Downloads")
        
        # Diálogo para elegir ubicación de descarga
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"paquete_instalacion_{timestamp}.zip"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar paquete de instalación",
            os.path.join(downloads_folder, default_filename),
            "ZIP Files (*.zip)"
        )

        if not file_path:
            return

        try:
            # Descargar archivos temporales
            temp_folder = os.path.join(DOWNLOAD_FOLDER, "temp_pack")
            os.makedirs(temp_folder, exist_ok=True)

            downloaded_files = []

            for app in selected_apps:
                try:
                    if app["type"] == "url":
                        filename = app["name"] + ".exe"
                        path = os.path.join(temp_folder, filename)
                        self.download(app["source"], path)
                        downloaded_files.append((filename, path))

                    elif app["type"] == "file":
                        # Copiar archivo local
                        if os.path.exists(app["source"]):
                            filename = os.path.basename(app["source"])
                            path = os.path.join(temp_folder, filename)
                            shutil.copy(app["source"], path)
                            downloaded_files.append((filename, path))

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo descargar {app['name']}: {str(e)}")

            # Crear ZIP
            if downloaded_files:
                with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as z:
                    for filename, filepath in downloaded_files:
                        z.write(filepath, arcname=filename)

                # Limpiar temporal
                shutil.rmtree(temp_folder)

                # Mostrar éxito y abrir carpeta
                response = QMessageBox.information(
                    self,
                    "OK",
                    f"ZIP creado exitosamente:\n\n{os.path.basename(file_path)}\n\n¿Deseas abrir la carpeta?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if response == QMessageBox.Yes:
                    os.startfile(os.path.dirname(file_path))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear ZIP: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Installer()
    w.show()
    sys.exit(app.exec())