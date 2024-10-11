from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from usuarios.models import Usuario
from usuarios.api.serializers import (
    UserSerializer, UserListSerializer, UpdateUserSerializer,
    PasswordSerializer
)

class UserViewSet(viewsets.GenericViewSet):
    model = Usuario
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects\
                            .filter(is_active=True)\
                            .values('id', 'username', 'email', 'nombre')
        return self.queryset

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Contraseña actualizada correctamente'
            })
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario registrado correctamente.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Hay errores en el registro',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)
    
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario actualizado correctamente'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la actualización',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'Usuario eliminado correctamente'
            })
        return Response({
            'message': 'No existe el usuario que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)






"""
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from usuarios.models import Usuario
from usuarios.api.serializers import UserSerializer, UserListSerializer

"""
"""
class UsuarioAPIView(APIView):

    def get(self,request):
        usuarios = Usuario.objects.all()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return Response(usuarios_serializer.data)
"""
"""



@api_view(['GET', 'POST'])
def user_api_view(request):

    if request.method == 'GET':
        #usuarios = Usuario.objects.all()
        
        #permite customizar las variables que se quieren ver en la view. Hay que agregar la funcion to_representation en serializers.py
        usuarios = Usuario.objects.all().values('email','password', 'username', 'nombre')
        usuarios_serializer = UserListSerializer(usuarios, many=True)

        return Response(usuarios_serializer.data, status = status.HTTP_200_OK)
    
    elif request.method == 'POST':
        usuario_serializer = UserSerializer(data = request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

"""
# test_validate por campos
"""
@api_view(['GET', 'POST'])
def user_api_view(request):

    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)

        test_data = {
            'nombre': 'losmillo',
            'email': 'losmillo@gmail.com'
        }

        test_user = TestUserSerializer(data = test_data, context = test_data)
        if test_user.is_valid():
            user_instance = test_user.save()
            print(user_instance)
        else:
            print(test_user.errors)

        return Response(usuarios_serializer.data, status = status.HTTP_200_OK)

    
    elif request.method == 'POST':
        usuario_serializer = UsuarioSerializer(data = request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data, status = status.HTTP_201_CREATED)
        
        return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """
"""

@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detail_view(request, pk = None):
    usuario = Usuario.objects.filter(id = pk).first()

    if usuario:

        if request.method == 'GET':    
            usuario_serializer = UserSerializer(usuario)
            return Response(usuario_serializer.data, status = status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            usuario_serializer = UserSerializer(usuario, data = request.data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                return Response(usuario_serializer.data, status = status.HTTP_200_OK)
            
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            usuario.delete()
            return Response({'message': 'Usuario eliminado correctamente'}, status = status.HTTP_200_OK)
        
    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


#test para update por campos

"""
"""
@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detail_view(request, pk = None):
    usuario = Usuario.objects.filter(id = pk).first()

    if usuario:

        if request.method == 'GET':    
            usuario_serializer = UsuarioSerializer(usuario)
            return Response(usuario_serializer.data, status = status.HTTP_200_OK)
        
        elif request.method == 'PUT':
            usuario_serializer = TestUserSerializer(usuario , data = request.data, context = request.data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                return Response(usuario_serializer.data, status = status.HTTP_200_OK)
            
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            usuario.delete()
            return Response({'message': 'Usuario eliminado correctamente'}, status = status.HTTP_200_OK)
        
    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status = status.HTTP_400_BAD_REQUEST)

"""
