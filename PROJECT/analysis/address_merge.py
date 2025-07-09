import pandas as pd
import re

targetPath = "analysis/"
filename = '통합주소.csv'
fullPath = targetPath + filename
df = pd.read_csv(fullPath, encoding='utf-8-sig')
print("컬럼명:", df.columns.tolist())

df['address'] = df['address'].str.strip()

df = df.drop_duplicates(subset=['address'], keep='first')

# 1. 도로명 주소 추출 
# 5. 최종 정렬

df.to_csv('정리된_숙소_주소.csv', index=False, encoding='utf-8-sig')