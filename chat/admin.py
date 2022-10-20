from django.contrib import admin
from .models import Room, Message, UserRoomList

# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserRoomList)