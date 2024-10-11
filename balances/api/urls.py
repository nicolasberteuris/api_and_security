from django.urls import path

from api.views.core_views import Notification_apiViewSet

urlpatterns = [
    # Otras rutas...
    path('notification_api/<int:pk>/mark_as_read/', Notification_apiViewSet.as_view({'post': 'mark_as_read'}), name='mark_as_read'),
]