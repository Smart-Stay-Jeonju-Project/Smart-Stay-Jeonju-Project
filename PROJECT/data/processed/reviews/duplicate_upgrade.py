# nickname, text, write_date 일치 시 광고로 판단 하고 중복 내용 제거까지

import pandas as pd

# 파일 경로 설정
duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_reviews.csv"
only_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_only_texts.csv"
ai_cleaned_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_ai_cleaned_reviews.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_filtered_up.csv"
# duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews.csv"
# only_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_only_texts.csv"
# ai_cleaned_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_ai_cleaned_reviews.csv"
# output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_filtered_up.csv"

# 데이터 불러오기
df_duple = pd.read_csv(duple_path)
df_only = pd.read_csv(only_path, header=None, names=["text"])

# 공백 제거
df_duple["text_no_space"] = df_duple["text"].astype(str).str.replace(" ", "")
df_only["text_no_space"] = df_only["text"].astype(str).str.replace(" ", "")

# 딕셔너리 생성
duple_dict = df_duple.drop_duplicates(subset="text_no_space").set_index("text_no_space").to_dict(orient="index")

# ai_cleaned 결과 불러오기
with open(ai_cleaned_path, "r", encoding="utf-8-sig") as f :
    lines = [line.strip().strip('"') for line in f if line.strip()]

if len(lines) != len(df_only) :
    raise ValueError(f"줄 수 불일치: ai_cleaned({len(lines)}), only_texts({len(df_only)})")

# ai_cleaned 내용 분리
df_ai = pd.DataFrame(lines, columns=["ai_result"])
df_ai[["type", "clean_reviews"]] = df_ai["ai_result"].str.split(",", n=1, expand=True)
df_ai.drop(columns=["ai_result"], inplace=True)

# df_only와 df_ai 병합
df_only["type"] = df_ai["type"]
df_only["clean_reviews"] = df_ai["clean_reviews"]

# df_duple 정보 병합 (순서 보존)
merged_rows = []
for _, row in df_only.iterrows() :
    key = row["text_no_space"]
    if key in duple_dict:
        base = duple_dict[key].copy()
        base["type"] = row["type"]
        base["clean_reviews"] = row["clean_reviews"]
        merged_rows.append(base)

# 최종 병합 DataFrame
df_merged = pd.DataFrame(merged_rows)

# 중복 제거 (nickname + text + write_date)
df_final = df_merged.drop_duplicates(subset=["nickname", "text", "write_date"], keep="first").reset_index(drop=True)

# 저장
df_final.to_csv(output_path, index=False, encoding="utf-8-sig")
print(f"병합 및 중복 제거 완료: {output_path} (총 {len(df_final)}개)")