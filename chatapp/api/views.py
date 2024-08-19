# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import  Message, UserProfile
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
#  Notification
from .serializers import  MessageSerializer, UserSerializer, UserProfileSerializer
# NotificationSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            # Create UserProfile with additional data
            profile_data = {
                'profile_picture': request.data.get('profile_picture'),
                'address': request.data.get('address'),
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save(user=user)  # Link the profile to the user
                return Response(user_serializer.data, status=201)
            return Response(profile_serializer.errors, status=400)
        return Response(user_serializer.errors, status=400)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status= status.HTTP_404_NOT_FOUND)

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Update the profile
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=404)



class UserProfileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(UserProfile, user=user)
        serializer = UserProfileSerializer(profile)
        
        return Response(serializer.data)
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=400)


class MessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MessageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# class ChatRoomListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         chat_rooms = ChatRoom.objects.all()
#         serializer = ChatRoomSerializer(chat_rooms, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ChatRoomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DirectMessageListCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         direct_messages = DirectMessage.objects.filter(receiver=request.user).order_by('-timestamp')
#         serializer = DirectMessageSerializer(direct_messages, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = DirectMessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(sender=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class NotificationListView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
#         serializer = NotificationSerializer(notifications, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = NotificationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
