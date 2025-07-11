import os
import pandas as pd


# new_df = pd.read_csv('analysis/정리된_숙소_주소.csv', encoding='utf-8')
# old_df = pd.read_csv('data/야놀자/N_clean_info_jeonju.csv', encoding='utf-8')

# name_map = dict(zip(old_df['addr'], old_df['name']))

# new_df['name'] = new_df['address'].map(name_map).fillna(new_df['name'])


# new_df.to_csv('data/야놀자/진짜바꾼다.csv', encoding='utf-8-sig', index=False)
#import pandas as pd

new_df = pd.read_csv('data/processed/accommodations/yeogi/clean_yeogi_info.csv', encoding='utf-8-sig')
old_df = pd.read_csv('analysis/정리된_숙소_주소.csv', encoding='utf-8-sig')

# old_df 에 있는 주소가 같으면, 위도 경도를 추가한다
# name_map = dict(zip(old_df['name'], old_df['addr']))
lat_map = dict(zip(old_df['address'], old_df['lat']))
lng_map = dict(zip(old_df['address'], old_df['lng']))

new_df['lat'] = new_df['address'].map(lat_map).fillna(new_df.get('lat'))
new_df['lng'] = new_df['address'].map(lng_map).fillna(new_df.get('lng'))


# new_df.drop_duplicates(subset=['lat', 'lng'], keep='first', inplace=True)
# address 기준으로 중복된 행 보기

# 'address' 컬럼에서 결측값(NaN)이 있는 행 제거
# new_df.dropna(subset=['address'], inplace=True)
new_df.to_csv('analysis/진짜바꾼다2.csv', encoding='utf-8-sig', index=False)

