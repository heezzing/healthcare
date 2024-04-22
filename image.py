import os
import shutil


def organize_files(base_path):
    image_dir = os.path.join(base_path, '')  # 이미지가 저장된 폴더 경로
    label_dir = os.path.join(base_path, 'labels')  # 라벨이 저장된 폴더 경로
    true_dir = os.path.join(base_path, 'true')  # 일치하는 파일을 저장할 폴더 경로
    false_dir = os.path.join(base_path, 'false')  # 일치하지 않는 파일을 저장할 폴더 경로
    
    true_file = 0
    false_file = 0


    # true와 false 폴더가 없다면 생성
    os.makedirs(true_dir, exist_ok=True)
    os.makedirs(false_dir, exist_ok=True)


    # 라벨 파일 이름 추출 (확장자 제외)
    label_files = {os.path.splitext(file)[0] for file in os.listdir(label_dir) if file.endswith('.txt')}

    # 이미지 파일을 순회하며 이름 비교
    for image in os.listdir(image_dir):
        if image.endswith(('.png', '.jpg', '.jpeg')):  # 이미지 파일 확장자 체크
            image_name = os.path.splitext(image)[0]  # 파일 이름만 추출 (확장자 제외)
            if image_name in label_files:
                shutil.move(os.path.join(image_dir, image), os.path.join(true_dir, image))  # true 폴더로 이동
                true_file += 1
            else:
                shutil.move(os.path.join(image_dir, image), os.path.join(false_dir, image))  # false 폴더로 이동
                false_file += 1
    
    return true_file, false_file


def average_confidence(directory, output_file,true_file,false_file):
    total_confidence = 0
    count = 0
   
    
    # 폴더 내 모든 파일 순회
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):  # txt 파일 확인
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) > 4:  # 적어도 클래스, x, y, w, h, conf 형식을 가정
                        confidence = float(parts[5])  # 마지막 요소가 신뢰도
                        total_confidence += confidence
                        count += 1
                    
    
    # 결과를 파일에 출력
    with open(output_file, 'w') as file:
        if count > 0:
            average_confidence = total_confidence / count
            file.write(f"Average Confidence: {average_confidence:.3f}\n")
        else:
            file.write("No detections found.\n")


        file.write(f"Total Files Count: {true_file + false_file}\n")
        file.write(f"True Files Count: {true_file}\n")
        file.write(f"False Files Count: {false_file}\n")

# 사용자 입력으로 기본 경로 받기
base_path = input("경로를 지정해주세요: ")

# 파일 정리 함수 호출
true_file,false_file = organize_files(base_path)

# 사용자가 지정한 디렉토리
directory_path = base_path+'/labels'  # 실제 폴더 경로로 변경하세요
output_file = base_path+'/average_confidence.txt'  # 결과를 저장할 파일 경로

average_confidence(directory_path, output_file,true_file,false_file)
