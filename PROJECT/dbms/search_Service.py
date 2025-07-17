from dbms.DBM import DBManager
from dotenv import load_dotenv
import os
load_dotenv()

# DMB 객체 생성
dbm = DBManager()

# 검색 페이지의 목록에 출력할 데이터 DB에서 가져오는
# 검색타입 : 상호명일때 / sql문으로 조건 검색
def accommodations_list(search_type, search_term):
    result_list = None
    if dbm : 
        try :
            dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))
            print(search_term)
            if search_type == 'name':
                sql = 'select * from accommodations where name like %s'
                dbm.OpenQuery(sql, ("%"+search_term+"%",))
                total = dbm.GetTotal()
                if total > 0 :
                    print(f"상호명으로 조회된 숙소 수 : {total}")
                else :
                    return result_list
                datas = dbm.GetDatas()
                    
                if datas : 
                    result_list = {
                        'total': total, 
                        'list' : datas
                        }
                #print("검색결과 :",result_list)


            elif search_type == 'address':
                sql = 'select * from accommodations where address like %s'
                dbm.OpenQuery(sql, ("%"+search_term+"%",))
                total = dbm.GetTotal()
                if total > 0 :
                    print(f"주소로 조회된 숙소 수 : {total}")
                else :
                    return result_list
                datas = dbm.GetDatas()
                    
                if datas : 
                    result_list = {
                        'total': total, 
                        'list' : datas
                        }
                print("검색결과 :",result_list)

            elif search_type == 'keyword':
                sql = '''
                    SELECT DISTINCT a.*
                    FROM accommodations a
                    join accom_source s ON a.accommodation_id = s.accommodation_id
                    JOIN review r ON s.source_id = r.source_id
                    JOIN keywords k ON r.review_id = k.review_id
                    WHERE k.keyword_text = %s
                    ORDER BY a.rating DESC;
                    '''
                dbm.OpenQuery(sql, (search_term,))
                total = dbm.GetTotal()
                if total > 0 :
                    print(f"키워드로 조회된 숙소 수 : {total}")
                else :
                    return result_list
                datas = dbm.GetDatas()
                    
                if datas : 
                    result_list = {
                        'total': total, 
                        'list' : datas
                        }
                print("검색결과 :",result_list)


        except Exception as e :
            print(e)
        finally :
            dbm.CloseQuery()
            dbm.DBClose()
            return result_list

    else :
        print("DB에 연결하지 못했습니다")
        return result_list
    

    
# 키워드 목록들
def load_keywords():
    keyword_list = None
    if dbm : 
        try :
            dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))

            # 여러 리뷰에서 나온 keyord_text의 빈도수를 합산하여, 빈도수가 높은 상위 10개 키워드만 출력 
            # -> 랜덤 키워드로 변경
            sql = '''SELECT keyword_text, SUM(keyword_score) AS total_score
                    FROM keywords
                    GROUP BY keyword_text
                    ORDER BY rand()
                    LIMIT 10;'''
            dbm.OpenQuery(sql, )
            total = dbm.GetTotal()
            if total > 0 :
                print("상위 10개 키워드가 조회되었습니다")
            else :
                return keyword_list
            datas = dbm.GetDatas()
                
            if datas : 
                keyword_list = {
                    'total': total, 
                    'list' : datas
                    }
            #print("검색결과 :",keyword_list['list'])

        except Exception as e :
            print(e)
        finally :
            dbm.CloseQuery()
            dbm.DBClose()
            return keyword_list
    else :
        print("DB에 연결하지 못했습니다")
        return keyword_list