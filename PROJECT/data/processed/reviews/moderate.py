# 임시 오류 확인

import pandas as pd

df = pd.read_csv("data/processed/reviews/y_ai_cleaned_reviews.csv", header=None)
print("전체 줄 수:", len(df))
print("정제 성공 리뷰 수:", df[0].apply(lambda x: x != "ERROR").sum())
print("정제 실패 (ERROR) 수:", df[0].apply(lambda x: x == "ERROR").sum())
