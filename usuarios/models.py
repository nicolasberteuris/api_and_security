from cgi import MiniFieldStorage
from email.mime.image import MIMEImage
from enum import unique
import mimetypes
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import BooleanField, ImageField
from numpy import true_divide
from simple_history.models import HistoricalRecords

# Create your models here.

class UsuarioManager(BaseUserManager):
    def _create_user(self,username,nombre,direccion,email,password,is_staff,is_superuser,**extra_fields):
        user = self.model(
            username = username,
            nombre = nombre,
            direccion = direccion,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields 
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
        
    def create_user(self,username,nombre,direccion,email,password = None, **extra_fields):
        return self._create_user(username,nombre,direccion,email,password,False,False,**extra_fields)  

    def create_superuser(self,username,nombre,direccion,email, password = None, **extra_fields):
        return self._create_user(username,nombre,direccion,email,password,True,True,**extra_fields)
 

class Categoria_Usuario(models.Model):
    id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Categoria_Usuario'
        verbose_name = 'Categoria_Usuario'
        verbose_name_plural = 'Categoria_Usuarios'
        ordering = ['id']

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key= True)
    username = models.CharField('Username/Mail', unique=True, max_length=100)
    email = models.EmailField(unique=True, default=None, verbose_name='email')
    nombre = models.CharField(max_length = 200, blank = False, default=None, verbose_name='nombre')
    #tipo_usuario = models.ForeignKey(Categoria_Usuario, on_delete=models.CASCADE, related_name='tipo_usuario', default=1, null=True)
    direccion = models.CharField(max_length = 100, blank = True, default=None, verbose_name='direccion')
    is_active = models.BooleanField(default=True) #usuarios que inician sesión
    is_staff = models.BooleanField(default=False) #usuario en el administrador de django
    objects = UsuarioManager()
    """
        imagen = models.ImageField('Imgen de Perfil', upload_to='perfil/', height_field=None, width_field=None, max_length=200, blank= True, null = True)
    """

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre','direccion', 'email']

    class Meta:
        permissions = [('permiso_desde_codigo', 'Este es un permiso creado desde código'),
                        ('segundo_permiso_codigo', 'Este es un segundo permiso creado desde código')] 

    def __str__(self):
        return f'{self.nombre} {self.email}'
    
