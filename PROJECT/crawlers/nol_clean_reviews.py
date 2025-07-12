import os
import pandas as pd

targetPath = 'DATA/results/accommodations/'
filename = 'yanolja_review.csv'

fullPath = targetPath + filename

reviews = []
def load_review_file() :
    if os.path.exists(fullPath) :
        reviews = pd.read_csv(fullPath, encoding='utf-8-sig')
    else :
        print("파일 경로를 찾을 수 없습니다")
        print("현재 작업 경로:", os.getcwd())
    return reviews


def delete_none_data(reviews):
    # 특정 주요 컬럼에 결측치가 있는 행 제거
    content = reviews.dropna(subset=['name'], how='any', axis=0)
    content = content.dropna(subset=['review_rating'], how='any', axis=0)
    content = content.dropna(subset=['text'], how='any', axis=0)
    content = content.dropna(subset=['nickname'], how='any', axis=0)
    content = content.dropna(subset=['write_date'], how='any', axis=0)
    content = content.dropna(subset=['source'], how='any', axis=0)
    content['text'] = (
            content['text']
            .str.replace(r"[^가-힣 ]", "", regex=True)
            .str.replace(r"\u200b", '', regex=True)
            .str.replace(r'\s+', ' ', regex=True)
            .str.strip()
        )
    print(content.info())  # 삭제 후 데이터 정보 출력
    return content

def main() :
    # 숙소 리뷰 파일 불러오기
    try:
        reviews = load_review_file()
        print("파일을 로드했습니다")
    except Exception as e:
        print(f"파일을 불러오는데 실패했습니다 {e}")
        return

    # 숙소 리뷰 데이터 정제 구간
    try:
        content = delete_none_data(reviews)
    except Exception as e:
        print(f"삭제하는 데 오류가 발생했습니다 {e}")
        return
    
    # 숙소 리뷰 데이터 정제
    saveFullPath = os.path.join(targetPath, 'n_cleaned_reviews_full.csv')
    content.to_csv(saveFullPath, encoding='utf-8-sig', index=False, header=True)

    # 텍스트만 추출해서 저장 (빈 값 제외)
    new_review_df = content['text'].dropna()

    filename = 'n_cleaned_review_texts.csv'
    savePath = os.path.join(targetPath, filename)
    new_review_df.to_csv(savePath, encoding='utf-8-sig', index=False, header=False)

    # 중복 제거된 리뷰 저장
    duple_review = new_review_df.drop_duplicates()
    datePath = 'CRAWLERS/'
    filename = 'n_reviews.csv'
    savePath = os.path.join(datePath, filename)
    duple_review.to_csv(savePath, encoding='utf-8-sig', index=False, header=False)

if __name__ == '__main__' :
    main()
