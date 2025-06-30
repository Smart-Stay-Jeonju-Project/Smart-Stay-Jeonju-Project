from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pandas as pd
import time
import requests


targetPath = "PROJECT/DATA/LIST/"
savetargetPath = "PROJECT/DATA/REVIEWS/"
File_Suffix = '여기어때_link.txt'
print("현재 작업 경로:", os.getcwd())


# 웹 드라이버 객체 생성
def initialze_driver():
    driver = webdriver.Chrome()
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


def load_info() :
    filename = "숙소상세정보.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)
    new_df = df.drop_duplicates(['name'], keep='first')
    filename = "숙소상세정보(중복제거).csv"
    fullPath = targetPath + filename
    new_df.to_csv(f"{fullPath}", index=False, encoding='utf-8-sig',header=False)
    return new_df

def review_count(i, soup) :
    try :
        full = soup.select("div.css-vd152j")
        if full :
            full = len(full)
        else :
            full = 0
    except Exception as e :
        print("별점 없음")
        full = 0
    try :
        harf = soup.select("div.css-19sk4h4")
        if harf :
            harf = 0.5
        else :
            harf = 0
    except Exception as e :
        print("별점 없음")
        harf = 0
    try :
        blank = soup.select("div.css-7fm92b")
        if blank :
            blank = 0
    except Exception as e :
        print("no blank")
        blank = 0
        rating = (full + harf + blank)
    except Exception as e :
        print(f"평점을 가져오지 못했습니다.\n에러메세지 : {e}")
        rating = 0
    try :
        name = soup.select_one('h1.css-17we8hh').text
    except Exception as e :
        print(f"숙소 이름을 가져오지 못했습니다.\n에러메세지 : {e}")
    try :
        review_content = soup.select_one('#review > div.css-1y11ixe > div:nth-child(2) > div > div.css-k4n5rw > div.css-23goey > div.css-1tof81b > p').text
    except Exception as e :
        print(f"평점을 가져오지 못했습니다.\n에러메세지 : {e}")
        review_content = 0
    try :
        write_date = soup.select_one('#review > div.css-1y11ixe > div:nth-child(2) > div > div.css-k4n5rw > div.css-1xow60n > span.css-ua6i0v').text
    except Exception as e :
        print(f"날짜를 가져오지 못했습니다.\n에러메세지 : {e}")
    review_post = {'idnex': i, 'name':name, 'review_content':review_content, 'rating':rating, 'write_date':write_date }
    return review_post

# 키워드로 검색된 숙소의 상세 정보를 가져오기
def get_accommodation_details(driver, links):
    posts = []
    for link in links[:3] :
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        driver.implicitly_wait(10)
        try :
            reviews = soup.select('div.css-1bjv6bx')
            count = len(reviews)
        except Exception  as e :
            print("태그가 없습니다", e)
            continue
        for i in range(count) :
            soup = BeautifulSoup(driver.page_source, 'lxml')
            post = review_count(soup)
            posts.append(post)
        driver.implicitly_wait(3)
        if len(posts) >= 6 :
            load_info()
            print("6개의 정보를 수집하여 중간 저장합니다")
            if save_info(posts) :
                print("중간 저장 완료했습니다")
                posts = []
            else :
                print("중간저장 하지 못했습니다")
                return
    load_info(posts)


def save_info(all_info) :
    if all_info :
        filename = "리뷰상세정보.csv"
        fullPath = savetargetPath + filename
        df = pd.DataFrame(all_info)
        try :
            df.to_csv(f"{fullPath}", mode='a',index=False, encoding='utf-8-sig',header=False)
            print(f"{len(all_info)}개의 숙소의 상세 정보를 저장했습니다")
            return True
        except Exception as e :
            print(f"숙소의 상세 정보를 저장하지 못했습니다 {e}")
            return False

def main():
    driver = initialze_driver()
    fullPath = targetPath + File_Suffix
    links = load_links_from_file(fullPath)
    if get_accommodation_details(driver, links) :
        print("저장이 완료되었습니다")
    else :
        print("전부 저장하지 못했습니다")
    driver.quit()


if __name__ == "__main__":
    main()