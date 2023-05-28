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
    path('list/', views.ListUserView.as_view()),
    path('Token/', views.CreateTokenView.as_view()),
    path('Registro/', views.CreateUserView.as_view()),
    path('Usuario/', views.RetriveUpdateUserView.as_view()),
]