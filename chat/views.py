from email.policy import HTTP
import json
from msilib.schema import Error
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Message, UserRoomList
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request=request, template_name='chat/user_home.html')

    return render(request=request, template_name='chat/home.html')

def create_account(request):
    if request.user.is_authenticated:
        return redirect('/user_home/')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            userName = form.cleaned_data.get('username')
            login(request, user)
            
            return redirect('/home/')
        else:
            for msg in form.errors:
                print(form.errors[msg])
            # print(form.errors)
            print(msg)
            return HttpResponse(form.errors[msg])
    else:
        form = UserCreationForm
        return render(request=request, template_name='chat/create_account.html',
            context={'form':form})        

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/home/')

    if(request.method == 'POST'):
        userName = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=userName, password=password)
        
        if user is not None:
            login(request, user)

        return redirect('/home/')
    else:
        return render(request, template_name='chat/login.html')

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/home/')

@login_required
def join_room(request, roomName, adminName):
    if request.method == 'POST':
        userName = request.user.username

        try:
            user = User.objects.get(username=userName)
        except:
            return HttpResponse('User does not exist.')
        try:
            room = Room.objects.get(room_name=roomName, admin_name=adminName)
        except:
            return HttpResponse('Room does not exist.')

        if room.password != request.POST['roomPassword']:
            return HttpResponse('Incorrect Room Password')
        else:
            try:
                roomList = UserRoomList.objects.get(user=user, room=room)
                return HttpResponse('You have already joined this room.')
            except:
                roomList = UserRoomList.objects.create(user=user, room=room)
                roomList.save()
                return redirect(f'/room/{roomName}/{adminName}')
    else:
        return HttpResponse('Error!')

@login_required(login_url='/login/')
def enter_room(request, roomName, adminName):
    userName = request.user.username

    try:
        user = User.objects.get(username=userName)
    except:
        return HttpResponse('User does not exist.')
    try:
        room = Room.objects.get(room_name=roomName, admin_name=adminName)
    except:
        return HttpResponse('Room does not exist.')
    try:
        roomList = UserRoomList.objects.get(user=user, room=room)
    except:
        return render(request=request, template_name='chat/join_room.html',
        context={'roomName':roomName, 'adminName':adminName})

    return render(request = request, template_name='chat/room.html',
        context={'roomName':roomName, 'adminName':adminName, 'password':room.password})

@login_required
def create_room(request):
    if request.method == 'POST':
        userName = request.user.username
        roomName = request.POST.get('roomName', 'default')
        roomPassword = request.POST.get('roomPassword')

        if roomName == '':
            return HttpResponse('Please enter a room name.')
        if roomPassword == '':
            return HttpResponse('Please enter a room password.')
        
        if(Room.objects.filter(room_name=roomName, admin_name=userName)):
            msg = '''This room already exists.
            You can not create multiple rooms with the same name.
            Please enter another Room Name.'''
            return HttpResponse(msg)

        room = Room.objects.create(room_name=roomName, admin_name=userName, message_count=0,  password=roomPassword)
        room.save()

        try:
            user = User.objects.get(username=userName)
        except:
            return

        roomList = UserRoomList.objects.create(user=user,room=room)
        roomList.save()

        return redirect(f'/room/{roomName}/{userName}/')
        # return render(request=request, template_name='chat/user_home.html',
        #     context={'roomName':roomName, 'userName':userName})
    else:
        return HttpResponse("Wrong Page!")
    
@login_required
def delete_room(request):
    roomName = request.POST.get('deleteRoomName')
    adminName = request.POST.get('deleteAdminName')
    userName = request.user.username

    if adminName != userName:
        return HttpResponse("You do not have permission to delete this room!")

    try:
        room = Room.objects.get(room_name=roomName, admin_name=adminName)
        room.delete()
    except:
        return HttpResponse("Room does not exist.")

    return redirect("/home/")

@login_required
def send_message(request, roomName, adminName):
    if request.method == 'POST':
        userName = request.user.username

        try:
            user = User.objects.get(username=userName)
        except:
            return HttpResponse('User does not exist')
        try:
            room = Room.objects.get(room_name=roomName, admin_name=adminName)
            roomList = UserRoomList.objects.get(user=user, room=room )
        except:
            return HttpResponse('You do not have access to this room.')
        else:
            req = json.loads(request.body)
            text = req['messageText']
            message = Message.objects.create(room=room, user_name=userName, text=text)
            message.save()
            room.message_count = room.message_count + 1
            room.save()

            return HttpResponse('ok')
    else:
        return HttpResponse('Error!')

@login_required
def get_message(request, roomName, adminName):
    userName = request.user.username

    try:
        user = User.objects.get(username=userName)
    except:
        return JsonResponse({'error':'User does not exist.'})
    try:
        room = Room.objects.get(room_name=roomName, admin_name=adminName)
    except:
        return HttpResponse({'error':'User does not exist.'})
    try:
        roomList = UserRoomList.objects.get(user=user, room=room)
    except:
        return JsonResponse({'error':'You do not have access to this room.'})
    else:
        msg = Message.objects.filter(room=room)

        text = []
        userName = []
        for i in msg:
            text.append(i.text)
            userName.append(i.user_name)

        return JsonResponse({'msgCount': room.message_count, 'text': text, 'user': userName})

@login_required
def get_room_list(request):
    userName = request.user.username
    try:
        user = User.objects.get(username=userName)
    except:
        return JsonResponse({'error':'User does not exist.'})
    
    userRooms = UserRoomList.objects.filter(user=user)

    roomList = []
    adminList = []
    for i in userRooms:
        roomList.append(i.room.room_name)
        adminList.append(i.room.admin_name)

    return JsonResponse({'roomList':roomList, 'adminList':adminList})

@login_required
def get_user_list(request, roomName, adminName):
    try:
        user = User.objects.get(username=adminName)
        room = Room.objects.get(room_name=roomName, admin_name=adminName)
    except:
        return JsonResponse({'error':'Room does not exist.'})
        
    usersInRoom = UserRoomList.objects.filter(room=room)

    userList = []
    for i in usersInRoom:
        userList.append(i.user.username)

    return JsonResponse({'userList':userList})




