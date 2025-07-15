from flask import Blueprint, request, render_template, flash, redirect, current_app
import os
import pandas as pd
from utils.filename import get_image_url

bp = Blueprint('result', __name__, url_prefix='/result')

# result.html 숙소정보 제공
@bp.route('/', methods=['GET'])
def on_result() :
    name = request.args.get('name', '').strip()
    # print(f"[DEBUG] 요청된 name: {name}")

    csv_path = os.path.join('data', 'tmp', 'practice.csv')
    df = pd.read_csv(csv_path, encoding='utf-8')

    # print("[DEBUG] CSV 로드 완료. 행 개수:", len(df))

    matched = df[df['name'].astype(str).str.strip() == name]
    # print("[DEBUG] 매칭된 행 개수:", len(matched))
    if matched.empty :
        flash("해당 숙소 정보를 찾을 수 없습니다.", "error")
        return redirect('/')

    # 숙소 정보 딕셔너리
    row = matched.iloc[0].to_dict()
    # 이미지 경로 추가
    row['image_url'] = get_image_url(row['name'])

    # print(">>> lat:", row.get('lat'), "lng:", row.get('lng'))
    # print(">>> type:", type(row.get('lat')), type(row.get('lng')))

    return render_template(
        'result.html',
        accommodation=row,
        search_term=name,
        google_maps_api_key=current_app.config['API_KEY_MAPS']
    )
