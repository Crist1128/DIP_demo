import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QDialog

from match_calvulate import calculate_match

class MatchFailureDialog(QDialog):
    def __init__(self, match_failure_info):
        super().__init__()
        self.setWindowTitle("Match Failures")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.match_failure_text = QTextEdit(self)
        self.match_failure_text.setPlainText("\n".join(match_failure_info))
        layout.addWidget(self.match_failure_text)
        self.setLayout(layout)

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 创建主窗口
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("DIP Demo")

        # 创建主窗口中的主要布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # 创建文件选择按钮
        self.file_button = QPushButton("Select Excel File", self)
        self.file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.file_button)

        # 创建分值单价输入框
        self.price_label = QLabel("Scoring Unit Price:", self)
        layout.addWidget(self.price_label)
        self.price_input = QLineEdit(self)
        layout.addWidget(self.price_input)

        # 创建计算按钮
        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # 创建结果显示框
        self.result_text = QTextEdit(self)
        layout.addWidget(self.result_text)

        # 创建显示匹配失败信息的按钮
        self.show_failures_button = QPushButton("Show Match Failures", self)
        self.show_failures_button.clicked.connect(self.show_match_failures)
        layout.addWidget(self.show_failures_button)

        central_widget.setLayout(layout)

    def open_file_dialog(self):
        # 打开文件对话框，获取用户选择的文件路径
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            self.file_button.setText(file_path)

    def calculate(self):
        # 获取用户输入的文件路径和分值单价
        file_path = self.file_button.text()
        scoring_unit_price = float(self.price_input.text())
        
        # 调用计算函数
        total_scoring_value, total_payment_amount, results_per_case, match_failure_info = calculate_match(file_path, scoring_unit_price)

        # 更新结果显示框
        result_text = f"Total ScoringValue: {total_scoring_value}, Total Payment Amount: {total_payment_amount}\n\nResults per case:\n"
        for result in results_per_case:
            result_text += f"Case Number: {result[0]}, Value: {result[1]}, Difference: {result[2]}\n"
        self.result_text.setText(result_text)

        # 将匹配失败的信息传递给显示匹配失败信息的方法
        self.match_failure_info = match_failure_info

    def show_match_failures(self):
        dialog = MatchFailureDialog(self.match_failure_info)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())
