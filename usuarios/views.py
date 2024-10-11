from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from usuarios.api.serializers import (
    CustomTokenObtainPairSerializer, CustomUserSerializer
)
from usuarios.models import Usuario
from balances.security import *
from balances.firma_digital import firmaaaa
from balances.models import *



class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                try:
                    set_session_token(request)
                    print("paso session 1 ")
                    print(request)
                    print(user)
                    set_session_token_2(request,user)
                    print("paso session 2 ")
                    save_user_ip(user,request)
                    ip = real_ip_user(request)
                    print("paso buscar ip")
                    rate_limit, _ = RateLimit.objects.get_or_create(ip_address=ip)
                    rate_limit.reset_request_count()
                    print("paso rate_limit")
                    request.session.set_expiry(timedelta(hours=1))
                    max_security(request, user,ip)
                    print("paso max_security")
                    tomo_fernet(user,request)
                    print("paso tomo_fernet")
                    firmaaaa()
                    print("paso firmaaaa")
                except Exception as e:
                    print(f"estoy en login {e}")
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = Usuario.objects.filter(id=request.data.get('user', 0))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message': 'Sesión cerrada correctamente.'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario.'}, status=status.HTTP_400_BAD_REQUEST)






































"""


from datetime import datetime
from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.sessions.models import Session

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from usuarios.api.serializers import UserTokenSerializar
from usuarios.authentication_mixins import Authentication

class UserToken(Authentication,APIView):

    def get(self, request, *args, **kwargs):
        print("hola")
        print(self.user)
        try:
            user_token = Token.objects.get_or_create(user = self.user)
            user = UserTokenSerializar(self.user)
            return Response({
                'token': user_token.key,
                'user':user.data,
                
                })
        except:
            return Response({
                'error':'Credenciales enviadas incorrectas'
            }, status= status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request':request})
        print(login_serializer)
        if login_serializer.is_valid():
            user = login_serializer.validated_data['usuario']
            print("antes de user")
            print(user)
            if user.is_active:
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializar(user)
                if created:
                    return Response({
                        'token': token.key, 
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso'
                                     }, status= status.HTTP_201_CREATED)
                else:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()

                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key, 
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso'
                                     }, status= status.HTTP_201_CREATED)
                
                    
                    #cuando no queremos que permita el inicio de sesion cuando ya se encuentra iniciado
                    token.delete()
                    return Response({'error':'Ya se ha iniciado sesion con este usuario}, status = status.HTTP_409_CONFLICT)
                    

            else:
                return Response({'error': 'Este usuario no puede iniciar sesion'}, status= status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Nombre de usuario o contraseña incorrecto'}, status= status.HTTP_400_BAD_REQUEST) 
   
        #return Response({'message': 'Response'}, status= status.HTTP_200_OK)
    

class Logout(APIView):

    def post(self, request, *args, **kwargs):
        try:
            token = request.POST.get('token')
            token = Token.objects.filter(key = token).first()
        
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()

                token.delete()

                session_message = 'Sesiones de usuario eliminados'
                token_message = 'Token eliminado'
                return Response({'token_message': token_message, 'session_message': session_message}, status= status.HTTP_200_OK )
            
            return Response({'error': 'No se ha encontrado un usuario con estas credenciales'}, status= status.HTTP_401_UNAUTHORIZED)
        
        except:
            return Response({'error': 'No se ha encontrado token en la peticion'}, status= status.HTTP_409_CONFLICT)
        



"""

