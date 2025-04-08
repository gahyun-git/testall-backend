from django.db import models
from .base import TimeStampModel
from .test import Test  # Test 모델이 있다면 사용, 아니면 AbstractTest를 참조
from .ad_mixin import AdMixin

class TestResult(TimeStampModel, AdMixin):
    """
    모든 테스트 결과의 공통 모델.
    테스트 종류에 따라 추가 데이터는 extra_data에 JSON 형식으로 저장.
    """
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="테스트")
    birth_date = models.DateField(verbose_name="생년월일")
    birth_time = models.TimeField(verbose_name="태어난 시간")
    result_image = models.ImageField(upload_to="test/result", blank=True, verbose_name="결과 이미지")
    extra_data = models.JSONField(blank=True, null=True, verbose_name="테스트별 추가 정보")
    story_response = models.JSONField(blank=True, null=True, verbose_name="이야기 AI 응답 데이터")
    image_response = models.JSONField(blank=True, null=True, verbose_name="이미지 AI 응답 데이터")

    class Meta:
        verbose_name = "테스트 결과"
        verbose_name_plural = "테스트 결과 목록"

    def __str__(self):
        return f"{self.test.title} - {self.birth_date} {self.birth_time}"