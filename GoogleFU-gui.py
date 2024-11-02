import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from modules.sort import Sort
from modules.search import Search
import time
from urllib.error import HTTPError, URLError

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
        desc_label = QLabel("This tool will find information on Google about someone or a topic.")
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

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        layout.addWidget(self.results_display)

        # Clear and Save buttons
        clear_button = QPushButton("Clear Results")
        clear_button.clicked.connect(self.clear_results)
        layout.addWidget(clear_button)

        save_button = QPushButton("Save Results")
        save_button.clicked.connect(self.save_results)
        layout.addWidget(save_button)

    def perform_search(self):
        query = self.query_input.text()
        dork = self.dorks_combo.currentText()
        dork_param = self.dorks_input.text()

        if dork != "None" and dork_param:
            query = f"{query} {dork}{dork_param}"

        max_retries = 5
        retry_delay = 1  # Start with a 1-second delay

        for attempt in range(max_retries):
            try:
                urls = Search(query).urls()  # Assuming this method returns a list of URLs.
                sorted_urls = Sort(urls).sort()  # Assuming this method sorts the URLs.

                results = f"Search Query: {query}\n\n"
                for item in sorted_urls:
                    if sorted_urls[item]:
                        results += f"{item.capitalize()}: {', '.join(sorted_urls[item])}\n\n"

                self.results_display.setText(results)
                return  # Exit the function if successful

            except HTTPError as e:
                if e.code == 429:
                    # Handle Too Many Requests
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)  # Wait before retrying
                        retry_delay *= 2  # Exponential backoff
                    else:
                        self.results_display.setText("Error: Too many requests. Please try again later.")
                        return
                else:
                    self.results_display.setText(f"HTTP Error: {e.code} - {e.reason}")
                    return

            except URLError as e:
                self.results_display.setText(f"URL Error: {str(e)}")
                return

            except Exception as e:
                self.results_display.setText(f"An unexpected error occurred: {str(e)}")
                return

    def clear_results(self):
        """Clear the results display."""
        self.results_display.clear()

    def save_results(self):
        """Save the results to a text file."""
        
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.results_display.toPlainText())
                QMessageBox.information(self, "Success", "Results saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save results: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GoogleFuApp()
    window.show()
    sys.exit(app.exec_())
