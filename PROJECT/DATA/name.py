from bs4 import BeautifulSoup
import time
import os
import requests
import re

save_dir = "./imgs/"
os.makedirs(save_dir, exist_ok=True)

# 기본 주소
agent_head = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

names = []
src_imgs = []
batch_index = 1

def save_images(name_list, src_list, batch_index):
    for i, (name, src) in enumerate(zip(name_list, src_list)):
        safe_name = re.sub(r'[\\/*?:"<>| ]', "_", name)
        filename = f"{batch_index:02d}_{safe_name}.jpg"
        filepath = os.path.join(save_dir, filename)
        try:
            img_data = requests.get(src).content
            with open(filepath, "wb") as f:
                f.write(img_data)
            print(f"저장 완료: {filename}")
        except Exception as e:
            print(f"저장 실패: {filename} → {e}")

for page in range(1, 21) :
    url = f"https://www.yeogi.com/domestic-accommodations?sortType=RECOMMEND&keyword=%EC%A0%84%EC%A3%BC&page={page}&personal=2&checkIn=2025-09-03&checkOut=2025-09-04&freeForm=true"
    result =requests.get(url=url,headers=agent_head)
    time.sleep(3)
    html = result.text
    soup = BeautifulSoup(html, "lxml")
    time.sleep(5)
    img_tags = soup.select(".css-nl3cnv img")

    for img in img_tags:
        name = img.get('alt')
        src = img.get('src')

        if name and src:
            names.append(name)
            src_imgs.append(src)

        if len(names) % 20 == 0:
            save_images(names, src_imgs, batch_index)
            names.clear()
            src_imgs.clear()
            batch_index += 1

if names:
    save_images(names, src_imgs, batch_index)