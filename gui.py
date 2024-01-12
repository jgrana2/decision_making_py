import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
from decision_maker_app import DecisionMakerApp
from PySide6.QtCore import QThread, Signal

class ScoreCalculatorThread(QThread):
    # Define a signal to emit the output
    output = Signal(str)

    def __init__(self, decision_maker_app):
        super().__init__()
        self.decision_maker_app = decision_maker_app

    def run(self):
        # Call run method of DecisionMakerApp instance and emit the output
        for decision_maker_output in self.decision_maker_app.run():
            self.output.emit(decision_maker_output)

class DecisionMakerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.decision_maker_app = DecisionMakerApp()
        self.setWindowTitle("Decision Making Process with AI Assistance")
        
        # Set the fixed window width
        width = 500
        self.setFixedWidth(width)
        
        # Main layout
        self.layout = QVBoxLayout()
        
        # Context input
        self.context_label = QLabel("Please provide the decision context:")
        self.context_input = QLineEdit()
        self.layout.addWidget(self.context_label)
        self.layout.addWidget(self.context_input)
        
        # Criteria input
        self.criteria_label = QLabel("Enter your list of criteria separated by commas:")
        self.criteria_input = QLineEdit()
        self.layout.addWidget(self.criteria_label)
        self.layout.addWidget(self.criteria_input)
        
        # Options input
        self.options_label = QLabel("Enter your options separated by commas:")
        self.options_input = QLineEdit()
        self.layout.addWidget(self.options_label)
        self.layout.addWidget(self.options_input)
        
        # Calculate scores button
        self.calculate_button = QPushButton("Calculate Scores")
        self.calculate_button.clicked.connect(self.calculate_scores)
        self.layout.addWidget(self.calculate_button)
        
        # Print area
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.layout.addWidget(self.text_area)
        
        # Set main widget and layout
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        
        # Initialize the thread (but do not start it yet)
        self.score_calculator_thread = ScoreCalculatorThread(self.decision_maker_app)

        # Connect the thread's output signal to the method that updates the text area
        self.score_calculator_thread.output.connect(self.update_text_area)
        
    def assign_weights(self):
        # Here you would implement the logic to assign weights
        pass

    def evaluate_options(self):
        # Here you would implement the logic to evaluate options
        pass

    def calculate_scores(self):
        # Get the criteria and options from the input fields
        context_text = self.context_input.text()
        criteria_text = self.criteria_input.text()
        options_text = self.options_input.text()

        # Assuming the input is comma-separated, split into lists
        context_list = [x.strip() for x in context_text.split(',')]
        criteria_list = [c.strip() for c in criteria_text.split(',')]
        options_list = [o.strip() for o in options_text.split(',')]
        
        # Set the criteria and options in the DecisionMakerApp
        self.decision_maker_app.set_context(context_list)
        self.decision_maker_app.set_criteria(criteria_list)
        self.decision_maker_app.set_options(options_list)
        
        if not self.score_calculator_thread.isRunning():
            # Clear the text area before starting the calculation
            self.text_area.clear()
            # Start the thread
            self.score_calculator_thread.start()
            
    def update_text_area(self, text):
        # Append the output to the text area
        self.text_area.insertPlainText(text)
        
    def show_message(self, message):
        QMessageBox.information(self, "Information", message)

# Entry point of the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DecisionMakerGUI()
    window.show()
    sys.exit(app.exec())