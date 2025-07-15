import pandas as pd

# 🔹 파일 경로
input_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/accommodations/yeogi/clean_yeogi_info.csv"
output_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/accommodations/yeogi/y_duple.csv"

# 🔹 CSV 파일 로드
df = pd.read_csv(input_path)

# 🔹 address 기준으로 중복 제거 (첫 번째 행만 유지)
df_deduped = df.drop_duplicates(subset="address", keep="first")

# 🔹 결과 저장
df_deduped.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"✅ 중복 제거 완료: {len(df) - len(df_deduped)}개 중복 제거 → 총 {len(df_deduped)}개 남음")
