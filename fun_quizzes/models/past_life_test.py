from django.db import models
from .test_base import AbstractTest

class PastLifeTest(AbstractTest):
    """
    전생 테스트 모델
    """
    prompt_template = models.TextField(
        blank=True,
        verbose_name='AI 프롬프트 템플릿',
        help_text='생년월일, 시간 등의 변수는 {birth_date}, {birth_time} 형식으로 입력'
    )

    class Meta:
        verbose_name = '전생 테스트'
        verbose_name_plural = '전생 테스트 목록'