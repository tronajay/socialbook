from django.contrib import admin
from accounts.models import User, FriendRequest

# Register your models here.
admin.site.register(User)
admin.site.register(FriendRequest)
