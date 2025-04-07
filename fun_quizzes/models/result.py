from django.db import models

from TestAll.backend.fun_quizzes.models.test import Test
from .base import TimeStampModel

class TestResult(TimeStampModel):
    """
    테스트 결과 저장모델
    """
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="테스트")

    # 생년월일
    birth_date = models.DateField(verbose_name="생년월일")
    # 태어난 시간
    birth_time = models.TimeField(verbose_name="태어난 시간")

    past_life_name = models.CharField(
        max_length=100,
        verbose_name="전생 이름"
    )

    past_life_story = models.TextField(
        blank=True,
        verbose_name="전생 이야기"
    )

    past_life_image = models.ImageField(
        upload_to="test/result",
        blank=True,
        verbose_name="전생 이미지"
    )

    # AI 응답 저장
    story_response = models.JSONField(
        blank=True,
        null=True,
        verbose_name="이야기 AI 응답 데이터"
    )

    image_response = models.JSONField(
        blank=True,
        null=True,
        verbose_name="이미지 AI 응답 데이터"
    )
    

    # 광고 노출 관련
    ad_shown = models.BooleanField(default=False, verbose_name="광고 노출 여부")
    ad_shown_at = models.DateTimeField(null=True, verbose_name="광고 노출 시간")

    class Meta:
        verbose_name = "테스트 결과"
        verbose_name_plural = "테스트 결과 목록"

    def __str__(self):
        return f"{self.test.title} - {self.birth_date} {self.birth_time}"