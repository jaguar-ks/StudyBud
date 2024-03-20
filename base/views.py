from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import UserCreationForm

# rooms = [
#     {'id':1, 'name':'Learn C'},
#     {'id':2, 'name':'Learn C++'},
#     {'id':3, 'name':'Learn Python'},
#     {'id':4, 'name':'Learn JavaScript'},
# ]

# Logging Page
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exists')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

# Logging out user
def logoutUser(request):
    logout(request)
    return redirect('home')

#Register
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'an allowed username or did not respect password policy')
    return render(request, 'base/login_register.html', {'form':form})

# Home Page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    msgs = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'msgs':msgs}
    return render(request, 'base/home.html', context)
    # return HttpResponse('Hello World!')

# Room Page
def room(request, pk):
    room = Room.objects.get(id=pk)
    msgs = room.message_set.all()
    members = room.members.all()
    if request.method == 'POST':
        msg = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)
    context = {'room':room, 'msgs':msgs, 'members':members}
    return render(request, 'base/room.html', context)
    # return HttpResponse('room')

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    msgs = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'msgs':msgs, 'topics':topics}
    return render(request, 'base/profile.html', context)

# Creating Room Page
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

# Updating Room info Page
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse('You are Not allowed to change the room imfo!!')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

# Deleting Room Page
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are Not allowed to change the room imfo!!')
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


# Deleting Message
@login_required(login_url='login')
def deleteMessage(request, pk):
    msg = Message.objects.get(id=pk)
    room = msg.room
    if request.user != msg.user and request.user != msg.room.host:
        return HttpResponse('You are Not allowed to change the room imfo!!')
    if request.method == "POST":
        msg.delete()
        return redirect('room', pk=room.id)
    return render(request, 'base/delete.html', {'obj':msg})

# def deleteMessage(request, pk):
#     room = Room.objects.get(id=pk)
#     msg = Message.objects.get(User=request.user)
#     return redirect('room', pk=room.id)
