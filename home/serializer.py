from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    '''VALIDATING USERNAME AND EMAIL'''

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already exists")
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("Email already exists")

        return data


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']


class PersonSerializaer(serializers.ModelSerializer):
    # color = ColorSerializer()

    class Meta:
        model = Person
        fields = "__all__"
        depth = 1

    '''INPUT VALILDATION FOR THE API VIEW'''
    # def validate(self, data):
    #     special_chars = '!@#$%^&*()__+_?><,.\|`'
    #     if any(c in special_chars for c in data['name']):
    #         return serializers.ValidationError("name cannot contain special chars")
    #     if data['age'] > 18:
    #         return serializers.ValidationError("Under age")
