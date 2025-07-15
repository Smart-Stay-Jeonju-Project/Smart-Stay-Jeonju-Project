import os
import json
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import re
import time

# 환경변수 로드 및 모델 설정
load_dotenv()
API_KEY = os.getenv("API_KEY_AI").split(",")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# 입력 및 출력 경로
# input_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/y_duple_filtered_up.csv"
input_path = "C:/Users/MYCOM/Documents/GitHub/Smart-Stay-Jeonju-Project/PROJECT/data/processed/reviews/n_duple_filtered_up.csv"
output_dir = "data/processed/reviews/report"
os.makedirs(output_dir, exist_ok=True)

# 완료된 숙소 목록 = report 폴더의 파일 이름 기반
done_names = set()
for filename in os.listdir(output_dir):
    if filename.endswith(".csv"):
        name = filename.replace(".csv", "").replace("_", "/").strip()
        done_names.add(name)

# 리뷰 데이터 로드 및 정렬
df = pd.read_csv(input_path)
df["write_date"] = pd.to_datetime(df["write_date"], errors="coerce")
df = df.sort_values("write_date", ascending=False)

# 프롬프트 템플릿
system_prompt = """아래는 하나의 숙소에 대한 여러 리뷰입니다.

각 숙소에 대해 다음 조건에 맞춰 분석해 주세요:
1. content 컬럼의 모든 데이터들을 순회하며 숙소를 대표할 형용사 형태의 키워드 10개~30개를 선정하세요 (예: 깨끗한, 편리한).
2. 키워드는 긍정리뷰, 부정리뷰 두 곳에서 전부 추출하세요.
3. 리뷰 내용을 바탕으로 2~4문장 분량의 평가 문장을 작성하세요.
4. 긍정리뷰와 부정리뷰는 5:5 비율로 작성하세요.
5. 예시로 긍정이 300개 부정이 5개여도 5:5 비율로 맞추세요.
6. 부정리뷰가 평가내용에 포함될 경우 '아쉬운점은' 이라는 문구로 시작을 하고 반드시 개선 사항을 작성하세요.
7. 만약 긍정리뷰와 부정리뷰의 총합이 10개 이하일 때는 '리뷰양이 충분하지 않습니다.' 를 출력하고 키워드도 표시하지 않게 작성하세요.
8. 한 타입의 리뷰가 10개 이상이고 다른 타입의 리뷰가 존재하지 않거나 개수가 2개 이하일 경우에는 10개 이상의 타입의 리뷰로 평가 내용을 작성하세요.

출력 형식은 아래와 같습니다:
{
  "list": [
    {
      "name": "<숙소 이름>",
      "keywords": "형용사1,형용사2,...",
      "content": "평가 요약 문장"
    }
  ]
}
"""

# 숙소별 처리
for name, group in df.groupby("name"):
    if name.strip() in done_names:
        print(f" 이미 처리됨: {name}, 건너뜁니다.")
        continue

    group = group[group["type"].isin(["긍정", "부정"])]
    group = group.sort_values("write_date", ascending=False)

    pos_reviews = group[group["type"] == "긍정"].head(25)
    neg_reviews = group[group["type"] == "부정"].head(25)

    count = min(len(pos_reviews), len(neg_reviews))
    if count > 0:
        pos_final = pos_reviews.head(count)
        neg_final = neg_reviews.head(count)
    else:
        # 한쪽만 있거나 극단적 imbalance일 경우
        pos_final = pos_reviews.head(50) if len(pos_reviews) > len(neg_reviews) else pd.DataFrame()
        neg_final = neg_reviews.head(50) if len(neg_reviews) > len(pos_reviews) else pd.DataFrame()

    selected = pd.concat([pos_final, neg_final])
    selected = selected.sort_values("write_date", ascending=False)

    if len(selected) < 5:
        continue

    reviews = [f"{row['type']},{row['clean_reviews']}" for _, row in selected.iterrows()]
    prompt = f"숙소명: {name}\n\n리뷰 목록:\n" + "\n".join(reviews)
    full_prompt = system_prompt + "\n\n" + prompt

    if len(full_prompt) > 15000:
        print(f" {name} 입력 너무 김 → 일부 자름")
        full_prompt = full_prompt[:15000]

    print(f"▶ 숙소 처리 중: {name} ({len(reviews)}건)")

    try:
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.7)
        )

        if not response.text.strip():
            raise ValueError("응답이 비어 있음")

        clean_text = re.sub(r"^```json\n|\n```$", "", response.text.strip(), flags=re.MULTILINE)
        parsed = json.loads(clean_text)
        output_data = parsed["list"][0]

        safe_filename = name.replace('/', '_').replace(':', '_').strip() + ".csv"
        save_path = os.path.join(output_dir, safe_filename)
        pd.DataFrame([output_data]).to_csv(save_path, index=False, encoding="utf-8-sig")

        print(f" 저장 완료 → {save_path}")
        time.sleep(0.5)

    except Exception as e:
        print(f" 오류 발생: {name} → {e}")
        continue
