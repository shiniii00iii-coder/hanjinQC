import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel
from PyQt5.QtCore import Qt

class PipeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PIPE_KS 규격서 관리자')
        self.setGeometry(300, 300, 400, 500)
        
        layout = QVBoxLayout()
        
        self.label = QLabel('📋 등록된 KS 규격서 목록', self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        # 파일 목록 표시창
        self.list_widget = QListWidget()
        self.load_files()
        layout.addWidget(self.list_widget)
        
        # 열기 버튼
        self.btn = QPushButton('선택한 규격서 열기', self)
        self.btn.clicked.connect(self.open_pdf)
        layout.addWidget(self.btn)
        
        self.setLayout(layout)

    def load_files(self):
        # pdf_files 폴더 안의 PDF 목록 가져오기
        pdf_path = os.path.join(os.getcwd(), 'pdf_files')
        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
            
        files = [f for f in os.listdir(pdf_path) if f.lower().endswith('.pdf')]
        self.list_widget.addItems(files)

    def open_pdf(self):
        selected_file = self.list_widget.currentItem()
        if selected_file:
            file_path = os.path.join(os.getcwd(), 'pdf_files', selected_file.text())
            # 윈도우 기본 PDF 뷰어로 실행
            os.startfile(file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PipeApp()
    ex.show()
    sys.exit(app.exec_())