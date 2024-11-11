import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolBar, QAction, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter, QTextCursor
from PyQt5.QtCore import QRegularExpression, QTimer


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        self.highlighting_rules = []

        # Keyword, operator, and brace rules
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))
        keywords = [
            'and', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally',
            'for', 'from', 'global', 'if', 'import', 'in',
            'is', 'lambda', 'not', 'or', 'pass', 'print',
            'raise', 'return', 'try', 'while', 'yield', 'None'
        ]
        for word in keywords:
            pattern = QRegularExpression(r'\b' + word + r'\b')
            rule = (pattern, keyword_format)
            self.highlighting_rules.append(rule)

        # Class name rule
        class_format = QTextCharFormat()
        class_format.setFontWeight(QFont.Bold)
        class_format.setForeground(QColor("#0000AA"))
        self.highlighting_rules.append((QRegularExpression(r'\bQ[A-Za-z]+\b'), class_format))

        # Single and double-quoted string rules
        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(QColor("#008800"))
        self.highlighting_rules.append((QRegularExpression(r'#.*'), single_line_comment_format))

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#800000"))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), quotation_format))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), quotation_format))

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#0000FF"))
        self.highlighting_rules.append((QRegularExpression(r'\b[A-Za-z0-9_]+(?=\()'), function_format))

        self.multi_line_comment_format = QTextCharFormat()
        self.multi_line_comment_format.setForeground(QColor("#777777"))

        self.tri_single = (QRegularExpression(r"'''"), 1, self.multi_line_comment_format)
        self.tri_double = (QRegularExpression(r'"""'), 2, self.multi_line_comment_format)

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        self.setCurrentBlockState(0)

        # Multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter.match(text).capturedStart()
            add = delimiter.match(text).capturedLength()

        while start >= 0:
            end = delimiter.match(text[start + add:]).capturedStart()
            if end >= add:
                length = end - start + add + delimiter.match(text[start + add:]).capturedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            self.setFormat(start, length, style)

            # 更新 start 位置，避免无限循环
            start = delimiter.match(text[start + length:]).capturedStart()

        if self.currentBlockState() == in_state:
            return True
        else:
            return False