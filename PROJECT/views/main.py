<<<<<<< HEAD
# 0627 이태양 작업중

from flask import Blueprint, render_template, redirect, url_for, request

bp = Blueprint('main', __name__, url_prefix='/')

# 메인페이지 연결
@bp.route('/')
def main() :  
    return render_template('main.html')

# 검색결과 페이지 연결
@bp.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        type = request.form.get('search_type')
        word = request.form.get('keyword')
        return redirect(url_for('search.search', search_type=type, keyword=word))
        # return redirect(url_for('search', data=data))
        # return redirect(url_for('search.html', data=data))
    return render_template('search.html')
=======
from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def main() : 
    # 메인페이지 
    return "메인페이지"
>>>>>>> f65089d4acbb4c0a2622a316e7e98f5d005042df
