import os
from flask import url_for

# name 컬럼 이름 정제
def get_image_url(name):
    target_clean_name = name.replace(" ", "").replace("-", "")
    image_dir = os.path.join("static", "images", "tmp")
    # 이미지 파일이름 정제
    try:
        for filename in os.listdir(image_dir):
            name_without_ext, ext = os.path.splitext(filename)
            clean_filename = name_without_ext.replace(" ", "").replace("-", "")
            if target_clean_name == clean_filename:
                return url_for("static", filename=f"images/tmp/{filename}")
    except FileNotFoundError:
        pass

    return url_for("static", filename="images/tmp/default.jpg")