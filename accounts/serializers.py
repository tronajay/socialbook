from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts import models as accounts_models, constants as accounts_constants
from accounts.services.user_friend_request_manager_service import UserFriendsRelationManager



class UserAccountCreationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField()
    email = serializers.EmailField(validators=[UniqueValidator(queryset=accounts_models.User.objects.all())])
    password = serializers.CharField(min_length=8, max_length=15, write_only=True)

    def save(self):
        created_user = accounts_models.User.objects.create(
            full_name=self.validated_data['full_name'],
            email=self.validated_data['email']
        )
        created_user.set_password(self.validated_data['password'])
        created_user.save()
        return created_user


class UserAccountSearchSerializer(serializers.Serializer):

    current_user_id = serializers.IntegerField()
    query = serializers.CharField()
    
    def search_output_data(self):
        search_query = self.validated_data['query']
        search_query_upper = self.validated_data['query'].upper()
        search_query_lower = self.validated_data['query'].lower()
        return accounts_models.User.objects.filter(
            Q(full_name__icontains=search_query) | Q(email__icontains=search_query)
            | Q(full_name__icontains=search_query_upper) | Q(email__icontains=search_query_upper) 
            | Q(full_name__icontains=search_query_lower) | Q(email__icontains=search_query_lower)
        ).exclude(id=self.validated_data['current_user_id']).values('id', 'full_name', 'email')


class UserAccountFriendsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()
    email = serializers.EmailField()


class UserFriendsRelationSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=accounts_models.User.objects.all())
    friend = serializers.PrimaryKeyRelatedField(queryset=accounts_models.User.objects.all())

    def validate(self, validated_data):
        if validated_data['user'] == validated_data['friend']:
            raise serializers.ValidationError(detail='Current Logged In User & Friend Cannot be same')
        return validated_data
    
    def relation_manager(self):
        return UserFriendsRelationManager(**self.validated_data)