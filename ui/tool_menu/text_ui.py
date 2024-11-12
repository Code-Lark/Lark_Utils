import re
from functools import partial

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QHBoxLayout, QLineEdit, \
    QStackedWidget

from utils.common_utils import send_notification


class TextPage(QWidget):
    def __init__(self, stacked_widget, timer_interval=500):
        """
        构造函数：初始化类的实例。

        参数:
        - stacked_widget (QStackedWidget): 用于管理多个页面的堆叠窗口部件。
        - timer_interval (int): 计时器的时间间隔（毫秒）。
        """
        if not isinstance(stacked_widget, QStackedWidget):
            raise ValueError("stacked_widget must be an instance of QStackedWidget")
        super().__init__()
        self.stacked_widget = stacked_widget

        # 初始化标志变量
        self.fr_flag = False

        # 初始化用户界面元素
        self.result_text_edit = None
        self.upper_button = None
        self.lower_button = None
        self.main_text_edit = None

        # 初始化帆软相关的界面元素
        self.fr_date_input = None
        self.fr_toggle_button = None

        # 调用 initUI 方法初始化用户界面
        try:
            self.initUI()
        except Exception as e:
            print(f"Error initializing UI: {e}")
            raise

        # 设置计时器
        self.timer = QTimer(self)
        self.timer.setInterval(timer_interval)  # 使用可配置的时间间隔
        self.timer.timeout.connect(self.input_valid)
        # self.main_text_edit.textChanged.connect(self.start_timer)


    def start_timer(self):
        """
        启动计时器，但仅在计时器未活动时启动。
        """
        if not self.timer.isActive():
            self.timer.start()

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

        # 创建结果显示文本编辑区
        self.result_text_edit = QTextEdit(self)
        self.result_text_edit.setText('hello')
        # 创建垂直布局
        main_layout = QVBoxLayout()
        # 将主文本编辑区添加到布局中
        main_layout.addWidget(self.main_text_edit)
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

        self.setLayout(main_layout)


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

        yyyy_mm_dd=self.fr_date_input.text()
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



    def go_to_page(self,index):
        self.stacked_widget.setCurrentIndex(index)