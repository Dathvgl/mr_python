from os import walk
from PyQt6 import QtCore, QtGui, QtWidgets

from based import decent


class DesktopApp(QtWidgets.QWidget):
    __SPACE = 30
    __SIZE = 16
    __BASESEEN = 30

    __BASEDWIDTH = 800
    __BASEDHEIGHT = 600

    __flexSeen = 0

    __resized = QtCore.pyqtSignal()

    __indexed = 0
    __chaps = []
    __images = []

    __keyLast = False
    __keyCombine = ""

    def __init__(self):
        super().__init__()
        self.__init()
        self.__setup_folder()
        self.__setup_scroll()
        self.__resized.connect(self.__resize_all)

    def __init(self):
        BASEDWIDTH = self.__BASEDWIDTH
        BASEDHEIGHT = self.__BASEDHEIGHT

        self.setBaseSize(BASEDWIDTH, BASEDHEIGHT)
        self.setMinimumSize(BASEDWIDTH, BASEDHEIGHT)
        self.setWindowIcon(QtGui.QIcon("./icon.jpg"))
        self.setWindowTitle("Desktop App Python")
        self.__center()

    def resizeEvent(self, event):
        self.__resized.emit()
        return super(DesktopApp, self).resizeEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        self.__keyLast = True
        if event.key() == QtCore.Qt.Key.Key_Alt:
            self.__keyRecord("alt")
        elif event.key() == QtCore.Qt.Key.Key_Shift:
            self.__keyRecord("shift")
        else:
            if self.__keyCombine == "":
                self.__keyLast = False
            self.__keyRecord(event.text())

    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
        if self.__keyLast:
            self.__keyShotcuts()
            self.__keyCombine = ""
        self.__keyLast = False

    def __keyRecord(self, label: str):
        if label in self.__keyCombine:
            return
        if self.__keyCombine == "":
            self.__keyCombine = label
        else:
            self.__keyCombine += "+" + label

    def __keyShotcuts(self):
        SHOTCUT = self.__keyCombine
        if "alt" in SHOTCUT and "q" in SHOTCUT:
            self.__alt_chapter(1)
        elif "alt" in SHOTCUT and "w" in SHOTCUT:
            self.__alt_chapter(-1)
        elif "alt" in SHOTCUT and "s" in SHOTCUT:
            self.__flexSeen += 100
            self.__alt_scroll()
        elif "alt" in SHOTCUT and "a" in SHOTCUT:
            self.__flexSeen -= 100
            self.__alt_scroll()

    def __alt_chapter(self, num: int):
        CURRENT = self.__indexed + num
        if CURRENT > -1 and CURRENT < len(self.__chaps) - 1:
            self.__indexed = CURRENT
            self.__setup_chapter()

    def __resize_all(self):
        SPACE = self.__SPACE
        SIZE = self.__SIZE

        WIDTH = self.width()
        HEIGHT = self.height()

        self.__dirPath.move(WIDTH - self.__dirPath.width() - SIZE, SPACE)
        self.__lineEdit.resize(
            WIDTH - (WIDTH - self.__dirPath.pos().x()) - SIZE * 3, SPACE)

        HSCROLL = SPACE * 3

        self.__scroll.resize(WIDTH, HEIGHT - HSCROLL)
        self.__scroll.move(0, HSCROLL)
        self.__alt_scroll()

    def __center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __open_select(self):
        directory = str(QtWidgets.QFileDialog.getExistingDirectory())
        self.__lineEdit.setText('{}'.format(directory.replace("/", "\\")))

        DIR = self.__directory()
        if DIR == "":
            return

        all = next(walk(DIR))[1]

        self.__indexed = 0
        self.__chaps.clear()
        self.__images.clear()

        for dir in all:
            self.__chaps.append(DIR + "\\" + dir)

        self.__setup_chapter()

    def __setup_chapter(self):
        self.__images.clear()
        CURRENT = walk(self.__chaps[self.__indexed])
        for __, __, files in CURRENT:
            for image in files:
                full = self.__chaps[self.__indexed] + "\\" + image
                self.__images.append(full.replace("\\", "/"))

        self.__scroll.verticalScrollBar().setSliderPosition(0)
        self.__alt_scroll()

    def __setup_folder(self):
        SPACE = self.__SPACE
        SIZE = self.__SIZE

        self.__dirPath = QtWidgets.QToolButton(self)
        self.__dirPath.setFont(QtGui.QFont("Times", SIZE))
        self.__dirPath.resize(SPACE, SPACE)
        self.__dirPath.setObjectName("__dirPath")
        self.__dirPath.clicked.connect(self.__open_select)

        self.__lineEdit = QtWidgets.QLineEdit(self)
        self.__lineEdit.setFont(QtGui.QFont("Times", SIZE))
        self.__lineEdit.setEnabled(False)
        self.__lineEdit.move(SPACE, SPACE)
        self.__lineEdit.setObjectName("__lineEdit")

        self.__retranslate()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslate(self):
        _translate = QtCore.QCoreApplication.translate
        self.__dirPath.setText(_translate("Directory", "..."))

    def __directory(self):
        return self.__lineEdit.text()

    def __setup_scroll(self):
        self.__scrollLayout = QtWidgets.QVBoxLayout()
        self.__scrollWidget = QtWidgets.QWidget()
        self.__scroll = QtWidgets.QScrollArea(self)

        self.__scrollLayout.setSpacing(0)
        self.__scrollLayout.addStretch(0)
        self.__scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.__scrollLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.__scrollWidget.setLayout(self.__scrollLayout)

        self.__scroll.setWidgetResizable(True)
        self.__scroll.setWidget(self.__scrollWidget)

    def __alt_scroll(self):
        BASESEEN = self.__BASESEEN
        WIDTH = self.width()
        WSCROLL = WIDTH - int(decent(WIDTH, BASESEEN))

        while self.__scrollLayout.count():
            child = self.__scrollLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        IMAGES = self.__images
        for item in IMAGES:
            image = QtGui.QPixmap(item)
            label = QtWidgets.QLabel(self)

            label.setScaledContents(True)
            label.setPixmap(image.scaledToWidth(
                WSCROLL + self.__flexSeen,
                QtCore.Qt.TransformationMode.SmoothTransformation))
            self.__scrollLayout.addWidget(label)
