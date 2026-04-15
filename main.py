import sys
import subprocess
import json
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)

        # Layout principal
        layout = QVBoxLayout(self)

        # Seletor de tema
        self.theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setCurrentText(current_settings.get("theme", "Light"))
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)

        # Caixa de seleção para ícones
        self.icons_check = QCheckBox("Show Icons")
        self.icons_check.setChecked(current_settings.get("show_icons", True))
        layout.addWidget(self.icons_check)

        # Botões de diálogo
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_settings(self):
        return {
            "theme": self.theme_combo.currentText(),
            "show_icons": self.icons_check.isChecked()
        }

class IDEManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Books - IDE Manager")
        self.setGeometry(100, 100, 500, 400)

        # Menu Bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # File
        file_menu = self.menu_bar.addMenu("File")
        open_action = file_menu.addAction("Open")
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        # Edit
        edit_menu = self.menu_bar.addMenu("Edit")
        edit_menu.addAction("Preferences")

        # View
        view_menu = self.menu_bar.addMenu("View")
        view_menu.addAction("Toggle Fullscreen")

        # Settings
        settings_menu = self.menu_bar.addMenu("Settings")
        settings_action = settings_menu.addAction("Appearance")
        settings_action.triggered.connect(self.open_settings)

        # Configurações Padrão
        self.settings = {
            "theme": "Dark",
            "show_icons": True
        }
        self.load_settings()

        # IDEs pré-configuradas
        self.ides = {
            "VS Code": "code",
            "CLion": "clion",
            "IntelliJ IDEA": "idea",
            "PyCharm": "charm",
        }

        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Lista de IDEs
        self.list_widget = QListWidget()
        self.update_ide_list()
        layout.addWidget(self.list_widget)

        # Adicionar IDEs
        add_layout = QHBoxLayout()
        self.name_input = QLineEdit(placeholderText="IDE Name")
        self.cmd_input = QLineEdit(placeholderText="Execute command")
        add_layout.addWidget(QLabel("Name:"))
        add_layout.addWidget(self.name_input)
        add_layout.addWidget(QLabel("Command:"))
        add_layout.addWidget(self.cmd_input)
        layout.addLayout(add_layout)

        # Botões
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add IDE")
        self.add_button.clicked.connect(self.add_ide)
        self.remove_button = QPushButton("Remove IDE")
        self.remove_button.clicked.connect(self.remove_ide)
        self.open_button = QPushButton("Open IDE")
        self.open_button.clicked.connect(self.open_ide)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.remove_button)
        button_layout.addWidget(self.open_button)
        layout.addLayout(button_layout)

    def update_ide_list(self):
        self.list_widget.clear()
        for name in self.ides.keys():
            self.list_widget.addItem(name)

    def add_ide(self):
        name = self.name_input.text().strip()
        cmd = self.cmd_input.text().strip()
        if name and cmd:
            self.ides[name] = cmd
            self.update_ide_list()
            self.name_input.clear()
            self.cmd_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Put the name and command for the IDE!")

    def remove_ide(self):
        selected = self.list_widget.currentItem()
        if selected:
            del self.ides[selected.text()]
            self.update_ide_list()

    def open_ide(self):
        selected = self.list_widget.currentItem()
        if selected:
            ide_name = selected.text()
            cmd = self.ides[ide_name]
            try:
                subprocess.Popen([cmd])
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Can't open IDE: {e}")

    def open_settings(self):
        dialog = SettingsDialog(self.settings, self)  # Passe self.settings em vez de self
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_settings = dialog.get_settings()
            self.settings.update(new_settings)
            self.apply_theme()
            self.save_settings()

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                loaded_settings = json.load(f)
                self.settings.update(loaded_settings)
        except FileNotFoundError:
            pass

    def apply_theme(self):
        if self.settings["theme"] == "Dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #333; color: #fff; }
                QListWidget { background-color: #444; color: #fff; }
                QLineEdit { background-color: #555; color: #fff; }
                QPushButton { background-color: #666; color: #fff; }
            """)
        else:
            self.setStyleSheet("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IDEManager()
    window.show()
    sys.exit(app.exec())