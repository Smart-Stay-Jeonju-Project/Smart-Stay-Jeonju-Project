from DBM import DBManager
from dotenv import load_dotenv
import pandas as pd
import os


load_dotenv()

# DMB 객체 생성
dbm = DBManager()

targetPath = "project/data/processed/reviews/"
filename = "N_clean_info_dupl_test.csv"

fullPath = targetPath + filename

# 숙소 정보 저장
# 통합 숙소 테이블에 저장 test 완료
# test로 실제 통합 테이블에는 저장 X
def save_accom():
    accom_list = pd.read_csv(fullPath)
    print(accom_list)
    try : 
        dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))

        #for accom in accom_list : 
        # .iterrows()는 데이터프레임을 한 행씩 순회
        for _, accom in accom_list.iterrows():  # <- 수정: iterrows() 사용

            sql =  """
                INSERT INTO accommodations 
                (name, category, address, rating, image, feature)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
            params = (
                accom['name'],
                accom['category'],
                accom['addr'], 
                accom['rating_score'], 
                accom['image'], 
                accom['feature'] )
            
            if not dbm.RunSQL(sql, params):
                print(f"숙소 저장 실패")
                exit()
            dbm.CloseQuery()

        dbm.DBClose()
    except Exception as e :
        print(e)


# 원본 숙소 정보 저장
def save_accom_source():
    filename = "clean_yeogi_info.csv"
    #filename = "y_duple_filtered_up.csv"
    fullPath = targetPath + filename
    accom_list = pd.read_csv(fullPath)
    print(accom_list)
    try : 
        dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))

        #for accom in accom_list : 
        # .iterrows()는 데이터프레임을 한 행씩 순회
        for _, accom in accom_list.iterrows():  # <- 수정: iterrows() 사용

            # 여기어때는 feature X
            # 야놀자
            # (source, source_name, source_category, source_addr, source_image, source_rating, source_feature, latitude, longitude)
            # 여기어때
            # (source, source_name, source_category, source_addr, source_image, source_rating, latitude, longitude)

            sql =  """
                INSERT INTO accom_source 
               (source, source_name, source_category, source_addr, source_image, source_rating, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            params = (
                accom['source'],
                accom['name'],
                accom['category'], 
                accom['address'], 
                accom['image'], 
                accom['rating_score'],
                #accom['feature'],
                accom['lat'],
                accom['lng'])
            try:
                if not dbm.RunSQL(sql, params):
                    print(f"숙소 저장 실패: {accom['name']}")
                else:
                    print(f"숙소 저장 완료: {accom['name']}")
            except Exception as e:
                print(f"쿼리 실행 중 에러 발생: {e} - 숙소: {accom['name']}")

        dbm.DBClose()
    except Exception as e :
        print(e)

# 리뷰csv의 숙소명과 숙소 테이블의 숙소명 매칭하여 저장
def save_review():
    filename = "y_duple_filtered_up_0716.csv"
    fullPath = targetPath + filename
    # 리뷰 파일 불러오기
    review_list = pd.read_csv(fullPath)
    
    #nan can not be used with MySQL
    # 원인 : 데이터프레임에 빈 값이 NaN으로 채워져 있는데, 이 부분을 MySQL에 넣어주면서 오류 발생
    # 시도 : 해당 값을 None으로 변경. MySQL에는 NULL 값으로 들어감.
    # 해결 : not null 삭제
    review_list = review_list.where(pd.notnull(review_list), None)

    #print(review_list)

    try : 
        dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))
        #sql = 'SELECT accommodation_id, name FROM accommodations'
        sql = 'SELECT source_id, source_name FROM accom_source'
        dbm.OpenQuery(sql,)

        datas = dbm.GetDatas()

        # (숙소테이블)datas 리스트를 한 행씩(row) 반복하면서,
        # 각 행에서 'name'을 키(key)로, 'source_id'를 값(value)으로 하는 딕셔너리 생성
        name_to_id = {row['source_name']: row['source_id'] for row in datas}
    
        
        for _, review in review_list.iterrows():  # <- 수정: iterrows() 사용
            # 리뷰에서 숙소명 가져오기
            accom_name = review['name']

            # 숙소명이 딕셔너리에 있는지 확인
            #accommodation_id = name_to_id.get(accom_name)
            source_id = name_to_id.get(accom_name)

            #if accommodation_id is None:
            if source_id is None:
                print(f"숙소명 '{accom_name}'을(를) 숙소테이블에서 찾을 수 없습니다. 건너뜁니다.")
                continue
            
            #중복데이터 제외
            check_sql = """
                SELECT 1 FROM review
                WHERE source_id = %s
                AND content = %s
                AND write_date = %s
                AND review_rating = %s
                AND review_source = %s
                AND review_type = %s
                AND nickname = %s
                AND clean_reviews = %s
                LIMIT 1
            """
            params = (
                source_id,
                review['text'],
                review['write_date'],
                review['rating'],
                review['source'],
                review['type'],
                review['nickname'],
                review['clean_reviews']
            )

            dbm.OpenQuery(check_sql, params)
            exists = dbm.GetDatas()
            dbm.CloseQuery()

            if exists:
                print(f"중복된 리뷰가 있어 건너뜀: 숙소명 {accom_name}")
                continue

            sql =  """
                INSERT INTO review
                (source_id, content, write_date, review_rating, review_source, review_type, nickname, clean_reviews)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            
            if not dbm.RunSQL(sql, params):
                print(f"저장 실패한 숙소명: {accom_name}")
                exit()
            dbm.CloseQuery()

        dbm.DBClose()
    except Exception as e :
        print(e)


# 키워드csv의 리뷰내용과 리뷰 테이블의 리뷰내용 매칭하여 저장
# 테스트 완료
def save_keyword():
    targetPath = "project/data/tmp/"
    filename = "keyword_test copy.csv"
    fullPath = targetPath + filename
    # 리뷰 파일 불러오기
    keyword_list = pd.read_csv(fullPath)

    try : 
        dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))

        # CSV 데이터 프레임을 한 행씩 순회
        for _, row in keyword_list.iterrows():
            review_id = row['review_id']
            keyword_texts = row['keyword_text'].split()  # 공백 기준 분리

            # 키워드 빈도수(keyword_score)
            keyword_freq = {}
            for keyword in keyword_texts:
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1

            sql = 'SELECT review_id FROM review WHERE review_id = %s'
            dbm.OpenQuery(sql, (review_id,))
            datas = dbm.GetDatas()

            if datas:
                # 리뷰가 존재하면 review_id를 변수에 저장
                review_id = datas[0]['review_id']
                print(review_id)
            
                # 각 키워드별로 삽입
                for keyword_text, freq in keyword_freq.items():
                    sql = ''' INSERT INTO keywords (review_id, keyword_text, keyword_score)
                            VALUES (%s, %s, %s)'''
                    
                    dbm.RunSQL(sql, (review_id, keyword_text, freq))
                print(f'{len(keyword_texts)} 개 키워드가 {review_id}에 삽입되었습니다')
            else:
                # review 테이블에 매칭되는 clean_review가 없을 경우 경고 메시지 출력
                print(f'매칭되는 리뷰 id가 없습니다 : {review_id}.')

            dbm.CloseQuery()
        dbm.DBClose()
    except Exception as e :
        print(e)


# 리포트 저장
# 리포트csv의 숙소명과 숙소 테이블의 숙소명 매칭하여 저장
def save_report():
    targetPath = "project/data/processed/report/"
    filename = "ai_y_report.csv"
    fullPath = targetPath + filename
    # 레포트 파일 불러오기
    report_list = pd.read_csv(fullPath)
    print(report_list)

    try : 
        dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))
        sql = 'SELECT source_id, source_name FROM accom_source'

        dbm.OpenQuery(sql,)
        datas = dbm.GetDatas()

        # (숙소테이블)datas 리스트를 한 행씩(row) 반복하면서,
        # 각 행에서 'name'을 키(key)로, 'accommodation_id'를 값(value)으로 하는 딕셔너리 생성
        name_to_id = {row['source_name']: row['source_id'] for row in datas}
    
        
        for _, report in report_list.iterrows():  # <- 수정: iterrows() 사용
            # 리포트에서 숙소명 가져오기
            accom_name = report['name']

            # 숙소명이 딕셔너리에 있는지 확인
            source_id = name_to_id.get(accom_name)

            #if accommodation_id is None:
            if source_id is None:
                print(f"숙소명 '{accom_name}'을(를) 숙소테이블에서 찾을 수 없습니다. 건너뜁니다.")
                continue

            sql =  """
                INSERT INTO report
                (source_id, report_text, positive_img, negative_img)
                VALUES (%s, %s, %s, %s)
                """
            params = (
                source_id,
                report['content'],
                f'{accom_name}_positive_img',
                f'{accom_name}_negative_img'
            )
            
            if not dbm.RunSQL(sql, params):
                print(f"저장 실패한 숙소명: {accom_name}")
                exit()
            dbm.CloseQuery()

        dbm.DBClose()
    except Exception as e :
        print(e)


# db 데이터 csv파일로 저장
def db2csv() :
    # MySQL 연결
    dbm.DBOpen(os.getenv('DBHOST'), os.getenv('DBNAME'), os.getenv('ID'), os.getenv('PW'))

    sql = '''SELECT 
            a.accommodation_id, 
            a.name,
            r.review_id, 
            r.content,
            r.review_type
            FROM accommodations a
            JOIN accom_source s ON a.accommodation_id = s.accommodation_id
            JOIN review r ON s.source_id = r.source_id;
            '''
    # sql = "SELECT review_id, content, clean_reviews FROM review"
    dbm.OpenQuery(sql,)

    datas = dbm.GetDatas()

    columns = ["accommodation_id", "name", "review_id", "content","review_type"]

    # 리스트를 DataFrame으로 변환
    df = pd.DataFrame(datas, columns=columns)

    # CSV로 저장
    df.to_csv("accom_review_source.csv", index=False, encoding='utf-8-sig')

    # 연결 종료
    dbm.CloseQuery()
    dbm.DBClose()



if __name__ == "__main__":
    # 숙소 통합 정보 저장
    #save_accom()

    # 숙소 원본 데이터 저장
    #save_accom_source()

    # 리뷰 저장
    #save_review()

    # 키워드 저장
    #save_keyword()

    # 리포트 저장
    #save_report()

    # db 데이터 csv파일 저장
    db2csv()
