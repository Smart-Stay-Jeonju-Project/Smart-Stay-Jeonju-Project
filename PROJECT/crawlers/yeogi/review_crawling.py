from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import time

targetPath = "DATA/RAW/LINKS/"
savetargetPath = "DATA/RAW/REVIEWS/"
File_Suffix = 'yeogi_link.txt'
print("현재 작업 경로:", os.getcwd())
review_id = 'y'

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

def review_count(review, name, page_num, number) :
    import re
    try :
        nickname_tag = review.select_one('div.css-1bh2qmi > div > p')
        if nickname_tag :
            nickname = nickname_tag.get_text()
        else :
            nickname = ""
    except Exception as e :
        print(f"닉네임을 가져오지 못했습니다.\n에러메세지 : {e}")
        nickname = ""
    try :
        content_tag = review.select_one('div.css-23goey > div > p')
        if content_tag :
            #content = re.sub(r"[^ㄱ-ㅎㅏ-ㅣ-가-힣0-9 ]", "", content_tag.get_text().strip())
            review_text = content_tag.get_text()
            review_text = re.sub(r'[\r\n\t ]+', ' ', review_text)     # 줄바꿈/탭 → 공백
            review_text = re.sub(r'\s+', ' ', review_text)           # 연속 공백 → 하나의 공백
            content = review_text.replace('\u200b', '').strip()  # 특수 공백 제거 + 양끝 공백 제거
        else :
            content = ""
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
        harf = 0.5 if review.find("svg.css-19sk4h4") else 0
    except Exception as e :
        harf = 0
    rating = full + harf
    review_id_name = f"{review_id}_{number:03d}"
    review_post = {'id': review_id_name, 'nickname':nickname, 'name': name, 'review_content':content, 'rating':rating, 'write_date':write_date }
    print(review_post)
    return review_post

def all_save_reviews(all_review) :
    if not all_review :
        print("전체 리뷰 없음")
        return
    filename = f"yeogi_all_reviews.csv"
    fullPath = savetargetPath + filename
    df = pd.DataFrame(all_review)
    df.to_csv(fullPath, index=False, encoding='utf-8-sig', header=True)
    print(f"전체 리뷰 {len(all_review)}개 저장됨 → {fullPath}")

def save_reviews(reviews, num) :
    if not reviews :
        print("저장할 리뷰가 없습니다")
    filename = f"{num}_y_reviews.csv"
    fullPath = savetargetPath + filename
    existing = set()

    if os.path.exists(fullPath) :
        try :
            old_df = pd.read_csv(fullPath)
            if 'id' in old_df.columns :
                existing = set(old_df['id']) # 모든 ID를 문자열로 변환
        except Exception as e :
            print("기존 파일이 없거나 비어있어 새로 저장합니다\n파일경로 :", fullPath)
    
    new_reviews = [item for item in reviews if item['id'] not in existing]

    if not new_reviews :
        print("새로운 리뷰가 없습니다")
        return

    df = pd.DataFrame(new_reviews)
    write_header = not os.path.exists(fullPath)
    try :
        df.to_csv(fullPath, mode='a',index=False, encoding='utf-8-sig',header=write_header)
        print(f"{len(new_reviews)}개의 리뷰를 저장했습니다 -> {fullPath}")
    except Exception as e :
        print("저장의 오류가 발생하였습니다", e)

def get_review_details(driver, links):
    all_reviews = []
    link_num = 0
    try :
        for link in links[:] :
            link_num += 1
            reviews = []
            count = 1
            number = 0
            driver.get(link)
            time.sleep(4)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            name = soup.select_one('h1.css-17we8hh').text.strip()
            print(f"{name} 리뷰를 수집하겠습니다...")
            search_tag = soup.select('div.css-1bjv6bx')     # <class 'bs4.element.ResultSet'>

            # 리뷰 페이지 수 구하기
            rating_count = soup.select_one('span.css-1294han').text
            if rating_count :
                rating_count = rating_count.replace(',','')
                rating_count = [ int(rating) for rating in rating_count if rating.isdigit() ]
                rating_count = int(''.join(map(str, rating_count)))
            print(rating_count)

            review_page = round (rating_count / 5)
            print(f"총 리뷰 페이지 : {review_page}")
            try :
                for page_num in range(1, review_page + 1) :
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    time.sleep(1)
                    search_tag = soup.select('div.css-xogpio')
                    time.sleep(1)
                    for review in search_tag :
                        number += 1
                        post = review_count(review, name, page_num, number)
                        reviews.append(post)
                        all_reviews.append(post)
                        if len(reviews) >= 20 :
                            save_reviews(reviews,link_num)
                            reviews = []
                        count += 1
                        try :
                            if count % 5 == 1 :
                                next_btn_selector = "button[aria-label='다음']"
                            else :
                                now_btn_selector = 'button.css-1rpwxx7'
                                next_btn_selector = now_btn_selector + ' + button.css-1v52o0s'
                            
                            next_btn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, next_btn_selector))
                            )
                            driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                            time.sleep(1)
                            driver.execute_script("arguments[0].click();", next_btn)
                            print(f"{page_num+1} 페이지로 이동합니다")
                        except Exception as e :
                            print("다음 페이지로 이동 실패", e)
                            print("다음 숙소 리뷰를 수집하겠습니다")
            except Exception as e :
                print("버튼 클릭 실패 :", e)
                print("다음 숙소 리뷰를 수집하겠습니다")
            finally :
                save_reviews(reviews,link_num)
    except Exception as e :
        print('링크 이동에 오류가 발생하였습니다', e)
    finally :
        return all_reviews

def main():
    driver = initialze_driver()
    fullPath = targetPath + File_Suffix
    links = load_links_from_file(fullPath)

    if links == 0 :
        print("링크를 가져오지 못했습니다")
        return

    print("링크를 수집하였습니다\n리뷰 수집하겠습니다\n...")
    try :
        all_reviews = get_review_details(driver, links)
        all_save_reviews(all_reviews)
    except Exception as e :
        print("리뷰 수집 중 오류 발생 :", e)
    driver.quit()

if __name__ == "__main__":
    main()