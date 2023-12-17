from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
import npk_parser

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        # Create QLabel to display the image
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.button = QPushButton('Upload CSV')
        self.button.clicked.connect(self.upload_csv)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def upload_csv(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open CSV file', '', 'CSV files (*.csv)')

        if not file_path:
            print(f"Unable to open selected file.")
            return

        image_path = npk_parser.load_csv(file_path)
        if image_path:
            self.show_image(image_path)

    def show_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()

    # Set the size of the main window
    window.resize(400, 500)

    window.show()
    app.exec_()
