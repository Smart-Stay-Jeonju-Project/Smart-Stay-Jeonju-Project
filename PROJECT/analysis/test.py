import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time
from pykospacing import Spacing

'''
pip install git+https://github.com/haven-jeon/PyKoSpacing.git
'''

# 네이버 맞춤법 API 설정 PASSPORT_KEY 변동
PASSPORT_KEY = "dbc0dc1e7ae1070bacecf1a3865c72b5d121abc2"
BASE_URL = "https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy"

spacing = Spacing()

def remove_tags(text: str) -> str:
    text = u'<content>{}</content>'.format(text).replace('<br>', '')
    return ''.join(ET.fromstring(text).itertext())

def spell_check_naver(text: str) -> tuple:
    params = {
        "passportKey": PASSPORT_KEY,
        "q": text,
        "color_blindness": "0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://search.naver.com/"
    }
    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        data = response.json()['message']['result']
        html = data.get('html', '')
        corrected = remove_tags(html)
        return corrected, data.get('errata_count', 0)
    except Exception as e:
        print(f"❌ 오류: {e}")
        return text, -1

def extract_diff_words(original: str, corrected: str) -> str:
    ori_words = original.split()
    cor_words = corrected.split()
    diffs = []

    for o, c in zip(ori_words, cor_words):
        if o != c:
            diffs.append(f"{o}→{c}")

    if len(ori_words) != len(cor_words):
        min_len = min(len(ori_words), len(cor_words))
        tail_ori = ori_words[min_len:]
        tail_cor = cor_words[min_len:]
        for o, c in zip(tail_ori, tail_cor):
            if o != c:
                diffs.append(f"{o}→{c}")

    return ", ".join(diffs)

def process_and_add_columns(input_path: str, output_path: str, text_column: str = "review"):
    df = pd.read_csv(input_path, encoding='utf-8')

    corrected_list = []
    error_count_list = []
    diff_list = []

    for idx, row in df.iterrows():
        text = str(row[text_column])
        print(f"[{idx + 1}/{len(df)}] 원문: {text[:30]}...")

        # 1. pykospacing으로 띄어쓰기 자동 보정
        text_spaced = spacing(text)
        print(f" → 띄어쓰기 보정: {text_spaced[:30]}...")

        # 2. 네이버 맞춤법 검사
        corrected, error_count = spell_check_naver(text_spaced)

        # 3. 차이 추출
        diff = extract_diff_words(text_spaced, corrected) if error_count > 0 else ""

        corrected_list.append(corrected)
        error_count_list.append(error_count)
        diff_list.append(diff)

        time.sleep(0.8)

    df['spacing_fixed'] = [spacing(str(x)) for x in df[text_column]]  # 띄어쓰기 자동 보정 컬럼도 추가
    df['corrected_review'] = corrected_list
    df['spell_error_count'] = error_count_list
    df['spell_diff'] = diff_list

    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n✅ 결과 저장 완료: {output_path}")

if __name__ == "__main__":
    input_file = "ANALYSIS/dict_review_texts.csv"
    output_file = "ANALYSIS/result_dict_review_texts.csv"
    try :
        df = pd.read_csv(input_file, encoding='utf-8')
        print("파일을 불러왔습니다")
    except Exception as e :
        print("파일을 불러오지 못했습니다")
        exit()
    
    space = []
    try :
        for _, row in df.iterrows():
            text = str(row['text'])
            ptext_spaced = spacing(text)
            space.append(ptext_spaced)
            print(f"{text} -> {ptext_spaced}")
        print("띄어쓰기 수정이 완료되었습니다")
    except Exception as e :
        print("띄어쓰기 수정을 하지 못했습니다", e)
    try :
        new_df = pd.DataFrame(space)
    except Exception as e :
        print("데이터프레임으로 만들지 못했습니다", e)
    try :
        new_df.to_csv(output_file, index=False, encoding='utf-8-sig', header=False)
    except Exception as e :
        print("저장하지 못했습니다")
    #process_and_add_columns(input_file, output_file)
