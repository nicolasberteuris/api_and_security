from django.urls import path
#from usuarios.api.api import UsuarioAPIView
from usuarios.api.api import user_api_view, usuario_detail_view

"""
urlpatterns = [
    path('usuario/', UsuarioAPIView.as_view(), name='usuario_api')
]
"""
urlpatterns = [
    path('usuario/', user_api_view, name='usuario_api'),
    path('usuario/<int:pk>', usuario_detail_view, name='usuario_api_detail')
]