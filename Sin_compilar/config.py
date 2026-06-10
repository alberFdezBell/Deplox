import sys
import os
import json
import shutil

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget,
    QListWidgetItem, QLabel,
    QLineEdit, QFileDialog, QMessageBox
)

CONFIG_FILE = "config.json"
LOCAL_FOLDER = "local_files"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"apps": []}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {"apps": []}
            return json.loads(content)
    except:
        return {"apps": []}


def save_config(data):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class ConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CONFIG IT TOOL")
        self.setMinimumSize(600, 450)

        self.data = load_config()

        self.init_ui()
        self.refresh()

    def init_ui(self):
        container = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("CONFIGURADOR IT"))

        # Inputs
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre de la app")
        layout.addWidget(self.name_input)

        # URL/Archivo
        url_file_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("URL o ruta del archivo")
        url_file_layout.addWidget(self.url_input)
        
        btn_file = QPushButton("Seleccionar archivo")
        btn_file.clicked.connect(self.pick_file)
        url_file_layout.addWidget(btn_file)
        
        layout.addLayout(url_file_layout)

        # Lista
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # Botones de acción
        btn_del = QPushButton("Eliminar seleccionado")
        btn_del.clicked.connect(self.delete)
        layout.addWidget(btn_del)

        btn_save = QPushButton("Guardar configuración")
        btn_save.clicked.connect(self.save_entry)
        layout.addWidget(btn_save)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.selected_file = None

    def pick_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo")
        if file_path:
            self.url_input.setText(file_path)

    def save_entry(self):
        name = self.name_input.text().strip()
        source = self.url_input.text().strip()

        if not name or not source:
            QMessageBox.warning(self, "Error", "Nombre y URL/archivo son requeridos")
            return

        # Detectar si es un archivo local o URL
        if os.path.exists(source) and os.path.isfile(source):
            os.makedirs(LOCAL_FOLDER, exist_ok=True)
            dest = os.path.join(LOCAL_FOLDER, os.path.basename(source))
            shutil.copy(source, dest)
            entry_type = "file"
            entry_source = dest
        else:
            entry_type = "url"
            entry_source = source

        self.data["apps"].append({
            "name": name,
            "type": entry_type,
            "source": entry_source
        })

        self.refresh()
        self.name_input.clear()
        self.url_input.clear()
        QMessageBox.information(self, "OK", f"'{name}' agregado y guardado")
        save_config(self.data)

    def delete(self):
        item = self.list_widget.currentItem()
        if not item:
            return

        name = item.text().split(" - ")[0]

        self.data["apps"] = [
            a for a in self.data["apps"]
            if a["name"] != name
        ]

        self.refresh()
        save_config(self.data)

    def refresh(self):
        self.list_widget.clear()

        for app in self.data["apps"]:
            self.list_widget.addItem(
                f"{app['name']} - {app['type']} - {app['source']}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigApp()
    window.show()
    sys.exit(app.exec())