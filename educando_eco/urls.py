from django.urls import path
from rest_framework import routers
from educando_eco import views

router = routers.DefaultRouter()
router.register(r'Categoria', views.CategoriaViewSet,'categoria')
router.register(r'Curso', views.CursoViewSet,'curso')
router.register(r'Carrito', views.CarritoViewSet,'carrito')
router.register(r'Foro', views.ForoViewSet,'foro')
router.register(r'Contacto', views.ContactoViewSet,'contacto')

urlpatterns = [
    *router.urls,  # Se incluyen las URLs generadas por el enrutador

    # URL para el registro de usuarios
    path('Registro/', views.UsuarioView.as_view(), name='registro'),

    # URL para el inicio de sesión de usuarios
    path('Login/', views.UsuarioView.inicio_sesion, name='login'),

    # URL para obtener la lista de usuarios
    path('Usuarios/', views.UsuarioView.lista_usuarios, name='lista_usuarios'),

    path('Mis_cursos/', views.MisCursosView.as_view(), name='mis_cursos'),

    path('Adquirir_curso/', views.AdquirirCursoView.as_view(), name='adquirir_curso')
]