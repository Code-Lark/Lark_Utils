import re
import sys
from functools import partial

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, \
    QLineEdit


class MainWindow(QMainWindow):
    """
    这是一个使用 PyQt5 创建的简单的GUI应用程序的类。

    这个类定义了一个主窗口，其中包含一个文本编辑框和一个按钮。当按钮被点击时，它会计算并打印出文本编辑框中输入的文本的行数。
    """

    def __init__(self):
        """
        构造函数：初始化类的实例。

        调用父类的构造函数进行初始化，然后调用initUI方法来初始化用户界面。
        """
        # 调用父类的构造函数，确保类的继承链被正确初始化
        super().__init__()

        # flag
        self.fr_flag=False

        # 调用initUI方法来初始化用户界面，确保界面元素被正确设置
        self.result_text_edit = None
        self.upper_button = None
        self.lower_button=None
        self.main_text_edit = None

        # 帆软部分
        self.fr_date_input=None
        self.fr_toggle_button=None

        self.initUI()

        self.timer = QTimer(self)
        self.timer.setInterval(500)  # 500毫秒
        self.timer.timeout.connect(self.input_valid)
        self.main_text_edit.textChanged.connect(self.start_timer)

    def initUI(self):
        """
        初始化用户界面。
        设置窗口标题和尺寸，创建文本编辑区和按钮，并连接按钮点击事件到相应的处理方法。
        最后，将这些组件添加到布局中，并将布局设置为中央小部件。
        """
        # 设置窗口标题
        self.setWindowTitle('SQL CHANGE')
        # 设置窗口的位置和大小
        self.setGeometry(100, 100, 400, 300)
        # 创建主文本编辑区
        self.main_text_edit = QTextEdit(self)
        self.main_text_edit.textChanged.connect(self.start_timer)

        # 创建大写转换按钮，并连接点击事件到大写转换方法
        self.upper_button = QPushButton('UPPER', self)
        self.upper_button.clicked.connect(self.to_upper)
        # 创建小写转换按钮，并连接点击事件到小写转换方法
        self.lower_button = QPushButton('LOWER', self)
        self.lower_button.clicked.connect(self.to_lower)
        # 创建结果显示文本编辑区
        self.result_text_edit = QTextEdit(self)
        self.result_text_edit.setText('hello')
        # 创建垂直布局
        main_layout = QVBoxLayout()
        # 将主文本编辑区添加到布局中
        main_layout.addWidget(self.main_text_edit)
        # 创建大写和小写转换按钮的水平布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upper_button)
        button_layout.addWidget(self.lower_button)
        main_layout.addLayout(button_layout)
        # 创建帆软日期输入框和转换按钮的水平布局
        fr_layout = QHBoxLayout()
        # 帆软日期输入框
        self.fr_date_input = QLineEdit(self)
        # self.fr_date_input.setMaximumHeight(28)
        self.fr_date_input.setPlaceholderText("yyyy-mm-dd")
        fr_layout.addWidget(self.fr_date_input)
        # 帆软转换按钮
        self.fr_toggle_button = QPushButton('转帆软', self)
        self.fr_toggle_button.clicked.connect(partial(self.fr_toggle_change, self.fr_flag))
        fr_layout.addWidget(self.fr_toggle_button)
        main_layout.addLayout(fr_layout)
        # 将结果显示文本编辑区添加到布局中
        main_layout.addWidget(self.result_text_edit)
        # 创建一个容器小部件，并设置其布局为之前创建的布局
        container = QWidget()
        container.setLayout(main_layout)
        # 将容器设置为中央小部件
        self.setCentralWidget(container)

        # self.main_text_edit.textChanged.disconnect(self.input_valid)
        # self.main_text_edit.textChanged.connect(self.start_timer)

    def start_timer(self):
        self.timer.start()


    def input_valid(self):
        """
        检查输入
        """
        text=self.main_text_edit.toPlainText()

        # 检查text中是否包含${}
        if '${' in text:
            self.fr_flag=True
            self.fr_toggle_button.setText('转回SQL')
        else:
            self.fr_flag = False
            self.fr_toggle_button.setText('转为帆软')


    def to_upper(self):
        text = self.main_text_edit.toPlainText()
        # line_count = len(text.split('\n'))
        # print(f'Line count: {line_count}')
        self.result_text_edit.setText(text.upper())

    def to_lower(self):
        text = self.main_text_edit.toPlainText()
        # line_count = len(text.split('\n'))
        # print(f'Line count: {line_count}')
        self.result_text_edit.setText(text.lower())

    def fr_toggle_change(self, flag):
        """
        flag：true 转为sql语句，false：转为帆软语句
        :param flag:
        :return:
        """
        if self.fr_date_input.text()=='':
            text = self.main_text_edit.toPlainText()
            # 提取 text 中的第一个日期
            # 定义正则表达式模式
            date_pattern = r'\d{4}-\d{2}-\d{2}'

            # 使用 re.findall 查找所有匹配的日期
            dates = re.findall(date_pattern, text)
            print(dates)

            if len(dates) > 0:
                self.fr_date_input.setText(dates[0])
                self.result_text_edit.setText('日期不能为空,确认预测日期无误后再次点击')
            else:
                print('未找到日期')
                self.result_text_edit.setText('日期不能为空,且未找到日期')

            return

        yyyy_mm_dd=self.fr_date_input.toPlainText()
        yyyymmdd=yyyy_mm_dd.replace('-', '')
        yyyy=yyyy_mm_dd[0:4]

        text:str=self.main_text_edit.toPlainText()

        if flag:
            pass
        else:
            text=text.replace(yyyy_mm_dd,'${dt}')
            text=text.replace(yyyymmdd,'${format(dt,"yyyyMMdd")}')
            text=text.replace(yyyy,'${format(dt,"yyyy")}')
            self.result_text_edit.setText(text)



if __name__ == '__main__':
    # 创建QApplication对象，初始化应用程序
    app = QApplication(sys.argv)

    # 实例化主窗口对象
    window = MainWindow()

    # 显示主窗口
    window.show()

    # 执行应用程序，并在退出时返回状态码
    sys.exit(app.exec_())
