import pandas as pd

# 🔹 파일 경로 설정
duple_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews_filtered.csv"
cleaned_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_ai_cleaned_reviews.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_reviews_final.csv"

# 🔹 1. 원본 리뷰 데이터 로드
df_duple = pd.read_csv(duple_path)

# 🔹 2. 정제된 리뷰 데이터 로드 및 처리
with open(cleaned_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# 🔹 3. 큰따옴표 제거 + 첫 쉼표 기준으로 분리
cleaned_data = []
for line in lines:
    line = line.strip().strip('"')  # 큰따옴표 제거 및 줄바꿈 제거
    if "," in line:
        type_part, review_part = line.split(",", 1)  # 첫 쉼표 기준 분리
        cleaned_data.append([type_part.strip(), review_part.strip()])
    else:
        cleaned_data.append(["ERROR", "ERROR"])  # 예외 처리

# 🔹 4. DataFrame 생성
df_cleaned = pd.DataFrame(cleaned_data, columns=["type", "clean_reviews"])

# 🔹 5. 길이 일치 확인 후 병합
if len(df_duple) != len(df_cleaned):
    print(f"❌ 길이 불일치: duple({len(df_duple)}), cleaned({len(df_cleaned)})")
else:
    # 🔹 컬럼 추가
    df_final = df_duple.copy()
    df_final["type"] = df_cleaned["type"]
    df_final["clean_reviews"] = df_cleaned["clean_reviews"]

    df_final = df_final[[
    "name", "nickname", "text", "review_rating", "write_date", "source",
    "type", "clean_reviews"
    ]]

    # 🔹 결과 저장
    df_final.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 병합 완료 → {output_path} 저장됨 (총 {len(df_final)}개)")
