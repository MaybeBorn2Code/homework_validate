from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ValidationError


User: AbstractBaseUser = get_user_model()


class Chat(models.Model):
    """
    Chat. Can be 1 people or group chat.
    """

    owner: bool = models.ForeignKey(
        to=User,
        related_name='own_chats',
        on_delete=models.CASCADE,
        verbose_name='создатель'
    )
    is_many: bool = models.BooleanField(
        verbose_name='групповой ли?',
        default=False
    )
    name: str = models.CharField(
        verbose_name='название',
        max_length=120
    )
    members: list['User'] = models.ManyToManyField(
        to=User,
        related_name='chats'
    )

    class Meta:
        ordering = (
            '-id',
        )
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'

    def __str__(self) -> str:
        return (
            f'Owner: {self.owner if self.owner is not None else "Basic"}.'
            f'Count users: {len(self.members.get_queryset())}'
        )


class Message(models.Model):
    """
    Message between users.
    """

    sender: 'User' = models.ForeignKey(
        to=User,
        related_name='messages',
        verbose_name='сообщения',
        on_delete=models.CASCADE,
        null=True
    )
    to_send: 'Chat' = models.ForeignKey(
        to='Chat',
        related_name='messages',
        verbose_name='чат',
        on_delete=models.CASCADE
    )
    text: str = models.TextField(
        verbose_name='сообщение',
        max_length=2000
    )
    datetime_send = models.DateTimeField(
        verbose_name='время отправления',
        auto_now=False,
        auto_now_add=True
    )

    def clean(self):
        if not self.to_send.is_many and self.to_send.members.count() != 1:
            print(self.to_send.members.count())
            raise ValidationError(
                'The number of members must be 1 for non-group chat messages.')

    class Meta:
        ordering = (
            '-datetime_send',
        )
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'

    def __str__(self) -> str:
        return f'[{self.datetime_send.strftime("%d %B - %H:%M:%S")}] {self.sender}: {self.text}'
