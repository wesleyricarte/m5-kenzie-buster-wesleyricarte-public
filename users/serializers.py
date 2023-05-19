from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=127)

    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, default=None)

    password = serializers.CharField(max_length=127, write_only=True)

    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict) -> User:
        email = validated_data.get("email")
        username = validated_data.get("username")

        if (
            User.objects.filter(email=email).exists()
            and User.objects.filter(username=username).exists()
        ):
            raise serializers.ValidationError(
                {
                    "email": ["email already registered."],
                    "username": ["username already taken."],
                }
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["email already registered."]})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": ["username already taken."]})

        return (
            User.objects.create_superuser(**validated_data)
            if validated_data["is_employee"]
            else User.objects.create_user(**validated_data)
        )

    def update(self, instance: User, validated_data: dict):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)

        instance.password = validated_data.get("password")
        if instance.password:
            instance.set_password(instance.password)

        instance.save()
        return instance
