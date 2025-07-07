from flask import Blueprint, render_template, request, url_for
import os
import pandas as pd
from utils.filename import get_image_url

bp = Blueprint('search', __name__, url_prefix='/search')

# search.html에서 검색 타입, 검색 결과 제공
@bp.route('/', methods=['GET'])
def on_search():
    search_type = request.args.get('search_type', '')
    search_term = request.args.get('search_term', '')

    csv_path = os.path.join('data', 'tmp', 'practice.csv')
    df = pd.read_csv(csv_path, encoding='utf-8')
    df = df[['name', 'address', 'lat', 'lng']].dropna()

    accommodations = df.to_dict(orient='records')

    for row in accommodations:
        row['image_url'] = get_image_url(row['name'])
        print(f"숙소 이름: {row['name']}, 생성된 이미지 URL: {row['image_url']}")

    return render_template(
        'search.html',
        search_type=search_type,
        search_term=search_term,
        accommodations=accommodations,
        result=f"검색 결과 {len(accommodations)}건"
    )