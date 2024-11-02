import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
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
        banner_label = QLabel()
       # banner_pixmap = QPixmap("banner.png")  # You'll need to create this image
        # banner_label.setPixmap(banner_pixmap.scaledToWidth(700))
        # layout.addWidget(banner_label, alignment=Qt.AlignCenter)

        # Description
        desc_label = QLabel("This tool will find information that are on Google about someone.\nIt works good with invented online names.")
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

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

    def perform_search(self):
        query = self.query_input.text()
        urls = Search(query).urls()
        sorted_urls = Sort(urls).sort()

        results = ""
        for item in sorted_urls:
            if sorted_urls[item]:
                results += f"{item.capitalize()}: {', '.join(sorted_urls[item])}\n\n"

        self.results_display.setText(results)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoogleFuApp()
    window.show()
    sys.exit(app.exec_())
