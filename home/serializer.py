from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            return serializers.ValidationError("User not found")
        # return validated data
        return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    """VALIDATING USERNAME AND EMAIL"""

    def validate(self, data):
        if data["username"]:
            if User.objects.filter(username=data["username"]).exists():
                raise serializers.ValidationError("Username already exists")
        if data["email"]:
            if User.objects.filter(email=data["email"]).exists():
                raise serializers.ValidationError("Email already exists")

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return validated_data


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        exclude = ["created", "modified"]


class PersonSerializer(serializers.ModelSerializer):
    # color = ColorSerializer()

    class Meta:
        model = Person
        exclude = ["created", "modified"]
        depth = 1

    """INPUT VALIDATION FOR THE API VIEW"""

    def validate(self, data):
        if int(data["age"]) < 18:
            return serializers.ValidationError("Under age")
        return data
