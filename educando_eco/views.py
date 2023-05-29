from rest_framework import viewsets, permissions, generics, authentication
from .serializer import  UsuarioSerializer, CategoriaSerializer, CursoSerializer, MisCursoSerializer, CarritoSerializer, ForoSerializer, ContactoSerializer
from .models import  Usuario, Categoria,Curso, MisCurso, Carrito, Foro, Contacto

from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def registro(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            password = data.get('password', '')
            nombre = data.get('nombre', '')

            # Verificar si el usuario ya existe
            usuario_existente = Usuario.objects.filter(email=email).exists()
            if usuario_existente:
                return JsonResponse({'mensaje': 'El correo electrónico ya está registrado'})

            # Crear un nuevo usuario
            usuario = Usuario.objects.create_user(email=email, password=password, nombre=nombre)
            usuario.save()

            # Generar JWT
            refresh = RefreshToken.for_user(usuario)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'id': usuario.id_usuario  # Utilizar el campo "id_usuario" en lugar de "id"
            }

            return JsonResponse({'mensaje': 'Registro exitoso', 'token': token})

        except json.JSONDecodeError:
            return JsonResponse({'mensaje': 'Datos no válidos'})

    return JsonResponse({'mensaje': 'Método no permitido'})


@csrf_exempt
def inicio_sesion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            password = data.get('password', '')

            # Validar las credenciales
            usuario = authenticate(request, email=email, password=password)

            if usuario is not None:
                # Generar JWT
                refresh = RefreshToken.for_user(usuario)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return JsonResponse({'mensaje': 'Inicio de sesión exitoso', 'token': token})
            else:
                return JsonResponse({'mensaje': 'Credenciales inválidas'})
        except json.JSONDecodeError:
            return JsonResponse({'mensaje': 'Datos no válidos'})

    return JsonResponse({'mensaje': 'Método no permitido'})

@csrf_exempt
def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    usuarios_data = [{'nombre': usuario.nombre, 'correo': usuario.email} for usuario in usuarios]
    return JsonResponse({'usuarios': usuarios_data})

#===========================================================================================================================================================================    


class CategoriaViewSet(viewsets.ModelViewSet):   
    queryset = Categoria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaSerializer  
class CursoViewSet(viewsets.ModelViewSet):  
    queryset = Curso.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CursoSerializer
class MisCursoViewSet(viewsets.ModelViewSet):   
    queryset = MisCurso.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = MisCursoSerializer
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
