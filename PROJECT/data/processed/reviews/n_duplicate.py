import pandas as pd

# 🔹 파일 경로 설정
duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews.csv"
only_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_only_texts.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews_filtered.csv"

# 🔹 데이터 로드
df_duple = pd.read_csv(duple_path)
df_only = pd.read_csv(only_path, header=None, names=["text"])

# 🔹 공백 제거한 only_texts 집합 생성
only_texts_set = set(df_only["text"].astype(str).str.replace(" ", "").tolist())

# 🔹 duple의 text 컬럼 공백 제거 후 비교
df_duple["text_no_space"] = df_duple["text"].astype(str).str.replace(" ", "")
df_filtered = df_duple[df_duple["text_no_space"].isin(only_texts_set)].copy()

# 🔹 임시 컬럼 제거
df_filtered.drop(columns=["text_no_space"], inplace=True)

# 🔹 결과 저장
df_filtered.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 필터링 완료: {len(df_filtered)}개 → {output_path} 저장됨")
