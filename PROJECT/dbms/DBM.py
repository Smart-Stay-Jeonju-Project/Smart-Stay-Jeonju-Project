# DBManager 클래스
import pymysql, pymysql.cursors
import pandas as pd

class DBManager :
    def __init__(self):             # 생성자
        self.con    = None
        self.cursor = None

    def DBOpen(self, host, dbname, id, pw) : # DBMS 연결 메소드
        try :
            self.con = pymysql.connect( host=host, user=id, password=pw, db=dbname, charset='utf8', cursorclass=pymysql.cursors.DictCursor )
            return True
        except Exception as e :
            print(e)
            return False

    def DBClose(self) :             # DBMS 연결 종료 메소드
        self.con.close()

    # select / insert,update,delete
    # insert,update,delete
    def RunSQL(self, sql, datas) :
        print(f"SQL : {sql}")
        try:
            self.cursor = self.con.cursor()
            count = self.cursor.execute(sql, datas)
            if count < 1 :
                print("데이터를 변경하지 못했습니다")
                return False
            self.con.commit()
            self.cursor.close()
            return True
        except Exception as e :
            print(e)
            self.con.rollback()
            self.cursor.close()
            return False
    # select
    # sql문 실행 메소드
    # 데이터 가져오는 메소드
    # 연결을 종료하는 메소드
    def OpenQuery(self, sql, datas) :
        print(f"SQL : {sql}")
        try :
            self.cursor = self.con.cursor()
            if datas :
                self.cursor.execute(sql, datas)
            else :
                self.cursor.execute(sql)
            # 데이터를 가져오지 못한경우??
            self.dataList = self.cursor.fetchall()
            return True
        except Exception as e :
            print(e)
            return False

    # select 닫기 메소드
    def CloseQuery(self):
        self.cursor.close()

    # 조회 결과 개수를 받는 메소드
    def GetTotal(self):
        return len(self.dataList)

    # 컬럼 이름으로 컬럼 값을 가져오는 메소드
    def GetValue(self,index,column):
        # 커서 객체가 없거나, 가져온 데이터가 없으면
        if not self.cursor or not self.dataList :
            print("DB에 연결되어있지 않거나, 조회된 데이터가 없습니다")
            return None
        # 인덱스가 범위를 벗어나면
        if index < 0 or index >= len(self.dataList) :
            print("인덱스 범위가 올바르지 않습니다")
            return None
        # 컬럼 이름이 올바르지 않으면
        if column == None or column == "":
            print("컬럼 이름이 올바르지 않습니다")
            return None
        if column in self.dataList[index] :
            return self.dataList[index][column]
        else :
            print("컬럼 이름이 없습니다")
            return None

    # 인덱스 번호로 한건씩 값을 가져오는 메소드
    def GetData(self,index):
        # 커서 객체가 없거나, 가져온 데이터가 없으면
        if not self.cursor or not self.dataList :
            return None
        # 인덱스가 범위를 벗어나면
        if index < 0 or index >= len(self.dataList) :
            return None
        # 인덱스 번호로 해당 데이터를 반환
        return self.dataList[index]

    # 데이터 전부를 반환하는 메소드
    def GetDatas(self):
        # 커서 객체가 없거나, 가져온 데이터가 없으면
        if not self.cursor or not self.dataList :
            return None
        return self.dataList

    # 전체 데이터를 DataFrame으로 받아오는 메소드
    def GetDf(self) :
        if not self.dataList :
            print("조회된 데이터가 없습니다")
            return pd.DataFrame()   # 빈 Df를 반환
        return pd.DataFrame(self.dataList)
