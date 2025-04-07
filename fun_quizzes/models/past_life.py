from django.db import models
from .test_base import BaseTest

class PastLifeTest(BaseTest):
    """전생 테스트 모델"""
    prompt_template = models.TextField(
        blank=True, 
        verbose_name='AI 프롬프트 템플릿',
        help_text='생년월일, 시간 등의 변수는 {birth_date}, {birth_time} 형식으로 입력'
    )

    class Meta:
        verbose_name = '전생 테스트'
        verbose_name_plural = '전생 테스트 목록'

class PastLifeResult(models.Model):
    """전생 테스트 결과 모델"""
    test = models.ForeignKey(PastLifeTest, on_delete=models.CASCADE, verbose_name='테스트')
    
    # 사용자 입력 정보
    birth_date = models.DateField(verbose_name='생년월일')
    birth_time = models.TimeField(verbose_name='태어난 시간')
    
    # 전생 정보
    past_life_name = models.CharField(max_length=100, blank=True, verbose_name='전생 이름')
    past_life_story = models.TextField(blank=True, verbose_name='전생 이야기')
    result_image = models.ImageField(upload_to='past_life_results/', blank=True, verbose_name='결과 이미지')
    
    # AI 응답 저장
    story_response = models.JSONField(blank=True, null=True, verbose_name='이야기 AI 응답')
    image_response = models.JSONField(blank=True, null=True, verbose_name='이미지 AI 응답')
    
    # 광고 노출 관련
    ad_shown = models.BooleanField(default=False, verbose_name='광고 노출 여부')
    ad_shown_at = models.DateTimeField(null=True, blank=True, verbose_name='광고 노출 시간')
    
    # 시간 정보
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '전생 테스트 결과'
        verbose_name_plural = '전생 테스트 결과 목록'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.test.title} - {self.birth_date}"
