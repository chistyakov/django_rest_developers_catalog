from rest_framework.routers import DefaultRouter

from developers.views import DeveloperViewSet

router = DefaultRouter()
router.register(r'developers', DeveloperViewSet, base_name='developer')

urlpatterns = router.urls
