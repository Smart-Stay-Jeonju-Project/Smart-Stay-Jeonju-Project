import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 환경 변수 불러오기
load_dotenv()
API_KEY_AI = os.getenv("API_KEY_AI").split(",")

INPUT_CSV_PATH = "n_cleaned_review_texts.csv"
OUTPUT_CSV_PATH = "n_ai_cleaned_reviews.csv"

current_api_index = 0

def create_client(api_key):
    return genai.Client(api_key=api_key.strip())

def batch_generate(sliced_df, start_idx):
    global current_api_index
    while current_api_index < len(API_KEY_AI):
        api_key = API_KEY_AI[current_api_index]
        try:
            client = create_client(api_key)

            user_input_parts = [
                types.Part.from_text(text=f"{start_idx + i}: {row.review.strip()}")
                for i, row in enumerate(sliced_df.itertuples())
                if isinstance(row.review, str) and row.review.strip()
            ]
            if not user_input_parts:
                return ["ERROR"] * len(sliced_df)

            contents = [
                types.Content(role="model", parts=[types.Part.from_text(text='{"list" : []}')]),
                types.Content(role="user", parts=user_input_parts),
            ]

            config = types.GenerateContentConfig(
                temperature=0.7,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
                response_mime_type="application/json",
                response_schema=genai.types.Schema(
                    type=genai.types.Type.OBJECT,
                    properties={
                        "list": genai.types.Schema(
                            type=genai.types.Type.ARRAY,
                            items=genai.types.Schema(
                                type=genai.types.Type.OBJECT,
                                properties={
                                    "idx": genai.types.Schema(type=genai.types.Type.STRING),
                                    "sentiment": genai.types.Schema(type=genai.types.Type.STRING),
                                    "cleaned_review_content": genai.types.Schema(type=genai.types.Type.STRING),
                                },
                            ),
                        )
                    },
                ),
                system_instruction=[
                    types.Part.from_text(text="""
1. 각 리뷰의 맞춤법과 띄어쓰기를 수정하세요.
2. 문장은 모두 문어체로 정제합니다.
3. 의미는 변경하지 않고 핵심 내용만 유지하세요.
4. 각 리뷰의 감정을 '긍정', '부정', '중립' 중 하나로 분류하세요.
5. 결과는 다음과 같은 Python dict 문자열 형식으로 반환하세요:
   {"idx": "1", "sentiment": "긍정", "cleaned_review_content": "정제된 문장"}
6. 모든 리뷰에 대해 이와 같은 형식의 JSON 객체들을 리스트로 반환하세요.
                    """)
                ]
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config,
            )
            output_text = response.text
            parsed = json.loads(output_text)

            cleaned_output = [""] * len(sliced_df)

            for item in parsed.get("list", []):
                try:
                    idx = int(item["idx"])
                    sentiment = item["sentiment"]
                    content = item["cleaned_review_content"]
                    relative_idx = idx - start_idx
                    cleaned_output[relative_idx] = f"{sentiment},{content}"
                except Exception as e:
                    continue

            return [r if r else "ERROR" for r in cleaned_output]

        except Exception as e:
            print(f"⚠️ 키 {api_key[:10]} 실패: {e}")
            current_api_index += 1
            print("🔁 다음 API 키로 전환합니다...\n")
            continue

    print("❌ 모든 API 키 실패. 중단.")
    return ["ERROR"] * len(sliced_df)

def run_batch_cleaning():
    df = pd.read_csv(INPUT_CSV_PATH, header=None, names=["review"])
    total = len(df)
    BATCH_SIZE = 50

    # ✅ 기존 결과 확인: 이어서 처리할 시작 인덱스 결정
    processed_count = 0
    last_saved_count = 0
    all_cleaned = []

    if os.path.exists(OUTPUT_CSV_PATH):
        try:
            existing_df = pd.read_csv(OUTPUT_CSV_PATH, header=None)
            all_cleaned = existing_df[0].tolist()
            processed_count = len(all_cleaned)
            print(f"📁 이전 정제 기록 발견 → {processed_count}개 리뷰 건너뜀")
        except Exception as e:
            print("⚠️ 기존 파일 읽기 실패. 새로 시작합니다:", e)

    for i in range(processed_count, total, BATCH_SIZE):
        sliced_df = df.iloc[i:i + BATCH_SIZE]
        print(f"▶ {i + 1} ~ {i + len(sliced_df)} 리뷰 정제 중...")

        cleaned = batch_generate(sliced_df, start_idx=i + 1)
        if not cleaned:
            print("⛔ 정제 실패 또는 응답 없음. 중단.")
            break

        all_cleaned.extend(cleaned)
        processed_count += len(cleaned)

        # ✅ 100개마다 저장현황 업데이트
        if processed_count - last_saved_count >= 100:
            with open(OUTPUT_CSV_PATH, "w", encoding="utf-8") as f:
                for review in all_cleaned:
                    f.write(f'"{review}"\n')
            last_saved_count = processed_count  # 저장 후 기준값 갱신
            print(f"저장 → {OUTPUT_CSV_PATH} (누적 : {processed_count}개)")

        time.sleep(1.0)

    # ✅ 최종 결과 저장
    with open(OUTPUT_CSV_PATH, "w", encoding="utf-8-sig") as f:
        for review in all_cleaned:
            f.write(f'"{review}"\n')

    print(f"\n✅ 전체 정제 완료 → {OUTPUT_CSV_PATH}")
    print(f"총 {len(all_cleaned)}개 리뷰 정제됨.")

if __name__ == "__main__":
    run_batch_cleaning()