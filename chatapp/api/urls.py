# urls.py
from django.urls import path
from .views import ChatRoomListCreateView, MessageListCreateView, DirectMessageListCreateView, NotificationListView

urlpatterns = [
    path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    path('chatrooms/<int:room_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('direct-messages/', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]
