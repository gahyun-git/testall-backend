from django.db import models
from .base import TimeStampModel
from .category import Category

class AbstractTest(TimeStampModel):
    """모든 테스트 유형의 기본이 되는 추상 모델"""
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='카테고리')
    title = models.CharField(max_length=100, verbose_name='테스트 제목')
    slug = models.SlugField(unique=True, verbose_name='URL용 이름')
    description = models.TextField(verbose_name='테스트 설명')
    thumbnail = models.ImageField(upload_to='test_thumbnails/', verbose_name='썸네일')
    
    # 통계 필드
    participant_count = models.PositiveIntegerField(default=0, verbose_name='참여자 수')
    share_count = models.PositiveIntegerField(default=0, verbose_name='공유 수')

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return self.title
