from rest_framework import viewsets, permissions
from .serializer import CursoSerializer
from .models import Curso

# Create your views here.

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CursoSerializer