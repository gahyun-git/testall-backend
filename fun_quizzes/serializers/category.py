from rest_framework import serializers
from ..models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    카테고리 시리얼라이저
    
    카테고리 모델을 JSON으로 직렬화/역직렬화합니다.
    """
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']
