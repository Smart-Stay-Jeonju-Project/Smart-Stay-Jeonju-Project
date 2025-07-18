import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
import re

# 환경설정
load_dotenv()
API_KEYS = os.getenv("API_KEY_AI").split(",")
genai.configure(api_key=API_KEYS[0].strip()) 
model = genai.GenerativeModel("gemini-2.5-flash")

# 경로 설정
INPUT_PATH = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_filtered_up.csv"
OUTPUT_CSV_PATH = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/ai_y_report.csv"
# INPUT_PATH = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_filtered_up.csv"
# OUTPUT_CSV_PATH = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/ai_n_report.csv"
os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)

current_api_index = 0

# 함수: API 키를 교체하면서 모델 재설정
def switch_api_key():
    global current_api_index
    current_api_index += 1
    if current_api_index < len(API_KEYS):
        print(f" API 키 교체: {current_api_index + 1}/{len(API_KEYS)}번 키 사용")
        genai.configure(api_key=API_KEYS[current_api_index].strip())
        return True
    else:
        print(" 모든 API 키 소진. 더 이상 호출 불가.")
        return False

# 기존 결과 불러오기
done_names = set()
write_header = not os.path.exists(OUTPUT_CSV_PATH)
if not write_header:
    try:
        df_done = pd.read_csv(OUTPUT_CSV_PATH)
        done_names = set(df_done["name"].astype(str).str.strip())
        print(f" 완료된 숙소 수: {len(done_names)} (건너뜀)")
    except Exception as e:
        print(f" 완료 파일 로드 실패. 새로 시작합니다: {e}")

# 데이터 로드 및 정렬
df = pd.read_csv(INPUT_PATH)
df["write_date"] = pd.to_datetime(df["write_date"], errors="coerce")
df = df.sort_values("write_date", ascending=False)

# 프롬프트 템플릿 (JSON 이스케이프 처리 적용)
system_prompt_template = """아래는 하나의 숙소에 대한 여러 리뷰입니다.

각 숙소에 대해 다음 조건에 맞춰 분석해 주세요:
1. content 컬럼의 모든 데이터들을 순회하며 숙소를 대표할 형용사 형태의 키워드 10개~30개를 선정하세요 (예: 깨끗한, 편리한).
2. 키워드는 긍정리뷰, 부정리뷰 두 곳에서 전부 추출하세요.
3. 리뷰 내용을 바탕으로 2~4문장 분량의 평가 문장을 작성하세요.
5. 부정 리뷰가 4개 이하면 긍정 리뷰만 사용하여 selected를 구성합니다. 이 경우 최대 10개의 긍정 리뷰를 사용하도록 합니다.
6. 부정 리뷰가 5개 이상이면 긍정 리뷰와 부정 리뷰를 5:5 비율로 n개씩 가져와 selected를 구성합니다. 리뷰 최대개수는 25개로 제한합니다.
7. 긍정리뷰가 평가내용에 포함될 경우 '이 숙소의 장점은' 이라는 문구로 시작 하세요.
8. 부정리뷰가 평가내용에 포함될 경우 '아쉬운점은' 이라는 문구로 시작하세요.
9. 평가내용에 부정리뷰가 포함될 경우 개선사항을 반드시 작성하고 '개선사항으로는' 이라는 문구로 시작하세요.
10. 긍정, 부정 리뷰의 총합이 10개 이하이면 '리뷰가 충분하지 않습니다.' 를 출력하고 키워드도 출력하지 마세요.

{dynamic_instructions}

출력 형식은 아래와 같습니다:
{{
  "list": [
    {{
      "name": "<숙소 이름>",
      "keywords": "형용사1,형용사2,...",
      "content": "평가 요약 문장"
    }}
  ]
}}
"""

# API 재시도 설정
MAX_RETRIES = 3 # 최대 재시도 횟수
RETRY_DELAY_SECONDS = 5 # 재시도 간격 (초)

