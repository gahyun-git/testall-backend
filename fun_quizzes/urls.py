from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet
from .views.past_life_viewsets import PastLifeTestViewSet, PastLifeResultViewSet
from .views.past_life_take_test_view import PastLifeTakeTestView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'past-life', PastLifeTestViewSet, basename='past-life')
router.register(r'past-life-results', PastLifeResultViewSet, basename='past-life-results')

urlpatterns = [
    # non-router endpoint 우선 배치
    # URL 패턴의 순서 때문에 non-router 엔드포인트가 뒤에 배치됨. 위에올려줘야 에러안남
    path('past-life/take_test/', PastLifeTakeTestView.as_view(), name='past-life-take-test'),
    # 그 이후에 라우터의 나머지 엔드포인트 포함
    path('', include(router.urls)),
]