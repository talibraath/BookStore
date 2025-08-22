from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role","first_name","last_name"]  
        read_only_fields = ('id', 'date_joined', 'last_login')


class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save()
        return instance