from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
import requests
import time

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

# navigator.webdriver 우회: 자동화 탐지 방지
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})

targetPath = "DATA/RAW/LINKS/"
imgTargetPath = "DATA/RAW/imgs/yanolja/"
linkFilename = "yanolja_link_modify.txt"
imgCSVFilename = "img_name.csv"

print("현재 작업 경로:", os.getcwd())

# 웹 드라이버 객체 생성
def initialze_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

# 텍스트 파일에서 URL 목록 불러오기  
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
        return None

# 숙소 상세 정보(이름, src) 크롤링
def get_accommodation_details(driver, links):
    if links :
        img_src_links = []

        for link in links[:] :
            driver.get(url=link)
            time.sleep(10)
            driver.implicitly_wait(10)

            soup = BeautifulSoup(driver.page_source, 'lxml')
            
            # 숙소 이름 가져오기
            try :
                name = soup.select_one('div.css-11vo59c > h1').text
                print(name)
            except Exception as e :
                print(f"숙소 이름을 가져오지 못했습니다.\n에러메세지 : {e}")
                continue
            
            # 이미지 src 가져오기
            try :
                img_tags = soup.select_one('div.swiper-slide-active > div > span > img')
                src = img_tags.get('src')
                print(src)
            except Exception as e :
                print(f"이미지를 가져오지 못했습니다. {e}")
                src = ""
            
            img_src_link = {'name':name, 'src':src}

            img_src_links.append(img_src_link)
            print(img_src_link)
            print(img_src_link['name'])
            time.sleep(5)

        return img_src_links
    else :
        return None
        

# 이미지 파일을 실제로 저장하는 함수
def save_img(links) :
    if links :
        # 저장할 폴더가 없다면 생성하기
        if not os.path.isdir(imgTargetPath) :
            os.makedirs(imgTargetPath)
        try :
            for link in links :
                img_name = f"{link['name']}.jpg"
                img_url = link['src']
                fullPath = os.path.join(imgTargetPath, img_name)
                # 이미지 다운로드 요청
                save_img = requests.get(img_url)
                # 파일로 저장하기
                with open(fullPath, 'wb') as f :
                    f.write(save_img.content)
        
        except Exception as e :
            print(f"이미지를 저장하지 못했습니다, {e}")
            return
    else :
        print("저장할 이미지가 없습니다")
        return
    return img_name
    


def main():
    # 드라이버가 생성 되었을 경우에 실행
    if driver is not None :
        fullPath = targetPath + linkFilename
    
        # yanolja_link_modify.txt 에서 url 불러오기
        links = load_links_from_file(fullPath)

        if links is None :
            print("url을 가져올 수 없습니다")
            driver.close()
            return
        
         # 각 숙소의 이미지 정보를 수집하기
        img_src_links = get_accommodation_details(driver, links)
        
        if img_src_links is None :
            print("이미지 정보 수집에 오류가 발생했습니다")
        

        # 실제 이미지 파일 저장
        if save_img(img_src_links) :
            print("이미지 저장이 전부 완료되었습니다")
            save_img(img_src_links)
        else :
            print("이미지 저장을 전부 완료하지 못했습니다")
    else :
        print("driver가 생성되지 않았습니다")
        return
    
    driver.close()

if __name__ == "__main__":
    main()
