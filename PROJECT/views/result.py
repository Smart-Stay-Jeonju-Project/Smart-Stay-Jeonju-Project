from flask import Blueprint, request, render_template, flash, redirect
import os
import pandas as pd
from utils.filename import get_image_url

bp = Blueprint('result', __name__, url_prefix='/result')

# result.html에서 검색 타입, 검색 결과 제공
@bp.route('/', methods=['GET'])
def on_result():
    search_type = request.args.get('search_type', '').strip()
    search_term = request.args.get('search_term', '').strip()
    name = request.args.get('name', '').strip()  # 숙소명

    csv_path = os.path.join('DATA', 'list', 'tmp', 'practice.csv')

    try:
        df = pd.read_csv(csv_path, encoding='utf-8')

        if name:  # 숙소 상세 보기
            matched = df[df['name'].astype(str).str.strip() == name]
            if matched.empty:
                flash("해당 숙소 정보를 찾을 수 없습니다.", "error")
                return redirect('/')
            row = matched.iloc[0].to_dict()
            row['image_url'] = get_image_url(row['name'])
            return render_template('result.html', accommodation=row)

        else:  # 기존 검색 결과 보기 (기존 방식 유지)
            return render_template(
                'result.html',
                search_type=search_type,
                search_term=search_term
            )

    except FileNotFoundError:
        flash("데이터 파일을 찾을 수 없습니다.", "error")
        return redirect('/')

