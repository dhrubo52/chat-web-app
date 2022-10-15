from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    room_name = models.CharField(max_length=20)
    admin_name = models.CharField(max_length=20, null=True)
    messege_count = models.IntegerField()
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.room_name

class Messege(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20)
    text = models.TextField(max_length=1000)

    def __str__(self):
        return (self.room.room_name+' - '+self.user_name)

class UserRoomList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return(self.user.username+' - '+self.room.room_name)