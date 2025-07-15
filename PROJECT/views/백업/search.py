from flask import Blueprint, render_template, request, url_for, current_app, flash, redirect
import os
import pandas as pd
from utils.filename import get_image_url

# 주소/search_map/ 으로 접근 => bp.route('/')에 의해 search.html 렌더링
bp = Blueprint('search', __name__, url_prefix='/search_map')

# search.html 지도 마커에 표시할 정보
@bp.route('/', methods=['GET'])
def on_search() :

    search_type = request.args.get('search_type', '')
    search_term = request.args.get('search_term', '')

    if not search_type or not search_term :
        flash("올바르지 않은 접근 방식입니다. 메인 페이지에서 검색을 진행해주세요.", "error")
        return redirect('/')  # 메인 페이지로 이동
    
    csv_path = os.path.join('data', 'tmp', 'practice.csv')
    df = pd.read_csv(csv_path, encoding='utf-8')
    df = df[['name', 'address', 'lat', 'lng']].dropna()

    # print("search.py API_KEY_MAPS:", current_app.config.get("API_KEY_MAPS"))

    # 숙소 리스트를 딕셔너리로
    accommodations = df.to_dict(orient='records')
    # 이미지 경로 추가
    for row in accommodations :
        row['image_url'] = get_image_url(row['name'])
        # print(f"숙소 이름: {row['name']}, 생성된 이미지 URL: {row['image_url']}")

    return render_template(
        'search.html',
        search_type=search_type,
        search_term=search_term,
        accommodations=accommodations,
        result=f"검색 결과 {len(accommodations)}건",
        google_maps_api_key=current_app.config['API_KEY_MAPS']
    )