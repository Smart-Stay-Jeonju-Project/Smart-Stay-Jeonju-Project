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
    filename = "n_duple_filtered_up_replace_source.csv"
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
        sql = 'SELECT accommodation_id, name FROM accommodations'
        dbm.OpenQuery(sql,)

        datas = dbm.GetDatas()

        # (숙소테이블)datas 리스트를 한 행씩(row) 반복하면서,
        # 각 행에서 'name'을 키(key)로, 'accommodation_id'를 값(value)으로 하는 딕셔너리 생성
        name_to_id = {row['name']: row['accommodation_id'] for row in datas}
    
        
        for _, review in review_list.iterrows():  # <- 수정: iterrows() 사용
            # 리뷰에서 숙소명 가져오기
            accom_name = review['name']

            # 숙소명이 딕셔너리에 있는지 확인
            accommodation_id = name_to_id.get(accom_name)

            if accommodation_id is None:
                print(f"숙소명 '{accom_name}'을(를) 숙소테이블에서 찾을 수 없습니다. 건너뜁니다.")
                continue

            #insert into -> replace into 로 변경
            #매일 바뀌는 데이터 값을 덮어쓰기 해줘야 하기 때문에
            sql =  """
                INSERT INTO review
                (accommodation_id, content, write_date, review_rating, review_source, review_type, nickname, clean_reviews)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
            params = (
                accommodation_id,
                review['text'],
                review['write_date'], 
                review['review_rating'], 
                review['source'], 
                review['type'], 
                review['nickname'], 
                review['clean_reviews'])
            
            if not dbm.RunSQL(sql, params):
                print(f"저장 실패한 숙소명: {accom_name}")
                exit()
            dbm.CloseQuery()

        dbm.DBClose()
    except Exception as e :
        print(e)



if __name__ == "__main__":
    # 숙소 통합 정보 저장
    #save_accom()

    # 숙소 원본 데이터 저장
    #save_accom_source()

    # 리뷰 저장
    save_review()
