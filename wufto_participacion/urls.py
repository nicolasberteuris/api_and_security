"""
URL configuration for wufto_participacion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
from django.urls import path,include, re_path
from django.contrib.auth.views import LoginView,logout_then_login
from django.contrib.auth.decorators import login_required
#from dashboard.views import ver_balances_totales
from django.conf import settings
from django.conf.urls.static import static
#from usuarios.views_old import Login
from usuarios.views import Login, Logout
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Documentacion de API",
      default_version='v0.1',
      description="Documentacion publica de API de Ecommerce",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ecommerce@gamil.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('balances/',include(('balances.api.routers'))),
    path('usuario/',include(('usuarios.api.routers'))),
    path('login/', Login.as_view(), name = 'login'),
    path('logout/',Logout.as_view(), name = 'Logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('dashboard/',include(('dashboard.urls','dashboard'))),
    #path('',login_required(ver_balances_totales), name = 'dashboard'),
    #path('accounts/login/', Login.as_view(),{'template_name':'login.html'}, name = 'login'),
    #path ('logout/', logout_then_login, name = 'logout')
    re_path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]




