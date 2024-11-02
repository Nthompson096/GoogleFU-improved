import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFileDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from modules.sort import Sort
from modules.search import Search

class GoogleFuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GoogleFu")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Banner
        banner_label = QLabel("GoogleFu")
        banner_label.setAlignment(Qt.AlignCenter)
        banner_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(banner_label)

        # Description
        desc_label = QLabel("This tool will find information on Google about someone or an image.\nIt works well with invented online names and reverse image search.")
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)

        # Query input
        query_layout = QHBoxLayout()
        query_label = QLabel("Query:")
        self.query_input = QLineEdit()
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.perform_search)
        query_layout.addWidget(query_label)
        query_layout.addWidget(self.query_input)
        query_layout.addWidget(search_button)
        layout.addLayout(query_layout)

        # Google Dorks section
        dorks_layout = QHBoxLayout()
        dorks_label = QLabel("Google Dork:")
        self.dorks_combo = QComboBox()
        self.dorks_combo.addItems([
            "None",
            "site:",
            "filetype:",
            "inurl:",
            "intitle:",
            "intext:",
            "cache:",
            "link:",
            "related:"
        ])
        self.dorks_input = QLineEdit()
        self.dorks_input.setPlaceholderText("Enter dork parameter")
        dorks_layout.addWidget(dorks_label)
        dorks_layout.addWidget(self.dorks_combo)
        dorks_layout.addWidget(self.dorks_input)
        layout.addLayout(dorks_layout)

        # Image search section
        image_layout = QHBoxLayout()
        image_label = QLabel("Image Search:")
        self.image_path = QLineEdit()
        self.image_path.setPlaceholderText("Image path")
        image_button = QPushButton("Browse")
        image_button.clicked.connect(self.browse_image)
        image_search_button = QPushButton("Search Image")
        image_search_button.clicked.connect(self.perform_image_search)
        image_layout.addWidget(image_label)
        image_layout.addWidget(self.image_path)
        image_layout.addWidget(image_button)
        image_layout.addWidget(image_search_button)
        layout.addLayout(image_layout)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

    def perform_search(self):
        query = self.query_input.text()
        dork = self.dorks_combo.currentText()
        dork_param = self.dorks_input.text()

        if dork != "None" and dork_param:
            query = f"{query} {dork}{dork_param}"

        urls = Search(query).urls()
        sorted_urls = Sort(urls).sort()

        results = f"Search Query: {query}\n\n"
        for item in sorted_urls:
            if sorted_urls[item]:
                results += f"{item.capitalize()}: {', '.join(sorted_urls[item])}\n\n"

        self.results_display.setText(results)

    def browse_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_name:
            self.image_path.setText(file_name)

    def perform_image_search(self):
        image_path = self.image_path.text()
        if not image_path:
            self.results_display.setText("Please select an image first.")
            return

        # Here you would implement the actual reverse image search
        # For demonstration, we'll just show a placeholder message
        self.results_display.setText(f"Performing reverse image search for: {image_path}\n\n"
                                     "Actual implementation of reverse image search would go here.\n"
                                     "This typically involves uploading the image to Google's servers\n"
                                     "and parsing the results, which requires additional libraries and APIs.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoogleFuApp()
    window.show()
    sys.exit(app.exec_())
