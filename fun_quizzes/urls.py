from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PastLifeTestViewSet, PastLifeResultViewSet

# Router 설정
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'past-life', PastLifeTestViewSet)
router.register(r'results', PastLifeResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
