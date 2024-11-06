import sys

from PyQt5.QtWidgets import QApplication

from page.home_page import HomePage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())