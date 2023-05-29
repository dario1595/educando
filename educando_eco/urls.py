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
    *router.urls,  # Se incluyen las URLs generadas por el enrutador

    # URL para el registro de usuarios
    path('registro/', views.UsuarioView.as_view(), name='registro'),

    # URL para el inicio de sesión de usuarios
    path('login/', views.UsuarioView.inicio_sesion, name='login'),

    # URL para obtener la lista de usuarios
    path('usuarios/', views.UsuarioView.lista_usuarios, name='lista_usuarios'),
]