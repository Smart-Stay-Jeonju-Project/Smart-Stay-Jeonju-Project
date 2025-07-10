import os
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

reviews = []
def load_review_file() :
    targetPath = 'DATA/RAW/REVIEWS/yeogi/'
    filename = 'yeogi_all_reviews.csv'

    fullPath = targetPath + filename
    if os.path.exists(fullPath) :
        reviews = pd.read_csv(fullPath, encoding='utf-8-sig')
    else :
        print("파일 경로를 찾을 수 없습니다")
        print("현재 작업 경로:", os.getcwd())
    return reviews

today = datetime.today()

# 결측치 제거, 리뷰 텍스트 정제 
def delete_none_data(reviews):
    content = reviews.dropna(subset=['review_content', 'write_date']).copy()

    content.loc[:, 'name'] = (
        content['name']
        .str.replace(r'"','', regex=True)
        .str.replace(r"[^가-힣 ]", "", regex=True)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )
    content.loc[:, 'review_content'] = (
        content['review_content']
        .str.replace(r'"','', regex=True)
        .str.replace(r"[^가-힣 ]", "", regex=True)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
    )
    # 리뷰 내용이 최소 3글자 이상인 것만 가져오기
    content = content[content['review_content'].str.len() >= 3]
    return content

# 날짜 포멧
def set_date(content) :
    today = datetime.today()
    converted_dates = []
    for date in content['write_date'] :
        date = date.strip()
        try :
            if '개월 전' in date :
                num = int(date.replace('개월 전', '').strip())
                new_date = today - timedelta(weeks=num)
            elif '일 전' in date :
                num = int(date.replace('일 전', '').strip())
                new_date = today - timedelta(days=num)
            elif '년 전' in date :
                num = int(date.replace('년 전', '').strip())
                new_date = today - relativedelta(years=num)
            elif '시간 전' in date :
                num = int(date.replace('시간 전', '').strip())
                new_date = today - relativedelta(hours=num)
            elif '분 전' in date :
                num = int(date.replace('분 전', '').strip())
                new_date = today - relativedelta(minutes=num)
            else :
                print(date)

            converted_dates.append(new_date.strftime('%Y-%m'))
        except Exception as e :
            print(f"오류 발생 : {date} {e}")
            new_date = None

    content['write_date'] = converted_dates
    return content

def main() :
    # 파일 불러오기
    try :
        reviews = load_review_file()
        print("파일을 로드했습니다")
    except Exception as e :
        print(f"파일을 불러오는데 실패했습니다 {e}")
        return
    
    # 결측치 제거
    try :
        new_content = delete_none_data(reviews)
    except Exception as e :
        print(f"데이터를 정제하는 데 오류가 발생했습니다 {e}")
    try :
        content = set_date(new_content)
        print("날짜를 변경하였습니다")
    except Exception as e :
        print(f"날짜를 변경하는데 실패했습니다 {e}")
    
    # 리뷰 데이터 저장
    content.drop_duplicates(subset=['nickname','review_content','rating'], inplace=True)
    targetPath = 'DATA/PROCESSED/'
    saveFullPath = os.path.join(targetPath, 'y_duple_reviews.csv')
    content.to_csv(saveFullPath, encoding='utf-8-sig', index=False, header=True)

    # 텍스트만 추출해서 저장 (빈 값 제외)
    new_review_df = content['review_content'].dropna().drop_duplicates()

    filename = 'y_only_texts.csv'
    savePath = os.path.join(targetPath, filename)
    new_review_df.to_csv(savePath, encoding='utf-8-sig', index=False, header=False)

if __name__ == '__main__' :
    main()
