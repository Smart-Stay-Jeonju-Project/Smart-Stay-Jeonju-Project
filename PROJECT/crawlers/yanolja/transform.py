# link list 중복제거

import os
from selenium import webdriver
import pandas as pd
import json
import csv


targetPath = "project/data/processed/reviews/"
File_Suffix = 'yanolja_link.txt'
filename = "yanolja_link_modify.txt"

fullPath = targetPath + File_Suffix

# 링크.txt 중복제거
def list_dupl() :
    try :
        with open(fullPath, 'r', encoding='utf-8') as file:
            # 파일의 내용을 읽고, 각 줄을 리스트의 요소로 저장
            lines = file.read().split('\n')
            modify_list = list(set(lines))
            print(lines[0])

        fullPath = targetPath + filename
        with open(fullPath, "w",encoding="utf-8") as f:
            for line in modify_list :
                f.write(line+"\n")

        print("txt파일 중복 제거 완료했습니다")
    except Exception as e :
        print("txt파일 중복 제거에 실패했습니다. error:", e)    


# csv파일 중복제거
def csv_dupl() :
    try :
        filename = "N_clean_info.csv"
        fullPath = targetPath + filename
        df = pd.read_csv(fullPath)

        # inplace=True이므로 df 자체가 수정됩니다 (새 DataFrame을 반환하지 않음)
        df.drop_duplicates(inplace=True)

        new_filename = "N_clean_info_dupl.csv"
        fullPath = targetPath + new_filename
        # 변경된 데이터프레임 저장
        df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)
        
        print("csv파일 중복 제거 완료했습니다")

    except Exception as e :
        print("csv파일 중복 제거에 실패했습니다. error:", e)    


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


# 기존 csv파일에 컬럼 추가하기
def add_lat() :

    # 기존 csv 파일 불러오기
    filename = "yanolja_img_add.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)

    # 위도,경도 csv
    filename = "정리된_숙소_주소.csv"
    fullPath = targetPath + filename
    add_df = pd.read_csv(fullPath)

    add_df = add_df[['name', 'lat', 'lng']]

    # 기존 csv파일의 name과 새로 수집한 name이 같으면 위도,경도 추가
    merged_df = pd.merge(df, add_df, on='name', how='left')

    print(merged_df.head())

    new_filename = "yanolja_list.csv"
    fullPath = targetPath + new_filename
    # 변경된 데이터프레임 저장
    merged_df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)


# csv파일 컬럼추가(출처)
def add_column() :
    filename = "숙소상세정보(중복제거,위도경도표시).csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)

    df['source'] = 'N'

    new_filename = "yanolja_source_add.csv"
    fullPath = targetPath + new_filename
    # 변경된 데이터프레임 저장
    df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)


# 리뷰 작성날짜 형식 변경
def review_replace() :
    filename = "n_duple_filtered_up.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)

    df['write_date'] = df['write_date'].str.replace('.','-')

    new_filename = "n_duple_filtered_up_replace.csv"
    fullPath = targetPath + new_filename
    # 변경된 데이터프레임 저장
    df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)


# 리뷰 출처 형식 변경
def review_source_replace() :
    filename = "n_duple_filtered_up_replace.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)

    df['source'] = df['source'].str.replace('N','n')

    new_filename = "n_duple_filtered_up_replace_source.csv"
    fullPath = targetPath + new_filename
    # 변경된 데이터프레임 저장
    df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)



# 이미지 소스 칼럼 추가
def add_image() :
    imgtargetPath = "DATA/imgs/yanolja_img"

    # 이미지 파일 목록 가져오기
    image_files = [f for f in os.listdir(imgtargetPath) if os.path.isfile(os.path.join(imgtargetPath, f))]


    filename = "yanolja_source_add.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)

    df['image'] = ""

    new_filename = "yanolja_all_list.csv"
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


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# 날짜형식 변경
def set_date() :

    targetPath = "project/data/processed/reviews/"
    filename = 'n_duple_filtered_up_replace_source.csv'

    fullPath = targetPath + filename
    if os.path.exists(fullPath) :
        reviews = pd.read_csv(fullPath, encoding='utf-8-sig')
    else :
        print("파일 경로를 찾을 수 없습니다")
        print("현재 작업 경로:", os.getcwd())

    #today = datetime.today()
    today = datetime(2025,7,7)
    converted_dates = []
    for date in reviews['write_date'] :
        date = date.strip()
        try :
            if '개월 전' in date :
                num = int(date.replace('개월 전', '').strip())
                new_date = today - timedelta(weeks=num)
            elif '일 전' in date :
                num = int(date.replace('일 전', '').strip())
                new_date = today - timedelta(days=num)
            elif '년 전' in date :
                num = int(date.replace('년 전', '').strip())
                new_date = today - relativedelta(years=num)
            elif '시간 전' in date :
                num = int(date.replace('시간 전', '').strip())
                new_date = today - relativedelta(hours=num)
            elif '분 전' in date :
                num = int(date.replace('분 전', '').strip())
                new_date = today - relativedelta(minutes=num)

            else :
                new_date = datetime.strptime(date, '%Y-%m-%d')
                

            converted_dates.append(new_date.strftime('%Y-%m'))
        except Exception as e :
            print(f"오류 발생 : {date} {e}")
            return
    reviews['write_date'] = converted_dates

    new_filename = "n_review_0715.csv"
    fullPath = targetPath + new_filename

    reviews.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)



if __name__ == "__main__":
    # 리스트 중복 제거
    #list_dupl()

    # csv파일 중복제거
    #csv_dupl()

    # JSON 변환
    #json_dupl()

    # csv파일 위도경도
    #add_lat()

    # 야놀자 리뷰 작성날짜 변경
    #review_replace()

    # 리뷰 출처 형식 변경
    #review_source_replace()
    
    # csv파일 컬럼추가(출처)
    #add_column()
    
    # 이미지 파일명 추가
    #add_image()

    # 날짜 형식 변경
    set_date()