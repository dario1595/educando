from rest_framework import viewsets, permissions, generics, authentication
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from .serializer import  UsuarioSerializer, CategoriaSerializer, CursoSerializer, MisCursoSerializer, CarritoSerializer, ForoSerializer, ContactoSerializer
from .models import  Usuario, Categoria,Curso, MisCurso, Carrito, Foro, Contacto


class ListUserView (generics.ListAPIView):
    serializer_class = UsuarioSerializer
    def get_queryset(self):
        return Usuario.objects.all()

class CreateUserView(generics.CreateAPIView):
    serializer_class = UsuarioSerializer

class RetriveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

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
