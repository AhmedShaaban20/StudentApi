from rest_framework import serializers, status
from .models import *

#from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'mobile')

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email','username', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create(
#             validated_data['email'],
#             validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#     class Meta:
#         model = User
#         fields = "__all__"

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

        