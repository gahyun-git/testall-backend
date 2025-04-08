import datetime
import json
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from fun_quizzes.models.category import Category
from fun_quizzes.models.past_life_test import PastLifeTest
from fun_quizzes.services import OpenAIService  # OpenAIService는 __init__.py에 정의되어 있음

class PastLifeTestViewSetTests(APITestCase):
    def setUp(self):
        # 먼저 category 객체를 생성합니다.
        self.category = Category.objects.create(
            name="Dummy Category",
            slug="dummy-category",
            description="테스트용 카테고리입니다.",
            icon="dummy_icon.jpg",  # 실제 파일 업로드가 필요하다면 File 객체로 처리하세요.
            order=1,
        )
        # 테스트용 전생 테스트 객체 생성 (category 필드를 전달)
        self.test_obj = PastLifeTest.objects.create(
            title="전생 테스트",
            description="당신의 전생을 알아봅니다.",
            slug="test",
            category=self.category
        )

        self.url = '/api/quizzes/past-life/take_test/'
    
    @patch('fun_quizzes.services.OpenAIService.generate_test_result')
    def test_take_test_success(self, mock_generate):
        # OpenAIService.generate_past_life가 반환할 dummy 결과 설정
        dummy_result = {
            "success": True,
            "name": "Test Soul",
            "story": "Once upon a time...",
            "image_url": "http://example.com/image.png",
            "raw_response": {
                "story": {"dummy": "story"},
                "image": {"dummy": "image"}
            },
            "result_id": 1  # 예시로 추가
        }
        mock_generate.return_value = dummy_result
        
        payload = {
            "birth_date": "2000-01-01",
            "birth_time": "12:00"
        }
        
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('result_id', response.data)

class OpenAIServiceTests(TestCase):
    @patch('fun_quizzes.services.openai.past_life_service.client')
    @patch('fun_quizzes.services.openai.image_service.client')
    def test_generate_past_life_success(self, mock_image_client, mock_past_client):
        # 전생 이야기 생성 dummy 응답 설정
        dummy_payload = {"name": "Test Soul", "story": "Once upon a time..."}
        dummy_story_response = MagicMock()
        dummy_story_response.choices = [
            MagicMock(message=MagicMock(content=json.dumps(dummy_payload)))
        ]
        mock_past_client.chat.completions.create.return_value = dummy_story_response
        
        # 이미지 생성 dummy 응답 설정
        dummy_image_response = MagicMock()
        dummy_image_response.data = [MagicMock(url="http://example.com/image.png")]
        mock_image_client.images.generate.return_value = dummy_image_response
        
        birth_date = datetime.date(2000, 1, 1)
        birth_time = datetime.time(12, 0)
        result = OpenAIService.generate_past_life(birth_date, birth_time)
        
        self.assertTrue(result.get('success'))
        self.assertEqual(result.get('name'), "Test Soul")
        self.assertEqual(result.get('story'), "Once upon a time...")
        self.assertEqual(result.get('image_url'), "http://example.com/image.png")
    
    @patch('fun_quizzes.services.openai.text_service.client')
    def test_generate_text_success(self, mock_text_client):
        # 일반 텍스트 생성 dummy 응답 설정
        dummy_text_response = MagicMock()
        dummy_text_response.choices = [
            MagicMock(message=MagicMock(content="Generated text"))
        ]
        mock_text_client.chat.completions.create.return_value = dummy_text_response
        
        result_text = OpenAIService.generate_text("Test prompt")
        self.assertEqual(result_text, "Generated text")