import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from image import FileOrganizer
import os

from_class = uic.loadUiType("C:/Users/liz/hk/healthcare/Dialog - untitled.ui")[0]

class WindowClass (QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.filePath = ""
        self.cmdpath = ""

        self.btn_search_1.clicked.connect(self.openFile)
        self.btn_run.clicked.connect(self.Filerun)

    def openFile(self):
        options = QFileDialog.Options()
        self.filePath = QFileDialog.getExistingDirectory(self.te_search,'Select Folder','', options = options)
        if self.filePath:  # 폴더 경로가 비어있지 않은 경우
        # 폴더 경로를 te_search 위젯의 텍스트로 설정합니다.
            self.te_search.setText(self.filePath)
        else:
        # 선택이 취소되었거나 아무 폴더도 선택되지 않았을 경우, 추가적인 알림이나 로그를 출력할 수 있습니다.
            print("No folder selected.")

    def Filerun(self):
        organizer = FileOrganizer(self.filePath)
        self.true_file, self.false_file = organizer.organize_files()
        organizer.average_confidence()
        self.displayFileContents()

    def displayFileContents(self):
        output_file = os.path.join(self.filePath, 'average_confidence.txt')
        if os.path.exists(output_file):
            with open(output_file,'r') as file:
                contents = file.read()

            self.text_display.setText(contents)
        else:
            self.text_display.setText("Result file not found")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()