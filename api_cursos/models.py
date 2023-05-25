from django.db import models

# Create your models here.
class Curso(models.Model):
    id_curso = models.AutoField(primary_key = True)
    nombre_curso = models.CharField(max_length = 45, null = True)
    duracion = models.IntegerField(null = True)
    precio = models.IntegerField(null = True)
    activo = models.BooleanField(default = True)


