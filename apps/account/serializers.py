from rest_framework import serializers
from .models import User

class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email')
class AdminUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','groups','user_permissions')
        extra_kwargs = {
			'joined': {'read_only':True},
			'last_login': {'read_only':True},
			'id': {'read_only':True},
		}
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email','phone_number')

class RegisterUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('name', 'email','phone_number', 'password', 'password2')
        extra_kwargs = {
			'password': {'write_only':True},
		}
    
    def create_user(self,validated_data):
        del validated_data['password2']
        User.objects.create_user(**validated_data)
    
    def validate_password(self,value):
        if len(value) >= 6:
            return value
        raise serializers.ValidationError('Password Is Short')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('passwords must match')
        return data