from  rest_framework import serializers

from .models import Rol, Categoria,Curso, MisCurso, Carrito, Foro, Contacto
from django.contrib.auth import get_user_model, authenticate

class RolSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Rol
        fields = '__all__'

#===========================================================================================================================================================================
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email','password','nombre', 'apellido']
        extra_kwargs = {'password': {'write_only':True}}    # le da a password una propiedad que es solamente escritura y no te devuelve el password en un get
    def create(self, valida_data):  # para crear usuario
        return get_user_model().objects.create_user(**valida_data)

    def update(self, instance, validate_data):  # para actualizacion de password
        password = validate_data.pop('password', None)
        user = super().update(instance, validate_data)

        if password:
            user.set_password(password)
            user.save()
        return user
    
class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type':'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password
        )

        if not user:
            raise serializers.ValidationError('No se pudo validar el usuario', code='authorization')
        data ['user'] = user
        return data
    
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
