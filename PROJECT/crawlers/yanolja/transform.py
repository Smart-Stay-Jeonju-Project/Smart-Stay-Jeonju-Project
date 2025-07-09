# link list 중복제거

import os
from selenium import webdriver
import pandas as pd
import json
import csv


targetPath = "DATA/LIST/"
File_Suffix = 'yanolja_link.txt'
filename = "yanolja_link_modify.txt"

fullPath = targetPath + File_Suffix

# 링크 중복제거
def list_dupl() :
    with open(fullPath, 'r', encoding='utf-8') as file:
        # 파일의 내용을 읽고, 각 줄을 리스트의 요소로 저장
        lines = file.read().split('\n')
        modify_list = list(set(lines))
        print(lines[0])


    fullPath = targetPath + filename
    with open(fullPath, "w",encoding="utf-8") as f:
        for line in modify_list :
            f.write(line+"\n")


# JSON 변환
def json_dupl() :

    data_list = []

    filename = "yanolja_accommodations(중복제거).csv"
    fullPath = targetPath + filename

    with open(fullPath, 'r', encoding='utf-8-sig') as f :
        data = csv.DictReader(f)
        for row in data :
            data_list.append(row)

    filename = "yanolja_detail_test.json"
    fullPath = targetPath + filename

    with open(fullPath,"w",encoding='utf-8-sig') as file:
        json.dump(data_list, file, ensure_ascii=False, indent=4)

    

# csv파일 컬럼추가(출처)
def add_column() :
    filename = "new_yanolja_accommodations.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)

    df['source'] = 'N'

    new_filename = "yanolja_add.csv"
    fullPath = targetPath + new_filename
    # 변경된 데이터프레임 저장
    df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)


# 이미지 소스 칼럼 추가
def add_image() :
    imgtargetPath = "DATA/imgs/yanolja_img"

    # 이미지 파일 목록 가져오기
    image_files = [f for f in os.listdir(imgtargetPath) if os.path.isfile(os.path.join(imgtargetPath, f))]


    filename = "source_add.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)

    df['image'] = ""

    new_filename = "yanolja_img_add.csv"
    fullPath = targetPath + new_filename

    # 확장자 제거한 이름 기준으로 매핑 생성
    image_file = {os.path.splitext(f)[0]: f for f in image_files}


    # name 컬럼과 이미지 이름이 매치되면 image 컬럼에 파일명 입력
    for idx, row in df.iterrows():
        name = str(row['name']).strip()
        if name in image_file:
            df.at[idx, 'image'] = image_file[name]  # 확장자 포함된 파일명 입력


    # 변경된 데이터프레임 저장
    df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)



if __name__ == "__main__":
    # 리스트 중복 제거
    #list_dupl()

    # JSON 변환
    #json_dupl()

    # csv파일 컬럼추가(출처)
    #add_column()
    
    # 이미지 파일명 추가
    add_image()