# 250704 수집 완료

from bs4 import BeautifulSoup
from selenium import webdriver
import os
import pandas as pd
import requests
import time
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.chrome.options import Options


agent_head ={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

targetPath = "DATA/LIST/"
imgTargetPath = "DATA/imgs/yanolja"
linkFilename = "yanolja_link_modify.txt"

print("현재 작업 경로:", os.getcwd())

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
        img_addrs = []

        for link in links :
            try :
                driver = initialze_driver()
                driver.get(link)
                time.sleep(7)
                
                soup = BeautifulSoup(driver.page_source, 'lxml')
                

                # 숙소 이름 가져오기
                try :
                    name = soup.select_one('div.css-11vo59c > h1').text
                    print(name)
                except Exception as e :
                    print(f"숙소 이름을 가져오지 못했습니다.\n에러메세지 : {e}")
                    continue


                # 숙소 상세주소 가져오기
                try :
                    ##domestic-pdp-info > div:nth-child(3) > section > div > div > div.css-cxbger > div.address.css-3ih6hc > span
                    addr = soup.select_one('div.address.css-3ih6hc > span').text
                    print(addr)
                except Exception as e :
                    print(f"숙소 주소를 가져오지 못했습니다.\n에러메세지 : {e}")
                    continue
                
                
                accom_addr = {'name':name, 'addr':addr}

                img_addrs.append(accom_addr)
                print(accom_addr)
                print(accom_addr['name'])
                print(accom_addr['addr'])
            except Exception as e:
                print(f"[ERROR] 링크 접근 중 오류: {e}")
            finally:
                driver.quit()  # ▶ 크롬 종료
                time.sleep(3)

        return img_addrs
    else :
        return None
        

def save_addr(addrs) :
    if addrs :
        # 기존 csv 파일 불러오기
        filename = "yanolja_accommodations(중복제거).csv"
        fullPath = targetPath + filename
        df = pd.read_csv(fullPath)

        # 수집한 이름, 주소
        new_df = pd.DataFrame(addrs)

        # 기존 csv파일의 name과 새로 수집한 name이 같으면 주소정보 추가
        merged_df = pd.merge(df, new_df, on='name', how='left')

        print(merged_df.head())

        new_filename = "new_yanolja_accommodations.csv"
        fullPath = targetPath + new_filename
        # 변경된 데이터프레임 저장
        merged_df.to_csv(fullPath, index=False, mode='w', encoding='utf-8-sig',header=True)


def main():
    # 드라이버 객체 생성하기
    driver = initialze_driver()

    # 드라이버가 생성 되었을 경우에 실행
    if driver is not None :
        fullPath = targetPath + linkFilename
    
        # yanolja_link_modify.txt 에서 url 불러오기
        links = load_links_from_file(fullPath)

        if links is None :
            print("url을 가져올 수 없습니다")
            driver.close()
            return
        
         # 각 숙소의정보를 수집하기
        accom_addrs = get_accommodation_details(driver, links)
        
        if accom_addrs is None :
            print("숙소 주소 수집에 오류가 발생했습니다")
        

        # 기존 파일에 주소 추가
        if save_addr(accom_addrs) :
            print("주소 저장이 전부 완료되었습니다")
            save_addr(accom_addrs)
        else :
            print("주소 저장을 전부 완료하지 못했습니다")
    else :
        print("driver가 생성되지 않았습니다")
        return
    
    driver.close()

if __name__ == "__main__":
    main()
