from django.contrib import admin
from .models import Room, Messege, UserRoomList

# Register your models here.

admin.site.register(Room)
admin.site.register(Messege)
admin.site.register(UserRoomList)