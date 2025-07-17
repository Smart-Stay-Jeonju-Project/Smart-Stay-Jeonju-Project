from flask import Blueprint, request, render_template, flash, redirect, current_app
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from utils.filename import get_image_url
from dbms.result_Service import result_accom
from views.main import keywords


bp = Blueprint('result', __name__, url_prefix='/result')
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
print('API KEY:', google_maps_api_key)

# result.html에서 검색 타입, 검색 결과 제공
@bp.route('/', methods=['GET'])
def on_result():
    search_type = request.args.get('search_type', '').strip()
    search_term = request.args.get('search_term', '').strip()

    name = request.args.get('name', '').strip()  # 숙소명
    #print(name)
    datas, r_datas, k_datas = result_accom(name)
    print('datas:',type(datas))      # dict
    #print('r_datas:',r_datas)        # list
    print("r_datas:",type(r_datas))     # list
    #print('k_datas:',k_datas)     # dict

    try:
        if not datas :
            flash("해당 숙소 정보를 찾을 수 없습니다.", "error")
            return redirect('/')
        else : 
            return render_template(
                'result.html',
                result_accommodation=datas,
                result_review=r_datas,
                result_keyword=k_datas,
                search_type=search_type,
                search_term=search_term,
                google_maps_api_key=google_maps_api_key,
                keyword_list=keywords()

        )
    except Exception as e:
        print(e)

