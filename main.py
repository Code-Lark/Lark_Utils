import sys

from PyQt5.QtWidgets import QApplication

from ui.home_ui import HomePage
from utils.db_utils import initialize_database

if __name__ == '__main__':
    initialize_database()

    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())