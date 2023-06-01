from django.urls import path, include
from rest_framework import routers
from educando_eco import views

router = routers.DefaultRouter()
router.register(r'Categoria', views.CategoriaViewSet, basename='categoria')
router.register(r'Curso', views.CursoViewSet, basename='curso')
router.register(r'Carrito', views.CarritoViewSet, basename='carrito')
router.register(r'Foro', views.ForoViewSet, basename='foro')
router.register(r'Contacto', views.ContactoViewSet, basename='contacto')


urlpatterns = [
    path('', include(router.urls)),
    path('Login/', views.UsuarioView.as_view({'post': 'inicio_sesion'}), name='login'),
    path('Registro/', views.UsuarioView.as_view({'post': 'create_user'}), name='crear_usuario'),
    path('Usuarios/', views.UsuarioView.as_view({'get': 'list_users'}), name='lista_usuarios'),

    path('Mis_cursos/', views.MisCursosView.as_view(), name='mis_cursos'),
    path('Adquirir_curso/', views.AdquirirCursoView.as_view(), name='adquirir_curso'),
]
