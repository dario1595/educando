from rest_framework import viewsets, permissions
from .serializer import  UsuarioSerializer, CategoriaSerializer, CursoSerializer, MisCursoSerializer, CarritoSerializer, ForoSerializer, ContactoSerializer
from .models import  Usuario, Categoria,Curso, MisCurso, Carrito, Foro, Contacto

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .serializer import UsuarioSerializer
import json
import jwt


class UsuarioView(APIView):
    @csrf_exempt
    def post(self, request):
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            nombre = serializer.validated_data.get('nombre')

            # Verificar si el usuario ya existe
            usuario_existente = Usuario.objects.filter(email=email).exists()
            if usuario_existente:
                return Response({'mensaje': 'El correo electrónico ya está registrado'}, status=400)

            # Crear un nuevo usuario
            usuario = Usuario.objects.create_user(email=email, password=password, nombre=nombre)

            # Generar JWT
            token_payload = {'user_id': usuario.id_usuario, 'email': email, 'nombre': nombre}
            token = jwt.encode(token_payload, 'your_secret_key', algorithm='HS256')

            return Response({'mensaje': 'Registro exitoso', 'token': token}, status=201)
        else:
            return Response({'mensaje': 'Datos no válidos', 'errores': serializer.errors}, status=400)

    @staticmethod
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
                    payload = {
                        'user_id': usuario.id_usuario,
                        'email': email,
                        'nombre': usuario.nombre
                    }
                    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')

                    return JsonResponse({'mensaje': 'Inicio de sesión exitoso', 'token': token}, status=200)
                else:
                    return JsonResponse({'mensaje': 'Credenciales inválidas'}, status=401)
            except json.JSONDecodeError:
                return JsonResponse({'mensaje': 'Datos no válidos'}, status=400)

        return JsonResponse({'mensaje': 'Método no permitido'}, status=405)

    @staticmethod
    @csrf_exempt
    def lista_usuarios(request):
        usuarios = Usuario.objects.all()
        usuarios_data = [{'nombre': usuario.nombre,'apellido': usuario.apellido, 'email': usuario.email} for usuario in usuarios]
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
