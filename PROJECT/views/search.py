<<<<<<< HEAD
from flask import Blueprint, render_template, request

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET'])
def search() : 
    print("search.py :: search()")
    type = request.args.get('search_type')
    word = request.args.get('keyword')
    print(f"search_type {type}")
    print(f"keyword {word}")
    # 검색결과 페이지
    return render_template('search.html')
=======
from flask import Blueprint

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET'])
def search() : 
    # 검색결과 페이지
    return "검색결과 페이지"
>>>>>>> f65089d4acbb4c0a2622a316e7e98f5d005042df
