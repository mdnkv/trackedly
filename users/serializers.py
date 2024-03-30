from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id', 'email', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        try:
            validate_password(password=validated_data['password'], user=user)
        except ValidationError as err:
            user.delete()
            raise serializers.ValidationError(err.messages)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class PasswordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        password = validated_data['password']
        try:
            validate_password(password=password, user=instance)
            instance.set_password(password)
            instance.save()
        except ValidationError as err:
            raise serializers.ValidationError(err.messages)
        return instance
