from rest_framework.serializers import ModelSerializer
from accounts.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role","first_name","last_name"]  
        read_only_fields = ('id', 'date_joined', 'last_login')