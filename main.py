import sys

from PyQt5.QtWidgets import QApplication

from ui.home_ui import HomePage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())