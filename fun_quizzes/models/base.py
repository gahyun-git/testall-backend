from django.db import models

class TimeStampedModel(models.Model):
    """모든 모델에서 공통으로 사용될 생성/수정 시간 필드"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        abstract = True
