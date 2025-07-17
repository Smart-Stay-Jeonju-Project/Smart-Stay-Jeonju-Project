from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os
import math

# URL에 보낼 Parameter 설정
KEYWORD = '전주'
PAGE_LIST_LENGTH = 20
CHECKIN_DATE = '2025-09-03'
CHECKOUT_DATE = '2025-09-04'

# 저장 변수
targetPath = "DATA/ROW/LINKS/"
link_filename = 'yeogi_accom_link.txt'

# URL
SEARCH_URL = f"https://www.yeogi.com/domestic-accommodations?keyword={KEYWORD}&checkIn={CHECKIN_DATE}&checkOut={CHECKOUT_DATE}&personal=2&freeForm=true"

# 웹 드라이버 객체 생성
def initialize_driver():
    try :
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        return driver
    except Exception as e :
        print("웹 드라이버 객체를 생성하지 못했습니다")
        return None

# 최대 페이지 수 계산하는 함수
def maxPage(driver) :
    driver.get(SEARCH_URL)
    time.sleep(5)

    # 페이지 전체 HTML 받고, 파싱하기
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try :
        total_text = ".css-1psit91 h1"
        MaxNum_tag = soup.select_one(total_text).text
        MaxNum = str(MaxNum_tag).replace(',','')
        MaxNum = ''.join([c for c in MaxNum if c.isdigit()])
        time.sleep(2)

        # 가져온 숫자를 정수로 변환하기
        totalNum = int(MaxNum)
        # 페이지 수 = ( 총 숙소 수 / 한 페이지 숙소 수 )
        # 결과 : 19.5 로, 20페이지가 나오도록 반올림하는 함수 : math.ceil() 사용
        page_count = math.ceil ( totalNum / PAGE_LIST_LENGTH )
        return page_count
    except Exception as e :
        print(f"페이지 수를 계산하지 못했습니다 {e}")
        return 0

# 각 페이지에서 숙소 링크 수집하기
def page_link(driver, max_page_num) :
    all_link = []
    search_link = "a.gc-thumbnail-type-seller-card.css-wels0m"

    for page in range(1, max_page_num + 1) :
        # 각 페이지 URL 구성
        url = SEARCH_URL + f"&page={page}"
        driver.get(url)
        time.sleep(5)

        # 한 페이지에서 숙소 링크 n개 가져오기
        obj_list = driver.find_elements(By.CSS_SELECTOR, search_link)

        # n개의 링크를 하나씩 꺼내면서 주소값('href') 꺼내기 
        link_list = [obj.get_attribute("href") for obj in obj_list ]

        # 전체 링크 리스트에 추가
        all_link += link_list

    # 혹시 모를 중복 링크를 제거
    all_link = list(set(all_link))
    return all_link

# 수집된 숙소 링크들을 텍스트 파일로 저장하기
def save_link(all_links) :
    fullPath = targetPath + link_filename
    try :
        existing = set()
        if os.path.exists(fullPath) :
            with open(fullPath, 'r', encoding='utf-8') as f :
                for line in f :
                    existing.add(line.strip())
        else :
            open(fullPath, 'w', encoding='utf-8').close()
        new_links = [ link for link in all_links if link not in existing ]
        if not new_links :
            print("새로운 링크가 없습니다")
            return True
        
        with open(fullPath, "a", encoding="utf-8") as f:
            for line in new_links :
                f.write(line+"\n")
        return True
    
    except Exception as e :
        print("페이지 링크를 저장하지 못했습니다", e)
        return False

def main() :
    # 드라이버 객체 생성하기
    driver = initialize_driver()

    # 드라이버가 생성되었을 경우에 함수 실행
    if driver is not None :
        # 링크 수집할 페이지 수 구하기
        max_page_num = maxPage(driver)
        if not max_page_num :
            print("링크 수집 페이지를 가져오지 못했습니다")
        else :
            print("크롤링을 시작합니다")
            all_links = page_link(driver, max_page_num)
        try :
            # 링크 텍스트 파일 저장 함수
            if save_link(all_links) :
                print("저장이 완료되었습니다")
            else :
                print("저장하지 못했습니다")
        except Exception as e :
            print("리뷰 수집 중 오류 발생 :", e)
        finally :
            driver.close()
    else :
        print("driver 가 생성되지 않았습니다")
        return

if __name__ == "__main__" :
    main()
