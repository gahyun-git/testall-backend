import json
import re
from pathlib import Path
import os
import openai
from datetime import datetime
from django.conf import settings

# OpenAI 클라이언트 초기화
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai

class OpenAIService:
    """
    OpenAI API를 사용하여 전생 이야기와 이미지를 생성하는 서비스
    """
    
    @staticmethod
    def generate_past_life(birth_date, birth_time):
        """
        생년월일과 태어난 시간을 기반으로 전생 이야기와 이미지를 함께 생성
        
        Args:
            birth_date: datetime.date 객체
            birth_time: datetime.time 객체
            
        Returns:
            dict: 전생 이름, 이야기, 이미지 URL을 포함한 딕셔너리
        """
        # 날짜와 시간 포맷팅
        birth_date_str = birth_date.strftime('%Y년 %m월 %d일')
        birth_time_str = birth_time.strftime('%H시 %M분')
        
        try:
            # 1. GPT로 이야기 생성
            story_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"My birthdate is {birth_date_str} and I was born at {birth_time_str}.\n"
                            "Based on this, imagine what kind of person I was in my past life. "
                            "Write a mystical and creative past life story for me using informal Korean (반말), and keep it under 600 characters.\n"
                            "Please respond in **exactly** this JSON format:\n"
                            "{\n  \"name\": \"past life name\",\n  \"story\": \"past life story content\"\n}"
                        )
                    }
                ]
            )
            
            # 응답에서 JSON 데이터 추출
            content = story_response.choices[0].message.content
            
            # JSON 추출 시도
            try:
                # JSON 형식 문자열 찾기
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                
                if json_match:
                    json_str = json_match.group(0)
                    result = json.loads(json_str)
                else:
                    # JSON을 찾지 못한 경우
                    raise ValueError("JSON 형식의 응답을 찾을 수 없습니다.")
                    
            except (json.JSONDecodeError, ValueError) as e:
                # 파싱 실패 시 직접 파싱 시도
                name_match = re.search(r'"name"\s*:\s*"([^"]+)"', content) or re.search(r'name\s*:\s*(.+?)[\n\r]', content)
                story_match = re.search(r'"story"\s*:\s*"([^"]+)"', content) or re.search(r'story\s*:\s*(.+)', content, re.DOTALL)
                
                name = name_match.group(1).strip() if name_match else "Unknown Soul"
                story = story_match.group(1).strip() if story_match else content
                
                result = {
                    "name": name,
                    "story": story
                }
            
            # 2. 이미지 생성
            image_prompt = (
                f"A doodle-style illustration based on this story: '{result.get('story', '')}' "
                f"The character's name is '{result.get('name', 'Unknown Soul')}'. "
                f"Use thick black outlines and flat pastel colors. "
                f"The illustration should be playful Korean hand-drawn style with simple lines and whimsical vibe."
            )
            
            image_response = client.images.generate(
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            
            image_url = image_response.data[0].url if image_response.data else None
            
            # 결과 반환
            return {
                "success": True,
                "raw_response": {
                    "story": story_response,
                    "image": image_response
                },
                "name": result.get("name", "Unknown Soul"),
                "story": result.get("story", "알 수 없는 전생이야기..."),
                "image_url": image_url
            }
            
        except Exception as e:
            # 에러 발생 시 기본값 반환
            return {
                "success": False,
                "error": str(e),
                "name": "Unknown Soul",
                "story": "일시적인 오류로 이야기를 생성할 수 없습니다. 다시 시도해주세요.",
                "image_url": None
            }
