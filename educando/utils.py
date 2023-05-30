import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def verificar_token(token):
    if not token:
        raise AuthenticationFailed('Token vacío')

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        id_usuario = payload.get('id_usuario')
        return id_usuario
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token expirado')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Token inválido')