# 숙소별 처리
for name, group in df.groupby("name"):
    if name in done_names:
        print(f" 이미 처리됨: {name}, 건너뛰ㅂ니다.")
        continue

    # 중요: pos_all, neg_all은 헤드(25)로 자르기 전의 전체 긍정/부정 리뷰를 나타냅니다.
    group_filtered_type = group[group["type"].isin(["긍정", "부정"])]
    group_filtered_type = group_filtered_type.sort_values("write_date", ascending=False)

    pos_all = group_filtered_type[group_filtered_type["type"] == "긍정"]
    neg_all = group_filtered_type[group_filtered_type["type"] == "부정"]

    selected_reviews_for_api = pd.DataFrame()
    dynamic_instructions_for_prompt = "" # 프롬프트에 동적으로 추가될 지시사항

    print(f"\n▶ 숙소 처리 시작: {name}")
    print(f"DEBUG: 숙소 '{name}' - **원본** 긍정 리뷰: {len(pos_all)}개, **원본** 부정 리뷰: {len(neg_all)}개")

    # 1. '리뷰가 충분하지 않습니다.' 판단 기준을 추출 전의 전체 리뷰 개수로 변경
    # 즉, pos_all과 neg_all의 총합을 사용합니다.
    if (len(pos_all) + len(neg_all)) < 10:
        print(f"DEBUG: 숙소 '{name}' - **총 원본 리뷰 수**가 10개 미만({len(pos_all)+len(neg_all)}개)이므로 '리뷰가 충분하지 않습니다.'로 저장합니다.")
        result_data = {
            "name": name,
            "keywords": "", # 리뷰가 부족하므로 키워드는 비워둡니다.
            "content": "리뷰가 충분하지 않습니다."
        }
        output_df = pd.DataFrame([result_data])
        try:
            output_df.to_csv(OUTPUT_CSV_PATH, mode="a", header=write_header, index=False, encoding="utf-8-sig")
            write_header = False
            print(f" 저장 완료 → {name} (리뷰 부족)")
        except Exception as e:
            print(f" 오류 발생 (리뷰 부족 숙소 저장): {name} → {e}")
        continue # 저장 후 다음 숙소로 넘어갑니다.

    # --- 아래는 API에 보낼 리뷰를 선택하는 로직 (기존 pos, neg 변수 사용) ---
    # 이제 pos와 neg는 API에 보낼 '선택된' 리뷰 개수를 나타냅니다.
    pos = pos_all.head(25) # API로 보낼 최대 25개 긍정 리뷰
    neg = neg_all.head(25) # API로 보낼 최대 25개 부정 리뷰


    # 2. 긍정 리뷰가 10개 이상이고 부정 리뷰가 0개인 경우 (이전 답변에서 추가된 로직)
    if len(pos_all) >= 10 and len(neg_all) == 0:
        # 이 경우 API에는 모든 긍정 리뷰를 보낼 수 있도록 pos_all을 사용
        selected_reviews_for_api = pos_all.head(len(pos_all)) # 모든 긍정 리뷰를 API로 보냄 (프롬프트는 최대 10개지만, 여기서는 모든 긍정을 고려)
        dynamic_instructions_for_prompt = """
        **매우 중요**: 이 숙소에는 부정 리뷰가 없습니다.
        content 필드에는 '이 숙소의 장점은'으로 시작하는 문장만 작성하세요.
        아쉬운 점이나 개선 사항은 절대로 언급하지 마세요.
        키워드는 긍정 리뷰 내용에서만 추출하여 10~30개를 선정하세요.
        content 필드에 '리뷰가 충분하지 않습니다.'와 같은 문구를 사용하지 마세요.
        """
        print(f"DEBUG: 숙소 '{name}' - 긍정 리뷰 {len(pos_all)}개, 부정 리뷰 0개이므로 긍정 리뷰만 사용하여 {len(selected_reviews_for_api)}개 선택 (API 전송용).")

    # 3. 부정 리뷰가 4개 이하인 경우 (기존 로직, 긍정 리뷰 10개 미만이거나 부정 리뷰가 있는 경우)
    elif len(neg_all) <= 4: # 이 조건은 neg_all.head(25)로 자르기 전의 개수를 사용
        selected_reviews_for_api = pos.head(10) # 긍정 리뷰만 최대 10개 선택 (프롬프트 5번)
        if len(neg) > 0: # neg는 head(25)로 잘린 부정 리뷰
             selected_reviews_for_api = pd.concat([selected_reviews_for_api, neg.head(len(neg))])
        
        dynamic_instructions_for_prompt = f"""
        (참고: 이 숙소의 부정 리뷰는 {len(neg_all)}개로 매우 적습니다. 이 점을 고려하여 평가 문장을 작성하세요.
        content 필드에 '리뷰가 충분하지 않습니다.'와 같은 문구를 사용하지 마세요.)
        """
        print(f"DEBUG: 숙소 '{name}' - 부정 리뷰가 {len(neg_all)}개 이하이므로 긍정 리뷰 위주로 {len(selected_reviews_for_api)}개 선택 (API 전송용).")

    # 4. 부정 리뷰가 5개 이상인 경우 (기존 로직)
    else:
        # 긍정/부정 각각 최대 25개씩 가져와서 5:5 비율을 맞춤 (프롬프트 6번 '리뷰 최대개수는 25개로 제한합니다.')
        n_to_take_each = min(len(pos), len(neg), 25) 
        pos_final = pos.head(n_to_take_each)
        neg_final = neg.head(n_to_take_each)
        selected_reviews_for_api = pd.concat([pos_final, neg_final])
        
        dynamic_instructions_for_prompt = """
        (참고: 긍정 리뷰와 부정 리뷰가 모두 존재하므로 양쪽을 균형 있게 평가 문장에 반영하세요.
        content 필드에 '리뷰가 충분하지 않습니다.'와 같은 문구를 사용하지 마세요.)
        """
        print(f"DEBUG: 숙소 '{name}' - 긍정: {len(pos_final)}개, 부정: {len(neg_final)}개 (총 {len(selected_reviews_for_api)}개) 선택 (API 전송용).")


    # 최종 선택된 리뷰가 비어있는지 확인 (안전 장치)
    if selected_reviews_for_api.empty:
        print(f"DEBUG: 숙소 '{name}' - 최종 선택된 리뷰가 없어 API 호출 생략 (이 경우는 리뷰가 10개 미만이 아니면서도 긍/부정 필터링 후 모두 사라진 극히 드문 경우).")
        # 이 경우도 사실상 리뷰가 부족한 것으로 간주될 수 있으나, 이미 상위 조건에서 대부분 처리됨.
        continue

    # 선택된 리뷰들을 최신순으로 다시 정렬
    selected_reviews_for_api = selected_reviews_for_api.sort_values("write_date", ascending=False)
    
    # API 요청을 위한 리뷰 목록 생성
    reviews_for_prompt = [f"{row['type']},{row['clean_reviews']}" for _, row in selected_reviews_for_api.iterrows()]

    print(f"▶ 숙소 처리 중: {name} (API 전송 리뷰 {len(reviews_for_prompt)}건)")
    
    # 최종 시스템 프롬프트 구성
    final_system_prompt = system_prompt_template.format(dynamic_instructions=dynamic_instructions_for_prompt)
    
    prompt_for_api = f"숙소명: {name}\n\n리뷰 목록:\n" + "\n".join(reviews_for_prompt)
    full_prompt_for_api = final_system_prompt + "\n\n" + prompt_for_api
    
    # 입력 길이 제한
    if len(full_prompt_for_api) > 15000 : 
        print(f"DEBUG: {name} → 입력 길이 초과 ({len(full_prompt_for_api)}자). 일부 자름.")
        full_prompt_for_api = full_prompt_for_api[:15000]

    # API 호출 및 재시도 로직
    for attempt in range(MAX_RETRIES):
    
        try :
            response = model.generate_content(
                full_prompt_for_api,
                generation_config=genai.types.GenerationConfig(temperature=0.7)
            )

            if not response.text or not response.text.strip():
                raise ValueError("모델 응답 텍스트가 비어 있거나 유효하지 않습니다.")

            text = re.sub(r"^```json\n|\n```$", "", response.text.strip(), flags=re.MULTILINE)
            parsed = json.loads(text)
            result_data = parsed["list"][0]

            # 결과 저장
            output_df = pd.DataFrame([result_data])
            output_df.to_csv(OUTPUT_CSV_PATH, mode="a", header=write_header, index=False, encoding="utf-8-sig")
            write_header = False

            print(f" 저장 완료 → {name} (시도 {attempt + 1}/{MAX_RETRIES})")
            break  # 성공 → 루프 탈출

        except (json.JSONDecodeError, ValueError) as e:
            print(f" JSON 파싱 오류 (시도 {attempt + 1}): {name} → {e}")
            
        except Exception as e:
            print(f" API 오류 (시도 {attempt + 1}): {name} → {e}")
            if "Quota" in str(e) or "PermissionDenied" in str(e) or "500" in str(e):
                if switch_api_key():
                    model = genai.GenerativeModel("gemini-2.5-flash")  # 키 바꾼 후 모델 새로 구성
                    continue  # 다시 시도
                else:
                    break  # 더 이상 키 없음 → 재시도 중단

        if attempt < MAX_RETRIES - 1:
            print(f"재시도 대기 중... ({RETRY_DELAY_SECONDS}초)")
            time.sleep(RETRY_DELAY_SECONDS)
        else:
            print(f" 모든 시도 실패 → {name} 은 처리되지 않음.")

    time.sleep(0.5) # 각 숙소 처리 후 짧은 대기 (과도한 API 요청 방지)