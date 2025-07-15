import pandas as pd

# 파일 경로
file_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_reviews.csv"

# CSV 파일을 문자열로 불러오기 (원본 형식 유지)
with open(file_path, "r", encoding="utf-8-sig") as f:
    lines = f.readlines()

# 각 줄 끝에 ',' 추가
updated_lines = [line.rstrip("\n").rstrip(",") + ",\n" for line in lines]

# 덮어쓰기 저장
with open(file_path, "w", encoding="utf-8-sig") as f:
    f.writelines(updated_lines)

print("✅ 모든 줄 끝에 ','를 추가 완료했습니다.")
