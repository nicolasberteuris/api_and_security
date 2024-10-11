from rest_framework.routers import DefaultRouter

from usuarios.api.api import UserViewSet

router = DefaultRouter()

router.register('', UserViewSet, basename="users")

urlpatterns = router.urls