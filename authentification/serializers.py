from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from .models import CustomUser as User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'role')
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True, "allow_blank": False},
            "role": {"required": True, "allow_blank": False}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        tokens = self.generate_tokens(user)
        self.send_confirmation_email(user)
        return tokens

    def generate_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def send_confirmation_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        confirmation_url = f"{settings.BASE_URL}/confirm/{uid}/{token}/"

        subject = 'Confirm your email'
        message = f'Please click the link to confirm your email: {confirmation_url}'
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = user.email

        send_mail(subject, message, sender_email, [recipient_email])


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)  # Hide password in responses

    # Validate fields as needed (e.g., ensuring both username and password are present)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required")

        return data
