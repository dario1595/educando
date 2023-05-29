from django.urls import path
from rest_framework import routers
from educando_eco import views

router = routers.DefaultRouter()
router.register(r'Categoria', views.CategoriaViewSet,'categoria')
router.register(r'Curso', views.CursoViewSet,'curso')
router.register(r'MisCurso', views.MisCursoViewSet,'misCurso')
router.register(r'Carrito', views.CarritoViewSet,'carrito')
router.register(r'Foro', views.ForoViewSet,'foro')
router.register(r'Contacto', views.ContactoViewSet,'contacto')

urlpatterns = [
    *router.urls,
    path('registro/', views.UsuarioView.as_view(), name='registro'),
    path('login/', views.UsuarioView.inicio_sesion, name='login'),
    path('usuarios/', views.UsuarioView.lista_usuarios, name='lista_usuarios'),
]