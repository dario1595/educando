from .serializer import  UsuarioSerializer, CategoriaSerializer, CursoSerializer, MisCursoSerializer, CarritoSerializer, CompraSerializer,ForoSerializer, ContactoSerializer
from .models import  Usuario, Categoria,Curso, MisCurso, Carrito, Compra,Foro, Contacto

from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from django.db import transaction, models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

import datetime, jwt
from django.contrib.auth.models import Group

class UsuarioView(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create_user(self, request):
        # Validar los datos del serializer
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            nombre = serializer.validated_data.get('nombre')
            apellido = serializer.validated_data.get('apellido')
            id_rol_id = serializer.validated_data.get('id_rol_id')

            # Verificar si el correo electrónico ya está registrado
            usuario_existente = Usuario.objects.filter(email=email).exists()
            if usuario_existente:
                return Response({'mensaje': 'El correo electrónico ya está registrado'}, status=400)

            # Crear un nuevo usuario
            usuario = Usuario.objects.create_user(email=email, password=password, nombre=nombre, apellido=apellido, id_rol_id=id_rol_id)

            # Obtener el objeto de grupo correspondiente al id_rol
            grupo = Group.objects.get(pk=id_rol_id)

            # Asignar el grupo al usuario
            usuario.groups.add(grupo)

            # Generar el token JWT
            expiration_time = timezone.now() + datetime.timedelta(hours=12)
            expiration_timestamp = int(expiration_time.timestamp())

            payload = {
                'id_usuario': usuario.id_usuario,
                'email': email,
                'nombre': usuario.nombre,
                'id_rol_id': usuario.id_rol_id,
                'exp': expiration_timestamp
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            # Devolver una respuesta de éxito con el token generado
            return Response({'mensaje': 'Registro exitoso', 'token': token,'usuario': payload}, status=201)
        else:
            # Devolver una respuesta de error con los mensajes de validación
            return Response({'mensaje': 'Datos no válidos', 'errores': serializer.errors}, status=400)
        
    def inicio_sesion(self, request):
        # Verificar si la solicitud es un método POST
        if request.method == 'POST':
            try:
                data = request.data
                email = data.get('email', '')
                password = data.get('password', '')

                # Autenticar al usuario
                usuario = authenticate(request, email=email, password=password)

                if usuario is not None:
                    # Generar el token JWT
                    expiration_time = timezone.now() + datetime.timedelta(hours=12)
                    expiration_timestamp = int(expiration_time.timestamp())

                    payload = {
                        'id_usuario': usuario.id_usuario,
                        'email': email,
                        'nombre': usuario.nombre,
                        'apellido': usuario.apellido,
                        'id_rol_id': usuario.id_rol_id,
                        'exp': expiration_timestamp
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                    # Devolver una respuesta de éxito con el token generado
                    return Response({'mensaje': 'Inicio de sesión exitoso', 'token': token, 'usuario': payload}, status=200)
                else:
                    # Devolver una respuesta de error si las credenciales son inválidas
                    return Response({'mensaje': 'Credenciales inválidas'}, status=401)
            except:
                # Devolver una respuesta de error si ocurre algún error durante el proceso
                return Response({'mensaje': 'Datos no válidos'}, status=400)

        # Devolver una respuesta de error si el método no está permitido
        return Response({'mensaje': 'Método no permitido'}, status=405)

    def list_users(self, request):
        # Obtener la lista de usuarios y serializarlos
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)

        # Devolver la lista de usuarios serializada
        return Response(serializer.data, status=200)
    
#===========================================================================================================================================================================    


class CategoriaViewSet(viewsets.ModelViewSet):   
    queryset = Categoria.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoriaSerializer  

class CursoViewSet(viewsets.ModelViewSet):  
    queryset = Curso.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CursoSerializer

class CursosPorCategoriaView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, categoria_id):
        try:
            cursos = Curso.objects.filter(id_categoria=categoria_id)  # Utiliza el campo correcto para la categoría

            serializer = CursoSerializer(cursos, many=True)
            return Response(serializer.data)

        except Curso.DoesNotExist:
            return Response({'mensaje': 'No se encontraron cursos para la categoría'}, status=404)

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
            # Decodificar el token y obtener el id_usuario del payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            id_usuario = payload.get('id_usuario')
            return id_usuario
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expirado')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Token inválido')

    def post(self, request):
        data = request.data  # Obtener el JSON completo del cuerpo de la solicitud
        token = data.get('token')  # Obtener el token del JSON

        try:
            usuario_id = self.verificar_token(token)
            if usuario_id is None:
                return Response({'mensaje': 'Token inválido'}, status=401)

            usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
            cursos = data.get('cursos', [])  # Obtener la lista de cursos del JSON (puede estar vacía)

            mis_cursos = []  # Lista para almacenar las instancias de MisCurso

            with transaction.atomic():
                for curso_data in cursos:
                    id_curso = curso_data.get('id_curso')

                    try:
                        curso = Curso.objects.get(id_curso=id_curso)

                        mis_curso = MisCurso.objects.create(id_usuario=usuario, id_curso=curso)
                        mis_cursos.append(mis_curso)  # Agrega la instancia a la lista

                        carrito = Carrito.objects.create(
                            id_curso=curso,
                            usuario=usuario,
                            nombre_curso=curso.nombre_curso,
                            cantidad=1,
                            total_suma=curso.precio
                        )

                    except Curso.DoesNotExist:
                        return Response({'mensaje': 'El curso no existe'}, status=400)

                # Calcular la suma total de los cursos en el carrito del usuario
                suma_total = usuario.carrito.aggregate(total_suma=models.Sum('total_suma'))['total_suma']

                # Actualizar o crear un registro en la tabla Compra con la suma total y el usuario
                compra, _ = Compra.objects.update_or_create(
                    id_usuario_id=usuario.id_usuario,
                    defaults={'importe_total': suma_total}
                )

                mis_curso_serializer = MisCursoSerializer(mis_cursos, many=True)  # Serializa la lista de instancias
                compra_serializer = CompraSerializer(compra)

                return Response({
                    'mensaje': 'Cursos adquiridos exitosamente',
                    'mis_cursos': mis_curso_serializer.data,
                    'compra': compra_serializer.data
                }, status=201)

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
