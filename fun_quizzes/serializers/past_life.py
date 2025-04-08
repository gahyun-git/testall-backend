from rest_framework import serializers

from ..models.category import Category
from ..models.past_life_test import PastLifeTest
from ..models.past_life_result import PastLifeResult
from .category import CategorySerializer

class PastLifeTestSerializer(serializers.ModelSerializer):
    """전생 테스트 시리얼라이저"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    
    class Meta:
        model = PastLifeTest
        fields = '__all__'
        read_only_fields = ['id', 'participant_count', 'share_count', 'created_at', 'updated_at']

class PastLifeResultSerializer(serializers.ModelSerializer):
    """전생 테스트 결과 시리얼라이저"""
    test = PastLifeTestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=PastLifeTest.objects.all(),
        source='test',
        write_only=True
    )
    
    class Meta:
        model = PastLifeResult
        fields = '__all__'
        read_only_fields = [
            'id', 'past_life_name', 'past_life_story', 'result_image',
            'ad_shown', 'ad_shown_at', 'created_at', 'updated_at'
        ]
