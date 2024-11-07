from rest_framework import serializers
from .models import User  # Import your custom User model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterUserModelSerializer(serializers.ModelSerializer):
    confirm_email = serializers.EmailField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'phone_number',
            'email', 'confirm_email', 'password', 'confirm_password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        # Validate email and confirm_email match
        if data['email'] != data['confirm_email']:
            raise serializers.ValidationError("Email addresses do not match.")

        # Validate password and confirm_password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        # Remove fields that aren't part of the model
        validated_data.pop('confirm_email')
        validated_data.pop('confirm_password')

        user = User.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data.get('date_of_birth'),
            phone_number=validated_data.get('phone_number'),
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
