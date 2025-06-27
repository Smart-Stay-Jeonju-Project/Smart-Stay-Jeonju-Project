from flask import Blueprint, render_template, request

bp = Blueprint('search', __name__, url_prefix='/search')

from dbms.search_Service import accommodations_list


@bp.route('/', methods=['GET'])
def search() : 
    print("search.py :: search()")
    type = request.args.get('search_type')
    word = request.args.get('keyword')
    print(f"search_type {type}")
    print(f"keyword {word}")
    # 검색결과 페이지
    return render_template('search.html', contents=accommodations_list(word))