# 숙소별 리뷰 개수 확인
# name 컬럼 데이터 몇개 있는지

import pandas as pd

# 파일 경로 설정
input_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/all_accm_datas.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/name_counts_all.csv"

# CSV 불러오기
df = pd.read_csv(input_path)

# name 컬럼 기준 숙소별 개수 세기
name_counts = df["name"].value_counts().reset_index()
name_counts.columns = ["name", "count"]

# CSV 파일로 저장
name_counts.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 숙소별 데이터 개수 저장 완료 → {output_path}")
