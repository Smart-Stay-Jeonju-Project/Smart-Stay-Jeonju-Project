import os
import pandas as pd
import re

targetPath = 'DATA/RAW/REVIEWS/'
filename = 'y_all_reviews.csv'

fullPath = targetPath + filename
reviews = []

if os.path.exists(fullPath) :
    reviews = pd.read_csv(fullPath, encoding='utf-8-sig')
else :
    print("파일 경로를 찾을 수 없습니다")
    print("현재 작업 경로:", os.getcwd())

print(reviews.info())
print(reviews.head())

try :
    for review in reviews :
        review['content'] = str(re.sub(r"[^ㄱ-ㅎㅏ-ㅣ-가-힣0-9 ]", "", review['content'].get_text().strip()))
        
except Exception as e :
    print(e)
# print(df.iloc['id'])