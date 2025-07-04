from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os

# URL에 보낼 Parameter 설정
targetPath = "PROJECT/DATA/LIST/"
KEYWORD = '전주'


# 저장 변수
link_filename = 'yanolja_link.txt'

# URL
SEARCH_URL = f"https://nol.yanolja.com/local/search?keyword={KEYWORD}&shortcut=all&pageKey=1751252871083"
#https://nol.yanolja.com/local/search?keyword={KEYWORD}&shortcut=all&pageKey=1751252871083


# 웹 드라이버 객체 생성
def initialze_driver():
    try :
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        return driver
    except Exception as e :
        print("웹 드라이버 객체를 생성하지 못했습니다")
        return None
    
# 숙소 링크 수집하기
def page_link(driver) :
    driver.get(SEARCH_URL)
    driver.implicitly_wait(10)
    time.sleep(5)

    #soup = BeautifulSoup(driver.page_source, 'lxml')
    count = 40

    for i in range(count) :
        driver.execute_script("window.scroll(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        time.sleep(5)
        i += 1

        # 32개만 수집되던 문제 -> soup을 for문안에 생성하여 해결
        soup = BeautifulSoup(driver.page_source, 'lxml')

        links = soup.select('div.flex.justify-center.pc\:justify-normal > div > div.mb-\[calc\(76px\+env\(safe-area-inset-bottom\)\)\].flex.h-full.flex-col.items-center.overflow-x-hidden.pc\:mb-96 > div > div > a')
        #div flex w-full max-w-legacy-pc-size flex-wrap pc:rounded-12 divide-y divide-line-neutral-weak1 overflow-hidden border-b border-t border-line-neutral-weak1 pc:divide-x pc:border pc:first:!border-t pc:[&>*:nth-child(2)]:!border-t-0 pc:[&>*:nth-child(2n+1)]:!border-l-0
        #a flex w-full min-w-[320px] flex-col p-16 pc:w-1/2
        # div > div.mb-\[calc\(76px\+env\(safe-area-inset-bottom\)\)\].flex.h-full.flex-col.items-center.overflow-x-hidden.pc\:mb-96 > div > a
        # body > div.flex.justify-center.pc\:justify-normal > div > div.mb-\[calc\(76px\+env\(safe-area-inset-bottom\)\)\].flex.h-full.flex-col.items-center.overflow-x-hidden.pc\:mb-96 > div > div:nth-child(2) > a
        # body > div.flex.justify-center.pc\:justify-normal > div > div.mb-\[calc\(76px\+env\(safe-area-inset-bottom\)\)\].flex.h-full.flex-col.items-center.overflow-x-hidden.pc\:mb-96 > div > div:nth-child(6) > a:nth-child(55)
        

        if links :
            print("검색 결과 페이지를 로드했습니다")
            print(f"링크 수{len(links)}")
        else :      # 스크롤 했지만, 게시글이 더 생기지 않음
            print("검색 결과가 없습니다")
            exit() 
        
        all_link = []
            
        # n개의 링크를 하나씩 꺼내면서 주소값('href') 꺼내기
        for link in links :
            href = link.get_attribute_list('href')
            if href:
                print("url을 찾았습니다")
                print(href)
                all_link.append(href)
            else :
                print("url을 찾지 못했습니다")
                return False
            
    return all_link


# 수집된 숙소 링크들을 텍스트 파일로 저장하기
def save_link(all_link) :
    fullPath = targetPath + link_filename

    if not all_link :
        print("저장할 내용이 없습니다")
        exit()
    try :
        if os.path.exists(fullPath) :
            with open(fullPath, "a",encoding="utf-8") as f:
                for line in all_link :
                    for url in line :
                        f.write(url+"\n")
            return True

        else :
            with open(fullPath, "w",encoding="utf-8") as f:
                for line in all_link :
                    for url in line :
                        f.write(url+"\n")
            return True
    
    except Exception as e :
        print("페이지 링크를 저장하지 못했습니다",e)
        return False

'''
def scroll(driver):
    try:
        driver.execute_script("window.scroll(0, document.body.scrollHeight);")
        driver.implicitly_wait(10)
        time.sleep(3)
        return True
    except Exception as e:
        print(e)
        return False
'''
    

def main() :
    # 드라이버 객체 생성하기
    driver = initialze_driver()

    # 드라이버가 생성되었을 경우에 함수 실행
    if driver is not None :
        all_links = page_link(driver)
        # 링크 텍스트 파일 저장 함수
        
        if save_link(all_links) :
            print("저장이 완료되었습니다")
        else :
            print("저장하지 못했습니다")
        
        '''
        while scroll(driver) :
            result = page_link(driver)
            if not result :
                print("탐색을 종료합니다")
                exit()
            save_link(result)
        '''

    else :
        print("driver 가 생성되지 않았습니다")
        return
    driver.close()

    
if __name__ == "__main__" :
    main()