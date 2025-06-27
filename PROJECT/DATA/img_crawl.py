from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time

targetPath = "PROJECT/DATA/LIST/"
File_Suffix = '여기어때_link.txt'
print("현재 작업 경로:", os.getcwd())

fullPath = targetPath + File_Suffix
# 경로와 파일이름을 병합하여, 파일을 읽어올 경로를 지정
# fullPath = targetPath + File_Suffix
# 파일에서 불러온 URL의 리스트

links = []
try :
    with open(fullPath, 'r', encoding='UTF-8') as f :
        for line in f :
            link = line.strip()
            if link :
                links.append(link)
    print(f"{len(links)}개의 게시글 URL을 불러옵니다")
except Exception as e :
    print(e)

driver = webdriver.Chrome()
driver.implicitly_wait(10)

domestic_info = []
posts = []

for link in links[:5] :
    driver.get(url=link)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.implicitly_wait(2)
    try :
        name = soup.select_one('h1.css-17we8hh').text
    except Exception as e :
        print(e)
    category = soup.select_one('div.css-1x007zy').text
    rating_score = soup.select_one('span.css-2d2ntr').text
    rating_count = soup.select_one('span.css-1294han').text[:3]
    address = soup.select_one('span.css-1t5t2dt').text
    try :
        feature = soup.select_one('li.css-1hit1zp').text
    except Exception as e :
        feature = ''
    post = {'name':name, 'category':category, 'ratring_score':rating_score, 'rating_count':rating_count, 'address':address , 'feature' : feature}
    fullPath = targetPath +"숙소상세정보.txt"
    try :
        with open(fullPath, 'a', encoding='UTF-8') as f :
            f.write(post+"\n")
            print("중간 저장 했습니다")
    except Exception as e :
        print(e)

# {'name': '전주 비지니스 호텔 궁', 'category': '모텔', 'ratring_score': '9.2', 'rating_count': '752', 'address': '전북특별자치도 전주시 덕진구 금암동 700-3'}


driver.quit()