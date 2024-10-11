from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseRedirect
from .models import RateLimit
from django.utils import timezone
from balances.security import real_ip_user
from datetime import timedelta
from .models import UserIP
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect
import re
from django.utils.html import escape
from django.middleware.csrf import CsrfViewMiddleware
from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from django.http import HttpResponseBadRequest
from django.urls import resolve
from markupsafe import Markup
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
import jwt
from .models import AuthToken_nico
from cryptography.fernet import Fernet
import bcrypt
from django.shortcuts import redirect
from balances.firma_digital import buscar_y_verificar_firma
import os

MAX_REQUESTS_PER_MINUTE = 1
RESET_INTERVAL = 86400


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = real_ip_user(request)
        print("adentro de rate limit")

        """
        '/wufto_dashboard/media/logo_black.svg','/wufto_dashboard/wufto_dashboard/media/logo_black.svg',
                         'https://www.wufto.com/wufto_dashboard/media/logo_black.svg','https://www.wufto.com/wufto_dashboard/wufto_dashboard/media/logo_black.svg',
                         'https://www.wufto.com/home/ubuntu/wufto_dashboard/media','https://www.wufto.com/media/logo_black.svg','/media/logo_black.svg'
        """
        # Verificar si la solicitud está en una URL excluida
        excluded_urls = ['/login/','api/token/refresh/','api/token/','logout/','swagger<format>/','swagger/','balances/',"","/"]
        
        #excluded_pattern = re.compile(r'^/edit_user/\d+/$')
        excluded_patterns = [
            re.compile(r'^/confirm-ip/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/ClaveViewSet/'),
            re.compile(r'^/api/ClaveViewSet'),
            re.compile(r'^/api/ClaveViewSet/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/refresh/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/login/'),
            re.compile(r'^/api/login'),
        ]

        print(request.path_info)
        if any(pattern.match(request.path_info) for pattern in excluded_patterns) or request.path_info in excluded_urls:
        #if request.path_info in excluded_urls or excluded_pattern.match(request.path_info):
            # Si la URL está excluida, no aplicar el límite de velocidad
            return self.get_response(request)
        
        if request.path_info.startswith('/balances/'):
            return self.get_response(request)
        
        # Incrementa el conteo de solicitudes
        rate_limit, created = RateLimit.objects.get_or_create(ip_address=ip)

        rate_limit.request_count += 1
        rate_limit.save()

        if rate_limit.request_count >= MAX_REQUESTS_PER_MINUTE:
            print("Demasiadas solicitudes. Por favor, inténtalo de nuevo más tarde.")
            return HttpResponseForbidden("Demasiadas solicitudes. Por favor, inténtalo de nuevo más tarde.")
        
        print("termino el middlware RateLimitMiddleware ")
        
        return self.get_response(request)


        """

        try:
            user_ip = UserIP.objects.filter(ip_address=ip).order_by('-last_login').first()
            if user_ip:
                pass
            else:
                rate_limit, created = RateLimit.objects.get_or_create(ip_address=ip)

                rate_limit.request_count += 1
                rate_limit.save()
                if rate_limit.request_count >= MAX_REQUESTS_PER_MINUTE:
                    return HttpResponseForbidden("Demasiadas solicitudes. Por favor, inténtalo de nuevo más tarde.")
                
                # Reiniciar el contador después de un cierto período de tiempo
                if timezone.now() > rate_limit.last_reset + timedelta(seconds=RESET_INTERVAL):
                        rate_limit.reset_request_count()

        except ObjectDoesNotExist:
            rate_limit, created = RateLimit.objects.get_or_create(ip_address=ip)

            rate_limit.request_count += 1
            rate_limit.save()

            if rate_limit.request_count >= MAX_REQUESTS_PER_MINUTE:
                return HttpResponseForbidden("Demasiadas solicitudes. Por favor, inténtalo de nuevo más tarde.")
            
            # Reiniciar el contador después de un cierto período de tiempo
            if timezone.now() > rate_limit.last_reset + timedelta(seconds=RESET_INTERVAL):
                    rate_limit.reset_request_count()

        return self.get_response(request)  
        """ 
    


class AllowOnlyURLsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redirect_url = 'http:///'

    def __call__(self, request):
        print("paso por el middleware AllowOnlyURLsMiddleware ")
        # Lista de URLs permitidas
        allowed_urls = ['/login/','api/token/refresh/','api/token/','logout/','swagger<format>/','swagger/','balances/',"","/"]
        

        # Verificar si la URL solicitada está permitida
        if not any(request.path_info.startswith(url) for url in allowed_urls):
            print("No tienes permiso para acceder a esta URL.")
            return HttpResponseRedirect(self.redirect_url)

        # Redirigir a la ruta madre si el host es app.wufto.com
        
        if request.path_info.startswith('/balances/'):
            return self.get_response(request)

        # Continuar con la solicitud si la URL está permitida y no es app.wufto.com

        print("termino el middlware AllowOnlyURLsMiddleware ")
        return self.get_response(request)
    




class XSSProtectionMiddleware(MiddlewareMixin):
    pass

    """


    def process_template_response(self, request, response):
        
        if not request.path.startswith('/balances/') and not request.path.startswith('/api/token/'):
                response.render()

                # Escapar el contenido de la respuesta como Markup seguro
                response.context_data['contenido_seguro'] = Markup(response.content.decode(response.charset))

        print("termino el middlware XSSProtectionMiddleware ")
        return response
        """
    

class CSRFProtectionMiddleware(CsrfViewMiddleware):
    def process_request(self, request):
        # Llama al método process_request del middleware CSRFViewMiddleware
        super().process_request(request)

        # Si el método de solicitud no es seguro, no se requiere protección CSRF
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            # Si el token CSRF no está presente en la solicitud, lo agrega a la respuesta
            if not request.META.get('CSRF_COOKIE'):
                get_token(request)

        print("termino el middlware CSRFProtectionMiddleware ")



class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Agrega encabezados de seguridad a la respuesta
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        #response['Content-Security-Policy'] = "default-src 'self'"

        print("termino el middlware SecurityHeadersMiddleware ")

        return response
    


class SQLInjectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener la ruta de la URL actual
        resolved_url = resolve(request.path)
        view_name = resolved_url.view_name
        print(f"view_name {view_name}")

        # Lista de vistas a excluir de la verificación de inyección SQL
        excluded_views = ['add-email-template']

        # Verificar si la solicitud está dirigida a una vista específica excluida
        if view_name in excluded_views:
            # Pasar la solicitud al siguiente middleware o al controlador de vista
            return self.get_response(request)

        # Verificar los parámetros GET y POST en busca de posibles inyecciones SQL
        unsafe_params = request.GET.dict() if request.method == 'GET' else request.POST.dict()
        for key, value in unsafe_params.items():
            if ';' in value:
                # Si encuentra un punto y coma en el valor de cualquier parámetro,
                # responde con un error 400 (Bad Request)
                return HttpResponseBadRequest("Posible intento de inyección de SQL detectado.")
        
        # Pasar la solicitud al siguiente middleware o al controlador de vista
        response = self.get_response(request)

        print("termino el middlware SQLInjectionMiddleware ")
        return response
    


    
class CSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Agregar la directiva CSP a las cabeceras de la respuesta
        response['Content-Security-Policy'] = (
            "default-src 'none'; "
            "script-src 'self' https://ajax.googleapis.com https://apis.google.com https://code.highcharts.com https://cdn.datatables.net https://kit.fontawesome.com https://cdn.amcharts.com https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline' https://maxcdn.bootstrapcdn.com https://cdn.datatables.net https://kit-free.fontawesome.com https://fonts.googleapis.com https://code.jquery.com https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' https://example.com https://cdn.datatables.net data:; "  # Agregar cdn.datatables.net aquí
            "font-src 'self' https://maxcdn.bootstrapcdn.com https://fonts.gstatic.com; "  
            "connect-src 'self'; "
            "frame-src 'self' https://www.tradingview.com https://www.youtube.com; "
            "media-src 'self'; "
            "object-src 'none'; "
            "form-action 'self';" 
        )
        
        print("termino el middlware CSPMiddleware ")
        return response
    



class VerificacionDeSesionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("middleware VerificacionDeSesionMiddleware")
        # Verificar si la solicitud es para la vista de inicio de sesión
        if request.path in [reverse('login'),"","/"]:
            # Si la solicitud es para la vista de inicio de sesión, permitir el acceso sin verificación
            response = self.get_response(request)
            return response
        
        expresiones_regulares = [
            re.compile(r'^/confirm-ip/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/ClaveViewSet/'),
            re.compile(r'^/api/ClaveViewSet'),
            re.compile(r'^/api/ClaveViewSet/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/refresh/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/login/'),
            re.compile(r'^/api/login'),
        ]

        # Verificar si la ruta solicitada coincide con alguna de las expresiones regulares
        if any(expresion.match(request.path) for expresion in expresiones_regulares):
            response = self.get_response(request)
            return response
        
        # Realizar verificaciones de sesión para todas las demás solicitudes
        #if not request.user.is_authenticated:
        #    print('No estás autenticado para acceder a esta página.')
        #    return redirect('login')

        # Verificar el rol del usuario
        
        # Verificar si el ID de sesión actual coincide con el ID de sesión almacenado en la sesión
        #if request.session.session_key != request.session.get('session_id'):
        #    return HttpResponseForbidden('ID de sesión no válido. La sesión puede haber sido comprometida.')
        
        # Verificar si ha pasado mucho tiempo desde el inicio de sesión
        tiempo_maximo_inactividad = 1000  # 1 hora en segundos
        #ultimo_acceso = datetime.fromisoformat(request.session['ultimo_acceso'])
        #inicio_sesion = datetime.fromisoformat(request.session['inicio_sesion'])
        try:
            ultimo_acceso = AuthToken_nico.objects.get(usuario=1).ultimo_acceso  
            inicio_sesion = AuthToken_nico.objects.get(usuario=1).inicio_sesion 
            ip = AuthToken_nico.objects.get(usuario=1).ip 
            user_agent = AuthToken_nico.objects.get(usuario=1).user_agent 
            print(f"user_agent {user_agent}")
        except Exception as e:
            print(f"clave_secreta_fernet {e}")

        # Calcular el tiempo transcurrido en segundos
        tiempo_transcurrido = (ultimo_acceso - inicio_sesion).total_seconds()
        if tiempo_transcurrido > tiempo_maximo_inactividad:
            # El usuario ha estado inactivo durante demasiado tiempo, cerrar la sesión
            del request.session['usuario_autenticado']
            print('La sesión ha expirado debido a inactividad.')
            return redirect('login')

        # Verificar si la dirección IP actual coincide con la dirección IP almacenada en la sesión
        if request.META.get('REMOTE_ADDR') != ip:
            print('Dirección IP no válida. La sesión puede haber sido comprometida.')
            return redirect('login')

        # Verificar si el agente de usuario actual coincide con el agente de usuario almacenado en la sesión
        if request.META.get('HTTP_USER_AGENT') != user_agent:
            print('Agente de usuario no válido. La sesión puede haber sido comprometida.')
            return redirect('login')
        

        #token = request.session.get('security_token')
        token = os.environ.get('security_token')
        #print(token)
        if not token:
            print('Token de seguridad faltante. La sesión puede haber sido comprometida.')
            return redirect('login')
        
        # Recuperar la clave secreta desde el modelo en la base de datos
        try:
            clave_secreta_usuario = AuthToken_nico.objects.get(usuario=1).encrypted_key  # Suponiendo que solo hay una clave secreta en la base de datos
        except clave_secreta_usuario.DoesNotExist:
            print('La clave secreta no está configurada. La sesión puede haber sido comprometida.')
            return redirect('login')
        
        

        try:
            payload = jwt.decode(token, clave_secreta_usuario, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print('Token de seguridad expirado. La sesión puede haber sido comprometida.')
            return redirect('login')
        except jwt.InvalidTokenError:
            print('Token de seguridad inválido. La sesión puede haber sido comprometida.')
            return redirect('login')
            
        
        # Realizar el resto de las verificaciones de sesión aquí...


        response = self.get_response(request)
        print("termino el middlware VerificacionDeSesionMiddleware ")
        return response
    


class VerificacionDeTomoFernet:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si la solicitud es para la vista de inicio de sesión
        if request.path in [reverse('login'),"","/"]:
            # Si la solicitud es para la vista de inicio de sesión, permitir el acceso sin verificación
            response = self.get_response(request)
            return response
        
        expresiones_regulares = [
            re.compile(r'^/confirm-ip/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/ClaveViewSet/'),
            re.compile(r'^/api/ClaveViewSet'),
            re.compile(r'^/api/ClaveViewSet/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/refresh/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/login/'),
            re.compile(r'^/api/login'),
        ]

        # Verificar si la ruta solicitada coincide con alguna de las expresiones regulares
        if any(expresion.match(request.path) for expresion in expresiones_regulares):
            response = self.get_response(request)
            return response
        
        try:
            clave_secreta_fernet = AuthToken_nico.objects.get(usuario=1).clave_secreta_fernet  
            token_jwt_request = AuthToken_nico.objects.get(usuario=1).token_jwt 
        except Exception as e:
            print(f"clave_secreta_fernet {e}")


        try:
            # Obtener la IP del cliente (asegúrate de haber configurado correctamente el middleware para esto)
            ip = real_ip_user(request)
            hashed_ip = bcrypt.hashpw(str(ip).encode(), bcrypt.gensalt())
            hashed_ip = hashed_ip.decode()
            print("La direccion IP real del usuario es:", ip)
        except Exception as e:
            print(f"hashed_ip {e}")
        
        try:
            # Obtener el ID de usuario
            user_id = 1
            hashed_user_id = bcrypt.hashpw(str(user_id).encode(), bcrypt.gensalt())
            hashed_user_id = hashed_user_id.decode()
        except Exception as e:
            print(f"hashed_user_id {e}")


        try:

            # Codificar el payload en formato JWT
            payload = jwt.decode(token_jwt_request, clave_secreta_fernet, algorithms=['HS256'])
            user_id_request = payload.get('user_id')
            ip_request = payload.get('ip')
        except Exception as e:
            print(f"token_jwt {e}")


        # Codificar el payload en formato JWT
        if user_id != user_id_request:
            print('Token_request de seguridad expirado. La sesión puede haber sido comprometida. 1')
            return redirect('login')
        
        if ip != ip_request:
            print('Token_request de seguridad expirado. La sesión puede haber sido comprometida. 3')
            return redirect('login')
        
        response = self.get_response(request)
        print("termino el middlware VerificacionDeTomoFernet ")
        return response


class DebugOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si la dirección IP del cliente no coincide con la dirección IP específica,
        # se devuelve un error 403 (Forbidden).
        try:
            if request.META.get('REMOTE_ADDR') == settings.DEBUG_IP:
                settings.DEBUG = True
            else:
                settings.DEBUG = False
                #return HttpResponseForbidden("Forbidden")
        except Exception as e:
            print(e)
        
        response = self.get_response(request)
        print("termino el middlware DebugOnlyMiddleware ")
        return response



class VerificarFirmaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Verificar si la solicitud es para la vista de inicio de sesión
        if request.path in [reverse('login'),"","/"]:
            # Si la solicitud es para la vista de inicio de sesión, permitir el acceso sin verificación
            return response
        
        expresiones_regulares = [
            re.compile(r'^/confirm-ip/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/ClaveViewSet/'),
            re.compile(r'^/api/ClaveViewSet'),
            re.compile(r'^/api/ClaveViewSet/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/token/refresh/[-\w]+/[-\w]+/$'),
            re.compile(r'^/api/login/'),
            re.compile(r'^/api/login'),
        ]

        # Verificar si la ruta solicitada coincide con alguna de las expresiones regulares
        if any(expresion.match(request.path) for expresion in expresiones_regulares):
            return response
        
        # Verificar la firma después de que la vista haya respondido
        if not self._verificar_firma(request):
            print("La firma de la transacción es inválida.")  # Forbidden
            try:
                return redirect('login')
            except Exception as e:
                print("La firma de la transacción es inválida.", e)

        print("termino el middleware VerificarFirmaMiddleware")
        return response

    def _verificar_firma(self, request):
        try:
            # Llamar a la función para verificar la firma
            a = buscar_y_verificar_firma(request)
            if a == True:
                return True  # La firma es válida
            else:
                print("en el middleware retorno false")
                return False
        except Exception as e:
            print("Error al verificar la firma:", e)
            return redirect('login')
            #return False  # La firma es inválida o no se pudo verificar