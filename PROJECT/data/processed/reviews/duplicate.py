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

# 공백 제거
df_duple["text_no_space"] = df_duple["text"].astype(str).str.replace(" ", "")
df_only["text_no_space"] = df_only["text"].astype(str).str.replace(" ", "")

# 중복 제거된 duple 딕셔너리 생성 (text_no_space 기준)
text_map = {}
for i, row in df_duple.iterrows():
    key = row["text_no_space"]
    if key not in text_map:
        text_map[key] = row

# ai_cleaned 파일에서 줄마다 대응
valid_rows = []
clean_results = []

with open(ai_cleaned_path, "r", encoding="utf-8-sig") as f:
    lines = [line.strip().strip('"') for line in f if line.strip()]

# 줄 수와 df_only 수가 반드시 같아야 함
if len(lines) != len(df_only):
    raise ValueError(f" 정제 데이터 줄 수({len(lines)})와 원본 리뷰 수({len(df_only)})가 일치하지 않습니다.")

for i in range(len(df_only)):
    key = df_only.loc[i, "text_no_space"]
    line = lines[i]
    if key in text_map:
        row = text_map[key].copy()
        row["ai_result"] = line
        valid_rows.append(row)

# DataFrame 생성 및 분리
df_filtered = pd.DataFrame(valid_rows).reset_index(drop=True)
df_filtered[["type", "clean_reviews"]] = df_filtered["ai_result"].str.split(",", n=1, expand=True)
df_filtered.drop(columns=["text_no_space", "ai_result"], inplace=True)

# 저장
df_filtered.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"정확히 매칭된 리뷰 {len(df_filtered)}개 병합 완료 → {output_path}")