from rest_framework import serializers
from django.contrib.auth.models import User

from mesages.models import Chat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class MessageSerializer(serializers.Serializer):
    """
    Serializer for get all message fields.
    """

   # sender: User = UserSerializer()
    to_send: Chat = serializers.PrimaryKeyRelatedField(
        queryset=Chat.objects.all()
    )
    text = serializers.CharField()
    datetime_send = serializers.DateTimeField()

    class Meta:
        fields = (
            'sender',
            'to_send',
            'text',
            'datetime_send'
        )

    def validate(self, attrs):
        if not attrs['to_send'].is_many and len(attrs['to_send'].members.all()) != 1:
            raise serializers.ValidationError(
                'If chat is not a group chat, there must be exactly 1 member.')
        return attrs


class ChatSerializer(serializers.Serializer):
    """
    Serializer for get all message fields.
    """

    owner = UserSerializer(required=False)
    is_many = serializers.BooleanField(read_only=True)
    name = serializers.CharField()
    members = UserSerializer(many=True)

    class Meta:
        fields = {
            'owner',
            'is_many',
            'name',
            'members'
        }
