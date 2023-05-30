import jwt
from django.conf import settings

def verificar_token(token):
    try:
        # Decodifica el token JWT utilizando el mismo secreto utilizado para generarlo
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        # El token es válido, devuelve el payload del token
        return payload
    except jwt.ExpiredSignatureError:
        # El token ha expirado
        return None
    except jwt.InvalidTokenError:
        # El token no es válido
        return None