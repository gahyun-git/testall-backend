from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.request import PastLifeTestRequestSerializer
from ..models.past_life_result import PastLifeResult
from ..models.past_life_test import PastLifeTest
from ..services.openai.openai_facade import OpenAIFacade
from ..models.category import Category

class PastLifeTakeTestView(APIView):
    """
    전생 테스트 진행 API – POST 요청으로 전생 테스트 결과 생성.
    """
    def post(self, request, *args, **kwargs):
        serializer = PastLifeTestRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        birth_date = data['birth_date']
        birth_time = data['birth_time']
        
        # OpenAIFacade에서 전생 테스트 결과 생성
        result_data = OpenAIFacade.generate_test_result('past_life', birth_date, birth_time)
        
        # 기본 카테고리 가져오기 또는 생성하기
        default_category, created = Category.objects.get_or_create(
            name="테스트 카테고리",
            defaults={
                'slug': 'test-category',
                'description': '테스트용 카테고리입니다.',
                'order': 1
            }
        )
        
        # 테스트 모델 인스턴스 가져오기 또는 없으면 생성하기
        default_test = PastLifeTest.objects.first()
        if not default_test:
            # 기본 테스트가 없으면 생성
            default_test = PastLifeTest.objects.create(
                category=default_category,  # 카테고리 필드 추가
                title="전생 테스트",
                slug="past-life-test",  # 필수 필드 추가
                description="당신의 전생을 알아보는 테스트입니다."
            )
        
        # past_life_name이 100자 이상이면 자르기
        past_life_name = result_data.get("name", "")
        if past_life_name and len(past_life_name) > 100:
            past_life_name = past_life_name[:97] + "..."
        
        test_result = PastLifeResult.objects.create(
            test=default_test,
            birth_date=birth_date,
            birth_time=birth_time,
            past_life_name=past_life_name,
            past_life_story=result_data.get("story"),
            result_image=result_data.get("image_url"),
            story_response=result_data.get("raw_response", {}).get("story"),
            image_response=result_data.get("raw_response", {}).get("image")
        )
        
        response_data = {
            "success": True,
            "result_id": test_result.id,
            **result_data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)