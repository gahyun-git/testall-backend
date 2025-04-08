import json
import datetime
from unittest.mock import patch, MagicMock
from django.test import TestCase
from fun_quizzes.services.openai import OpenAIFacade

class OpenAIServiceTests(TestCase):
    @patch('fun_quizzes.services.openai.past_life_service.client')
    @patch('fun_quizzes.services.openai.image_service.client')
    def test_generate_past_life_success(self, mock_image_client, mock_chat_client):
        # 전생 스토리 생성용 dummy 응답
        dummy_story_payload = {"name": "Test Soul", "story": "Once upon a time..."}
        dummy_story_response = MagicMock()
        dummy_story_response.choices = [
            MagicMock(message=MagicMock(content=json.dumps(dummy_story_payload)))
        ]
        # past_life_service 내부에서 사용하는 client.chat.completions.create를 모의
        mock_chat_client.chat.completions.create.return_value = dummy_story_response

        # 이미지 생성 dummy 응답
        dummy_image_response = MagicMock()
        dummy_image_response.data = [MagicMock(url="http://example.com/image.png")]
        mock_image_client.images.generate.return_value = dummy_image_response

        # 테스트 입력
        birth_date = datetime.date(2000, 1, 1)
        birth_time = datetime.time(12, 0)
        result = OpenAIFacade.generate_past_life(birth_date, birth_time)

        # 결과 검증
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('name'), "Test Soul")
        self.assertEqual(result.get('story'), "Once upon a time...")
        self.assertEqual(result.get('image_url'), "http://example.com/image.png")
    
    @patch('fun_quizzes.services.openai.text_service.client')
    def test_generate_text_success(self, mock_text_client):
        dummy_text_response = MagicMock()
        dummy_text_response.choices = [MagicMock(message=MagicMock(content="Generated text"))]
        mock_text_client.chat.completions.create.return_value = dummy_text_response

        result_text = OpenAIFacade.generate_text("Test prompt")
        self.assertEqual(result_text, "Generated text")