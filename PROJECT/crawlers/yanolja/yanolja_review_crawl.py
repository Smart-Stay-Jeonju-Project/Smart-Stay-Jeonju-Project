from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import re
import os
import pandas as pd
import time
import subprocess

targetPath = "DATA/LIST/"
File_Suffix = 'yanolja_link_modify.txt'
print("현재 작업 경로:", os.getcwd())

fullPath = targetPath + File_Suffix

all_review_list = []

# 경로와 파일이름을 병합하여, 파일을 읽어올 경로를 지정
# fullPath = targetPath + File_Suffix
# 파일에서 불러온 URL의 리스트

# 웹 드라이버 객체 생성
def initialze_driver():

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

# 파일에서 URL을 불러오기  
def load_links_from_file(fullPath):
    links = []
    try :
        with open(fullPath, 'r', encoding='UTF-8') as f :
            for line in f :
                link = line.strip()
                if link :
                    links.append(link)
        print(f"{len(links)}개의 게시글 URL을 불러옵니다")
        return links
    except Exception as e :
        print("파일을 불러오는 데 실패했습니다. error:", e)


# 링크 불러와서 리뷰 페이지로 이동
def get_accommodation_details(driver,links):

    for link in links[:3] :
        driver.get(link)
        time.sleep(7)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        try :
            name = soup.select_one('div.css-11vo59c > h1').text
            print(name)
        except Exception as e :
            print(f"숙소 이름을 가져오지 못했습니다.\n에러메세지 : {e}")
            continue

        cssSelector = "div.css-1sq5t3i > a"
        ahref = driver.find_element(By.CSS_SELECTOR, cssSelector)
        href = ahref.get_attribute("href")

        driver.get(href)
        time.sleep(5)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # review 영역 찾기
        ##__next > section > div > div.css-1js0bc8 > div
        review_list = soup.select("div.css-1js0bc8 > div")

        if review_list :
            print("리뷰 목록을 로드했습니다")
            all_review_list = get_review(name, review_list, driver)

        else :      # 스크롤 했지만, 목록이 더 생기지 않음
            print("리뷰 결과가 없습니다")
            continue
        
    return all_review_list

def get_review(name, review_list, driver) : 

    for review in  review_list[:6]:
        # 리뷰 내용
        try :
            review_text = review.select_one('div.css-1kpa3g > p').text
            print(repr(review_text))
            # 정규 표현식을 이용한 처리
            '''
            pat = re.compile("\n+")
            review_text = pat.sub("\n",review_text)
            pat = re.compile("\t+")
            review_text = pat.sub("\t",review_text)
            review_text = re.sub(r"( )+"," ", review_text)
            review_text = review_text.replace("\u200b","")
            '''

            #review_text = p_tag.text

            # 줄바꿈, 탭, 유니코드 공백 제거 → 한 줄로 만들기
            review_text = re.sub(r'[\r\n\t]+', ' ', review_text)     # 줄바꿈/탭 → 공백
            review_text = re.sub(r'\s+', ' ', review_text)           # 연속 공백 → 하나의 공백
            review_text = review_text.replace('\u200b', '').strip()  # 특수 공백 제거 + 양끝 공백 제거

            print(review_text)
        except Exception as e :
            print(f"리뷰 내용을 가져오지 못했습니다.\n에러메세지 : {e}")

        #div.css-1ivchjf > div.css-1ivchjf > p
        try :
            date = review.select_one('div.css-1ivchjf > p').text
        except Exception as e :
            print(f"날짜를 가져오지 못했습니다.\n에러메세지 : {e}")

        try :
            rating = review.select("div.css-rz7kwu > svg > path[fill-rule='evenodd']")
            print("평점 :",5-len(rating))

        except Exception as e :
            print(f"평점을 가져오지 못했습니다.\n에러메세지 : {e}")

        review_all = {'name':name,'text':review_text,'review_rating':5-len(rating),'write_date':date,'source':'yanolja'}
        all_review_list.append(review_all)

    return all_review_list


def save_info(reviews) :
    if reviews :
        filename = "yanolja_review.csv"
        fullPath = targetPath + filename
        df = pd.DataFrame(reviews)
        try :
            if os.path.exists(fullPath) :
                df.to_csv(f"{fullPath}", mode='a',index=False, encoding='utf-8-sig',header=False)
            else :
                print(f"{len(reviews)}개의 리뷰를 저장했습니다")
                df.to_csv(f"{fullPath}", mode='w',index=False, encoding='utf-8-sig',header=True)
            return True
        except Exception as e :
            print(f"숙소의 리뷰를 저장하지 못했습니다 {e}")
            return False

def main():
    driver = initialze_driver()
    links = load_links_from_file(fullPath)
    all_review_list =  get_accommodation_details(driver, links)
    save_info(all_review_list)
    driver.quit()


if __name__ == "__main__":
    main()