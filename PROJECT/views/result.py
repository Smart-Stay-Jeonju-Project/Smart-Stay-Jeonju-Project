<<<<<<< HEAD
from flask import Blueprint, render_template

bp = Blueprint('result', __name__, url_prefix='/result')

@bp.route('/')
def result() : 
    print("result.py :: result()")
    # 상세 페이지
    return render_template('result.html')

# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
# 이 페이지 삭제 고민
=======
from flask import Blueprint

bp = Blueprint('result', __name__, url_prefix='/result')

@bp.route('/')
def result() : 
    # 상세 페이지
    return "상세 페이지"

>>>>>>> f65089d4acbb4c0a2622a316e7e98f5d005042df
