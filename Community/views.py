from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from . models import Room,Topic,Message
from . forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

# Create your views here.


# rooms = [
#     {'id':1, 'name':'lets Learn python'},
#     {'id':2, 'name':'lets Learn C'},
#     {'id':3, 'name':'lets Learn Java'},
# ]


@login_required(login_url='login')
def community(request):
    
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    
    topics = Topic.objects.all()
    room_count = rooms.count()

    recent_activity = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    # print(room_count)
    return render(request,"Community/community.html",{'rooms':rooms, 'topics':topics, 'room_count':room_count,'recent_activity':recent_activity})


@login_required(login_url='')
def room(request,pk):
    room = Room.objects.get(id=pk)
    print(room.host)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participant.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            
            user = request.user,
            room = room,
            body = request.POST.get('body')
            
        )
        room.participant.add(request.user)
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    
    return render(request,'Community/ChatRoom.html',context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('community')
        # else:
        #     form = RoomForm()
        
    context = {'form':form}
    return render(request,'Community/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('community')
    context = {'form':form}
    
    return render(request,'Community/room_form.html',context)


# @login_required(login_url='login')
# def deleteRoom(request, pk):
#     room = get_object_or_404(Room, pk=pk)
    
#     if request.user != room.host:
#         return HttpResponse('You are not allowed here')

#     if request.method == "POST":
#         room.delete()
#         return redirect('community')
    
#     return render(request, 'Community/delete.html', {'obj': room})



@login_required(login_url='login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    print("hello")
    # print(request.user)
    # print(room.host)
    print("------------")
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        print("hello")
        
        if request.user == room.host:
            room.delete()
            print("hello")
            messages.success(request, 'Question deleted successfully.')
            return redirect('community')
        else:
            messages.error(request, 'You are not authorized to delete this question.')
            return redirect(reverse('room', kwargs={'pk': pk}))
    
    return redirect('home')  




@login_required(login_url='login')
def deleteMessage(request,pk):
    
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == "POST":
        message.delete()
        return redirect('community')
    return render(request,'Community/delete.html',{'obj':message})
    