import os
import re
import difflib
import pandas as pd
import shutil  # 파일 복사/이동용

# === 1. 설정 ===
image_folder = "data/raw/yanolja_img/"  # 원본 이미지 폴더
save_folder = "data/raw/yanolja_img_renamed/"  # 새 폴더
extension = ".jpg"

# 새 폴더가 없으면 생성
os.makedirs(save_folder, exist_ok=True)

# === 2. 정제된 숙소 이름 불러오기 ===
info_df = pd.read_csv("analysis/정리된_숙소_주소.csv")
clean_names = info_df["name"].tolist()

# === 3. 리네이밍 및 복사 수행 ===
for filename in os.listdir(image_folder):
    if filename.lower().endswith(extension):
        # 1) 숫자_ 제거
        name_only = re.sub(r'^\d+_', '', filename).replace(extension, '')

        # 2) 가장 유사한 숙소 이름 찾기
        matches = difflib.get_close_matches(name_only, clean_names, n=1, cutoff=0.5)
        try:
            if matches:
                best_match = matches[0]
                new_filename = best_match + extension
                src = os.path.join(image_folder, filename)
                dst = os.path.join(save_folder, new_filename)

                # 3) 이름이 다를 경우 새 폴더에 복사 (또는 이동)
                if filename != new_filename:
                    shutil.copy2(src, dst)  # 복사: 원본 유지
                    print(f"✔ {filename} → {new_filename}")
                else:
                    shutil.copy2(src, dst)
            else:
                print(f"✖ No match found for: {filename}")
        except Exception as e:
            print(f"⚠ 오류: {filename} - {e}")
