
from django.urls import path
from accounts.views import UserAccountSearchViewSet, UserAccountCreationViewSet, UserAccountFriendsViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', UserAccountCreationViewSet.as_view({'post': 'create_user'})),
    path('generate_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('search/', UserAccountSearchViewSet.as_view({'get': 'search_user'})),
    path('friends/', UserAccountFriendsViewSet.as_view({'get': 'friends_list'})),
    path('friends_requests/', UserAccountFriendsViewSet.as_view({'get': 'friend_requests_list'})),
    path('friend/request/send/', UserAccountFriendsViewSet.as_view({'post': 'send_friend_request'})),
    path('friend/request/accept/', UserAccountFriendsViewSet.as_view({'post': 'accept_friend_request'})),
    path('friend/request/reject/', UserAccountFriendsViewSet.as_view({'post': 'reject_friend_request'})),
    path('friend/remove/', UserAccountFriendsViewSet.as_view({'post': 'remove_friend'}))
]
