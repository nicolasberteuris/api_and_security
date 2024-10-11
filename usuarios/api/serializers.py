from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from usuarios.models import Usuario

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username','email','nombre')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
    
    def create(self,validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre')

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password':'Debe ingresar ambas contraseñas iguales'}
            )
        return data

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'nombre': instance['nombre'],
            'username': instance['username'],
            'email': instance['email']
        }



























"""

from rest_framework import serializers


class UserTokenSerializar(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'nombre')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def create(self, validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario
    
    def update(self, instance, validated_data):
        updated_usuario = super().update(instance, validated_data)
        updated_usuario.set_password(validated_data['password'])
        updated_usuario.save()
        return updated_usuario


class UserListSerializar(serializers.ModelSerializer):
    class Meta:
        model = Usuario 

        # to representation (es para la vista que traiga los campos que solo quiero que se vean)

    def to_representation(self, instance):
            return{
                'nombre': instance['nombre'],
                'email': instance['email'],
                'password': instance['password'],
                'username': instance['username']
            }

class TestUserSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length= 200)
    email = serializers.EmailField()

    def validate_nombre(self, value):
        if 'losmillo___' in value:
            raise serializers.ValidationError('Error, no puede existir un usuario con ese nombre')
        
        return value
    
    def validate_email(self, value):
        if value == '':
            raise serializers.ValidationError('Tiene que indicar un mail')
        
        if self.validate_nombre(self.context['nombre']) in value:
            raise serializers.ValidationError('El email no puede contener el nombre')
        return value
    
    def validate(self, data):        
        return data
    
    def create(self, validated_data):
        return self.model.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
"""