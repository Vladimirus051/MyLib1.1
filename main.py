import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
                             QHeaderView, QTextEdit, QDialog, QDialogButtonBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sqlite3
import subprocess


class BookApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadBooks()

    def initUI(self):
        self.setWindowTitle('MyLib')
        self.setGeometry(100, 100, 1000, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #1c1c1e;
                color: #f5f5f7;
            }
            QLabel {
                color: #f5f5f7;
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #3a3a3c;
                border-radius: 5px;
                background-color: #2c2c2e;
                color: #f5f5f7;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #0a84ff;
            }
            QLineEdit[placeholderText], QTextEdit[placeholderText] {
                color: #8e8e93;
            }
            QPushButton {
                background-color: #0a84ff;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0060df;
            }
            QTableWidget {
                background-color: #2c2c2e;
                color: #f5f5f7;
                border: 1px solid #3a3a3c;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #3a3a3c;
                color: #f5f5f7;
                font-size: 14px;
                border: 1px solid #3a3a3c;
            }
        """)

        main_layout = QVBoxLayout()
        form_layout = QGridLayout()

        label_font = QFont("Arial", 12)
        input_font = QFont("Arial", 10)

        # Название книги
        lbl_name = QLabel('Название книги:')
        lbl_name.setFont(label_font)
        self.name_input = QLineEdit(self)
        self.name_input.setFont(input_font)
        self.name_input.setPlaceholderText('Введите название книги')
        form_layout.addWidget(lbl_name, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)

        # Автор
        lbl_author = QLabel('Автор:')
        lbl_author.setFont(label_font)
        self.author_input = QLineEdit(self)
        self.author_input.setFont(input_font)
        self.author_input.setPlaceholderText('Введите автора книги')
        form_layout.addWidget(lbl_author, 1, 0)
        form_layout.addWidget(self.author_input, 1, 1)

        # Жанр
        lbl_genre = QLabel('Жанр:')
        lbl_genre.setFont(label_font)
        self.genre_input = QLineEdit(self)
        self.genre_input.setFont(input_font)
        self.genre_input.setPlaceholderText('Введите жанр книги')
        form_layout.addWidget(lbl_genre, 2, 0)
        form_layout.addWidget(self.genre_input, 2, 1)

        # Рейтинг
        lbl_rating = QLabel('Рейтинг:')
        lbl_rating.setFont(label_font)
        self.rating_input = QLineEdit(self)
        self.rating_input.setFont(input_font)
        self.rating_input.setPlaceholderText('Введите рейтинг книги')
        form_layout.addWidget(lbl_rating, 3, 0)
        form_layout.addWidget(self.rating_input, 3, 1)

        # Статус
        lbl_status = QLabel('Статус:')
        lbl_status.setFont(label_font)
        self.status_input = QLineEdit(self)
        self.status_input.setFont(input_font)
        self.status_input.setPlaceholderText('Введите статус книги')
        form_layout.addWidget(lbl_status, 4, 0)
        form_layout.addWidget(self.status_input, 4, 1)

        # PDF файл
        lbl_pdf = QLabel('PDF файл:')
        lbl_pdf.setFont(label_font)
        self.pdf_path_input = QLineEdit(self)
        self.pdf_path_input.setFont(input_font)
        self.pdf_path_input.setPlaceholderText('Путь к PDF')
        form_layout.addWidget(lbl_pdf, 5, 0)
        form_layout.addWidget(self.pdf_path_input, 5, 1)

        # Комментарии
        lbl_comments = QLabel('Комментарии:')
        lbl_comments.setFont(label_font)
        self.comments_input = QTextEdit(self)
        self.comments_input.setFont(input_font)
        self.comments_input.setPlaceholderText('Введите комментарии')
        self.comments_input.setFixedHeight(100)
        form_layout.addWidget(lbl_comments, 6, 0)
        form_layout.addWidget(self.comments_input, 6, 1)

        # Кнопка загрузки PDF
        self.upload_pdf_btn = QPushButton('Загрузить PDF', self)
        self.upload_pdf_btn.setFont(label_font)
        self.upload_pdf_btn.clicked.connect(self.uploadPDF)
        form_layout.addWidget(self.upload_pdf_btn, 7, 0, 1, 2)

        # Кнопка добавления книги
        self.submit_btn = QPushButton('Добавить книгу', self)
        self.submit_btn.setFont(label_font)
        self.submit_btn.clicked.connect(self.addBook)
        form_layout.addWidget(self.submit_btn, 8, 0, 1, 2)

        main_layout.addLayout(form_layout)

        # Таблица для отображения книг
        self.table = QTableWidget(self)
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Автор', 'Жанр', 'Рейтинг', 'Статус', 'PDF файл', 'Комментарии', 'Открыть', 'Удалить',
             'Коммент.'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def uploadPDF(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить PDF файл", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.pdf_path_input.setText(file_path)

    def loadBooks(self):
        conn = sqlite3.connect('my_lib.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
            view_btn = QPushButton('Открыть')
            view_btn.setFont(QFont("Arial", 10))
            view_btn.clicked.connect(self.viewBook)
            self.table.setCellWidget(i, 8, view_btn)

            delete_btn = QPushButton('Удалить')
            delete_btn.setFont(QFont("Arial", 10))
            delete_btn.clicked.connect(self.deleteBook)
            self.table.setCellWidget(i, 9, delete_btn)

            comment_btn = QPushButton('Коммент.')
            comment_btn.setFont(QFont("Arial", 10))
            comment_btn.clicked.connect(self.viewComments)
            self.table.setCellWidget(i, 10, comment_btn)

    def addBook(self):
        name = self.name_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        rating = self.rating_input.text()
        status = self.status_input.text()
        pdf_path = self.pdf_path_input.text()
        comments = self.comments_input.toPlainText()

        if not all([name, author, genre, rating, status, pdf_path]):
            return

        conn = sqlite3.connect('my_lib.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (name, author, genre, rating, status, pdf_path, comments) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, author, genre, rating, status, pdf_path, comments))
        conn.commit()
        conn.close()

        self.clearInputs()
        self.loadBooks()

    def deleteBook(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        book_id = self.table.item(index.row(), 0).text()

        conn = sqlite3.connect('my_lib.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        conn.close()

        self.loadBooks()

    def viewBook(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        pdf_path = self.table.item(index.row(), 6).text()

        if pdf_path and os.path.exists(pdf_path):
            try:
                if sys.platform == 'win32':
                    os.startfile(pdf_path)
                elif sys.platform == 'darwin':
                    subprocess.call(['open', pdf_path])
                else:
                    subprocess.call(['xdg-open', pdf_path])
            except Exception as e:
                print(f'Не удалось открыть PDF файл: {e}')
        else:
            print('Путь к PDF файлу не найден или файл не существует!')

    def viewComments(self):
        button = self.sender()
        index = self.table.indexAt(button.pos())
        comments = self.table.item(index.row(), 7).text()

        dialog = QDialog(self)
        dialog.setWindowTitle("Комментарии")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1c1c1e;
                color: #f5f5f7;
            }
            QLabel, QTextEdit {
                font-size: 14px;
                padding: 8px;
                border: 1px solid #3a3a3c;
                border-radius: 5px;
                background-color: #2c2c2e;
                color: #f5f5f7;
            }
        """)

        layout = QVBoxLayout(dialog)
        comments_text = QTextEdit(dialog)
        comments_text.setText(comments)
        comments_text.setReadOnly(True)
        layout.addWidget(comments_text)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok, Qt.Horizontal, dialog)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.exec_()

    def clearInputs(self):
        self.name_input.clear()
        self.author_input.clear()
        self.genre_input.clear()
        self.rating_input.clear()
        self.status_input.clear()
        self.pdf_path_input.clear()
        self.comments_input.clear()

    def cellClicked(self, row, column):
        # Do nothing for now
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BookApp()
    ex.show()
    sys.exit(app.exec_())
