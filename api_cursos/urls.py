
from django.urls import path, include
from rest_framework import routers
from api_cursos import views

routers = routers.DefaultRouter()
routers.register(r'cursos',views.CursoViewSet)

urlpatterns = [
    path ('', include(routers.urls)),
]