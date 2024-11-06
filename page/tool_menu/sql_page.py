from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QAction


class SqlPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        # 创建布局
        layout = QVBoxLayout()

        # 创建 QAction 和按钮
        # text_action = QAction("Go to Page 2", self)
        # # text_action.triggered.connect(self.go_to_page_2)
        button1 = QPushButton("Go to Page 2sql")
        # button1.setDefaultAction(text_action)  # 将 QAction 绑定到按钮
        layout.addWidget(button1)

        # 设置布局
        self.setLayout(layout)

    def go_to_page_2(self):
        self.stacked_widget.setCurrentIndex(1)