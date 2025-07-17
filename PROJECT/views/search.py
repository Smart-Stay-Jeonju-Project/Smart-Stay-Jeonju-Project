from flask import Blueprint, render_template, request, redirect, flash
from dbms.search_Service import accommodations_list
from views.main import keywords 
import os

bp = Blueprint('search', __name__, url_prefix='/')
google_maps_api_key = os.getenv('API_KEY_MAPS')
print('API KEY:', google_maps_api_key)

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
            
            df['name'] = str(df['name']).strip()
            df['address'] = str(df['address']).strip()
            df['rating'] = float(df['rating'])
            

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
                    google_maps_api_key=google_maps_api_key,
                    result=f"'{search_term}' 검색 결과 {accom_result['total']}건"
                )
            else:
                return redirect('/')
    
    except Exception as e:
        print(e)
        return redirect('/')
