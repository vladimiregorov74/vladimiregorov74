import sys

from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QMainWindow, QApplication

from bmi import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
	"""
		Главное окно приложения чат-клиента.
		Этот класс представляет главное окно приложения чата, обрабатывающее
		пользовательский интерфейс, сетевое общение и обновления чата.
	"""
	
	def __init__(self):
		"""
			Инициализирует экземпляр MyApp.
			Настраивает пользовательский интерфейс, соединяет сигналы и слоты, инициализирует
			модель чата, считывает имя пользователя и запускает сетевой поток
			и обновить таймер.
		"""
		super().__init__()
		self.setupUi(self)
		self.label_2.setStyleSheet(
			"background-image: url(./Индикатор_нормального_веса.jpg);")
		self.flag = 1
		self.pushButton.clicked.connect(self.calc)
		
	
	def calc(self):
		if self.flag:
			if float(self.lineEdit.text()) <= 0 or float(self.lineEdit_2.text()) <= 0:
				return
			weight = float(self.lineEdit.text().strip())
			height = float(self.lineEdit_2.text().strip())
			bmi = self.calculate_bmi(weight, height)
			if bmi is not None:
				category = self.interpret_bmi(bmi,weight, height)
				self.label.setText(f"Ваш ИМТ: {bmi}")
				self.label_3.setText(f"Категория: {category}")
			self.flag=0
			self.pushButton.setText('Очистить')
		else:
			self.lineEdit.clear()
			self.lineEdit_2.clear()
			self.label.setText('Ваш индекс массы: ...')
			self.label_3.clear()
			self.flag = 1
			self.pushButton.setText('Готово')
	
	def calculate_bmi(self, weight, height):
		"""Вычисляет индекс массы тела (ИМТ)."""
		try:
			bmi = weight / ((height / 100) ** 2)
			return round(bmi, 2)
		except ZeroDivisionError:
			print("Рост не может быть равен нулю.")
			return None
	
	def interpret_bmi(self, bmi,weight, height):
		"""Интерпретирует значение ИМТ."""
		if bmi < 18.5:
			delta = - weight + 18.5 * ((height / 100) ** 2)
			return f"Недостаточный вес, рассмотрите возможность поправиться на {delta:.2f} кг"
		elif 18.5 <= bmi < 24.9:
			return "Нормальный вес"
		elif 25 <= bmi < 29.9:
			delta = weight - 24.9 * ((height / 100) ** 2)
			return f"Избыточный вес, рассмотрите возможность похудеть на {delta:.2f} кг"
		else:
			delta = weight - 24.9 * ((height / 100) ** 2)
			return f"Ожирение, рассмотрите возможность похудеть на {delta:.2f} кг"

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MyApp()
	window.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
	window.show()
	sys.exit(app.exec())