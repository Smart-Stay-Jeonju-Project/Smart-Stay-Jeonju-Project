from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import time

print("현재 작업 경로:", os.getcwd())

targetPath = "DATA/RAW/LINKS/"
savetargetPath = "DATA/RAW/REVIEWS/"
File_Suffix = '여기어때_link.txt'
print("현재 작업 경로:", os.getcwd())
review_id = 'yeogi_accom'


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

number = 0

def review_count(review, name, page_num, link_num) :
    global number
    number += 1
    import re
    try :
        time.sleep(3)
        content_tag = review.select_one('div.css-1tof81b > p')
        if content_tag :
            content = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ-가-힣0-9 ]", "", content_tag.get_text().strip())
    except Exception as e :
        print(f"현재 리뷰 페이지 : {page_num}")
        print(f"리뷰내용을 가져오지 못했습니다.\n에러메세지 : {e}")
        content = ""
    try :
        date_tag = review.select_one('span.css-ua6i0v')
        write_date = date_tag.get_text() if date_tag else ""
    except Exception as e :
        print(f"날짜를 가져오지 못했습니다.\n에러메세지 : {e}")
        write_date = ""
    try :
        full = len(review.select("svg.css-vd152j"))
    except Exception as e :
        full = 0
    try :
        harf = 0.5 if review._find("svg.css-19sk4h4") else 0
    except Exception as e :
        harf = 0

    rating = full + harf
    review_id_name = f"{review_id}_{link_num:03d}_{number:03d}"
    review_post = {'id': review_id_name,'name':name, 'review_content':content, 'rating':rating, 'write_date':write_date }
    print(review_post)
    return review_post

def all_save_reviews(all_review) :
    import json
    if not all_review :
        print("저장할 리뷰가 없습니다")
    
    filename = "모든리뷰상세정보.json"
    fullPath = savetargetPath + filename
    try :
        with open(fullPath, 'w', encoding='utf-8-sig') as f :
            json.dump(all_review, f, indent=4, ensure_ascii=False)
            print(f"리뷰 저장 완료, {len(all_review)} 건 추가 됨")
    except Exception as e :
        print(f"저장 오류 : {e}")

def save_reviews(reviews) :
    import json

    if not reviews :
        print("저장할 리뷰가 없습니다")

    print(reviews)
    filename = "리뷰상세정보.json"
    fullPath = savetargetPath + filename

    old_df = []
    old_contents = []
    try :
        if os.path.exists(fullPath) and os.path.getsize(fullPath) > 0 :
            with open(fullPath, 'r', encoding='utf-8-sig') as f :
                old_df = json.load(f)
            old_contents = [ reviews['id'] for reviews in old_df ]
        else :
            print("기존 파일이 없거나 비어있습니다")
    except Exception as e :
        print("기존 파일 로딩 오류 :",e)
    
    new_list = [ item for item in reviews if item['id'] not in old_contents ]

    if not new_list :
        print("새로운 리스트가 존재하지 않습니다")
        return
    combined = old_df + new_list

    unique_combined = []
    seen_contents = set()
    for r in combined:
        content = r['id']
        if content not in seen_contents:
            unique_combined.append(r)
            seen_contents.add(content)
    try :
        with open(fullPath, 'w', encoding='utf-8-sig') as f :
            json.dump(unique_combined, f, indent=4, ensure_ascii=False)
            print(f"리뷰 저장 완료, {len(new_list)} 건 추가 됨")
    except Exception as e :
        print(f"저장 오류 : {e}")

def get_review_details(driver, links):
    reviews = []
    all_reviews = []
    link_num = 0
    for link in links[:] :
        link_num += 1
        driver.get(link)
        time.sleep(4)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        name = soup.select_one('h1.css-17we8hh').text.strip()

        search_tag = soup.select('div.css-1bjv6bx')     # <class 'bs4.element.ResultSet'>

        # 리뷰 페이지 수 구하기
        rating_count = soup.select_one('span.css-1294han').text[:3]
        if rating_count :
            rating_count = int(rating_count)
        review_page = round (rating_count / 5)
        print(f"총 리뷰 페이지 : {review_page}")
        # 총 리뷰 페이지 : 153
        try :
            '''
            첫 페이지 리뷰 수집
            1. 리뷰 페이지를 도는 동안 리뷰 상세 정보를 가져온다
            2. 페이지당 가져올 리뷰 수는 5개
            3. 정보를 수집하면 페이지 이동(동적: 버튼 클릭)
            3-1. 페이지 이동시 버튼의 class 이름이 새로 할당됨
            3-2. 새로 할당된 버튼의 class 이름을 다시 가져옴
            3-3. 현재 페이지 class 가 'button.css-1rpwxx7' 다음 페이지 class 가 'button.css-1v52o0s' 임
            3-4. 현재 페이지 class 다음에 오는 class가 존재한다면 버튼을 클릭
            3-5. 다음에 오는 class 가 존재하지 않다면, 5페이지 모두 수집 했기 때문에 'class['aria-label':'다음']' 버튼을 클릭
            4. 다음 페이지로 이동하면 정보 수집
            '''
            count = 1
            for page_num in range(1, review_page + 1) :
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                search_tag = soup.select('div.css-1bjv6bx')
                time.sleep(5)
                for review in search_tag :
                    post = review_count(review, name, page_num, link_num)
                    reviews.append(post)
                    all_reviews.append(post)
                try :
                    if len(reviews) >= 50 :
                        save_reviews(reviews)
                        reviews = []
                    count += 1
                    if count % 5 == 1 :
                        next_btn = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='다음']"))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                        time.sleep(5)
                        driver.execute_script("arguments[0].click();",next_btn)
                        print(f"다음 {count} 페이지로 이동합니다")
                        time.sleep(7.5)
                    else :
                        now_btn = 'button.css-1rpwxx7'
                        next_btn = now_btn + ' + button.css-1v52o0s'
                        next_page = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, next_btn))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
                        time.sleep(4)
                        driver.execute_script("arguments[0].click();",next_page)
                        print(f"{count} 페이지로 이동합니다")
                        time.sleep(7.5)
                except Exception as e :
                    print("다음 페이지로 이동 실패", e)
                    return all_reviews
        except Exception as e :
            print("버튼 클릭 실패 :", e)
            return all_reviews

def main():
    driver = initialze_driver()
    fullPath = targetPath + File_Suffix
    links = load_links_from_file(fullPath)

    if links == 0 :
        print("링크를 가져오지 못했습니다")
        return

    print("링크를 수집하였습니다\n리뷰 수집하겠습니다\n...")
    all_reviews = get_review_details(driver, links)
    all_reviews = [ item for item in all_reviews ]
    try :
        all_save_reviews(all_reviews)
        print(f"{len(all_reviews)} 건이 저장되었습니다")
    except Exception as e :
        print("최종 저장하지 못했습니다", e)

    driver.quit()


if __name__ == "__main__":
    main()