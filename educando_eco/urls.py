from django.urls import path, include
from rest_framework import routers
from educando_eco import views

router = routers.DefaultRouter()
router.register(r'Usuario', views.UsuarioViewSet,'usuario')
router.register(r'Categoria', views.CategoriaViewSet,'categoria')
router.register(r'Curso', views.CursoViewSet,'curso')
router.register(r'MisCurso', views.MisCursoViewSet,'misCurso')
router.register(r'Carrito', views.CarritoViewSet,'carrito')
router.register(r'Foro', views.ForoViewSet,'foro')
router.register(r'Contacto', views.ContactoViewSet,'contacto')
urlpatterns = router.urls

