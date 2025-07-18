from rest_framework import serializers
from apps.user.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate_mobile_number(self, value):
        if not re.match(r'^\+88\d{11}$', value):
            raise serializers.ValidationError("Mobile number must start with +88 and be 14 digits total.")
        if UserModel.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already exists.")
        return value

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8 or not re.search(r'[A-Z]', value) or not re.search(r'\d', value) or not re.search(r'[@$!%*?&]', value):
            raise serializers.ValidationError("Password must be at least 8 characters with 1 uppercase, 1 digit, and 1 special character.")
        return value

    def validate_profile_image(self, value):
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Image size must be under 5MB.")
            if not value.content_type in ['image/jpeg', 'image/png']:
                raise serializers.ValidationError("Only JPEG and PNG formats are supported.")
        return value

    def validate_user_type(self, value):
        valid_types = ['Admin', 'Doctor', 'Patient']
        if value not in valid_types:
            raise serializers.ValidationError("Invalid user type.")
        return value

    def validate(self, data):
        user_type = data.get("user_type")
        if user_type == "Doctor":
            required_fields = ["license_no", "experience_years", "consultation_fee"]
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f"{field.replace('_', ' ').title()} is required for doctors."})
        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = f"{user.id}"
        token['email'] = user.email
        token['phone'] = user.phone
        token['superuser'] = user.is_superuser
        token['is_acitve'] = user.is_active
        return token
    
    def validate(self, attrs):
        user = self.context['user']

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    