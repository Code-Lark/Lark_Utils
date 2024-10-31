import re
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout


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
        self.text_edit_second = None
        self.button_up = None
        self.button_low=None
        self.text_edit_first = None

        # 帆软部分
        self.fr_date=None
        self.fr_toggle=None

        self.initUI()

    def initUI(self):
        """
        初始化用户界面。

        设置窗口标题和尺寸，创建文本编辑区和按钮，并连接按钮点击事件到行数统计方法。
        最后，将这些组件添加到布局中，并将布局设置为中央小部件。
        """
        # 设置窗口标题
        self.setWindowTitle('SQL CHANGE')
        # 设置窗口的位置和大小
        self.setGeometry(100, 100, 400, 300)

        # 创建文本编辑区
        self.text_edit_first = QTextEdit(self)
        self.text_edit_first.textChanged.connect(self.input_valid)
        # 创建按钮，并连接点击事件到统计行数的方法
        self.button_up = QPushButton('UPPER', self)
        self.button_up.clicked.connect(self.to_upper)

        # 创建按钮
        self.button_low = QPushButton('LOWER', self)
        self.button_low.clicked.connect(self.to_lower)

        # 创建一个label
        self.text_edit_second = QTextEdit(self)
        self.text_edit_second.setText('hello')

        # 创建垂直布局
        layout = QVBoxLayout()
        # 将文本编辑区和按钮添加到布局中
        layout.addWidget(self.text_edit_first)

        # 大小写转换按钮
        layout_btn=QHBoxLayout()
        layout_btn.addWidget(self.button_up)
        layout_btn.addWidget(self.button_low)
        layout.addLayout(layout_btn)

        # 转换为帆软部分、转换回帆软部分
        layout_fr=QHBoxLayout()
        # 帆软日期 提示写入日期格式
        self.fr_date=QTextEdit(self)
        self.fr_date.setMaximumHeight(28)
        self.fr_date.setPlaceholderText("yyyy-mm-dd")
        layout_fr.addWidget(self.fr_date)
        self.fr_toggle=QPushButton('转帆软', self)
        self.fr_toggle.clicked.connect(lambda: self.fr_toggle_change(self.fr_flag))


        layout_fr.addWidget(self.fr_toggle)
        layout.addLayout(layout_fr)



        layout.addWidget(self.text_edit_second)

        # 创建一个容器小部件，并设置其布局为之前创建的布局
        container = QWidget()
        container.setLayout(layout)
        # 将容器设置为中央小部件
        self.setCentralWidget(container)

    def input_valid(self):
        """
        检查输入
        """
        text=self.text_edit_first.toPlainText()

        # 检查text中是否包含${}
        if '${' in text:
            self.fr_flag=True
            self.fr_toggle.setText('转回SQL')
        else:
            self.fr_flag = False
            self.fr_toggle.setText('转为帆软')


    def to_upper(self):
        text = self.text_edit_first.toPlainText()
        # line_count = len(text.split('\n'))
        # print(f'Line count: {line_count}')
        self.text_edit_second.setText(text.upper())

    def to_lower(self):
        text = self.text_edit_first.toPlainText()
        # line_count = len(text.split('\n'))
        # print(f'Line count: {line_count}')
        self.text_edit_second.setText(text.lower())

    def fr_toggle_change(self, flag):
        """
        flag：true 转为sql语句，false：转为帆软语句
        :param flag:
        :return:
        """
        if self.fr_date.toPlainText()=='':
            text = self.text_edit_first.toPlainText()
            # 提取 text 中的第一个日期
            # 定义正则表达式模式
            date_pattern = r'\d{4}-\d{2}-\d{2}'

            # 使用 re.findall 查找所有匹配的日期
            dates = re.findall(date_pattern, text)
            print(dates)

            if len(dates) > 0:
                self.fr_date.setText(dates[0])
                self.text_edit_second.setText('日期不能为空,确认预测日期无误后再次点击')
            else:
                print('未找到日期')
                self.text_edit_second.setText('日期不能为空,且未找到日期')

            return

        yyyy_mm_dd=self.fr_date.toPlainText()
        yyyymmdd=yyyy_mm_dd.replace('-', '')
        yyyy=yyyy_mm_dd[0:4]

        text:str=self.text_edit_first.toPlainText()

        if flag:
            pass
        else:
            text=text.replace(yyyy_mm_dd,'${dt}')
            text=text.replace(yyyymmdd,'${format(dt,"yyyyMMdd")}')
            text=text.replace(yyyy,'${format(dt,"yyyy")}')
            self.text_edit_second.setText(text)



if __name__ == '__main__':
    # 创建QApplication对象，初始化应用程序
    app = QApplication(sys.argv)

    # 实例化主窗口对象
    window = MainWindow()

    # 显示主窗口
    window.show()

    # 执行应用程序，并在退出时返回状态码
    sys.exit(app.exec_())
