from rest_framework.routers import DefaultRouter
from .views import NoticiaViewSet

router = DefaultRouter()
router.register(r'noticias', NoticiaViewSet)

urlpatterns = router.urls