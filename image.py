import os
import shutil
import json


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
                            total_confidence += confidence
                            count += 1

        
        if count > 0:
            average_confidence = total_confidence / count
            self.data["Average Confidence"] = average_confidence        
        else:
            file.write("No detections found.\n")

        self.data["Total Files Count"] = self.true_file + self.false_file
        self.data["True Files Coun"] = self.true_file
        self.data["False Files Count"] = self.false_file

        with open(output_file, 'w',encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)

