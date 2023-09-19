from CONSTANTS import MEME_FOLDER, CURSOR, UIC_FOLDER, RESULT_FOLDER
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QLabel, \
    QColorDialog
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic
from functional_code.create_meme import change_results, search_results
from functional_code.add_tag import addition
from functional_code.add_meme import add
from functional_code.saving import export


# основное окно
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UIC_FOLDER / "main_window.ui"), self)
        self.create_meme.clicked.connect(self.creating_meme)
        self.add_template.clicked.connect(self.addition)
        self.add_tag.clicked.connect(self.tag_add)

    # переходы в другие окна
    def creating_meme(self):
        self.hide()
        selector.placeholder.clear()
        selector.restart()
        selector.show()

    def addition(self):
        self.hide()
        adder.show()
        adder.restart()

    def tag_add(self):
        self.hide()
        tag_adder.show()
        tag_adder.restart()


# выбор поиск
class Selection(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UIC_FOLDER / "creator.ui"), self)
        self.restart()
        self.search.clicked.connect(self.search_results)
        self.names_list.itemClicked.connect(self.preview)
        self.result.itemClicked.connect(self.preview)
        self.tags_list.itemClicked.connect(self.change_results)
        self.select.clicked.connect(self.redactor)
        self.back.clicked.connect(self.go_back)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.go_back()

    # сброс
    def restart(self):
        self.file = None
        self.result.clear()
        self.tags_list.clear()
        self.names_list.clear()
        meme_names = CURSOR.execute("select title from memes").fetchall()
        for meme in meme_names:
            self.names_list.addItem(meme[0])
        tags = CURSOR.execute("select tag from tags").fetchall()
        for tag in tags:
            self.tags_list.addItem(tag[0])

    # поиск
    def search_results(self):
        self.result.clear()
        results = search_results(
            self.search_bar.text())
        for result in results:
            self.result.addItem(result)

    # из тэгов
    def change_results(self):
        self.result.clear()
        results = change_results(self.tags_list.
                                 currentItem().text())
        for result in results:
            self.result.addItem(result)

    # другое окно
    def go_back(self):
        self.hide()
        main_window.show()

    # превьюшка
    def preview(self):
        selected_meme = self.sender().currentItem().text()
        file_name = CURSOR.execute("select file_name from memes where title "
                                   "= ?", (selected_meme,)).fetchall()[0][0]
        self.file = str(MEME_FOLDER / file_name)
        self.placeholder.setPixmap(QPixmap(self.file).scaled(
            590, 580, Qt.KeepAspectRatio))

    # следующее окно
    def redactor(self):
        self.hide()
        redactor.run()
        redactor.show()


