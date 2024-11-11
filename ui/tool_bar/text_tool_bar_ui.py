from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction, qApp


class TextToolbar(QToolBar):
    def __init__(self,parent=None):
        # super().__init__(parent)
        super(TextToolbar, self).__init__("Text Toolbar", parent)
        self.parent=parent
        # self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        # 转大写
        toUpperAct = QAction(QIcon('./res/img/touppercase'), '转大写', self)
        toUpperAct.setShortcut('Ctrl+U')
        toUpperAct.triggered.connect(self.to_upper)

        # 转小写
        toLowerAct = QAction(QIcon('./res/img/tolowercase'), '转小写', self)
        toLowerAct.setShortcut('Ctrl+L')
        toLowerAct.triggered.connect(self.to_lower)

        self.addAction(toUpperAct)
        self.addAction(toLowerAct)


    def to_upper(self):

        text:str=self.parent.stacked_widget.currentWidget().main_text_edit.textCursor().selectedText()
        text=text.upper()

        self.parent.stacked_widget.currentWidget().main_text_edit.textCursor().insertText(text)

    def to_lower(self):
        text:str=self.parent.stacked_widget.currentWidget().main_text_edit.textCursor().selectedText()
        text=text.lower()
        self.parent.stacked_widget.currentWidget().main_text_edit.textCursor().insertText(text)




