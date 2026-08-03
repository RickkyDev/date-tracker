import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.utils import getResourcePath
from src.appController import AppController

def main():
    app = QApplication(sys.argv)

    appIcon = QIcon(getResourcePath("src/icon.png"))
    app.setWindowIcon(appIcon)
    
    app.setQuitOnLastWindowClosed(False)

    appController = AppController(app)
    appController.start()

    sys.exit(app.exec())

main()