from flask import Blueprint

bp = Blueprint('search', __name__, url_prefix='/search')

@bp.route('/', methods=['GET'])
def search() : 
    # 검색결과 페이지
    return "검색결과 페이지"
