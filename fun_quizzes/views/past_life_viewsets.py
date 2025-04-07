import tempfile
import requests
from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files import File

from ..models.past_life import PastLifeTest, PastLifeResult
from ..serializers.past_life import PastLifeTestSerializer, PastLifeResultSerializer
from ..serializers.request import PastLifeTestRequestSerializer
from ..services.openai_service import OpenAIService



class PastLifeTestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    전생 테스트 조회 ViewSet
    """
    queryset = PastLifeTest.objects.all()
    serializer_class = PastLifeTestSerializer
    # slug 필드를 사용하는 이유는 사용자 친화적 URL과 SEO를 위해씀
    # 예시: https://testall.com/past-life/123
    # 예시: https://testall.com/past-life/test
    lookup_field = 'slug'  # ID 대신 slug로 조회
    
    @action(detail=False, methods=['post'])
    def take_test(self, request, slug=None):
        """
        테스트 참여 API
        생년월일과 시간을 받아 전생 정보를 생성
        """
        # 테스트 객체 가져오기 (첫 번째 또는 기본 테스트 사용)
        try:
            test = PastLifeTest.objects.first()
            if not test:
                # 테스트 객체가 없으면 새로 생성
                test = PastLifeTest.objects.create(
                    title="전생 테스트",
                    description="당신의 전생을 알아보세요",
                    slug="test"
                )
        except Exception as e:
            return Response({
                'error': f"테스트 객체를 찾을 수 없습니다: {str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # 요청 데이터 검증
        serializer = PastLifeTestRequestSerializer(data={
            'test_id': test.id,
            **request.data
            # 딕셔너리 언패킹( **을 쓰면 이렇게 됨):
            # {
            #     'test_id': test.id,
            #     'birth_date': '2000-01-01',
            #     'birth_time': '12:00'
            # }
        })
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 데이터 가져오기
        validated_data = serializer.validated_data
        birth_date = validated_data['birth_date']
        birth_time = validated_data['birth_time']
        
        # 세션 초기화: 새로운 테스트 시작 시 광고 시청 여부 초기화
        request.session['ad_shown'] = False

        try:
            # OpenAI 서비스를 통해 전생 정보 생성
            result_data = OpenAIService.generate_past_life(birth_date, birth_time)
            
            # 테스트 결과 생성
            result = PastLifeResult(
                test=test,
                birth_date=birth_date,
                birth_time=birth_time,
                past_life_name=result_data['name'],
                past_life_story=result_data['story'],
                story_response=result_data.get('raw_response', {}).get('story'),
                image_response=result_data.get('raw_response', {}).get('image')
            )
            
            # 이미지 URL이 있으면 이미지 다운로드 및 저장
            if result_data.get('image_url'):
                img_temp = tempfile.NamedTemporaryFile(delete=True)
                img_temp.write(requests.get(result_data['image_url']).content)
                img_temp.flush()
                
                # 파일명 설정
                filename = f"past_life_{test.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.png"
                result.result_image.save(filename, File(img_temp))
            
            # 결과 저장
            result.save()
            
            # 참여자 수 증가
            test.participant_count += 1
            test.save()
            
            return Response({
                'result_id': result.id,
                'message': '테스트 결과가 생성되었습니다. 결과를 확인하려면 광고를 시청해주세요.',
                'has_image': bool(result.result_image)
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PastLifeResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    전생 테스트 결과 ViewSet
    """
    queryset = PastLifeResult.objects.all()
    serializer_class = PastLifeResultSerializer
    
    @action(detail=True, methods=['post'])
    def confirm_ad(self, request, pk=None):
        """
        광고 시청 확인 및 결과 조회 API
        """
        # 테스트 결과 객체 가져오기
        result = self.get_object()
        
        # 광고 시청 여부를 세션에 저장
        if request.data.get('ad_shown'):
            request.session['ad_shown'] = True
        
        # 결과 반환
        return Response({
            'past_life_name': result.past_life_name,
            'past_life_story': result.past_life_story,
            'result_image': request.build_absolute_uri(result.result_image.url) if result.result_image else None,
            'created_at': result.created_at
        })

    @action(detail=True, methods=['get'])
    def view_result(self, request, pk=None):
        """
        결과 조회 API
        """
        # 광고 시청 여부 확인
        if not request.session.get('ad_shown'):
            return Response({'message': '결과를 보기 전에 광고를 시청해야 합니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 테스트 결과 객체 가져오기
        result = self.get_object()

        # 결과 반환
        return Response({
            'past_life_name': result.past_life_name,
            'past_life_story': result.past_life_story,
            'result_image': request.build_absolute_uri(result.result_image.url) if result.result_image else None,
            'created_at': result.created_at
        })
