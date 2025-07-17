from dbms.DBM import DBManager
from dotenv import load_dotenv
import os
load_dotenv()

# DMB 객체 생성
dbm = DBManager()


# 메인의 카테고리별 숙소목록
def load_categorys(category):
    category_list = None
    if dbm : 
        try :
            if category in ['모텔/호텔', '게하/한옥', '펜션', '홈&빌라'] :
                dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))
                sql = 'select * from accommodations where category = %s'
                dbm.OpenQuery(sql, (category,))
                total = dbm.GetTotal()
                if total > 0 :
                    print(f"조회된 카테고리 수 : {total}")
                else :
                    return category_list
                datas = dbm.GetDatas()
                    
                if datas : 
                    category_list = {
                        'total': total, 
                        'list' : datas
                        }
                #print("검색결과 :",category_list['list'])
            else:
                print("지원하지 않는 카테고리입니다.")

        except Exception as e :
            print(e)
        finally :
            dbm.CloseQuery()
            dbm.DBClose()
            return category_list
    else :
        print("DB에 연결하지 못했습니다")
        return category_list
    

