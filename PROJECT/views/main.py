from flask import Blueprint, render_template, request, redirect, flash, jsonify
import pandas as pd
import os
from utils.filename import get_image_url
from dbms.search_Service import accommodations_list
from dbms.main_Service import load_categorys
from dbms.main_Service import load_keywords


bp = Blueprint('main', __name__, url_prefix='/')

# 메인 페이지 카테고리 별 숙소 목록
@bp.route('/')
def main():
    category = request.args.get('category', '모텔/호텔').strip() # 일단 기본값 호텔
    accommodations = []

    # 선택한 카테고리별 숙소리스트 데이터베이스에서 가져오기
    category_list = load_categorys(category)

    if category_list :
        print("데이터베이스를 불러왔습니다")
    else : 
        print("데이터를 불러오지 못했습니다")
        return redirect('/')
    
    #csv_path = os.path.join('DATA', 'tmp', 'practice.csv')
    datas = category_list['list']
    #print("data :", datas)

    try:
        #df = pd.read_csv(csv_path, encoding='utf-8')
        for data in datas :
            
            category_list = str(data.get('category', '')).strip()

            data['category'] = str(data['category']).strip()
            data['name'] = str(data['name']).strip()
            data['address'] = str(data['address']).strip()
            data['feature'] = str(data['feature']).strip()
            data['rating'] = float(data['rating'])


            # main.html에 보낼 숙소 목록
            accommodation = {
                "name": data['name'],
                "address": data['address'],
                "rating": data['rating'],
                "feature": data['feature'],
                "image": data['image'],
            }
            accommodations.append(accommodation)
            #print(accommodations)

    except Exception as e:
        print(e)

    return render_template(
        'main.html',
        category_list=category_list,
        accommodations=accommodations,
        selected_category=category,
        keyword_list=keywords()
    )


def keywords():
    keyword_list = []

    # 데이터베이스에서 불러온 리스트
    keywords = load_keywords()
    if keywords :
        print("데이터베이스를 불러왔습니다")
    else : 
        print("데이터를 불러오지 못했습니다")
        flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
        return redirect('/')
    
    datas = keywords['list']
    #print("keyword :", datas)

    try:
        for data in datas :
            data = data['keyword_text']

            print(data)
            keyword_list.append(data)

        return keyword_list

    except Exception as e:
        print(e)


# 검색타입 선택에 따른 기능들
@bp.route('/search', methods=['GET'])
def search():
    search_type = request.args.get('search_type', '').strip()
    search_term = request.args.get('search_term', '').strip()

    # 데이터베이스에서 불러온 리스트
    accom_result = accommodations_list(search_type, search_term)
    if accom_result :
        print("데이터베이스를 불러왔습니다")
    else : 
        print("데이터를 불러오지 못했습니다")
        flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
        return redirect('/')

    datas = accom_result['list']    # list
    print("datas :", type(datas))

    try:
        for df in datas :   # dict
            #print("df :", df)
            '''
            df['name'] = str(df['name']).strip()
            df['address'] = str(df['address']).strip()
            df['rating'] = float(df['rating'])
            '''

            # 선택 타입 : 상호명
            if search_type == 'name':
                if len(search_term) < 2:
                    flash("검색어는 2글자 이상 입력해주세요.", "error")
                    return redirect('/')
                # 2글자 이상 단어 포함하면 검색 되게 하는

            # 선택 타입 : 키워드
            elif search_type == 'keyword':
                '''
                df['keyword'] = df['keyword'].astype(str).fillna('').str.strip()
                word = df['keyword'].apply(lambda x: any(search_term == k.strip().replace(" ", "") for k in x.split(',')))
                filtered_df = df[word]
                '''

            # 선택 타입 : 주소
            elif search_type == 'address':
                #if search_term not in ['덕진구', '완산구']:
                if not search_term :
                    flash("주소를 정확히 입력해주세요.", "error")
                    return redirect('/')
            else:
                flash("지원하지 않는 검색 유형입니다.", "error")
                return redirect('/')
            
            if df:
                # 키워드 검색일 때 selected_keywords
                selected_keywords = [search_term] if search_type == 'keyword' else []
                print('선택한 키워드 :',selected_keywords)
                
                return render_template(
                    'search.html',
                    results=df, # results를 보내줍니다.
                    search_type=search_type,
                    search_term=search_term,
                    accom_list = accom_result['list'],  # search.html script로 리스트 보내기
                    accommodations=df, # html에 보여줄 accommodations
                    keyword_list=keywords(),
                    selected_keywords=selected_keywords,
                    result=f"'{search_term}' 검색 결과 {accom_result['total']}건"
                )
            else:
                flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
                return redirect('/')
    
    except Exception as e:
        print(e)
        return redirect('/')

# 자동완성 검색기능
@bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    search_type = request.args.get('search_type', '')
    term = request.args.get('term', '').strip().lower().replace('-', '').replace(' ', '')

    suggestions = []

    autolist = accommodations_list(search_type, term)
    if autolist :
        print("데이터베이스를 불러왔습니다")
    else : 
        print("데이터를 불러오지 못했습니다")
        flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
        return redirect('/')

    datas = autolist['list']

    try:
        for data in datas :
            # 선택 타입 : 상호명
            if search_type == 'name':
                name = data['name']
                name_lower = name.lower().replace('-', '').replace(' ', '')

                # 단어별 검색을 위해 원래 단어 기준도 따로 보존
                words = name.lower().replace('-', ' ').split()

                # 각 단어도 공백, '-' 제거 후 비교
                normalized_words = [w.replace(' ', '') for w in words]

                if (name_lower.startswith(term) or                          # 전체 이름이 term으로 시작
                    any(term in w and len(term) >= 2 for w in normalized_words)) : # 2글자 이상 포함된 
                    suggestions.append(name)

        return jsonify(sorted(set(suggestions))[:5])    # 인덱스 0-4까지만 출력

    
    except Exception as e:
        print(e)
        return redirect('/')