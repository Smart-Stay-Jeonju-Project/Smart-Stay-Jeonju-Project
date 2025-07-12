from DBM import DBManager

# DBManager 객체 생성
dbm = DBManager()

from dotenv import load_dotenv
import os
load_dotenv()

host = os.getenv('DBHOST')
dbname = os.getenv('DBNAME')
user = os.getenv('ID')
passwd = os.getenv('PW')

#dbm.DBOpen('aiclass', 'root', 'ezen')
try : 
    dbm.DBOpen(host, dbname, user, passwd, 3366)
    
    # 주소로 숙소 조회
    sql = 'select * from accommodations where address like %s'
    keyword = '전주시'
    dbm.OpenQuery(sql, ("%"+keyword+"%",))
    datas = dbm.GetDatas()
    dbm.CloseQuery()
    #dbm.DBClose()
    # 조회된 결과를 출력
    if datas :
        print(datas)
        for data in datas :
            print(f"숙소번호 : {data['accommodation_id']}")
            print(f"상호명 : {data['name']}")
            print(f"카테고리 : {data['category']}")
            print(f"상세주소 : {data['address']}")
            print(f"별점 : {data['rating']}")
            print(f"이미지 : {data['image']}")
            print(f"특징 : {data['feature']}")
            #print(f"감성분석수치 : {data['score']}")
            #print(f"Ai리포트 : {data['aiReport']}")
            print('-'*20)

    # 숙소명으로 조회
    sql = 'select * from accommodations where name like %s'
    keyword = '전주'
    dbm.OpenQuery(sql, ("%"+keyword+"%",))
    datas = dbm.GetDatas()
    dbm.CloseQuery()
    #dbm.DBClose()
    # 조회된 결과를 출력
    if datas :
        #print(datas)
        for data in datas :
            print(f"숙소번호 : {data['accommodation_id']}")
            print(f"상호명 : {data['name']}")
            print(f"카테고리 : {data['category']}")
            print(f"상세주소 : {data['address']}")
            print(f"이미지 : {data['image']}")
            print(f"특징 : {data['feature']}")
            #print(f"감성분석수치 : {data['score']}")
            #print(f"Ai리포트 : {data['aiReport']}")
            print('-'*20)


    dbm.DBClose()

except Exception as e :
    print(e)