# редач
class Redactor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UIC_FOLDER / "redactor.ui"), self)
        self.back.clicked.connect(self.go_back)
        self.add_text.clicked.connect(self.add_a_text)
        self.text_labels = dict()
        self.selected = False
        self.size_.valueChanged.connect(self.change_size)
        self.texts.itemClicked.connect(self.movement)
        self.color.clicked.connect(self.color_choice)
        self.saving.clicked.connect(self.save_meme)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.go_back()

    # меняет размер текста
    def change_size(self):
        try:
            self.text_labels[self.texts.currentItem().text()][0].setFont(
                QFont("Impact", self.size_.value()))
            self.text_labels[self.texts.currentItem().text()][1] = \
                self.size_.value()
            self.text_labels[self.texts.currentItem().text()][0].setGeometry(
                self.text_labels[self.texts.currentItem().text()][0].x(),
                self.text_labels[self.texts.currentItem().text()][0].y(),
                len(self.texts.currentItem().text()) * self.size_.value() + 4,
                self.size_.value() * 2)
        except AttributeError:
            pass

    # меняет цвет текста
    def color_choice(self):
        try:
            color = QColorDialog.getColor()
            self.item.setStyleSheet("color: rgb({}, {}, {});"
                                    "background-color: "
                                    "rgba(0, 0, 0, 0)".format(
                color.red(), color.green(), color.blue()))
            self.text_labels[self.item.text()[1:]][-1] = color
        except AttributeError:
            error.show()

    # выбирает текст
    def movement(self):
        self.item = self.text_labels[self.texts.currentItem().text()][0]
        self.size_.setValue(self.text_labels[self.texts.currentItem().text(
        )][1])

    # лочит текст
    def mousePressEvent(self, event):
        try:
            self.to_item = [event.x() - self.item.x(),
                            event.y() - self.item.y()]
        except AttributeError:
            pass

    # перемещает текст
    def mouseMoveEvent(self, event):
        try:
            if 10 <= event.x() - self.to_item[0] \
                    <= 810 - self.item.width() + 20 \
                    and\
                    10 <= event.y() - self.to_item[1] <= \
                    810 - self.item.height():
                self.item.move(event.x() - self.to_item[0],
                               event.y() - self.to_item[1])
        except AttributeError:
            pass

    # возвращает к предыдушему окну
    def go_back(self):
        self.hide()
        selector.show()

    # сетит выбранную картинку
    def run(self):
        if selector.file is not None:
            self.placeholder.setAlignment(Qt.AlignCenter)

            self.placeholder.setPixmap(QPixmap(selector.file).
                                       scaled(800, 800, Qt.KeepAspectRatio))
            self.texts.clear()

    # добавляет текст
    def add_a_text(self):
        if self.text.text() != '':
            self.texts.addItem(self.text.text())
            new_text = QLabel(self)
            new_text.setGeometry(410, 410, len(self.text.text()) * 16 + 30, 32)
            new_text.setText(' ' + self.text.text())
            new_text.setFont(QFont("Impact", 16))
            new_text.setStyleSheet("background-color: rgba(0, 0, 0, 0);"
                                   "color: rgba(0, 0, 0, 255);"
                                   "outline: 10px solid black")
            self.text_labels[self.text.text()] = [new_text, 16, QColor(0,
                                                                       0,
                                                                       0)]
            new_text.show()
        self.text.clear()

    # сохранение
    def save_meme(self):
        if self.name.text() != '':
            result = export(QPixmap(selector.file),
                            self.text_labels)
            for text in self.text_labels.keys():
                self.text_labels[text][0].deleteLater()
            self.texts.clear()
            self.text_labels = dict()
            result.save(str(RESULT_FOLDER / f'{self.name.text()}.png'))
            self.hide()
            main_window.show()
        else:
            error.show()
        self.restart()

    # ребутит
    def restart(self):
        self.text_labels.clear()
        self.texts.clear()


# новый мем
class AddMeme(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UIC_FOLDER / "adder.ui"), self)
        self.restart()
        self.file.clicked.connect(self.choose_file)
        self.saving.clicked.connect(self.addition)
        self.back.clicked.connect(self.go_back)

    # ребут
    def restart(self):
        self.name.clear()
        self.tags.clear()
        self.file_name = ''
        tags = CURSOR.execute("select tag from tags").fetchall()
        for tag in tags:
            self.tags.addItem(tag[0])
        self.filename.setText('')

    # выбор файла
    def choose_file(self):
        self.file_name = QFileDialog.getOpenFileName(self,
                                                     'chose a pic',
                                                     "",
                                                     "Images "
                                                     "(*.png *.jpg)")[0]
        self.filename.setText(self.file_name[self.file_name.rfind('/') + 1:])

    # добавляет в базу
    def addition(self):
        result = add(self.file_name, self.name.text(),
                     self.tags.selectedItems())
        if result == -1:
            error.show()
        tag_adder.restart()
        selector.restart()
        self.restart()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.go_back()

    # другое окно
    def go_back(self):
        self.hide()
        main_window.show()


# новый тэг
class TagAdder(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UIC_FOLDER / "tagadder.ui"), self)
        self.restart()
        self.saving.clicked.connect(self.addition)
        self.back.clicked.connect(self.go_back)

    # ребут
    def restart(self):
        self.name.clear()
        self.memes.clear()
        all_meme_names = CURSOR.execute("select title from memes").fetchall()
        for meme in all_meme_names:
            self.memes.addItem(meme[0])

    # добавляет в дб
    def addition(self):
        result = addition(self.name.text(), self.memes.selectedItems())
        if result == -1:
            error.show()
        selector.restart()
        adder.restart()
        self.restart()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.go_back()

    # другое окно
    def go_back(self):
        self.hide()
        main_window.show()


# ошибка
class Error(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(str(UIC_FOLDER / "error.ui"), self)
        self.closing.clicked.connect(self.go_back)

    def go_back(self):
        self.hide()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    selector = Selection()
    redactor = Redactor()
    adder = AddMeme()
    tag_adder = TagAdder()
    error = Error()
    sys.excepthook = except_hook
    sys.exit(app.exec())
