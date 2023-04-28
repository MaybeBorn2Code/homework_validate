from django.contrib import admin
from django.urls import (
    include,
    path,
)

from mesages.views import (
    MessageViewSet,
    ChatViewSet,
    ChatMessageViewSet
)

from rest_framework.routers import DefaultRouter


router = DefaultRouter(
    trailing_slash=False
)

router.register('messages', MessageViewSet)
router.register('chat', ChatViewSet)
router.register('chat_check', ChatMessageViewSet)

urlpatterns = (
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls))
)
