import os
from flask import url_for

# 이미지 경로 설정
def get_image_url(name) :
    # name 컬럼 정제 : 공백 & - 제거, 대문자로
    target_name = name.replace(" ", "").replace("-", "").upper()
    # print(target_name)
    image_dir = os.path.join("static", "images", "tmp")
    # 이미지 파일 이름 정제
    try:
        for filename in os.listdir(image_dir) :
            name_without_ext, ext = os.path.splitext(filename)
            # 인덱스가 포함된 경우와 없는 경우 모두 처리
            if '_' in name_without_ext :
                # 인덱스_ 제거
                parts = name_without_ext.split('_', 1)
                image_name_part = parts[1]  
            else:
                image_name_part = name_without_ext
            # 공백 & - 제거, 대문자로
            image_name = image_name_part.replace(" ", "").replace("-", "").upper()
            # print(image_name)

            # 일치시 이미지 가져옴
            if target_name == image_name:
                return url_for("static", filename=f"images/tmp/{filename}")

    except Exception as e:
        print(e)

    return
