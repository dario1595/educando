from  rest_framework import serializers

from .models import Rol, Usuario, Categoria,Curso, MisCurso, Carrito, Foro, Contacto

class RolSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Rol
        fields = '__all__'

#===========================================================================================================================================================================
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        usuario = Usuario.objects.create_user(password=password, **validated_data)
        return usuario
    
#===========================================================================================================================================================================
class CategoriaSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Categoria
        fields = '__all__'
class CursoSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Curso
        fields = '__all__'
class MisCursoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = MisCurso
        fields = '__all__'
class CarritoSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Carrito
        fields = '__all__'
class ForoSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Foro
        fields = '__all__'
class ContactoSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Contacto
        fields = '__all__'
