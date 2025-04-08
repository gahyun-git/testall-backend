from .client import client
from .past_life_service import generate_past_life_story
from .image_service import generate_image
from .text_service import generate_text 

class OpenAIFacade:
    """
    다양한 심리 테스트(전생, 미래 등)의 AI 결과를 생성하는 Facade.
    각 테스트 타입(예: past_life 등)에 따라 핸들러를 호출.
    """
    handlers = {
        'past_life': generate_past_life_story,
        # 미래 테스트 등 추가 시 'future': generate_future, 등 등록
    }

    @classmethod
    def generate_test_result(cls, test_type, *args, **kwargs):
        if test_type not in cls.handlers:
            raise ValueError(f"지원하지 않는 테스트 유형입니다: {test_type}")
        result = cls.handlers[test_type](*args, **kwargs)
        image_data = generate_image(result.get("result", {}).get("story", ""), result.get("result", {}).get("name", "Unknown Soul"))
        
        # OpenAI 응답 객체에서 필요한 정보만 추출
        raw_image_data = {
            'url': image_data.get("image_url"),
            'created': str(image_data.get("raw_image_response").created) if hasattr(image_data.get("raw_image_response"), 'created') else None,
        }
        
        return {
            "success": True,
            "raw_response": {
                "test": result.get("raw_story_response"),
                "image": raw_image_data,  # 직렬화 가능한 딕셔너리
            },
            "name": result.get("result", {}).get("name", "Unknown Soul"),
            "story": result.get("result", {}).get("story", "알 수 없는 테스트 결과..."),
            "image_url": image_data.get("image_url")
        }

    @classmethod
    def generate_past_life(cls, birth_date, birth_time):
        story_result = generate_past_life_story(birth_date, birth_time)
        image_result = generate_image(story_result.get('story', ''), story_result.get('name', ''))
        return {
            "success": True,
            "name": story_result.get('name', ''),
            "story": story_result.get('story', ''),
            "image_url": image_result.get('image_url', '')
        }

    @classmethod
    def generate_text(cls, prompt, model="gpt-4o"):
        return generate_text(prompt, model)