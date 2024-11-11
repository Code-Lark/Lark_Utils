import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolBar, QAction, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter, QTextCursor
from PyQt5.QtCore import QRegularExpression, QTimer

class SqlHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        self.highlighting_rules = []

        # SQL Keyword rules
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))
        keywords = [
            'SELECT', 'select', 'FROM', 'from', 'WHERE', 'where', 'INSERT', 'insert', 'UPDATE', 'update', 'DELETE',
            'delete',
            'CREATE', 'create', 'ALTER', 'alter', 'DROP', 'drop', 'TABLE', 'table', 'INDEX', 'index', 'VIEW', 'view',
            'JOIN', 'join', 'INNER', 'inner', 'LEFT', 'left', 'RIGHT', 'right', 'FULL', 'full', 'OUTER', 'outer', 'ON',
            'on',
            'AND', 'and', 'OR', 'or', 'NOT', 'not', 'IN', 'in', 'BETWEEN', 'between', 'LIKE', 'like', 'AS', 'as',
            'DISTINCT', 'distinct', 'GROUP', 'group', 'BY', 'by', 'ORDER', 'order', 'ASC', 'asc', 'DESC', 'desc',
            'LIMIT', 'limit', 'OFFSET', 'offset', 'CASE', 'case', 'WHEN', 'when', 'THEN', 'then', 'ELSE', 'else', 'END',
            'end',
            'EXISTS', 'exists', 'UNION', 'union', 'ALL', 'all', 'ANY', 'any', 'SOME', 'some', 'NULL', 'null', 'IS',
            'is',
            'TRUE', 'true', 'FALSE', 'false'
        ]
        for word in keywords:
            pattern = QRegularExpression(r'\b' + word + r'\b')
            rule = (pattern, keyword_format)
            self.highlighting_rules.append(rule)

        # Function name rule
        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#0000FF"))
        self.highlighting_rules.append((QRegularExpression(r'\b[A-Za-z0-9_]+(?=\()'), function_format))

        # Single and double-quoted string rules
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#800000"))
        self.highlighting_rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        self.highlighting_rules.append((QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))

        # Comment rules
        single_line_comment_format = QTextCharFormat()
        single_line_comment_format.setForeground(QColor("#008800"))
        self.highlighting_rules.append((QRegularExpression(r'--.*'), single_line_comment_format))

        multi_line_comment_format = QTextCharFormat()
        multi_line_comment_format.setForeground(QColor("#777777"))
        self.multi_line_comment_format = multi_line_comment_format

        self.tri_single = (QRegularExpression(r"/\*"), 1, self.multi_line_comment_format)
        self.tri_double = (QRegularExpression(r"\*/"), 2, self.multi_line_comment_format)

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

        self.setCurrentBlockState(0)

        # Multi-line comments
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, start_delimiter, in_state, style):
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = start_delimiter.match(text).capturedStart()
            add = start_delimiter.match(text).capturedLength()

        while start >= 0:
            end = self.tri_double[0].match(text[start + add:]).capturedStart()
            if end >= add:
                length = end - start + add + self.tri_double[0].match(text[start + add:]).capturedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            self.setFormat(start, length, style)

            # 更新 start 位置，避免无限循环
            start = start_delimiter.match(text[start + length:]).capturedStart()

        if self.currentBlockState() == in_state:
            return True
        else:
            return False
