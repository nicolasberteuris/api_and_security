from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed



class ExpiringTokenAuthentication(TokenAuthentication):
    #expired = False #se le envia la variable al frontend para que refresque la ruta cuando expiro

    def expires_in(self,token):
        time_elapse = timezone.now() - token.created 
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapse
        return  left_time

    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)

    def token_expire_handler(self,token):
        is_expired = self.is_token_expired(token)
        if is_expired:
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user = user)

        return token #si se le da un token nuevo retornan tambien token

    def authenticate_credentials(self, key):
        user = None
        try:
            token = self.get_model().objects.select_related('usuario').get(key = key)
            token = self.token_expire_handler(token)
            user = token.user
        except self.get_model().DoesNotExist:
            pass
        
        return (user)
        

