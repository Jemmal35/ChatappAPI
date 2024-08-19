# urls.py
from django.urls import path
from .views import  MessageView, UserProfileView, UserRegistrationView, LoginView, UserProfileDetailView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('<str:username>/profile/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('message/', MessageView.as_view(), name='users-message'),
    # path('chatrooms/', ChatRoomListCreateView.as_view(), name='chatroom-list-create'),
    # path('direct-messages/', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),
    # path('notifications/', NotificationListView.as_view(), name='notification-list'),
]
