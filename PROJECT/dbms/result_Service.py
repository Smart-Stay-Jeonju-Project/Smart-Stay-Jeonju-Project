from dbms.DBM import DBManager
from dotenv import load_dotenv
import os
load_dotenv()

# DMB 객체 생성
dbm = DBManager()

# 검색 페이지의 목록에 출력할 데이터 DB에서 가져오는
# 검색타입 : 상호명일때 / sql문으로 조건 검색
def result_accom(name):
    result_list = []
    review_list = []
    keyword_list = []
    if dbm : 
        try :
            dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))
            # 숙소상세정보 조회
            # report 테이블에서 긍부정 워드클라우드와 요약내용 조회
            sql = '''select * , (select positive_img from report r where r.accommodation_id = a.accommodation_id) as p_img,
            (select negative_img from report r where r.accommodation_id = a.accommodation_id) as n_img,
            (select report_text from report r where r.accommodation_id = a.accommodation_id) as report_text
            from accommodations a where a.name =  %s'''
            dbm.OpenQuery(sql, (name,))
            total = dbm.GetTotal()
            if total == 1 :
                print("숙소가 조회되었습니다")
            else :
                return result_list
            datas = dbm.GetDatas()
            print(type(datas))
            print(datas)
            
            # list -> dict로
            if datas : 
                for data in datas :
                    result_list = data

            print("상세페이지 검색결과 :",result_list)

            # 숙소별 리뷰 최신순으로 조회
            sql = '''SELECT 
                        a.name,
                        r.content,
                        r.write_date,
                        r.review_rating,
                        r.review_source,
                        r.review_type,
                        r.nickname
                    FROM accommodations a
                    JOIN review r ON a.accommodation_id = r.accommodation_id
                    WHERE a.name = %s
                    ORDER BY r.write_date DESC;'''
            dbm.OpenQuery(sql, (name,))
            r_total = dbm.GetTotal()
            if r_total > 0 :
                print(r_total, "개 리뷰가 조회되었습니다")
            else :
                return review_list
            r_datas = dbm.GetDatas()
            #print("리뷰 조회결과 :", r_datas)
            if r_datas : 
                review_list = {
                        'total': r_total, 
                        'list' : r_datas
                        }
                #print("검색결과 :",review_list['list'])

            # 숙소별 빈도수 상위 5개 키워드 조회
            sql = '''SELECT k.keyword_text, SUM(k.keyword_score) AS total_score
                    FROM keywords k
                    JOIN review r ON k.review_id = r.review_id
                    JOIN accommodations a ON r.accommodation_id = a.accommodation_id
                    WHERE a.name = %s
                    GROUP BY k.keyword_text
                    ORDER BY total_score DESC
                    LIMIT 5;'''
            dbm.OpenQuery(sql, (name,))
            k_total = dbm.GetTotal()
            if k_total > 0 :
                print("키워드가 조회되었습니다")
            else :
                return keyword_list
            k_datas = dbm.GetDatas()
            print(k_datas)
                
            if k_datas : 
                keyword_list = k_datas
                print("키워드 조회결과 :",keyword_list)


        except Exception as e :
            print(e)
        finally :
            dbm.CloseQuery()
            dbm.DBClose()
            return result_list, review_list, keyword_list
    else :
        print("DB에 연결하지 못했습니다")
        return result_list, review_list, keyword_list
    