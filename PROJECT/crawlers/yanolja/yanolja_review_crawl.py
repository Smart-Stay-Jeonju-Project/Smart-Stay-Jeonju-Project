from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import time

import re
import os
import pandas as pd
import time

targetPath = "DATA/LIST/"
File_Suffix = 'yanolja_link_modify.txt'
print("현재 작업 경로:", os.getcwd())

fullPath = targetPath + File_Suffix


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
def get_review_page(links):
    all_review_list = []
    for link in links :
        try :
            driver = initialze_driver()
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
            driver.implicitly_wait(5)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            # 스크롤을 끝까지
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # 스크롤 완료 후 리뷰 수집
            soup = BeautifulSoup(driver.page_source, 'lxml')
            review_list = soup.select("div.css-1js0bc8 > div")
            print(f"{len(review_list)}개의 리뷰를 찾았습니다.")

            if review_list :
                print("리뷰 목록을 로드했습니다")
            else :
                print("리뷰 결과가 없습니다")
                continue

            # 리뷰 내용 등 수집, 중간저장
            for review in review_list :
                    
                reviews = get_review(name, review)
                all_review_list.append(reviews)

                print(len(all_review_list))
                
                if len(all_review_list) >= 20 :
                    print("20개의 정보를 중간 저장합니다")
                    #save_info(all_review_list)
                    if save_info(all_review_list) :
                        print("중간 저장 완료했습니다")
                        # 리스트 초기화
                        all_review_list = []
                    else :
                        print("중간저장 하지 못했습니다")
                        return
                    
        except Exception as e:
            print(f"[ERROR] 링크 접근 중 오류: {e}")
        finally:
            driver.quit()  # ▶ 크롬 종료
            time.sleep(3)

    # 남은 20개 미만 리뷰 저장
    if all_review_list :
        save_info(all_review_list)
        print("남은 리뷰를 저장했습니다")

    return all_review_list


def get_review(name, review) :
    # 리뷰 내용
    try :
        review_text = review.select_one('div.css-1kpa3g > p').text
        #print(repr(review_text))
        
        # 정규 표현식을 이용한 처리
        # 줄바꿈, 탭, 유니코드 공백 제거 → 한 줄로 만들기
        review_text = re.sub(r'[\r\n\t]+', ' ', review_text)     # 줄바꿈/탭 → 공백
        review_text = re.sub(r'\s+', ' ', review_text)           # 연속 공백 → 하나의 공백
        review_text = review_text.replace('\u200b', '').strip()  # 특수 공백 제거 + 양끝 공백 제거
        print(review_text)

    except Exception as e :
        print(f"리뷰 내용을 가져오지 못했습니다.\n에러메세지 : {e}")

    try :
        nickname = review.select_one("div > p> span:nth-child(1)").text
        print("닉네임 :", nickname)
    except Exception as e :
        print(f"닉네임을 가져오지 못했습니다.\n에러메세지 : {e}")


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

    review_all = {'name':name,'nickname':nickname,'text':review_text,'review_rating':5-len(rating),'write_date':date,'source':'N'}

    return review_all


def save_info(reviews) :
    if reviews :
        filename = "yanolja_review.csv"
        fullPath = targetPath + filename
        df = pd.DataFrame(reviews)
        try :
            # 기존 파일이 있으면 header=False, 이어쓰기
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
    links = load_links_from_file(fullPath)
    get_review_page(links)


if __name__ == "__main__":
    main()