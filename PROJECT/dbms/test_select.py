from DBM import DBManager
from dotenv import load_dotenv
import os
load_dotenv()

# DMB 객체 생성
dbm = DBManager()
if dbm : 
    try : 
        dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))
        sql = 'select * from review'
        dbm.OpenQuery(sql,)
        datas = dbm.GetDatas()
        dbm.CloseQuery()
        #dbm.DBClose()
        # 조회된 결과를 출력
        if datas :
            print(datas)
            for data in datas :
                print(f"리뷰번호 : {data['review_id']}")
                print(f"숙소번호 : {data['accommodation_id']}")
                print(f"내용 : {data['content']}")
                print(f"작성일 : {data['write_date']}")
                print(f"별점 : {data['review_rating']}")
                print(f"출처 : {data['review_source']}")
                print(f"타입 : {data['review_type']}")
                print(f"닉네임 : {data['nickname']}")
                print('-'*20)
        dbm.DBClose()

    except Exception as e :
        print(e)