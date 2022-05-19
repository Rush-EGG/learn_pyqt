import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 窗体标题
        self.setWindowTitle('NB的xx系统')

        # 窗体尺寸
        self.resize(980, 450)

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
