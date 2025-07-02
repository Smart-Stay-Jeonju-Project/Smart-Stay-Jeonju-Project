from flask import Blueprint, render_template, request
import os
import pandas as pd

bp = Blueprint('search', __name__, url_prefix='/search')

# search.html에서 검색 타입, 검색 결과 제공
@bp.route('/', methods=['GET'])
def on_search():
    search_type = request.args.get('search_type', '')
    search_term = request.args.get('search_term', '')

    csv_path = os.path.join('DATA', 'list', 'tmp', 'practice.csv')
    df = pd.read_csv(csv_path, encoding='utf-8')
    df = df[['name', 'lat', 'lng']].dropna()

    accommodations = df.to_dict(orient='records')

    return render_template(
        'search.html',
        search_type=search_type,
        search_term=search_term,
        accommodations=accommodations,
        result=f"검색 결과 {len(accommodations)}건"
    )