from rest_framework import viewsets, permissions, generics
from .serializer import  UsuarioSerializer, CategoriaSerializer, CursoSerializer, MisCursoSerializer, CarritoSerializer, ForoSerializer, ContactoSerializer
from .models import  Usuario, Categoria,Curso, MisCurso, Carrito, Foro, Contacto

from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .serializer import UsuarioSerializer
import json, datetime
import jwt

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from educando.utils import verificar_token
from django.shortcuts import get_object_or_404

class UsuarioView(APIView):
    @csrf_exempt
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

    @staticmethod
    @csrf_exempt
    
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
                    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=12)
                    payload = {
                        'id_usuario': usuario.id_usuario,
                        'email': email,
                        'nombre': usuario.nombre,
                        'exp': expiration_time
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

    @staticmethod
    @csrf_exempt
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
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Obtén el token de la solicitud
        token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]

        # Verifica el token
        usuario_id = verificar_token(token)
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
    def post(self, request):
        # Obtiene el usuario logueado
        usuario = request.user
        
        # Obtén el ID del curso a adquirir desde los datos de la solicitud
        id_curso = request.data.get('id_curso')
        
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
