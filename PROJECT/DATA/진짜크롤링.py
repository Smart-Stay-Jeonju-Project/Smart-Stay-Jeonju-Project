from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests



# 기본 주소
agent_head = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

# 셀레니움으로 크롬 브라우저와 연동하는 웹 드라이버 객체 생성 
driver = webdriver.Chrome()
def maxPage() :
    driver.get("https://www.yeogi.com/domestic-accommodations?sortType=RECOMMEND&keyword=%EC%A0%84%EC%A3%BC&personal=2&checkIn=2025-09-03&checkOut=2025-09-04&freeForm=true")
    search_link = ".css-1psit91 h1"
    soup = BeautifulSoup(driver.page_source, 'lxml')
    MaxNum = soup.select_one(search_link).text[-4:-1]
    time.sleep(5)
    search_page = round( int(MaxNum) / 20 )
    return search_page

# page link 가져오기
def page_link(search_page) :
    all_link = []
    search_link = "a.gc-thumbnail-type-seller-card.css-wels0m"
    for page in range(search_page + 1) :
        url = f"https://www.yeogi.com/domestic-accommodations?sortType=RECOMMEND&keyword=%EC%A0%84%EC%A3%BC&page={page}&personal=2&checkIn=2025-09-03&checkOut=2025-09-04&freeForm=true"
        driver.get(url)
        obj_list = driver.find_elements(By.CSS_SELECTOR, search_link)
        time.sleep(5)
        link_list = [obj.get_attribute("href") for obj in obj_list ]
        all_link += link_list
    return all_link

def save_link(all_links) :
    if all_links :
        try:
            with open(f"여기어때_link.txt", "a", encoding="utf-8") as f:
                for line in all_links :
                    f.write(line+"\n")
        except Exception as e :
            print("페이지 링크를 저장하지 못했습니다")

# 페이지에서 페이지 이미지에 있는 alt 속성값과, src 속성값 가져오기
def page_info() :
    names = []
    for page in range(1,21) :
        url = f"https://www.yeogi.com/domestic-accommodations?sortType=RECOMMEND&keyword=%EC%A0%84%EC%A3%BC&page={page}&personal=2&checkIn=2025-09-03&checkOut=2025-09-04&freeForm=true"
        result =requests.get(url=url,headers=agent_head)
        html = result.text
        soup = BeautifulSoup(html, "lxml")
        src = soup.select(".css-nl3cnv img")
        img_names = src.find_all('alt')
        for name in img_names :
            names.append(name)

def save_info(all_info) :
    if all_info :
        try :
            with open(f"{all_info['title'].txt}","a", encoding="utf-8") as f :
                for line in all_info :
                    f.write(line+"\n")
        except Exception as e :
            print("숙소의 상세 정보를 저장하지 못했습니다")

def main() :
    maxPage = maxPage()
    all_links = page_link(maxPage)
    if save_link(all_links) :
        print("저장이 완료되었습니다")
    else :
        print("저장하지 못했습니다")
    driver.close()

if __name__ == "__main__" :
    main()