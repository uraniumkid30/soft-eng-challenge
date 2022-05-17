from rest_framework import serializers
from applications.account.models import User


class FilterSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False)
    name = serializers.CharField(required=False)


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "role",
            "ship",
        )
