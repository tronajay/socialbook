from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from accounts.models import FriendRequest, User
from accounts.serializers import (
    UserAccountSearchSerializer, 
    UserAccountFriendsSerializer, 
    UserAccountCreationSerializer, 
    UserFriendsRelationSerializer,
)

# Create your views here.

class UserAccountCreationViewSet(viewsets.ViewSet):

    def create_user(self, request, *args, **kwargs):
        serializer = UserAccountCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserAccountSearchViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def search_user(self, request, *args, **kwargs):
        request_data = dict(current_user_id=request.user.id, query=request.query_params.get('query'))
        serializer = UserAccountSearchSerializer(data=request_data)
        if serializer.is_valid():
            return Response(serializer.search_output_data(), status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserAccountFriendsViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]
    
    def friends_list(self, request, *args, **kwargs):
        serializer = UserAccountFriendsSerializer(request.user.friends, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def friend_requests_list(self, request, *args, **kwargs):
        friend_request_user_ids = FriendRequest.objects.filter(receiver=request.user).values_list('sender', flat=True)
        users_list = User.objects.filter(id__in=friend_request_user_ids)
        serializer = UserAccountFriendsSerializer(users_list, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def send_friend_request(self, request, *args, **kwargs):
        request_data = dict(user=request.user.id, **request.data)
        serializer = UserFriendsRelationSerializer(data=request_data)
        if serializer.is_valid():
            return Response(serializer.relation_manager().send_friend_request(), status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def accept_friend_request(self, request, *args, **kwargs):
        request_data = dict(user=request.user.id, **request.data)
        serializer = UserFriendsRelationSerializer(data=request_data)
        if serializer.is_valid():
            return Response(serializer.relation_manager().accept_friend_request(), status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def reject_friend_request(self, request, *args, **kwargs):
        request_data = dict(user=request.user.id, **request.data)
        serializer = UserFriendsRelationSerializer(data=request_data)
        if serializer.is_valid():
            return Response(serializer.relation_manager().reject_friend_request(), status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def remove_friend(self, request, *args, **kwargs):
        request_data = dict(user=request.user.id, **request.data)
        serializer = UserFriendsRelationSerializer(data=request_data)
        if serializer.is_valid():
            return Response(serializer.relation_manager().remove_friend(), status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


