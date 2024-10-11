
from pipes import Template
from django.urls import path
from django.urls import reverse_lazy
from usuarios.views_old import EditarCategoria_Usuario, EliminarCategoria_Usuario, ListadoCategoria_Usuario, ListadoUsuario, ModalRegistrarCategoria_Usuario, ModalRegistrarUsuario2, RegistrarUsuario,ModalRegistrarUsuario, EditarUsuario, EliminarUsuario, CambiarPassword
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from usuarios.views_old import InicioUsuarios



#app_name = 'accounts'

urlpatterns = [
    path('inicio_usuarios/', InicioUsuarios.as_view(), name='inicio_usuarios'),
    path('listar_usuarios/', login_required(ListadoUsuario.as_view()), name='listar_usuarios'),
    path('editar_usuarios/<int:pk>', login_required(EditarUsuario.as_view()), name='editar_usuarios'),
    path('eliminar_usuarios/<int:pk>', login_required(EliminarUsuario.as_view()), name='eliminar_usuarios'),
    path('registrar_usuarios/', ModalRegistrarUsuario2.as_view(), name='registrar_usuarios'),
    path('registrar__usuarios/', login_required(ModalRegistrarUsuario.as_view()), name='registrar__usuarios'),
    path('cambiar_password/', login_required(CambiarPassword.as_view()), name='cambiar_password'),

    path('listar_categoria_usuarios/', login_required(ListadoCategoria_Usuario.as_view()), name='listar_categoria_usuarios'),
    path('editar_categoria_usuarios/<int:pk>', login_required(EditarCategoria_Usuario.as_view()), name='editar_categoria_usuarios'),
    path('eliminar_categoria_usuarios/<int:pk>', login_required(EliminarCategoria_Usuario.as_view()), name='eliminar_categoria_usuarios'),
    path('crear__categoria_usuarios/', login_required(ModalRegistrarCategoria_Usuario.as_view()), name='crear__categoria_usuarios'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

"""
urlpatterns = [

    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/reset_password.html',
            success_url=reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'
    ),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_sent.html'), name='password_reset_done'),
    path(
        'password_reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/reset_password_form.html',
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_sucess.html'), name='password_reset_complete'),
]
"""

