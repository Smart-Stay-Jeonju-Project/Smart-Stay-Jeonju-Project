from flask import Blueprint, render_template, request, redirect, flash, url_for
import pandas as pd
import os

bp = Blueprint('main', __name__, url_prefix='/')

# 키워드 목록들
def load_keywords():
    csv_path = os.path.join('DATA', 'list', 'tmp', 'practice.csv')
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        df['keyword'] = df['keyword'].astype(str).str.strip()

        keywords = set()
        for kw in df['keyword']:
            if not kw:
                continue
            for part in kw.split(','):
                part = part.strip()
                if not part:
                    continue

                # 공백 제거한 키워드로 저장
                keywords.add(part.replace(" ", ""))

        return sorted(keywords)
    except:
        return []

# 키워드 목록들을 불러오는
@bp.route('/')
def home():
    keyword_list = load_keywords()
    return render_template('layout.html', keyword_list=keyword_list)

# 검색타입 선택에 따른 기능들
@bp.route('/search', methods=['GET'])
def search():
    search_type = request.args.get('search_type', '').strip()
    search_term = request.args.get('search_term', '').strip()
    print("search_type : ", search_type)
    print("search_term : ", search_term)

    csv_path = os.path.join('DATA', 'list', 'tmp', 'practice.csv')

    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        df['name'] = df['name'].astype(str).str.strip()
        df['address'] = df['address'].astype(str).str.strip()

        # 상호명 검색 (2글자 이상 포함)
        if search_type == 'name' :
            if len(search_term) < 2:
                flash("검색어는 2글자 이상 입력해주세요.", "error")
                return redirect('/')
            # 이름 컬럼이 NaN이 아닌 값으로만 구하는 필터
            df['name'] = df['name'].astype(str).fillna('').str.strip()
            # 검색 하는
            # case=False : 대소문자 구분X, na=False : NaN도 False로 처리
            filtered_df = df[df['name'].str.contains(search_term, case=False, na=False, regex=False)]
            #검색 결과 체크 해보는
            print("contains : \n",filtered_df[['name']])
            if not filtered_df.empty:
                results = filtered_df.to_dict(orient='records')
                print(filtered_df,results)
                return render_template(
                    'search.html',
                    results=results,
                    search_type=search_type,
                    search_term=search_term,
                    accommodations=results, 
                    keyword_list=load_keywords(),
                    result=f"검색 결과 {len(results)}건"
                )
            else :
                flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
                return redirect('/')

        # 키워드 검색
        elif search_type == 'keyword':
            df['keyword'] = df['keyword'].astype(str).fillna('').str.strip()
            
            # keyword 컬럼 내 쉼표로 구분된 키워드 각각에 대해 검색
            word = df['keyword'].apply(lambda x: any(search_term == k.strip().replace(" ", "") for k in x.split(',')))

            filtered_df = df[word]
            
            if not filtered_df.empty:
                results = filtered_df.to_dict(orient='records')
                return render_template(
                    'search.html',
                    results=results,
                    search_type=search_type,
                    search_term=search_term,
                    accommodations=results,
                    keyword_list=[search_term],
                    result=f"'{search_term}' 키워드 검색 결과 {len(results)}건"
                )
            else:
                flash("해당 키워드에 해당하는 자료가 없습니다.", "error")
                return redirect('/')
            
        # 주소 검색 (덕진구, 완산구 요청)
        # 직접 주소 입력, 전주시만 검색 등 다른 요소 추가
        elif search_type == 'address' :
            if search_term not in ['덕진구', '완산구']:
                flash("주소를 정확히 선택해주세요.", "error")
                return redirect('/')
            # 주소 컬럼에 선택한 구 이름 포함 여부 필터링
            filtered_df = df[df['address'].str.contains(search_term, case=False, na=False, regex=False)]
            # print(filtered_df[['address']])
            if not filtered_df.empty:
                results = filtered_df.to_dict(orient='records')
                return render_template(
                    'search.html',
                    results=results,
                    search_type=search_type,
                    search_term=search_term,
                    accommodations=results,
                    keyword_list=load_keywords(),
                    result=f"검색 결과 {len(results)}건"
                )
            else:
                flash("해당 주소에 일치하는 자료가 없습니다.", "error")
                return redirect('/')
        else:
            flash("지원하지 않는 검색 유형입니다.", "error")
            return redirect('/')
    except FileNotFoundError:
        flash("데이터 파일을 찾을 수 없습니다.", "error")
        return redirect('/')