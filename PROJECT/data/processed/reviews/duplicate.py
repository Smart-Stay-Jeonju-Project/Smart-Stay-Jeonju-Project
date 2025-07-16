import pandas as pd

# 파일 경로 설정
duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_reviews.csv"
only_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_only_texts.csv"
ai_cleaned_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_ai_cleaned_reviews.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_reviews_filtered.csv"
# duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews.csv"
# only_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_only_texts.csv"
# ai_cleaned_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_ai_cleaned_reviews.csv"
# output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews_filtered.csv"

# 데이터 로드
df_duple = pd.read_csv(duple_path)
df_only = pd.read_csv(only_path, header=None, names=["text"])

# 공백 제거한 버전
df_duple["text_no_space"] = df_duple["text"].astype(str).str.replace(" ", "")
df_only["text_no_space"] = df_only["text"].astype(str).str.replace(" ", "")

# 중복 제거된 duple 딕셔너리 생성
text_map = {}
for i, row in df_duple.iterrows():
    key = row["text_no_space"]
    if key not in text_map:
        text_map[key] = row

# only_texts 기준으로 실제 존재하는 텍스트만 추출
valid_texts = []
filtered_rows = []
for t in df_only["text_no_space"]:
    if t in text_map:
        valid_texts.append(t)
        filtered_rows.append(text_map[t])

# DataFrame으로 변환
df_filtered = pd.DataFrame(filtered_rows).reset_index(drop=True)
df_filtered.drop(columns=["text_no_space"], inplace=True)

# ai_cleaned 불러오기
with open(ai_cleaned_path, "r", encoding="utf-8-sig") as f:
    lines = [line.strip().strip('"') for line in f if line.strip()]

# 정제 결과도 valid_texts 수만큼 자르기
lines = lines[:len(valid_texts)]

# 병합을 위한 분리
df_ai = pd.DataFrame(lines, columns=["ai_result"])
df_ai[["type", "clean_reviews"]] = df_ai["ai_result"].str.split(",", n=1, expand=True)
df_ai.drop(columns=["ai_result"], inplace=True)

# 길이 일치 여부 확인
if len(df_filtered) != len(df_ai):
    raise ValueError(f"❌ 병합 불가: df_filtered({len(df_filtered)}), df_ai({len(df_ai)})")

# 병합
df_filtered["type"] = df_ai["type"]
df_filtered["clean_reviews"] = df_ai["clean_reviews"]

# 저장
df_filtered.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"✅ 병합 완료: {output_path} (총 {len(df_filtered)}개)")