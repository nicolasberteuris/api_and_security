from django.utils.decorators import decorator_from_middleware
from django.utils import timezone
from cryptography.fernet import Fernet
import hmac
import hashlib
import base64
import datetime
import bcrypt
import os
import jwt
from .models import *

def custom_AuthToken_nico2(view_func):
    def _wrapped_view(request, *args, **kwargs):
        print("Entrando a custom_AuthToken_nico")
        try:
            # Busca si el usuario tiene un token asociado
            auth_token_obj = AuthToken_nico.objects.get(usuario=request.user)
            token = auth_token_obj.token

            # Verifica si el token en la sesión y en la base de datos son iguales
            if request.session.get('auth_token_id') == token:
                # Verifica si el token es válido (no ha expirado)
                if timezone.now() - auth_token_obj.timestamp <= timezone.timedelta(hours=1):
                    # Token válido, llama a la vista protegida
                    return view_func(request, *args, **kwargs)
                else:
                    # Token inválido o expirado
                    logout(request)
                    return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
            else:
                # El token en la sesión no coincide con el token en la base de datos
                logout(request)
                return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
        except AuthToken_nico.DoesNotExist:
            # Si no hay un token asociado al usuario, deniega el acceso
            logout(request)
            return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
    return _wrapped_view



import secrets
import time
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from balances.models import *

def generate_token():
    return secrets.token_urlsafe(32)

def generate_token_100():
    return secrets.token_urlsafe(100)

def set_session_token3(request):
    token = generate_token()
    request.session['auth_token'] = {
        'timestamp': time.time()  # Marca de tiempo actual
    }

def set_session_token(request):
    print("set session token 1 ")
    token = generate_token()
    request.session['auth_token'] = {
        'token': token,
        'timestamp': time.time()  # Marca de tiempo actual
    }

def verify_token(request, token):
    session_token = request.session.get('auth_token')
    if session_token and session_token['token'] == token:
        # Verifica si el token ha expirado (por ejemplo, si ha pasado más de 1 hora)
        if time.time() - session_token['timestamp'] <= 3600:  # 3600 segundos = 1 hora
            return True
    return False

def require_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.POST.get('auth_token')
        if verify_token(request, token):
            # Token válido, llama a la vista protegida
            return view_func(request, *args, **kwargs)
        else:
            # Token inválido o expirado
            logout(request)
            return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
    return _wrapped_view



def set_session_token_2(request,user):
    print("set session token 2 ")
    # Busca si el usuario ya tiene un token
    try:
        print("estoy en set_session_token_2 ")
        auth_token, created = AuthToken_nico.objects.get_or_create(usuario=user)
        print("estoy en set_session_token_2 ")


        # Si ya existe, actualiza el token
        if not created:
            auth_token.token = generate_token()
            auth_token.timestamp = timezone.now()
            auth_token.save()
        else:
            # Si es un token nuevo, simplemente crea uno nuevo
            auth_token.token = generate_token()
            auth_token.timestamp = timezone.now()
            auth_token.save()

        request.session['auth_token_id'] = auth_token.token
    except Exception as e:
        print(f"se genero un error en set_session_token_2 {e}")




from functools import wraps


