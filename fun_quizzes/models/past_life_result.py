from django.db import models
from .past_life_test import PastLifeTest

class PastLifeResult(models.Model):
    """전생 테스트 결과 모델"""
    test = models.ForeignKey(PastLifeTest, on_delete=models.CASCADE, verbose_name='테스트')
    birth_date = models.DateField(verbose_name='생년월일')
    birth_time = models.TimeField(verbose_name='태어난 시간')
    past_life_name = models.CharField(max_length=500, blank=True, verbose_name='전생 이름')
    past_life_story = models.TextField(blank=True, verbose_name='전생 이야기')
    result_image = models.CharField(max_length=600, blank=True, verbose_name='결과 이미지 URL')
    story_response = models.JSONField(blank=True, null=True, verbose_name='이야기 AI 응답')
    image_response = models.JSONField(blank=True, null=True, verbose_name='이미지 AI 응답')
    ad_shown = models.BooleanField(default=False, verbose_name='광고 노출 여부')
    ad_shown_at = models.DateTimeField(null=True, blank=True, verbose_name='광고 노출 시간')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        verbose_name = '전생 테스트 결과'
        verbose_name_plural = '전생 테스트 결과 목록'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.test.title} - {self.birth_date}"