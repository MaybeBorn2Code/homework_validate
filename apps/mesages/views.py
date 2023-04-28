from django.db.models.query import QuerySet

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from mesages.mixins import (
    ResponseMixin,
    ObjectMixin,
)
from mesages.models import (
    Message,
    Chat,
    User
)
from mesages.serializers import (
    MessageSerializer,
    ChatSerializer,
    UserSerializer
)


class MessageViewSet(ResponseMixin, ObjectMixin, ViewSet):
    """ViewSet about chats and messages."""

    queryset: QuerySet[Message] = \
        Message.objects.select_related('to_send').all()

    # list of all
    def list(self, request: Request, *args: tuple) -> Response:
        """GET method."""

        serializer: MessageSerializer = MessageSerializer(
            self.queryset, many=True
        )

        return Response(
            data=serializer.data
        )

    def create(self, request):
        data = request.data  # 1
        user_serializer: UserSerializer = UserSerializer(
            User.objects.get(id=data.get('sender'))
        )
        data["sender"] = user_serializer.data.get("id")

        serializer: MessageSerializer = MessageSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "message": f"Message {serializer.validated_data.get('id')} is create!"
            }
        )


class ChatViewSet(ResponseMixin, ObjectMixin, ViewSet):
    """ViewSet about chats."""

    queryset: QuerySet[Chat] = \
        Chat.objects.select_related('owner').all()

    # list of all
    def list(self, request: Request, *args: tuple) -> Response:
        """GET method."""

        serializer: ChatSerializer = ChatSerializer(
            self.queryset, many=True
        )

        return Response(
            data=serializer.data
        )


class ChatMessageViewSet(ViewSet):
    """
    ViewSet about chats and messages.
    """

    queryset: QuerySet[Message] = \
        Message.objects.select_related('to_send').all()

    @action(methods=['GET'], detail=False)
    def list_chats(self, request: Request, *args: tuple) -> Response:
        chats: QuerySet[Chat] = [message.to_send for message in self.queryset]
        serializer: MessageSerializer = ChatSerializer(chats, many=True)

        return Response(
            data=serializer.data
        )

    @action(methods=['GET', 'POST'], detail=False)
    def list_messages(self, request: Request, *args: tuple) -> Response:
        if request.method == "GET":
            serializer: MessageSerializer = MessageSerializer(
                self.queryset, many=True
            )

            return Response(
                data=serializer.data
            )

        data = request.data  # 1

        serializer: MessageSerializer = MessageSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "message": f"Message {serializer.validated_data.get('id')} is create!"
            }
        )
