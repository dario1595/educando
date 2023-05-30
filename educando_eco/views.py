
from .serializer import  UsuarioSerializer, CategoriaSerializer, CursoSerializer, MisCursoSerializer, CarritoSerializer, ForoSerializer, ContactoSerializer
from .models import  Usuario, Categoria,Curso, MisCurso, Carrito, Foro, Contacto

from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

import json, datetime, jwt

class UsuarioView(APIView):

    def post(self, request):
        # Se recibe una solicitud POST con los datos del usuario a registrar
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            # Se extraen los datos validados del serializer
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            nombre = serializer.validated_data.get('nombre')
            apellido = serializer.validated_data.get('apellido')

            # Verificar si el usuario ya existe en la base de datos
            usuario_existente = Usuario.objects.filter(email=email).exists()
            if usuario_existente:
                # Si el usuario ya existe, se retorna un mensaje de error y un código de estado 400 (Solicitud incorrecta)
                return Response({'mensaje': 'El correo electrónico ya está registrado'}, status=400)

            # Crear un nuevo usuario en la base de datos
            usuario = Usuario.objects.create_user(email = email, password = password, nombre = nombre, apellido = apellido)

            # Generar un token JWT (JSON Web Token)
            token_payload = {'user_id': usuario.id_usuario, 'email': email, 'nombre': nombre}
            token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')

            # Se retorna una respuesta con un mensaje de éxito, el token y un código de estado 201 (Creado)
            return Response({'mensaje': 'Registro exitoso', 'token': token}, status=201)
        else:
            # Si los datos no son válidos, se retorna un mensaje de error con los errores del serializer y un código de estado 400 (Solicitud incorrecta)
            return Response({'mensaje': 'Datos no válidos', 'errores': serializer.errors}, status=400)


    def inicio_sesion(request):
        if request.method == 'POST':
            try:
                # Se obtienen los datos de inicio de sesión del cuerpo de la solicitud
                data = json.loads(request.body)
                email = data.get('email', '')
                password = data.get('password', '')

                # Se validan las credenciales del usuario utilizando la función authenticate de Django
                usuario = authenticate(request, email=email, password=password)

                if usuario is not None:
                    # Si las credenciales son válidas, se genera un token JWT (JSON Web Token) con tiempo de expiración
                    expiration_time = timezone.now() + datetime.timedelta(hours=12)
                    expiration_timestamp = int(expiration_time.timestamp())

                    payload = {
                        'id_usuario': usuario.id_usuario,
                        'email': email,
                        'nombre': usuario.nombre,
                        'exp': expiration_timestamp
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                    # Se retorna una respuesta JSON con un mensaje de éxito, el token y un código de estado 200 (Éxito)
                    return JsonResponse({'mensaje': 'Inicio de sesión exitoso', 'token': token}, status=200)
                else:
                    # Si las credenciales son inválidas, se retorna un mensaje de error y un código de estado 401 (No autorizado)
                    return JsonResponse({'mensaje': 'Credenciales inválidas'}, status=401)
            except json.JSONDecodeError:
                # Si los datos no son válidos, se retorna un mensaje de error y un código de estado 400 (Solicitud incorrecta)
                return JsonResponse({'mensaje': 'Datos no válidos'}, status=400)

        # Si el método de la solicitud no es POST, se retorna un mensaje de error y un código de estado 405 (Método no permitido)
        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

    
    def lista_usuarios(request):
        # Se obtienen todos los usuarios de la base de datos
        usuarios = Usuario.objects.all()
        # Se crea una lista de diccionarios con los datos de cada usuario
        usuarios_data = [{'nombre': usuario.nombre, 'apellido': usuario.apellido, 'email': usuario.email} for usuario in usuarios]
        # Se retorna una respuesta JSON con la lista de usuarios y un código de estado 200 (Éxito)
        return JsonResponse({'usuarios': usuarios_data}, status=200)
#===========================================================================================================================================================================    


class CategoriaViewSet(viewsets.ModelViewSet):   
    queryset = Categoria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaSerializer  

class CursoViewSet(viewsets.ModelViewSet):  
    queryset = Curso.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CursoSerializer


#===========================================================================================================================================================================

class MisCursosView(APIView):
    serializer_class = MisCursoSerializer
    permission_classes = [AllowAny]

    def verificar_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            id_usuario = payload.get('id_usuario')
            return id_usuario
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token inválido')

    def post(self, request):
        # Obtén el token del cuerpo de la solicitud
        token = request.data.get('token', '')

        # Verifica el token
        usuario_id = self.verificar_token(token)
        if usuario_id is None:
            # El token no es válido, devuelve un mensaje de error y un código de estado 401 (No autorizado)
            return Response({'mensaje': 'Token inválido'}, status=401)

        # El token es válido, obtén el usuario autenticado
        usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

        # Obtén los cursos del usuario y serialízalos
        cursos = MisCurso.objects.filter(id_usuario=usuario)
        serializer = MisCursoSerializer(cursos, many=True)

        # Devuelve los cursos serializados
        return Response(serializer.data)
    


class AdquirirCursoView(APIView):
    def verificar_token(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            id_usuario = payload.get('id_usuario')
            return id_usuario
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token inválido')

    def post(self, request):
        # Obtén el ID del curso a adquirir desde los datos de la solicitud
        id_curso = request.data.get('id_curso')
        
        # Obtén el token del usuario desde los datos de la solicitud
        token = request.data.get('token')

        try:
            # Verifica si el token es válido y obtén el ID del usuario autenticado
            usuario_id = self.verificar_token(token)
            if usuario_id is None:
                # El token no es válido, devuelve un mensaje de error y un código de estado 401 (No autorizado)
                return Response({'mensaje': 'Token inválido'}, status=401)
            
            # El token es válido, obtén el usuario autenticado
            usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
            
            try:
                # Verifica si el curso existe
                curso = Curso.objects.get(id_curso=id_curso)
                
                # Crea una instancia de MisCurso para vincular el usuario y el curso
                mis_curso = MisCurso.objects.create(id_usuario=usuario, id_curso=curso)
                
                # Serializa la instancia de MisCurso
                serializer = MisCursoSerializer(mis_curso)
                
                return Response(serializer.data, status=201)
            except Curso.DoesNotExist:
                return Response({'mensaje': 'El curso no existe'}, status=400)
        
        except AuthenticationFailed as e:
            return Response({'mensaje': str(e)}, status=401)


#===========================================================================================================================================================================
class CarritoViewSet(viewsets.ModelViewSet):    
    queryset = Carrito.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CarritoSerializer

class ForoViewSet(viewsets.ModelViewSet):   
    queryset = Foro.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ForoSerializer

class ContactoViewSet(viewsets.ModelViewSet):   
    queryset = Contacto.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ContactoSerializer  
