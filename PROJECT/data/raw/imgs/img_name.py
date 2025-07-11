import os
import re
import difflib
import pandas as pd

# === 1. 설정 ===
image_folder = "data/raw/imgs/"  # 이미지 폴더 경로를 여기에 설정
extension = ".jpg"

# === 2. 정제된 숙소 이름 불러오기 ===
info_df = pd.read_csv("analysis/my/정리된_숙소_주소.csv")  # 같은 디렉토리에 있을 경우
clean_names = info_df["name"].tolist()

# === 3. 리네이밍 수행 ===
for filename in os.listdir(image_folder):
    if filename.lower().endswith(extension):
        # 1) 숫자_ 제거
        name_only = re.sub(r'^\d+_', '', filename).replace(extension, '')

        # 2) 가장 유사한 숙소 이름 찾기
        matches = difflib.get_close_matches(name_only, clean_names, n=1, cutoff=0.5)
        try :
            if matches:
                best_match = matches[0]
                new_filename = best_match + extension
                src = os.path.join(image_folder, filename)
                dst = os.path.join(image_folder, new_filename)

                # 3) 이름이 다를 경우 덮어쓰기
                if filename != new_filename:
                    os.rename(src, dst)
                    print(f"✔ {filename} → {new_filename}")
            else:
                print(f"✖ No match found for: {filename}")
        except Exception as e :
            continue