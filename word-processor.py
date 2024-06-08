import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox, QInputDialog, QFontDialog, QTabWidget, QWidget, QVBoxLayout, QLabel, QStatusBar
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import QDateTime
import os


class WordProcessor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.currentFont = QFont()  # Variable to store the current font
        self.fileContents = {}  # Dictionary to store the contents of each page

    def initUI(self):
        self.centralWidget = QTabWidget()
        self.setCentralWidget(self.centralWidget)
        self.addPage()  # Add a page at the start

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        newFileAction = QAction('&New File', self)
        newFileAction.setShortcut('Ctrl+N')
        newFileAction.triggered.connect(self.newFile)
        fileMenu.addAction(newFileAction)

        openFileAction = QAction('&Open File', self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.triggered.connect(self.openFile)
        fileMenu.addAction(openFileAction)

        saveFileAction = QAction('&Save File', self)
        saveFileAction.setShortcut('Ctrl+S')
        saveFileAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveFileAction)

        saveAsFileAction = QAction('&Save File As', self)
        saveAsFileAction.setShortcut('Ctrl+Shift+S')
        saveAsFileAction.triggered.connect(self.saveFileAs)
        fileMenu.addAction(saveAsFileAction)

        editMenu = menubar.addMenu('&Edit')

        boldAction = QAction('&Bold', self)
        boldAction.setShortcut('Ctrl+B')
        boldAction.triggered.connect(self.boldText)
        editMenu.addAction(boldAction)

        italicAction = QAction('&Italic', self)
        italicAction.setShortcut('Ctrl+I')
        italicAction.triggered.connect(self.italicText)
        editMenu.addAction(italicAction)

        underlineAction = QAction('&Underline', self)
        underlineAction.setShortcut('Ctrl+U')
        underlineAction.triggered.connect(self.underlineText)
        editMenu.addAction(underlineAction)

        fontAction = QAction('&Change Font', self)
        fontAction.setShortcut('Ctrl+T')
        fontAction.triggered.connect(self.changeFont)
        editMenu.addAction(fontAction)

        countWordsAction = QAction('&Word Count', self)
        countWordsAction.setShortcut('Ctrl+W')
        countWordsAction.triggered.connect(self.countWords)
        editMenu.addAction(countWordsAction)

        findReplaceAction = QAction('&Find and Replace', self)
        findReplaceAction.setShortcut('Ctrl+F')
        findReplaceAction.triggered.connect(self.findAndReplace)
        editMenu.addAction(findReplaceAction)

        pageMenu = menubar.addMenu('&Page')

        addPageAction = QAction('&Add Page', self)
        addPageAction.setShortcut('Ctrl+Shift+N')
        addPageAction.triggered.connect(self.addPage)
        pageMenu.addAction(addPageAction)

        deletePageAction = QAction('&Delete Current Page', self)
        deletePageAction.setShortcut('Ctrl+Shift+D')
        deletePageAction.triggered.connect(self.deletePage)
        pageMenu.addAction(deletePageAction)

        self.setWindowTitle('Enhanced Word Processor')
        self.setGeometry(100, 100, 800, 600)
        self.show()

    def newFile(self):
        self.centralWidget.clear()
        self.fileContents.clear()  # Reset contents when creating a new file
        self.addPage()

    def addPage(self):
        newPage = QWidget()
        layout = QVBoxLayout()

        headerLabel = QLabel("")  # Create a QLabel for the header
        layout.addWidget(headerLabel)

        textEdit = QTextEdit()
        textEdit.textChanged.connect(self.updateFooter)  # Connect textChanged signal to updateFooter
        layout.addWidget(textEdit)

        footer = QStatusBar()
        layout.addWidget(footer)

        newPage.setLayout(layout)
        self.centralWidget.addTab(newPage, f'Page {self.centralWidget.count() + 1}')

        self.updateFooter()  # Initial update of the footer
        self.updateHeader()  # Initial update of the header

    def updateHeader(self):
        currentWidget = self.centralWidget.currentWidget()
        headerLabel = currentWidget.findChild(QLabel)
        if headerLabel:
            headerLabel.setText(f"Created: {QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm:ss')}")

    def updateFooter(self):
        currentWidget = self.centralWidget.currentWidget()
        textEdit = currentWidget.findChild(QTextEdit)
        footer = currentWidget.findChild(QStatusBar)

        text = textEdit.toPlainText()
        wordCount = len(text.split())

        footer.showMessage(f'Word Count: {wordCount}')

    def countWords(self):
        currentWidget = self.centralWidget.currentWidget()
        textEdit = currentWidget.findChild(QTextEdit)
        text = textEdit.toPlainText()
        wordCount = len(text.split())
        QMessageBox.information(self, 'Word Count', f'The document contains {wordCount} words.')

    def deletePage(self):
        currentIndex = self.centralWidget.currentIndex()
        if currentIndex >= 0:
            self.centralWidget.removeTab(currentIndex)
            self.updatePageTitles()

    def updatePageTitles(self):
        for i in range(self.centralWidget.count()):
            self.centralWidget.setTabText(i, f'Page {i + 1}')

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt)')
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                self.fileContents[self.centralWidget.currentIndex()] = {'content': content, 'filename': filename}  # Save file content and name
                self.addPage()
                currentWidget = self.centralWidget.currentWidget()
                textEdit = currentWidget.findChild(QTextEdit)
                textEdit.setPlainText(content)
                textEdit.setFont(self.currentFont)

    def saveFile(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory', '')
        if not directory:
            return  # Cancelled by user

        for index in range(self.centralWidget.count()):
            currentWidget = self.centralWidget.widget(index)
            textEdit = currentWidget.findChild(QTextEdit)
            content = textEdit.toPlainText()

            filename = os.path.join(directory, f"page{index + 1}.txt")

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)

            self.fileContents[index] = {'content': content, 'filename': filename}  # Update file contents dictionary

    def saveFileAs(self):
        currentIndex = self.centralWidget.currentIndex()
        currentWidget = self.centralWidget.widget(currentIndex)
        textEdit = currentWidget.findChild(QTextEdit)
        content = textEdit.toPlainText()

        filename, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'Text Files (*.txt)')
        if filename:
            directory = os.path.dirname(filename)
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            self.fileContents[currentIndex] = {'content': content, 'filename': filename}  # Update file contents dictionary

    def boldText(self):
        currentWidget = self.centralWidget.currentWidget()
        textEdit = currentWidget.findChild(QTextEdit)
        format = textEdit.currentCharFormat()
        format.setFontWeight(QFont.Bold if format.fontWeight() == QFont.Normal else QFont.Normal)
        textEdit.setCurrentCharFormat(format)

    def italicText(self):
        currentWidget = self.centralWidget.currentWidget()
        textEdit = currentWidget.findChild(QTextEdit)
        format = textEdit.currentCharFormat()
        format.setFontItalic(not format.fontItalic())
        textEdit.setCurrentCharFormat(format)

    def underlineText(self):
        currentWidget = self.centralWidget.currentWidget()
        textEdit = currentWidget.findChild(QTextEdit)
        format = textEdit.currentCharFormat()
        format.setFontUnderline(not format.fontUnderline())
        textEdit.setCurrentCharFormat(format)

    def changeFont(self):
        currentWidget = self.centralWidget.currentWidget()
        textEdit = currentWidget.findChild(QTextEdit)
        cursor = textEdit.textCursor()

        font, ok = QFontDialog.getFont(self.currentFont)
        if ok:
            self.currentFont = font
            format = cursor.charFormat()
            format.setFont(font)
            cursor.setCharFormat(format)

    def findAndReplace(self):
        currentWidget = self.centralWidget.currentWidget()
        textEdit = currentWidget.findChild(QTextEdit)
        text = textEdit.toPlainText()

        findText, ok1 = QInputDialog.getText(self, 'Find and Replace', 'Find:')
        if ok1 and findText:
            if findText in text:
                replaceText, ok2 = QInputDialog.getText(self, 'Find and Replace', 'Replace with:')
                if ok2:
                    newText = text.replace(findText, replaceText)
                    textEdit.setPlainText(newText)
            else:
                QMessageBox.warning(self, 'Find and Replace', 'Text not found for replacement.')


def main():
    app = QApplication(sys.argv)
    ex = WordProcessor()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
