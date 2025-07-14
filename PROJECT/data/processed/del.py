import pandas as pd
import os

df = pd.read_csv('data/processed/reviews/n_cleaned_reviews_full.csv', encoding='utf-8-sig')
# df = pd.read_csv('data/야놀자/N_cleaned_reviews_full_fin.csv', encoding='utf-8-sig')

name_df = pd.read_csv('data/야놀자/N_clean_info_jeonju.csv', encoding='utf-8-sig')

filtered_df = df[df['name'].isin(name_df['name'])]

filtered_df.drop_duplicates(subset=['nickname','text','review_rating'], inplace=True)

print(filtered_df.shape)

filtered_df.to_csv('data/야놀자/중복제거한야놀자리뷰.csv', encoding='utf-8-sig', index=False)