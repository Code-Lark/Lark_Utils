import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction

from highlighter.python_highlighter import PythonHighlighter
from highlighter.sql_highlighter import SqlHighlighter
from utils.common_utils import resource_path


class CodeToolbar(QToolBar):

    def __init__(self,parent=None):
        # super().__init__(parent)
        super(CodeToolbar, self).__init__("Code Toolbar", parent)
        self.highlighter = None
        self.parent=parent
        # self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # python 代码高亮
        # python_act = QAction(QIcon('./resources/img/Python.png'), 'Python高亮', self)
        python_act = QAction(QIcon(resource_path(os.path.join("resources/img","Python.png"))), 'Python高亮', self)
        python_act.triggered.connect(self.code_highlight_python)
        self.addAction(python_act)

        # sql 代码高亮
        sql_act = QAction(QIcon(resource_path(os.path.join("resources/img","sql.png"))), 'SQL高亮', self)
        sql_act.triggered.connect(self.code_highlight_sql)
        self.addAction(sql_act)

        self.rehighlight_timer = QTimer(self)
        self.rehighlight_timer.setSingleShot(True)
        self.rehighlight_timer.timeout.connect(self.rehighlight)

    def code_highlight_python(self):
        """
        设置 python 代码高亮
        :return:
        """
        self.highlighter = PythonHighlighter(self.parent.stacked_widget.currentWidget().main_text_edit.document())
        self.parent.stacked_widget.currentWidget().main_text_edit.textChanged.connect(self.schedule_rehighlight)

    def code_highlight_sql(self):
        """
        设置 sql 代码高亮
        :return:
        """
        self.highlighter= SqlHighlighter(self.parent.stacked_widget.currentWidget().main_text_edit.document())
        self.parent.stacked_widget.currentWidget().main_text_edit.textChanged.connect(self.schedule_rehighlight)


    def schedule_rehighlight(self):
        self.rehighlight_timer.start(200)  # 延迟 200 毫秒后重新高亮

    def rehighlight(self):
        self.highlighter.rehighlight()