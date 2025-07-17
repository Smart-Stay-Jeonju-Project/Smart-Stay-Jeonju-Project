from flask import Blueprint, render_template, request, redirect, flash, jsonify
import pandas as pd
import os
from utils.filename import get_image_url
from dbms.search_Service import accommodations_list
from dbms.main_Service import load_categorys
from dbms.search_Service import load_keywords


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
    
    datas = category_list['list']
    #print("data :", datas)

    try:
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
        #flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
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
        #flash("일치하는 자료가 없습니다. 다시 검색해주세요.", "error")
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