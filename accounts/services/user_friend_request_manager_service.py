from datetime import datetime, timedelta
from django.db import transaction
from accounts.models import FriendRequest, User

class UserFriendsRelationManager(object):

    def __init__(self, user, friend):
        self.current_user = user
        self.friend = friend
        self.is_accepted=False
        self.status_data = self._status_data()

    def _status_data(self):
        return {
            'is_success': False,
            'error': ''
        }
    
    def _is_friend_request_available(self):
        return FriendRequest.objects.filter(
            receiver=self.current_user,
            sender=self.friend
        ).exists()
    
    def _is_friend_request_already_sent(self):
        return FriendRequest.objects.filter(
            receiver=self.current_user,
            sender=self.friend
        ).exists()

    def accept_friend_request(self):

        def _accept_friend_request():
            with transaction.atomic():
                self.current_user.friends.add(self.friend)
                self.friend.friends.add(self.current_user)
                FriendRequest.objects.filter(
                    receiver=self.current_user,
                    sender=self.friend
                ).delete()

        self.status_data['error'] = 'No Friend Request Found'
        if self._is_friend_request_available():
            _accept_friend_request()
            self.status_data['error'] = ''
            self.status_data['is_success'] = True
        return self.status_data

    def reject_friend_request(self):
        self.status_data['error'] = 'No Friend Request Found'
        if self._is_friend_request_available():
            FriendRequest.objects.filter(
                receiver=self.current_user,
                sender=self.friend
            ).delete()
            self.status_data['error'] = ''
            self.status_data['is_success'] = True
        return self.status_data

    def send_friend_request(self):

        def _is_friend_request_hourly_sending_limit_exceeded():
            is_friend_request_hourly_sending_limit_exceeded = True
            last_1_minute_datetime = datetime.now() - timedelta(minutes=1)
            last_1_minute_friend_request_count = FriendRequest.objects.filter(sender=self.current_user, created_at__gte=last_1_minute_datetime).count()
            if last_1_minute_friend_request_count < 3:
                is_friend_request_hourly_sending_limit_exceeded = False
            return is_friend_request_hourly_sending_limit_exceeded

        self.status_data['error'] = 'Already Friend Request Sent'
        if _is_friend_request_hourly_sending_limit_exceeded():
            self.status_data['error'] = 'Sending Friend Request Quota Exceeded. Please Send after 1 Minute'
        elif not self._is_friend_request_already_sent():
            FriendRequest.objects.create(
                sender=self.current_user,
                receiver=self.friend
            )
            self.status_data['error'] = ''
            self.status_data['is_success'] = True
        return self.status_data

    def remove_friend(self):
        self.status_data['error'] = 'No Friend Found'
        try:
            self.current_user.friends.remove(self.friend)
            self.friend.friends.remove(self.current_user)
            self.status_data['error'] = ''
            self.status_data['is_success'] = True
        except Exception as e:
            pass
        return self.status_data