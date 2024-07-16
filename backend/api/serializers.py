from rest_framework import serializers
from .models import Usuario


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'password', 'fecha_nacimiento', 'nombre', 'apellido', 'ciudad_nacimiento', 'provincia_nacimiento', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        return user
