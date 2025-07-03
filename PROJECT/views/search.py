from flask import Blueprint, render_template, request

bp = Blueprint('search', __name__, url_prefix='/search')

# search.html에서 검색 타입, 검색 결과 제공
@bp.route('/', methods=['GET'])
def on_search():
    search_type = request.args.get('search_type', '')
    search_term = request.args.get('search_term', '')

    return render_template(
        'search.html',
        search_type=search_type,
        search_term=search_term
    )
