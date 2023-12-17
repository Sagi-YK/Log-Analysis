from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.button = QPushButton('Upload CSV')
        self.button.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def upload_csv(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, 'Open CSV file', '', 'CSV files (*.csv)')
        # Process the CSV file and generate the sequence diagram
 
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()        