from rest_framework import status, authentication, exceptions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from usuarios.authentication import ExpiringTokenAuthentication

class Authentication(authentication.BaseAuthentication):
    user = None

    def get_user(self,request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                 return None
            
            token_expired = ExpiringTokenAuthentication()
            user = token_expired.authenticate_credentials(token)

            if user != None:
                 self.user = user
                 return user

        return None


    """
    def dispatch(self, request, *args, **kwargs):
            user = self.get_user(request)
            print(user)
            # se econtro un token en la peticion
            if user is not None:
                if type(user) == str:
                    response = Response({'error':user, 'expired': self.user_token_expired}, status= status.HTTP_401_UNAUTHORIZED)
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = 'application/json'
                    response.renderer_context = {}
                    return response
                
                if not self.user_token_expired:          
                    return super().dispatch(request, *args, **kwargs)
            
            #no hay token
            response = Response({'error':'No se han enviado las credenciales', 'expired': self.user_token_expired}, status= status.HTTP_400_BAD_REQUEST)
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = 'application/json'
            response.renderer_context = {}
            return response
    """
    
    def authenticate(self, request):
         self.get_user(request)
         if self.user is None:
              raise exceptions.AuthenticationFailed('No se han enviado las credenciales')
         
         return (self.user, 1 )
        