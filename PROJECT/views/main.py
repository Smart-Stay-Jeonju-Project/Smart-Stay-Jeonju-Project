from flask import Blueprint, render_template, request, redirect, flash, jsonify
import pandas as pd
import os
from utils.filename import get_image_url

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main():
    category = request.args.get('category', '호텔').strip() # 일단 기본값 호텔
    accommodations = []
    keyword_list = load_keywords()

    csv_path = os.path.join('DATA', 'tmp', 'practice.csv')
    
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        # 추천 숙소 리스트에 띄울 데이터들 정제
        df['category'] = df['category'].astype(str).fillna('').str.strip()
        df['name'] = df['name'].astype(str).fillna('').str.strip()
        df['address'] = df['address'].astype(str).fillna('').str.strip()
        df['rating_score'] = df['rating_score'].astype(float)
        df['rating_count'] = (
            df['rating_count']
            .astype(str).str.replace('"', '').str.replace(',', '')
            .pipe(pd.to_numeric, errors='coerce')
            .fillna(0).astype(int)
        )

        # category 필터링
        filtered_df = df[df['category'].str.contains(category, case=False, na=False)]

        # 추천 숙소 데이터들
        for _, row in filtered_df.iterrows():
            accommodation = {
                "name": row['name'],
                "address": row['address'],
                "rating_score": row['rating_score'],
                "rating_count": row['rating_count'],
                "formatted_rating_count": f"{row['rating_count']:,}" if row['rating_count'] >= 1000 else str(row['rating_count']),
                "image_url": get_image_url(row['name'])
            }
            accommodations.append(accommodation)

    except Exception as e:
        print(e)

    return render_template(
        'main.html',
        keyword_list=keyword_list,
        accommodations=accommodations,
        selected_category=category
    )


# 키워드 목록들
def load_keywords():
    csv_path = os.path.join('DATA', 'tmp', 'practice.csv')
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
                keywords.add(part.replace(" ", ""))

        return sorted(keywords)
    except Exception as e:
        return []

# 검색타입 선택에 따른 기능들
@bp.route('/search', methods=['GET'])
def search():
    search_type = request.args.get('search_type', '').strip()
    search_term = request.args.get('search_term', '').strip()
    # print("search_type : ", search_type)
    # print("search_term : ", search_term)

    # csv 파일 경로
    csv_path = os.path.join('DATA', 'tmp', 'practice.csv')

    try:
        # CSV 파일에서 필요한 컬럼들을 모두 읽어옵니다.
        # 'rating_score'와 'rating_count' 추가
        df = pd.read_csv(csv_path, encoding='utf-8')
        df['name'] = df['name'].astype(str).str.strip()
        df['address'] = df['address'].astype(str).str.strip()
        # rating_score는 실수 타입으로
        df['rating_score'] = df['rating_score'].astype(float)
        # rating_count 
        # 문자열로 변환 후 따옴표와 쉼표 제거
        df['rating_count'] = df['rating_count'].astype(str).str.replace('"', '').str.replace(',', '')
        # 숫자로 강제 변환 시도 (errors='coerce'로 변환 실패 시 NaN으로)
        df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')
        # NaN 값은 0으로 채우거나 적절한 기본값으로 채운 후 정수로 변환
        df['rating_count'] = df['rating_count'].fillna(0).astype(int) # NaN은 0으로 채우고 정수로

        filtered_df = pd.DataFrame()

        # 선택 타입 : 상호명
        if search_type == 'name':
            if len(search_term) < 2:
                flash("검색어는 2글자 이상 입력해주세요.", "error")
                return redirect('/')
            # 2글자 이상 단어 포함하면 검색 되게 하는
            df['name'] = df['name'].astype(str).fillna('').str.strip()
            filtered_df = df[df['name'].str.contains(search_term, case=False, na=False, regex=False)]

        # 선택 타입 : 키워드
        elif search_type == 'keyword':
            df['keyword'] = df['keyword'].astype(str).fillna('').str.strip()
            word = df['keyword'].apply(lambda x: any(search_term == k.strip().replace(" ", "") for k in x.split(',')))
            filtered_df = df[word]

        # 선택 타입 : 주소
        elif search_type == 'address':
            if search_term not in ['덕진구', '완산구']:
                flash("주소를 정확히 선택해주세요.", "error")
                return redirect('/')
            # 덕진구, 완산구를 검색했을 때 검색 되게
            filtered_df = df[df['address'].str.contains(search_term, case=False, na=False, regex=False)]
        else:
            flash("지원하지 않는 검색 유형입니다.", "error")
            return redirect('/')

        # 검색 결과가 있는 경우에만 image_url을 추가하고 템플릿 렌더링
        if not filtered_df.empty:
            results = filtered_df.to_dict(orient='records')
            # 여기서 image_url을 각 결과에 추가 
            for row in results: # filtered_df가 아닌 results에 추가
                row['image_url'] = get_image_url(row['name'])
                # rating_score 포맷팅
                row['rating_score']
                # rating_count 포맷팅
                if row['rating_count'] < 1000:
                    row['formatted_rating_count'] = str(row['rating_count'])
                else:
                    row['formatted_rating_count'] = f"{row['rating_count']:,}"

            # 키워드 검색일 때 selected_keywords
            selected_keywords = [search_term] if search_type == 'keyword' else []

            return render_template(
                'search.html',
                results=results, # results를 보내줍니다.
                search_type=search_type,
                search_term=search_term,
                accommodations=results, # accommodations로도 results를 보냅니다.
                keyword_list=load_keywords(), # 모든 키워드 리스트
                selected_keywords=selected_keywords,
                result=f"'{search_term}' 검색 결과 {len(results)}건"
            )
        else:
            flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
            return redirect('/')

    except FileNotFoundError:
        flash("데이터 파일을 찾을 수 없습니다.", "error")
        return redirect('/')

# 자동완성 검색기능
@bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    search_type = request.args.get('search_type', '')
    term = request.args.get('term', '').strip().lower().replace('-', '').replace(' ', '')

    suggestions = []
    csv_path = os.path.join('DATA', 'tmp', 'practice.csv')

    try:
        df = pd.read_csv(csv_path, encoding='utf-8')
        df['name'] = df['name'].astype(str).fillna('').str.strip()
        if search_type == 'name':
            for name in df['name']:
                name_lower = name.lower().replace('-', '').replace(' ', '')

                # 단어별 검색을 위해 원래 단어 기준도 따로 보존
                words = name.lower().replace('-', ' ').split()

                # 각 단어도 공백, '-' 제거 후 비교
                normalized_words = [w.replace(' ', '') for w in words]

                if (name_lower.startswith(term) or                          # 전체 이름이 term으로 시작
                    # any(w.startswith(term) for w in normalized_words)) :     # 단어 중 하나라도 term으로 시작
                    any(term in w and len(term) >= 2 for w in normalized_words)) : # 2글자 이상 포함된 
                    suggestions.append(name)

        return jsonify(sorted(set(suggestions))[:5])    # 인덱스 0-4까지만 출력
    except Exception as e:
        print(e)