from flask import Blueprint

bp = Blueprint('result', __name__, url_prefix='/result')

@bp.route('/')
def result() : 
    # 상세 페이지
    return "상세 페이지"

