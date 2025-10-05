# scoring/urls.py
from rest_framework.routers import DefaultRouter
from .views import FinancingViewSet

router = DefaultRouter()
router.register(r'financings', FinancingViewSet)

urlpatterns = router.urls