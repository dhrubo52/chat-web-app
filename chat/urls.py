from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="homepage"),
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('create/', views.create_room, name="create"),
    path('room/join/<str:roomName>/<str:adminName>/', views.join_room, name="join"),
    path('room/<str:roomName>/<str:adminName>/', views.enter_room, name="enter"),
    path('send/<str:roomName>/<str:adminName>/', views.send_message, name="send_message"),
    path('delete_room/', views.delete_room, name="delete_room"),
    path('get_message/<str:roomName>/<str:adminName>/', views.get_message, name="get_message"),
    path('get_room_list/', views.get_room_list, name="room_list"),
    path('get_user_list/<str:roomName>/<str:adminName>/', views.get_user_list, name="user_list"),
]