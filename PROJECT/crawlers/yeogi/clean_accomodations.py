import os
import pandas as pd

targetPath = "DATA/RAW/accommodations/"
saveTargetPath = "DATA/results/accommodations/yeogi/"
print("현재 작업 경로:", os.getcwd())

# 파일에서 숙소 정보 불러오기
def load_accom_from_file():
    filename = "yeogi_info.csv"
    loadPath = targetPath + filename
    accoms = []
    try :
        accoms = pd.read_csv(loadPath, encoding='utf-8-sig')
        return accoms
    except Exception as e :
        print("파일을 불러오는 데 실패했습니다. error:", e)
        return accoms

# 숙소 데이터 정제 함수
def clean_accommodation(accoms) :
    try :
        # 숙소 이름 : 특수문자 제거, 공백 정리
        accoms['name'] = (
            accoms['name']
            .str.replace(r"[^ㄱ-ㅎㅏ-ㅣ가-힣0-9 ]", "", regex=True)
            .str.replace(r'\s+',' ',regex=True)
            .str.strip()
        )
        # 평가수 "1,234명" -> 1234 정제
        def clean_rating(rating) :
            if pd.isna(rating) :
                return 0
            rating = str(rating).replace(',','')
            digits = ''.join([c for c in rating if c.isdigit()])
            return int(digits) if digits else 0

        accoms['rating_count'] = accoms['rating_count'].apply(clean_rating)
        print('수정이 완료되었습니다')
        return accoms
    except Exception as e :
        print('수정에 실패하였습니다', e)
        return None

def clean_save_info(clean_accoms) :
    if clean_accoms is not None :
        filename = "clean_yeogi_info.csv"
        fullPath = saveTargetPath + filename
        df = pd.DataFrame(clean_accoms)
        try :
            df.to_csv(fullPath, mode='a',index=False, encoding='utf-8-sig',header=False)
            print("저장 완료하였습니다")
        except Exception as e:
            print("저장 실패")

def main():
    accoms = load_accom_from_file()
    clean_accoms = clean_accommodation(accoms)
    clean_save_info(clean_accoms)

if __name__ == "__main__":
    main()