from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main() : 
    # 메인페이지 
    return "메인페이지"