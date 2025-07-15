# nickname, text, write_date 일치 시 광고로 판단 하고 중복 내용 제거까지

import pandas as pd

# 🔹 파일 경로 설정
duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_reviews.csv"
only_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_only_texts.csv"
ai_cleaned_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_ai_cleaned_reviews.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_filtered_up.csv"
# duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews.csv"
# only_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_only_texts.csv"
# ai_cleaned_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_ai_cleaned_reviews.csv"
# output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_filtered_up.csv"

# 🔹 1. 데이터 로드
df_duple = pd.read_csv(duple_path)
df_only = pd.read_csv(only_path, header=None, names=["text"])

# 🔹 2. 공백 제거한 기준 생성
df_duple["text_no_space"] = df_duple["text"].astype(str).str.replace(" ", "")
df_only["text_no_space"] = df_only["text"].astype(str).str.replace(" ", "")

# 🔹 3. 중복 제거한 딕셔너리 생성 (key: 공백 제거한 text, value: 첫 번째 등장 row)
text_map = {}
for i, row in df_duple.iterrows():
    key = row["text_no_space"]
    if key not in text_map:
        text_map[key] = row

# 🔹 4. only_texts 기준으로 매칭된 행 추출
filtered_rows = []
for t in df_only["text_no_space"]:
    if t in text_map:
        filtered_rows.append(text_map[t])

df_filtered = pd.DataFrame(filtered_rows).reset_index(drop=True)
df_filtered.drop(columns=["text_no_space"], inplace=True)

# 🔹 5. 정제된 리뷰 로드 및 감성/본문 분리
with open(ai_cleaned_path, "r", encoding="utf-8-sig") as f:
    lines = [line.strip().strip('"') for line in f if line.strip()]

lines = lines[:len(df_filtered)]  # 정합성 맞춤
df_ai = pd.DataFrame(lines, columns=["ai_result"])
df_ai[["type", "clean_reviews"]] = df_ai["ai_result"].str.split(",", n=1, expand=True)
df_ai.drop(columns=["ai_result"], inplace=True)

# 🔹 6. 병합
if len(df_filtered) != len(df_ai):
    raise ValueError(f"병합 불가: df_filtered({len(df_filtered)}), df_ai({len(df_ai)})")

df_filtered["type"] = df_ai["type"]
df_filtered["clean_reviews"] = df_ai["clean_reviews"]

# 🔹 7. 중복 제거 (nickname, text, write_date 기준)
df_deduplicated = df_filtered.drop_duplicates(subset=["nickname", "text", "write_date"], keep="first").reset_index(drop=True)

# 🔹 8. 저장
df_deduplicated.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"병합 및 중복 제거 완료: {output_path} (총 {len(df_deduplicated)}개)")
