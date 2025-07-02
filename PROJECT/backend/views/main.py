from flask import Blueprint, render_template, request, redirect, flash
import pandas as pd
import os

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/search', methods=['GET'])
def search():
    search_type = request.args.get('search_type', '').strip()
    search_term = request.args.get('search_term', '').strip()

    print(f"search_type: {search_type}")
    print(f"search_term: {search_term}")
    
    csv_path = os.path.join('DATA', 'list', 'tmp', 'practice.csv')
    df = pd.read_csv(csv_path, encoding='utf-8')
    df['name'] = df['name'].astype(str).str.strip()

    if search_type == 'name' : 
        if len(search_term) < 2:
            flash("검색어는 2글자 이상 입력해주세요.", "error")
            return redirect('/')
        # case=False : 대소문자 구분 X, na=False : NaN인 경우에도 False로 처리
        check_df = df[df['name'].str.contains(search_term, case=False, na=False, regex=False)]
            # 검색 결과 체크 해보는
            # print(check_df[['name']])  
        if not check_df.empty:
            results = check_df.to_dict(orient='records')
            return render_template('search.html', results=results, search_term=search_term)
        else:
            flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
            return redirect('/')

    if search_type == 'address':
        # 덕진구, 완산구 중 하나만 허용
        if search_term not in ['덕진구', '완산구']:
            flash("주소를 정확히 선택해주세요.", "error")
            return redirect('/')
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            df['address'] = df['address'].astype(str)

            # 주소 컬럼에 선택한 구 이름 포함 여부 필터링
            # case=False : 대소문자 구분X, na=False : NaN도 False로 처리
            filtered_df = df[df['address'].str.contains(search_term, case=False, na=False, regex=False)]

            if not filtered_df.empty:
                results = filtered_df.to_dict(orient='records')
                return render_template('search.html', results=results, search_term=search_term)
            else:
                flash("해당 주소에 일치하는 자료가 없습니다.", "error")
                return redirect('/')
        except FileNotFoundError:
            flash("데이터 파일을 찾을 수 없습니다.", "error")
            return redirect('/')
    else:
        flash("지원하지 않는 검색 유형입니다.", "error")
        return redirect('/')