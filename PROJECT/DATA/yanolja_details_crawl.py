from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#targetPath = "PROJECT/DATA/LIST/"
#imgTargetPath = "PROJECT/DATA/imgs/"
targetPath = "DATA/LIST/"
KEYWORD = '전주'

# URL
SEARCH_URL = f"https://nol.yanolja.com/local/search?keyword={KEYWORD}&shortcut=all&pageKey=1751252871083"
#https://nol.yanolja.com/local/search?keyword={KEYWORD}&shortcut=all&pageKey=1751252871083


# 웹 드라이버 객체 생성
def initialze_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver


# 키워드로 검색된 숙소의 상세 정보를 가져오기
def get_accommodation_details(driver):
    driver.get(SEARCH_URL)
    driver.implicitly_wait(10)
    time.sleep(5)

    count = 30

    imsi_posts = {}
    posts = []
        

    for i in range(count) :
        driver.execute_script("window.scroll(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        time.sleep(5)
        i += 1

        soup = BeautifulSoup(driver.page_source, 'lxml')

        # detail 영역 찾기
        detail_list = soup.select("a > div.grid.w-full.grid-cols-\[126px_1fr\].gap-\[12px\]")

        if detail_list :
            print("숙소검색 페이지를 로드했습니다")
        else :      # 스크롤 했지만, 목록이 더 생기지 않음
            print("검색 결과가 없습니다")
            exit() 

        for detail in  detail_list:

            try :
                name = detail.select_one('div.py-2 > p').text
            except Exception as e :
                print(f"숙소 이름을 가져오지 못했습니다.\n에러메세지 : {e}")
            
            try :
                category = detail.select_one('div.py-2 > div > p').text
            except Exception as e :
                print(f"카테고리 항목을 가져오지 못했습니다.\n에러메세지 : {e}")
            
            # 평점
            # 6개월 내 작성된 평점만 수집됨
            try :
                rating_score = detail.select_one('div > p > span.typography-body-14-bold').text
            except Exception as e :
                print(f"평점을 가져오지 못했습니다.\n에러메세지 : {e}")
                rating_score = 0

            # 리뷰 건수
            try :
                rating_count = detail.select_one('div:nth-child(2) > p > span:nth-child(2)').text.replace("(", '').replace(")", '')   # 괄호제거
            except Exception as e :
                print(f"평가수를 가져오지 못했습니다.\n에러메세지 : {e}")
                rating_count = 0

            # 특징
            #body > div.flex.justify-center.pc\:justify-normal > div > div.mb-\[calc\(76px\+env\(safe-area-inset-bottom\)\)\].flex.h-full.flex-col.items-center.overflow-x-hidden.pc\:mb-96 > div > div:nth-child(2) > a:nth-child(1) > div.grid.w-full.grid-cols-\[126px_1fr\].gap-\[12px\] > div.flex.flex-col.overflow-hidden > div.pm-2.text-fill-neutral-main.typography-body-14-regular > div.mb-4.flex.items-center.justify-start.gap-2 > span
            try :
                feature = detail.select_one('div.mb-4.flex.items-center.justify-start.gap-2 > span').text
            except Exception as e :
                print(f"상세주소를 가져오지 못했습니다.\n에러메세지 : {e}")

            # 검색페이지에서 상세주소 수집 불가
                
            post = {'name':name, 'category':category, 'ratring_score':rating_score, 'rating_count':rating_count, 'feature' : feature}
            
            posts.append(post)
            imsi_posts = post
            print(imsi_posts)


            if len(posts) >= 20 :
                print("20개의 정보가 초과되어 중간 저장합니다")
                save_info(posts)
                if save_info(posts) :
                    print("중간 저장 완료했습니다")
                    posts = []
                else :
                    print("중간저장 하지 못했습니다")
                    return
    return posts

def save_info(all_info) :
    if all_info :
        filename = "yanolja_accommodations.csv"
        fullPath = targetPath + filename
        df = pd.DataFrame(all_info)
        try :
            # 저장된 파일이 있으면 header = False
            if os.path.exists(fullPath) :
                df.to_csv(f"{fullPath}", mode='a',index=False, encoding='utf-8-sig',header=False)
            else :
                print(f"{len(all_info)}개의 숙소의 상세 정보를 저장했습니다")
                df.to_csv(f"{fullPath}", mode='w',index=False, encoding='utf-8-sig',header=True)
            return True
        except Exception as e :
            print(f"숙소의 상세 정보를 저장하지 못했습니다 {e}")
            return False
        

# 중복제거
def load_info() :
    filename = "yanolja_accommodations.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)
    new_df = df.drop_duplicates()
    filename = "yanolja_accommodations(중복제거).csv"
    fullPath = targetPath + filename
    new_df.to_csv(f"{fullPath}", index=False, encoding='utf-8-sig',header=True)


def main():
    driver = initialze_driver()
    all_links = get_accommodation_details(driver)

    if save_info(all_links) :
        print("저장이 완료되었습니다")
    else :
        print("저장하지 못했습니다")
    
    # 중복제거
    load_info()
    
    driver.quit()

if __name__ == "__main__":
    main()