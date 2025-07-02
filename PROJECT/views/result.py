from flask import Blueprint, request, render_template

bp = Blueprint('result', __name__, url_prefix='/result')

# result.html에서 검색 타입, 검색 결과 제공
@bp.route('/', methods=['GET'])
def on_result():
    search_type = request.args.get('search_type', '')
    search_term = request.args.get('search_term', '')

    return render_template(
        'result.html',
        search_type=search_type,
        search_term=search_term
    )


