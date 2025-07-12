import os
import pandas as pd
import re
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

targetPath = 'DATA/RAW/REVIEWS/'
filename = 'y_all_reviews.csv'
content = 'result_contents.csv'

fullPath = targetPath + filename
datePath = 'CRAWLERS/'
saveFullPath = datePath + content
reviews = []
def load_review_file() :
    if os.path.exists(fullPath) :
        reviews = pd.read_csv(fullPath, encoding='utf-8-sig')
    else :
        print("파일 경로를 찾을 수 없습니다")
        print("현재 작업 경로:", os.getcwd())
    return reviews

#print(reviews.iloc[[2]].values)
#old_date = reviews['write_date'].tolist()
today = datetime.today()

#date_df = pd.DataFrame(old_date)

def delete_none_data(reviews):
    content = reviews.dropna(subset=['review_content'], how='any', axis=0)
    content = content.dropna(subset=['write_date'], how='any', axis=0)
    print(content.info())

    return content


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
            else :
                print(date)

            converted_dates.append(new_date.strftime('%Y-%m'))
        except Exception as e :
            print(f"오류 발생 : {date} {e}")
            return
    content['write_date'] = converted_dates
    print(content.info())
    return content


# try :
#     for review in reviews :
#         review['content'] = str(re.sub(r"[^ㄱ-ㅎㅏ-ㅣ-가-힣0-9 ]", "", review['content'].get_text().strip()))
        
# except Exception as e :
#     print(e)
# print(df.iloc['id'])
def main() :
    try :
        reviews = load_review_file()
        print("파일을 로드했습니다")
    except Exception as e :
        print(f"파일을 불러오는데 실패했습니다 {e}")
    try :
        content = delete_none_data(reviews) 
    except Exception as e :
        print(f"삭제하는 데 오류가 발생했습니다 {e}")
    try :
        content['name'] = (content['name'].str.replace(r"[^ㄱ-ㅎㅏ-ㅣ가-힣0-9 ]", "", regex=True).str.replace(r'\s+',' ',regex=True).str.strip())
        content['review_content'] = (content['review_content'].str.replace(r"[^ㄱ-ㅎㅏ-ㅣ가-힣0-9 ]", "", regex=True).str.replace(r'\s+',' ',regex=True).str.strip())
        print("내용을 변경하였습니다")
    except Exception as e :
        print(f"내용을 변경하는데 실패했습니다 {e}")
    try :
        new_content = set_date(content)
        print("날짜를 변경하였습니다")
    except Exception as e :
        print(f"날짜를 변경하는데 실패했습니다 {e}")

    new_df = pd.DataFrame(new_content)
    new_df.to_csv(saveFullPath, encoding='utf-8-sig', index=False)
    new_review_df = pd.DataFrame(content['review_content'].dropna())
    filename = 'clean_reviews.csv'
    savePath = datePath + filename
    new_review_df.to_csv(savePath, encoding='utf-8-sig', index=False, header=False)
    duple_review = new_review_df.drop_duplicates()
    filename = 'duple_reivews.csv'
    savePath = datePath + filename
    duple_review.to_csv(savePath, encoding='utf-8-sig', index=False, header=False)

if __name__ == '__main__' :
    main()
