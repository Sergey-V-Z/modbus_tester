import sys  # sys нужен для передачи argv в QApplication
import os

from PyQt5 import QtWidgets
from port import serial_ports, speeds
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

import serial
# import time
import serial.tools.list_ports

import MBtester  # Это наш конвертированный файл дизайна


class ExampleApp(QtWidgets.QMainWindow, MBtester.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.Port.addItems(serial_ports())
        self.Speed.addItems(speeds)
        self.realport = None
        self.ConnectButton.clicked.connect(self.connect)
        self.EnableBtn.clicked.connect(self.send)
        self.pushButton.clicked.connect(self.browse_folder)  # подключаем функцию к кнопке

# иконки для кнопок
#         icon = QIcon()
#         icon.addFile('icon/Dossier.ico', state=QIcon.Off)
#         icon.addFile('icon/Dossier.ico', state=QIcon.On)
#         self.toolButton.setIcon(icon)
#         self.toolButton.setIconSize(QSize(50, 50))
#         self.toolButton.setGeometry(50, 50, 200, 200)

    def connect(self):
        try:
            self.realport = serial.Serial(self.Port.currentText(), int(self.Speed.currentText()))
            self.ConnectButton.setStyleSheet("background-color: green")
            self.ConnectButton.setText('Подключено')
        except Exception as e:
            print(e)

    def send(self):
        if self.realport:
            self.realport.write(b'b')

    def browse_folder(self):
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            for file_name in os.listdir(directory):  # для каждого файла в директории
                self.listWidget.addItem(file_name)  # добавить файл в listWidget


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
