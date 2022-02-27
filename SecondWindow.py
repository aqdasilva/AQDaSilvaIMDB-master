from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox


class Comp490DataDemoWindow(QWidget):

    def __init__(self, data_to_show:dict):
        super().__init__()
        self.data = data_to_show
        self.setup_window()

    def setup_window(self):
        self.setWindowTitle("Change in Income over time")
        self.setGeometry(750, 100, 900, 200)  # put the new window next to the original one wider than it is tall
        label = QLabel(self)
        label.setText("State:")
        label.move(50, 50)
        state_display = QLineEdit(self.data['state_name'],self)
        state_display.move(120, 50)
        label = QLabel("2018 Income:", self)
        label.move(50, 100)
        income2018 = QLineEdit(str(self.data["median_income"]),self)
        income2018.move(120,100)
        label = QLabel("2017 Income:", self)
        label.move(250, 100)
        income2017 = QLineEdit(str(self.data["income2017"]),self)
        income2017.move(330,100)
        label = QLabel("2016 Income:", self)
        label.move(460, 100)
        income2017 = QLineEdit(str(self.data["income2016"]), self)
        income2017.move(540, 100)
        label = QLabel("2015 Income:", self)
        label.move(670, 100)
        income2017 = QLineEdit(str(self.data["income2015"]), self)
        income2017.move(750, 100)
