from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MemoryViewSet, PatientViewSet, CaretakerViewSet

router = DefaultRouter()
router.register(r'memories', MemoryViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'caretakers', CaretakerViewSet)

urlpatterns = [
      path('', include(router.urls)),   # API endpoints will start with /api/
]
