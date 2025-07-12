from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import pandas as pd
import time

targetPath = "DATA/RAW/LINKS/"
saveTargetPath = "DATA/RAW/accommodations/"
File_Suffix = 'yeogi_link.txt'
print("현재 작업 경로:", os.getcwd())

fullPath = targetPath + File_Suffix

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


# 키워드로 검색된 숙소의 상세 정보를 가져오기
def get_accommodation_details(driver, links):
    all_posts = []
    posts = []
    for link in links[:] :
        driver.implicitly_wait(3)
        driver.get(url=link)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        driver.implicitly_wait(3)
        try :
            name = soup.select_one('h1.css-17we8hh').text
        except Exception as e :
            print(f"숙소 이름을 가져오지 못했습니다.\n에러메세지 : {e}")
        try :
            category = soup.select_one('div.css-1x007zy').text
        except Exception as e :
            print(f"카테고리 항목을 가져오지 못했습니다.\n에러메세지 : {e}")
        try :
            rating_score = soup.select_one('span.css-2d2ntr').text
        except Exception as e :
            print(f"평점을 가져오지 못했습니다.\n에러메세지 : {e}")
            rating_score = 0
        try :
            rating_count = soup.select_one('span.css-1294han').text
            # if rating_count :
            #     rating_count = rating_count.replace(',','')
            #     rating_count = [ int(rating) for rating in rating_count if rating.isdigit() ]
            #     rating_count = int(''.join(map(str, rating_count)))
            print(rating_count)
        except Exception as e :
            print(f"평가수를 가져오지 못했습니다.\n에러메세지 : {e}")
            rating_count = 0
        try :
            address = soup.select_one('span.css-1t5t2dt').text
        except Exception as e :
            print(f"상세주소를 가져오지 못했습니다.\n에러메세지 : {e}")
        
        post = {'name':name, 'category':category, 'ratring_score':rating_score, 'rating_count':rating_count, 'address':address 
                # , 'feature' : feature
                }
        posts.append(post)
        all_posts.append(post)
        if len(posts) >= 20 :
            print("20개의 정보가 초과되어 중간 저장합니다")
            if save_info(posts) :
                print("중간 저장 완료했습니다")
                posts = []
            else :
                print("중간저장 하지 못했습니다")
        save_info(posts)
    save_info(all_posts)


def save_info(all_info) :
    if all_info :
        filename = "yeogi_info.csv"
        fullPath = targetPath + filename
        df = pd.DataFrame(all_info)
        if os.path.exists(fullPath) :
            df.to_csv(f"{fullPath}", mode='a',index=False, encoding='utf-8-sig',header=False)
            return True
        else :
            open(fullPath, 'w', encoding='utf-8-sig').close()
            print("기존 파일이 없거나 비어있어 새로 저장합니다\n파일경로 :", fullPath)
            return False



def main():
    driver = initialze_driver()
    links = load_links_from_file(fullPath)
    if get_accommodation_details(driver, links) :
        print("저장이 완료되었습니다")
    else :
        print("전부 저장하지 못했습니다")
    driver.quit()


if __name__ == "__main__":
    main()