import pandas as pd

# 🔹 파일 경로 설정
y_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_filtered_up.csv"
n_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_filtered_up.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/all_accm_datas.csv"

# 🔹 데이터 로드
df_y = pd.read_csv(y_path)
df_n = pd.read_csv(n_path)

# 🔹 df_y에서 id 컬럼 제거 (나머지는 동일)
df_y = df_y.drop(columns=["id"])

# 🔹 df_n의 review_rating → rating 으로 컬럼명 변경
df_n = df_n.rename(columns={"review_rating": "rating"})

# 🔹 컬럼 순서 통일
columns = ["name", "nickname", "text", "rating", "write_date", "source", "type", "clean_reviews"]
df_y = df_y[columns]
df_n = df_n[columns]

# 🔹 두 데이터 병합
df_all = pd.concat([df_y, df_n], ignore_index=True)

# 🔹 결과 저장
df_all.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 통합 완료: {len(df_all)}개 리뷰 → {output_path} 저장됨")
