from dbms.DBM import DBManager
from dotenv import load_dotenv
import os
load_dotenv()

# DMB 객체 생성
dbm = DBManager()

# 검색 페이지의 목록에 출력할 데이터 DB에서 가져오는
# 검색어 word 받아서 sql문으로 조건 검색
def accommodations_list(word):
    result_list = None
    if dbm : 
        try :
            dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))
            sql = 'select * from accommodations where address like %s'
            keyword = word
            dbm.OpenQuery(sql, ("%"+keyword+"%",))
            total = dbm.GetTotal()
            if total > 0 :
                print(f"조회된 숙소 수 : {total}")
            else :
                return result_list
            datas = dbm.GetDatas()
            if datas : 
                result_list = {
                    'total': total, 
                    'list' : datas
                    }
        except Exception as e :
            print(e)
        finally :
            dbm.CloseQuery()
            dbm.DBClose()
            return result_list
    else :
        print("DB에 연결하지 못했습니다")
        return result_list