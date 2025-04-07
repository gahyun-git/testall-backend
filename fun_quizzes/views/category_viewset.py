from rest_framework import viewsets
from ..models.category import Category
from ..serializers.category import CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    테스트 카테고리 조회 ViewSet
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'  # ID 대신 slug로 조회
