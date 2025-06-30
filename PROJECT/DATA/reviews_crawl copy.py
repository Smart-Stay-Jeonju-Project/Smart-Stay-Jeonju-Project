from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pandas as pd
import time
import requests

agent_head ={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

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
        return 0


def review_count(review, name) :
    count = 0
    try :
        content = review.select_one('div.css-1tof81b > p')
        review_content = content.get_text()
        print(f"리뷰내용 : {review_content}")
    except Exception as e :
        print(f"리뷰내용을 가져오지 못했습니다.\n에러메세지 : {e}")
        review_content = None
    try :
        date = review.select_one('span.css-ua6i0v')
        write_date = date.get_text()
        print(f"리뷰날짜 : {write_date}")
    except Exception as e :
        print(f"날짜를 가져오지 못했습니다.\n에러메세지 : {e}")
    try :
        full = review.select("svg.css-vd152j")
        if full :
            for i in full :
                count += 1
        else :
            count = 0
    except Exception as e :
        print("별점 없음")
        count = 0
    try :
        harf = review._find_one("svg.css-19sk4h4")
        if harf :
            harf = 0.5
        else :
            harf = 0
    except Exception as e :
        print("별점 없음")
        harf = 0
    try :
        blank = review._find_one("svg.css-7fm92b")
        if blank :
            blank = 0
    except Exception as e :
        print("no blank")
        blank = 0
    rating = (count + harf + blank)
    review_post = {'name':name, 'review_content':review_content, 'rating':rating, 'write_date':write_date }
    print(review_post)
    return review_post

# 키워드로 검색된 숙소의 상세 정보를 가져오기
def get_accommodation_details(driver, links):
    posts = []
    for link in links[:10] :
        try :
            driver.get(link)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            search_name_tag = soup.select_one('h1.css-17we8hh')
            name = search_name_tag.text
            print(name)
            search_tag = soup.select('div.css-1bjv6bx')     # <class 'bs4.element.ResultSet'>
            if search_tag :
                print("태그를 찾았습니다", type(search_tag))
            else :
                print("태그를 찾지 못했습니다")
            for reviews in search_tag :
                for review in reviews :
                    post = review_count(review, name)
                    posts.append(post)
            if len(posts) >= 20 :
                save_info(posts)
                posts = []
        except Exception  as e :
            print("태그가 없습니다", e)
            continue

def save_info(all_info) :
    if all_info :
        filename = "리뷰상세정보.csv"
        fullPath = savetargetPath + filename
        try :
            existing = set()
            if os.path.exists(fullPath) :
                with open(fullPath, 'r', encoding='utf-8') as f :
                    for line in f :
                        existing.add(line.strip())
            new_lists = [ re_list for re_list in all_info if re_list not in existing ]
            if not new_lists :
                print("새로운 리뷰가 없습니다")
                return True
            
            with open(fullPath, "a", encoding="utf-8") as f:
                for line in new_lists :
                    f.write(line+"\n")
            return True
        except Exception as e :
            print("페이지 링크를 저장하지 못했습니다")
            return False

def main():
    driver = initialze_driver()
    fullPath = targetPath + File_Suffix
    links = load_links_from_file(fullPath)
    if links == 0 :
        print("링크를 가져오지 못했습니다")
        return
    else :
        print("링크를 수집하였습니다\n리뷰 수집하겠습니다\n")
        if get_accommodation_details(driver, links) :
            print("저장이 완료되었습니다")
        else :
            print("전부 저장하지 못했습니다")
    driver.quit()


if __name__ == "__main__":
    main()