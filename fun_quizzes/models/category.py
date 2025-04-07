from django.db import models
from .base import TimeStampedModel

class Category(TimeStampedModel):
    """테스트 카테고리 모델"""
    name = models.CharField(max_length=50, verbose_name='카테고리명')
    slug = models.SlugField(unique=True, verbose_name='URL용 이름')
    description = models.TextField(blank=True, verbose_name='설명')
    icon = models.ImageField(upload_to='category_icons/', verbose_name='아이콘')
    order = models.PositiveIntegerField(default=0, verbose_name='정렬 순서')

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리 목록'
        ordering = ['order']

    def __str__(self):
        return self.name
