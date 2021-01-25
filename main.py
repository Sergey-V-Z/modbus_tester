import sys  # sys нужен для передачи argv в QApplication
import os

from PyQt5 import QtWidgets
from port import serial_ports, speeds

import serial
# import time
import serial.tools.list_ports

# import modeles_ui.MBtester as MBtester # Это наш конвертированный файл дизайна
# import modeles_ui.port_dialog as port_dialog
# import modeles_ui.add_dialog as add_dialog

from modeles_ui import MBtester
from modeles_ui import add_dialog
from modeles_ui import port_dialog


class ExampleApp(QtWidgets.QMainWindow, MBtester.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        print('Start')
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.Port.addItems(serial_ports())
        self.Speed.addItems(speeds)
        self.real_port = None
        self.ConnectButton.clicked.connect(self.connect)
        self.EnableBtn.clicked.connect(self.send)
        self.actionPort_Settings.triggered.connect(self.action_port_settings)  # подключаем функцию к action
        self.pushButton.clicked.connect(self.browse_folder)  # подключаем функцию к кнопке

    def connect(self):
        try:
            self.real_port = serial.Serial(self.Port.currentText(), int(self.Speed.currentText()))
            self.ConnectButton.setStyleSheet("background-color: green")
            self.ConnectButton.setText('Подключено')
        except Exception as e:
            print(e)

    def send(self):
        if self.real_port:
            self.real_port.write(b'b')

    def browse_folder(self):
        self.listWidget.clear()  # На случай, если в списке уже есть элементы
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            for file_name in os.listdir(directory):  # для каждого файла в директории
                self.listWidget.addItem(file_name)  # добавить файл в listWidget

    # функция для вызова диаллогового окна для настройки порта
    def action_port_settings(self):
        """Launch the employee dialog."""
        dlg = DialogPorts(self)
        dlg.exec()
        # print(dlg.ui.lineEdit.text())

    # функция для вызова диаллогового окна для настройки порта
    def action_add_line(self):
        """Launch the employee dialog."""
        dlg = DialogAddLine(self)
        dlg.exec()
        # print(dlg.ui.lineEdit.text())


# класс для вызова диаллогового окна
class DialogPorts(QtWidgets.QDialog):
    """dialog for settings ports"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = port_dialog.Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)


# класс для вызова диаллогового окна
class DialogAddLine(QtWidgets.QDialog):
    """dialog for settings ports"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = add_dialog.Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