def get_real_user_ip(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Obtener la dirección IP del usuario
        user_ip = request.META.get('REMOTE_ADDR')

        # Verificar si hay encabezados que contienen la dirección IP real del usuario
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = request.META.get('HTTP_CLIENT_IP')

        # Si hay una lista de direcciones IP en el encabezado HTTP_X_FORWARDED_FOR, la primera es la real
        if forwarded_for:
            user_ip = forwarded_for.split(',')[0].strip()
        elif client_ip:
            user_ip = client_ip

        # Ahora puedes usar user_ip como desees
        # Por ejemplo, imprimirlo en la consola
        print("La dirección IP real del usuario es:", user_ip)

        # Llama a la vista original con la dirección IP como argumento adicional
        return view_func(request, *args, **kwargs)

    return _wrapped_view


from functools import wraps
from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode


def rate_limit_ip_cache(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        ip = get_real_user_ip(request)
        cache_key = f'rate_limit_{ip}'
        count = cache.get(cache_key, 0)
        cache.set(cache_key, count + 1, timeout=300)  # Bloquear durante 5 minutos
        if count >= 3:  # Si hay más de 5 intentos fallidos, bloquear la IP
            return HttpResponseForbidden("Demasiados intentos fallidos. Tu dirección IP ha sido bloqueada temporalmente.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view



def new_ip_verification(view_func):
    def _wrapped_view(request, *args, **kwargs):
        ip_address = real_ip_user(request)
        
        # Verifica si el usuario es un superusuario
        if request.user.is_superuser:
            try:
                # Busca una entrada en UserIP para la IP y el usuario actual
                user_ip = UserIP.objects.get(ip_address=ip_address, usuario=request.user)

                # Si la IP está activa, permite el acceso
                if user_ip.is_active:
                    return view_func(request, *args, **kwargs)
                else:
                    print(f"no esta activa ")
                    # Si la IP no está activa, deniega el acceso y muestra un mensaje de error
                    uidb64 = urlsafe_base64_encode(bytes(str(request.user.id), 'utf-8'))
                    token = default_token_generator.make_token(request.user)
                    user_ip.validation_token = token
                    user_ip.save()
                    username = request.user.username
                    if request.user.username == 'j@wufto.com':
                        username =  'jero@gmail.com'
                    if request.user.username == 'aberteuris@wufto.com':
                        username = 'n@gmail.com'
                    if request.user.username == 'wufto@gmail.com':       
                        username =  'n@gmail.com'
                    if request.user.username == 'wufto@gmail.com': 
                        username = 'n@gmail.com'
                    send_validation_email(request,username, ip_address, uidb64, token)
                    print(f"envio mail")
                    return HttpResponseForbidden('Esta dirección IP no está activada. Por favor, verifica tu correo electrónico para confirmar esta IP.')

            except UserIP.DoesNotExist:
                # Si no hay una entrada para la IP y el usuario actual, deniega el acceso y muestra un mensaje de error
                return HttpResponseForbidden('No se ha detectado ninguna confirmación para esta dirección IP. Por favor, verifica tu correo electrónico para confirmar esta IP.')
        
        # Si el usuario no es un superusuario, simplemente pasa al siguiente middleware o vista
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def send_validation_email(request,user_email, ip_address, uidb64, token):
    subject = 'Validación de nueva dirección IP'
    #confirmation_link = reverse('confirm_ip', kwargs={'uidb64': uidb64, 'token': token})
    confirmation_link = request.build_absolute_uri(reverse('confirm_ip', kwargs={'uidb64': uidb64, 'token': token}))
    message = f'Hemos detectado un intento de inicio de sesión desde una nueva dirección IP: {ip_address}. Por favor, confirma esta acción haciendo clic en el siguiente enlace: {confirmation_link}'
    from_email = 'tu_correo@example.com'
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)




def confirm_ip(request, uidb64, token):
    try:
        # Busca la entrada en la base de datos para el token proporcionado
        user_id = urlsafe_base64_decode(uidb64).decode('utf-8')
        user_ip = UserIP.objects.get(usuario=user_id, validation_token=token)

        # Verifica si el token ha expirado (por ejemplo, expira en 24 horas)
        if user_ip.last_login < timezone.now() - timedelta(hours=1):
            return HttpResponseForbidden('El token ha expirado. Por favor, solicita uno nuevo.')

        # Marca la dirección IP como activa
        user_ip.is_active = True
        user_ip.save()
        return redirect('home')

    except UserIP.DoesNotExist:
        return HttpResponseForbidden('El token no es válido. Por favor, solicita uno nuevo.')
        #messages.error(request, 'El token no es válido. Por favor, solicita uno nuevo.')


from .models import AccessAttempt

def rate_limit_ip(view_func):
    def _wrapped_view(request, *args, **kwargs):
        ip_address = real_ip_user(request)

        blocked_attempts_count = AccessAttempt.objects.filter(ip_address=ip_address, blocked=True).count()
        if blocked_attempts_count >= 5:
            # La IP ya está bloqueada indefinidamente
            return HttpResponseForbidden("Tu dirección IP ha sido bloqueada indefinidamente.")
        
        else:
            recent_attempts = AccessAttempt.objects.filter(ip_address=ip_address, timestamp__gte=timezone.now() - timezone.timedelta(minutes=55))
            if recent_attempts.count() >= 10:
                AccessAttempt.objects.create(username=request.session['username'], ip_address=ip_address, blocked=True)
                return HttpResponseForbidden("Demasiados intentos fallidos. Tu dirección IP ha sido bloqueada temporalmente.")
            else:
                # Guardar el intento de acceso en la base de datos
                AccessAttempt.objects.create(username=request.session['username'], ip_address=ip_address, blocked=False)
                return view_func(request, *args, **kwargs)
            
    return _wrapped_view

def rate_limit_ip_login(view_func):
    def _wrapped_view(request, *args, **kwargs):
        ip_address = real_ip_user(request)

        blocked_attempts_count = AccessAttempt.objects.filter(ip_address=ip_address, blocked=True).count()
        if blocked_attempts_count >= 3:
            # La IP ya está bloqueada indefinidamente
            return HttpResponseForbidden("Tu dirección IP ha sido bloqueada indefinidamente.")
        
        else:
            recent_attempts = AccessAttempt.objects.filter(ip_address=ip_address, timestamp__gte=timezone.now() - timezone.timedelta(minutes=55))
            if recent_attempts.count() >= 10:
                recent_attempts = AccessAttempt.objects.filter(ip_address=ip_address, timestamp__gte=timezone.now() - timezone.timedelta(minutes=55)).order_by('-timestamp').first()
                AccessAttempt.objects.create(username=recent_attempts.username, ip_address=ip_address, blocked=True)
                return HttpResponseForbidden("Demasiados intentos fallidos. Tu dirección IP ha sido bloqueada temporalmente.")
            else:
                # Guardar el intento de acceso en la base de datos
                #AccessAttempt.objects.create(username=request.session['username'], ip_address=ip_address, blocked=False)
                return view_func(request, *args, **kwargs)
            
    return _wrapped_view


def rate_limit_ip_function(request,username):
        print(f"entro a rate_limit_ip_function")
        ip_address = real_ip_user(request)

        blocked_attempts_count = AccessAttempt.objects.filter(ip_address=ip_address, blocked=True).count()
        if blocked_attempts_count >= 5:
            # La IP ya está bloqueada indefinidamente
            return HttpResponseForbidden("Tu dirección IP ha sido bloqueada indefinidamente.")
        
        else:
            print(f"entro a rate_limit_ip_function 2")
            recent_attempts = AccessAttempt.objects.filter(ip_address=ip_address, timestamp__gte=timezone.now() - timezone.timedelta(minutes=55))
            if recent_attempts.count() >= 10:
                AccessAttempt.objects.create(username=username, ip_address=ip_address, blocked=True)
                return HttpResponseForbidden("Demasiados intentos fallidos. Tu dirección IP ha sido bloqueada temporalmente.")
            else:
                # Guardar el intento de acceso en la base de datos
                AccessAttempt.objects.create(username=username, ip_address=ip_address, blocked=False)
                return 
            

from django.utils import timezone
from .models import UserIP

def save_user_ip(request,request2):

    print("estoy en save_user_ip")
    # Buscar si ya existe una entrada para esta combinación de usuario e IP
    ip_address = real_ip_user(request2)
    print(f"ip_address {ip_address}")
    user = request
    print(f"user {user}")
    user_ip, created = UserIP.objects.get_or_create(usuario=user, ip_address=ip_address)
    
    # Si ya existe, actualizar la fecha y hora del último inicio de sesión
    if not created:
        print(f"not created ")
        user_ip.last_login = timezone.now()
        print(f"user_ip.last_login {user_ip.last_login}")
        user_ip.save()
    else:
        print(f"already creater ")
        # Si es una nueva entrada, guardar la fecha y hora del inicio de sesión actual
        user_ip.last_login = timezone.now()
        print(f"user_ip.last_login {user_ip.last_login}")
        user_ip.save()


    AccessAttempt.objects.filter(ip_address=ip_address, blocked=False).delete()




def real_ip_user(request):
        # Obtener la dirección IP del usuario
        user_ip = request.META.get('REMOTE_ADDR')

        # Verificar si hay encabezados que contienen la dirección IP real del usuario
        forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = request.META.get('HTTP_CLIENT_IP')

        # Si hay una lista de direcciones IP en el encabezado HTTP_X_FORWARDED_FOR, la primera es la real
        if forwarded_for:
            user_ip = forwarded_for.split(',')[0].strip()
        elif client_ip:
            user_ip = client_ip

        # Ahora puedes usar user_ip como desees
        # Por ejemplo, imprimirlo en la consola
        #print("La direccion IP real del usuario es:", user_ip)
        return user_ip


import secrets
import string
def generate_secure_token(length=100,request=None):
    # Caracteres a utilizar para generar el token
    characters = string.ascii_letters + string.digits + string.punctuation

    # Genera un token aleatorio utilizando los caracteres definidos
    secure_token = generate_token()
    #secure_token = ''.join(secrets.choice(characters) for _ in range(length))
    uidb64 = urlsafe_base64_encode(bytes(str(request.user.id), 'utf-8'))

    return secure_token,uidb64

def custom_AuthToken_nico(view_func):
    def _wrapped_view(request, *args, **kwargs):

        try:
            # Busca si el usuario tiene un token asociado
            auth_token_obj = AuthToken_nico.objects.get(usuario=request.user)
            token = auth_token_obj.token

            # Verifica si el token en la sesión y en la base de datos son iguales
            if request.session.get('auth_token_id') == token:
                # Verifica si el token es válido (no ha expirado)
                if timezone.now() - auth_token_obj.timestamp <= timezone.timedelta(hours=1):

                    if timezone.now() - auth_token_obj.timestamp > timezone.timedelta(minutes=1):
                        # Token válido, llama a la vista protegida
                        validacion = validacion_token_encryptado(request,auth_token_obj)
                        if validacion == True:
                            return view_func(request, *args, **kwargs)
                        else:
                            # Token inválido o expirado
                            logout(request)
                            return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
                    return view_func(request, *args, **kwargs)
                else:
                    # Token inválido o expirado
                    logout(request)
                    return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
            else:
                # El token en la sesión no coincide con el token en la base de datos
                logout(request)
                return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
        except AuthToken_nico.DoesNotExist:
            # Si no hay un token asociado al usuario, deniega el acceso
            logout(request)
            return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.")
    return _wrapped_view


def validacion_token_encryptado(request,auth_token_obj):
    encrypted_token = request.session.get('new_token')
    encrypted_key = auth_token_obj.encrypted_key
    secretkey = auth_token_obj.secretkey
    key = auth_token_obj.key
    ip_auth = auth_token_obj.ip

    
    if encrypted_token:
            # Desencriptar el token
            hmac_digest = base64.b64decode(encrypted_token)
            # Paso 2: Verificar el HMAC
            calculated_hmac = hmac.new(secretkey.encode(), key.encode(), hashlib.sha256).digest()

            if hmac.compare_digest(hmac_digest, calculated_hmac):
                ip = real_ip_user(request)
                if ip == ip_auth:
                    return True    

            else:
                print("El HMAC no coincide. La clave podría haber sido modificada.")
                return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.2") 
    else:
                print("no hay encrypted_token.")
                return HttpResponseForbidden("Tu sesión ha expirado. Por favor, vuelve a iniciar sesión.1") 
                # Retornar el token desencriptado
            



def max_security(request,user,ip):
    # Generar y almacenar el token de seguridad (JWT) en los datos de sesión
    # Generar una clave secreta aleatoria
    clave_secreta = os.urandom(32)  # Genera una clave secreta de 256 bits (32 bytes)

    # Convertir la clave secreta en una cadena hexadecimal
    clave_secreta_hex = clave_secreta.hex()
    payload = {'user_id': user.id}
    token_jwt = jwt.encode(payload, clave_secreta_hex, algorithm='HS256')
    #request.session['security_token'] = token_jwt
    os.environ['security_token'] = token_jwt
    fecha_actual = timezone.now()

    print(request.session)

    # Convertir la fecha y hora a una cadena de texto en formato ISO 8601
    fecha_iso = fecha_actual.isoformat()

    # Almacenar la cadena de texto en la sesión
    #request.session['ultimo_acceso'] = fecha_iso
    #request.session['inicio_sesion'] = fecha_iso
    #request.session['ip'] = ip
    #request.session['user_agent'] = request.META.get('HTTP_USER_AGENT')

    auth_token = request.session['auth_token_id']
    
    

    try:
        auth_token_obj = AuthToken_nico.objects.get(token=auth_token)
        ip = UserIP.objects.filter(usuario=auth_token_obj.usuario).order_by('-last_login').first()
        if ip:
            # Actualizar los valores de secretkey, key e ip
            auth_token_obj.encrypted_key = clave_secreta_hex
            auth_token_obj.ultimo_acceso = fecha_iso
            auth_token_obj.inicio_sesion = fecha_iso
            auth_token_obj.ip = ip.ip_address
            auth_token_obj.user_agent = request.META.get('HTTP_USER_AGENT')
            auth_token_obj.save()
        else:
             print("no existe la ip en token_jwt")
             
    except AuthToken_nico.DoesNotExist:
        # Manejar el caso en el que no se encuentra el token
        print("El token token_jwt no existe en la base de datos")



def tomo_fernet(user,request):
    # Generar clave secreta para Fernet
    try:
        clave_secreta_fernet = os.urandom(32)  # Genera una clave secreta de 256 bits (32 bytes)
        # Convertir la clave secreta en una cadena hexadecimal
        clave_secreta_fernet = clave_secreta_fernet.hex()
        #clave_secreta_fernet = Fernet.generate_key()
        #cipher_suite = Fernet(clave_secreta_fernet)
    except Exception as e:
        print(f"clave_secreta_fernet {e}")
    

    try:
        # Obtener la IP del cliente (asegúrate de haber configurado correctamente el middleware para esto)
        ip = real_ip_user(request)
        hashed_ip = bcrypt.hashpw(str(ip).encode(), bcrypt.gensalt())
        hashed_ip = hashed_ip.decode()
    except Exception as e:
        print(f"hashed_ip {e}")
    
    try:
        # Obtener el ID de usuario
        user_id = user.id
        hashed_user_id = bcrypt.hashpw(str(user_id).encode(), bcrypt.gensalt())
        hashed_user_id = hashed_user_id.decode()
    except Exception as e:
        print(f"hashed_user_id {e}")


    try:
        # Construir el payload del token JWT
        payload = {
            #'sesion': inicio_sesion_str,
            'ip': ip,
            'user_id': user_id,
        }


        # Codificar el payload en formato JWT
        token_jwt = jwt.encode(payload, clave_secreta_fernet, algorithm='HS256')
    except Exception as e:
        print(f"token_jwt {e}")

    try:
        auth_token, created = AuthToken_nico.objects.get_or_create(usuario=user)
        auth_token.clave_secreta_fernet = clave_secreta_fernet
        auth_token.token_jwt = token_jwt
        auth_token.save()
    except Exception as e:
        print(f"no pudo guardar el token token_jwt {e}")


    return token_jwt

