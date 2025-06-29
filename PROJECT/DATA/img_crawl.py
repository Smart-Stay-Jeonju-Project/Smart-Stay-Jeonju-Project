from bs4 import BeautifulSoup
from selenium import webdriver
import os
import pandas as pd
import requests

agent_head ={
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

targetPath = "PROJECT/DATA/LIST/"
imgTargetPath = "PROJECT/DATA/imgs/"
linkFilename = "여기어때_link.txt"
imgCSVFilename = "이미지_저장경로.csv"

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
        index = 0
        img_src_link = []

        for link in links[:] :
            result = requests.get(url=link, headers=agent_head)
            driver.implicitly_wait(3)

            html = result.text
            soup = BeautifulSoup(html, 'html.parser')
            
            # 숙소 이름 가져오기
            try :
                name = soup.select_one('h1.css-17we8hh').text
            except Exception as e :
                print(f"숙소 이름을 가져오지 못했습니다.\n에러메세지 : {e}")
                continue
            
            # 이미지 src 가져오기
            try :
                img_tags = soup.select_one('.css-qg470u > img')
                src = img_tags.get('src')
                print(img_tags)
            except Exception as e :
                print(f"이미지를 가져오지 못했습니다. {e}")
                src = ""
            
            # 이미지 파일 이름 : "순번_숙소이름.jpg"
            img_name = name.replace(' ','')
            index += 1
            imgs = {'name' : f"{index}_{img_name}", 'src' : src}
            img_src_link.append(imgs)

            # 20개 단위로 중간 저장
            if len(img_src_link) >= 20 :
                save_img_list(img_src_link)
                img_src_link = []

        return img_src_link
    else :
        return None

# 이미지 저장 리스트 csv 파일 불러오기
def load_img_list():
    img_list = []
    filename = "이미지_저장경로.csv"
    fullPath = targetPath + filename
    df = pd.read_csv(fullPath)
    
    for _, row in df.iterrows() :
        imgs = {'name' : row['name'], 'src' : row['src']}
        img_list.append(imgs)
    return img_list

# 이미지 관련 크롤링한 정보를 csv로 저장하기
def save_img_list(img_src_link) :
    if img_src_link :
        fullPath = targetPath + imgCSVFilename
        df = pd.DataFrame(img_src_link)
        
        try :
            df.to_csv(f"{fullPath}", mode='a',index=False, encoding='utf-8-sig',header=False)
            print(f"{len(img_src_link)}개의 숙소의 상세 정보를 저장했습니다")
            return True
        except Exception as e :
            print(f"숙소의 상세 정보를 저장하지 못했습니다 {e}")
            return False
    else :
        print("저장할 이미지 정보가 없습니다")
        return False

# 이미지 파일을 실제로 저장하는 함수
def save_img(imgs) :
    if imgs :
        # 저장할 폴더가 없다면 생성하기
        if not os.path.isdir(imgTargetPath) :
            os.makedirs(imgTargetPath)
        try :
            for img in imgs[:] :
                img_name = f"{img['name']}.jpg"
                img_url = img['src']
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


def main():
    # 드라이버 객체 생성하기
    driver = initialze_driver()

    # 드라이버가 생성 되었을 경우에 실행
    if driver is not None :
        fullPath = targetPath + linkFilename
    
        # 여기어때_link.txt 에서 url 불러오기
        links = load_links_from_file(fullPath)

        if links is None :
            print("url을 가져올 수 없습니다")
            driver.close()
            return
        
        # 각 숙소의 이미지 정보를 수집하기
        img_links = get_accommodation_details(driver, links)
        
        if img_links is None :
            print("이미지 정보 수집에 오류가 발생했습니다")
        else :
            # 이미지 저장 경로 파일 저장 ( 숙소 이름 , 이미지 src )
            if save_img_list(img_links) :
                print("이미지 저장 경로를 저장하였습니다")
            else :
                print("이미지 저장 경로를 저장하지 못하였습니다")
        
        # 이미지 저장 경로 파일 불러오기
        img_list = load_img_list()
        
        # 실제 이미지 파일 저장
        if save_img(img_list) :
            print("이미지 저장이 전부 완료되었습니다")
        else :
            print("이미지 저장을 전부 완료하지 못했습니다")
        driver.close()
    else :
        print("driver가 생성되지 않았습니다")
        return

if __name__ == "__main__":
    main()
