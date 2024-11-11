import sys
from tabnanny import check

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QAction, QDialog, QVBoxLayout, QLabel, QPushButton, \
    QStackedWidget

from ui.tool_bar_ui import TextToolbar
from ui.tool_menu.date_ui import DatePage
from ui.tool_menu.text_ui import TextPage
from ui.tool_menu.sql_ui import SqlPage


class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_toolbar = None
        self.stacked_widget = None
        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 创建菜单栏
        self.create_menu_bar()

        # 创建工具栏
        self.create_tool_bar()


        # 设置窗口属性
        self.setWindowTitle('Lark_Utils')
        self.setGeometry(100, 100, 800, 600)

    def create_tabs(self):
        # 创建第一个标签页
        tab1 = QWidget()
        layout1 = QVBoxLayout()
        label1 = QLabel('这是第一个标签页')
        button1 = QPushButton('按钮1')
        layout1.addWidget(label1)
        layout1.addWidget(button1)
        tab1.setLayout(layout1)
        self.tab_widget.addTab(tab1, '标签页1')

        # 创建第二个标签页
        tab2 = QWidget()
        layout2 = QVBoxLayout()
        label2 = QLabel('这是第二个标签页')
        button2 = QPushButton('按钮2')
        layout2.addWidget(label2)
        layout2.addWidget(button2)
        tab2.setLayout(layout2)
        self.tab_widget.addTab(tab2, '标签页2')

        # 创建第三个标签页
        tab3 = QWidget()
        layout3 = QVBoxLayout()
        label3 = QLabel('这是第三个标签页')
        button3 = QPushButton('按钮3')
        layout3.addWidget(label3)
        layout3.addWidget(button3)
        tab3.setLayout(layout3)
        self.tab_widget.addTab(tab3, '标签页3')

    def create_menu_bar(self):
        # 创建菜单栏
        menubar = self.menuBar()

        # 创建文件菜单
        self.create_file_menu(menubar)

        # 创建编辑菜单
        self.create_check_menu(menubar)

        self.create_tool_menu(menubar)

        # 创建两个页面
        text_page = TextPage(self.stacked_widget)
        date_page = DatePage(self.stacked_widget)
        sql_page = SqlPage(self.stacked_widget)

        self.stacked_widget.addWidget(text_page)
        self.stacked_widget.addWidget(date_page)
        self.stacked_widget.addWidget(sql_page)

    def create_file_menu(self, menubar):
        # 创建文件菜单
        file_menu = menubar.addMenu('文件')

    def create_check_menu(self, menubar):
        # 创建编辑菜单
        edit_menu = menubar.addMenu('查看')

        # 创建编辑菜单中的动作
        view_text_tool_action = QAction('文本工具栏', self,checkable=True)
        view_text_tool_action.setStatusTip('显示/隐藏文本工具栏')
        view_text_tool_action.setChecked(True)
        view_text_tool_action.triggered.connect(self.toggle_text_tool_bar)
        # paste_action = QAction('粘贴', self)
        # cut_action = QAction('剪切', self)

        # 将动作添加到编辑菜单
        edit_menu.addAction(view_text_tool_action)
        # edit_menu.addAction(paste_action)
        # edit_menu.addAction(cut_action)

    def toggle_text_tool_bar(self, flag):
        if flag:
            self.text_toolbar.show()
            print(flag)
        else:
            self.text_toolbar.hide()
            print(flag)

    def create_tool_menu(self, menubar):
        # 创建工具菜单
        tool_menu = menubar.addMenu('工具')

        tool_menu.addAction('文本', lambda: self.stacked_widget.setCurrentIndex(0))
        tool_menu.addAction('日期', lambda: self.stacked_widget.setCurrentIndex(1))
        tool_menu.addAction('SQL', lambda: self.stacked_widget.setCurrentIndex(2))

    def create_tool_bar(self):
        """
        创建工具栏
        :return:
        """
        self.text_toolbar=TextToolbar(self)
        self.addToolBar(self.text_toolbar)




    def show_new_dialog(self):
        # 创建一个简单的对话框
        dialog = QDialog(self)
        dialog.setWindowTitle('新建对话框')

        # 创建对话框的布局
        layout = QVBoxLayout()

        # 添加一个标签和一个按钮
        label = QLabel('这是一个新的对话框')
        button = QPushButton('确定')
        button.clicked.connect(dialog.accept)  # 关闭对话框

        # 将控件添加到布局中
        layout.addWidget(label)
        layout.addWidget(button)

        # 设置对话框的布局
        dialog.setLayout(layout)

        # 显示对话框
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomePage()
    window.show()
    sys.exit(app.exec_())
