import json
import os
import shutil

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class addTableItem:

    def __init__(self, table_widget, filepath):

        """  테이블 위젯 , json 파일을 불러오기 """

        self.table_widget = table_widget
        self.filepath = filepath
        self.data = {}
        self.load_property()

    def load_property(self):
        for filename in os.listdir(self.filepath):
            if filename.endswith('.json'):
                if filename:
                    jsonfilepath = self.filepath + "/" + filename
                    with open(jsonfilepath, 'r', encoding='utf-8') as file:
                        self.data = json.load(file)
                    self.populate_table()   # 테이블 채우기


    # 테이블 추가
    def populate_table(self):
        row = 0
        for key, value in self.data.items():
            self.table_widget.insertRow(row)

            key_item = QTableWidgetItem(f"{key}")
            vaule_item = QTableWidgetItem(str(value))

            key_item.setFlags(Qt.ItemIsEnabled) # 키 편집 못하게 설정
            vaule_item.setFlags(Qt.ItemIsEnabled) # 키 편집 못하게 설정

            self.table_widget.setItem(row, 0, key_item)
            self.table_widget.setItem(row, 1, vaule_item)

            row += 1



    # cell에 배경 색상 추가

    def set_cell_backgroundColor(self, row, column, color):
        """ row(행), column(열), color (배경 색상 or 색상 코드)"""
        item = self.table_widget.item(row, column)
        item.setBackground(QColor(color))


    # cell에 글자 폰트, 크기, 색상 추가

    def set_cell_foregroundColor(self, row, column, font_name = None, font_size = None, font_color = None):

        """ row(행), column(열), font_name(폰트 명), font_size(폰트 크기), font_color (글자 색상 or 색상 코드 )"""
        item = self.table_widget.item(row, column)

        if font_name or font_size or font_color:
            font = item.font()
            if font_name:
                font.setFamily(font_name)
            if font_size:
                font.setPointSize(font_size)
            if font_color:
                item.setForeground(QColor(font_color))

            item.setFont(font) 

         
    def on_cell_changed(self, row, column):

        if column == 1:

            self.save_properties()


    
class FileOrganizer:
    def __init__(self, base_path):
        self.base_path = base_path
        self.image_dir = os.path.join(base_path, '')  # 이미지 폴더 경로
        self.label_dir = os.path.join(base_path, 'labels')  # 라벨 폴더 경로
        self.true_dir = os.path.join(base_path, 'true')  # 일치하는 파일 폴더 경로
        self.false_dir = os.path.join(base_path, 'false')  # 일치하지 않는 파일 폴더 경로
        self.true_file = 0
        self.false_file = 0
        self.data = {}

        # true와 false 폴더 생성
        os.makedirs(self.true_dir, exist_ok=True)
        os.makedirs(self.false_dir, exist_ok=True)

    def organize_files(self):
        label_files = {os.path.splitext(file)[0] for file in os.listdir(self.label_dir) if file.endswith('.txt')}
        
        for image in os.listdir(self.image_dir):
            if image.endswith(('.png', '.jpg', '.jpeg')):
                image_name = os.path.splitext(image)[0]
                if image_name in label_files:
                    shutil.move(os.path.join(self.image_dir, image), os.path.join(self.true_dir, image))
                    self.true_file += 1
                else:
                    shutil.move(os.path.join(self.image_dir, image), os.path.join(self.false_dir, image))
                    self.false_file += 1

        return self.true_file, self.false_file

    def average_confidence(self):
        directory = self.label_dir
        output_file = os.path.join(self.base_path, 'average_confidence.json')
        if os.path.exists(output_file):
            print("Output file already exists. No further action taken.")
            return
        total_confidence = 0
        count = 0

        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) > 4:
                            confidence = float(parts[5])
                            confidence =  round(confidence, 3)
                            total_confidence += confidence
                            count += 1

        
        if count > 0:
            average_confidence = total_confidence / count
            average_confidence1 = round(average_confidence,3)
            self.data["Average Confidence"] = average_confidence1        
        else:
            file.write("No detections found.\n")

        self.data["Total Files Count"] = self.true_file + self.false_file
        self.data["True Files Coun"] = self.true_file
        self.data["False Files Count"] = self.false_file

        with open(output_file, 'w',encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)