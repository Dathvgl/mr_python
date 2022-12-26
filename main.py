import sys

from os import path
from PIL import Image
from PyQt6.QtWidgets import QApplication

from window import DesktopApp


def main():
    app = QApplication(sys.argv)
    # win = DesktopApp()
    # win.show()

    dir = "D:/Hen/Manga/Viet lam/[0] Oneshot/[Akiba Maou (Akiha@)] Kamimachi Kansai Musume Kimeseku Choukyou/5.jpg"
    print(path.basename(dir))
    print(Image.open(dir).format)
    print(Image.open(dir).info["dpi"])
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
