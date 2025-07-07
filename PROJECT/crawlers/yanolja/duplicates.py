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

    
if __name__ == "__main__":
    # 리스트 중복 제거
    #list_dupl()

     # JSON 변환
    json_dupl()
