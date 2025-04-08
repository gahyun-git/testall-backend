import tempfile
import requests
from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.files import File

from ..models.result import TestResult
from ..serializers.past_life import PastLifeTestSerializer, PastLifeResultSerializer
from ..services.openai.openai_facade import OpenAIFacade

class PastLifeTestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    전생 테스트 조회 ViewSet (POST요청은 별도 API 뷰로 처리)
    """
    queryset = TestResult.objects.all()
    serializer_class = PastLifeTestSerializer
    lookup_field = 'slug'
    
class PastLifeResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    전생 테스트 결과 ViewSet
    """
    queryset = TestResult.objects.all()  # 실제 결과 모델에 맞게 수정
    serializer_class = PastLifeResultSerializer
    
    @action(detail=True, methods=['post'])
    def confirm_ad(self, request, pk=None):
        result = self.get_object()
        if request.data.get('ad_shown'):
            request.session['ad_shown'] = True
        return Response({
            'past_life_name': result.extra_data.get('name', ''),
            'past_life_story': result.extra_data.get('story', ''),
            'result_image': request.build_absolute_uri(result.result_image.url) if result.result_image else None,
            'created_at': result.created_at
        })

    @action(detail=True, methods=['get'])
    def view_result(self, request, pk=None):
        if not request.session.get('ad_shown'):
            return Response({'message': '결과를 보기 전에 광고를 시청해야 합니다.'}, status=status.HTTP_403_FORBIDDEN)
        result = self.get_object()
        return Response({
            'past_life_name': result.extra_data.get('name', ''),
            'past_life_story': result.extra_data.get('story', ''),
            'result_image': request.build_absolute_uri(result.result_image.url) if result.result_image else None,
            'created_at': result.created_at
        })
