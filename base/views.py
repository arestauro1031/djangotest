from django.shortcuts import render  , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm


# Create your views here.

#rooms = [
 #   {'id': 1, 'name': 'Lets Play'},
  #  {'id': 2, 'name': 'Lets Duel'},
   # {'id': 3, 'name': 'Zone'},
#]


def loginPage(request):
    
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
        except:
            user = authenticate(request,username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username OR password does not exist')
    context = {'page':page}
    return render (request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
            
    return render (request, 'base/login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q')    if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | #used to search with topic name
        Q(name__icontains=q) |          #used to search with user name
        Q(description__icontains=q)  #used to search with description
        )         # This means that the variable rooms will be available in the template as a variable called rooms
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}      # This means that the variable rooms will be available in the template as a variable called rooms
    return render(request, 'base/home.html', context) #context refers to the value of the dictionary
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')  #-created to get the latest messages first
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
            
        )
        room.participants.add(request.user)
        return redirect ('room', pk=room.id)
    
    context = {'room': room, 'room_messages':room_messages, 'participants':participants}        
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topics= Topic.objects.all()
    context={'user':user, 'rooms':rooms, 'room_messagesd':room_message, 'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':            #  POST means the user has submitted the form
        topic_name = request.POST.get('topic')  
        topic, created = Topic.objects.get_or_create(name=topic_name)
        #print(request.POST)
        #request.POST.get('name')
        # form = RoomForm(request.POST)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
        
    context= {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk) # get the object
    form = RoomForm(instance=room) # create a form with the object
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')  
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room')
    if request.method == 'POST':
        room.delete()           # delete the object
        return redirect('home')  # after deletion, redirect to home
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('You are not authorized to edit this room')
    if request.method == 'POST':
        message.delete()           # delete the object
        return redirect('home')  # after deletion, redirect to home
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        
    
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    topics = Topic.objects.all()
    return render(request, 'base/topics.html', {})