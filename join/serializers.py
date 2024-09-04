from rest_framework import serializers
from django.contrib.auth import authenticate

from join.models import Task, User


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials."
                )
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "user_color"]


class TaskSerializer(serializers.ModelSerializer):
    assignedTo = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=False
    )

    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        assignedTo_data = validated_data.pop("assignedTo", [])
        task = Task.objects.create(**validated_data)
        if assignedTo_data:
            task.assignedTo.set(assignedTo_data)
        return task

class TaskReadSerializer(serializers.ModelSerializer):
    assignedTo = UserSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = "__all__"