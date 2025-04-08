import json
import re
from datetime import datetime
from .client import client

def generate_story(birth_date, birth_time):
    birth_date_str = birth_date.strftime('%Y년 %m월 %d일')
    birth_time_str = birth_time.strftime('%H시 %M분')
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": (
                f"My birthdate is {birth_date_str} and I was born at {birth_time_str}.\n"
                "Imagine what kind of person I was in my past life. "
                "Please write a mystical and creative past life story in informal Korean (반말) under 600 characters.\n"
                "Respond in this **exact** JSON format:\n"
                "{\n  \"name\": \"past life name\",\n  \"story\": \"past life story content\"\n}"
            )
        }]
    )
    content = response.choices[0].message.content
    try:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
        else:
            raise ValueError("JSON 형식의 응답을 찾을 수 없습니다.")
    except Exception:
        # 간단 파싱 fallback
        result = {"name": "Unknown Soul", "story": content}
    return {"raw_story_response": response, "result": result}

def generate_past_life_story(birth_date, birth_time):
    """
    전생 스토리 생성을 위한 함수 (더미 구현)
    실제 API 호출과 로직은 이 함수를 확장하여 구현합니다.
    """
    # 예시 dummy 결과 반환
    return {"name": "Test Soul", "story": "Once upon a time..."}