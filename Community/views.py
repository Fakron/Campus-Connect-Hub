import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Q
from . models import Room,Topic,Message
from . forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
import uuid


@login_required(login_url='login')
def community(request):
    q = request.GET.get('q', '')
    topic_name = request.GET.get('topic', '')  # Get the selected topic from query parameters

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    
    # logged = request.user
    
    # for room in rooms:
    #     if logged in room.participant.all():
    #         print(True)
    
    
    logged_user = request.user
    
    # Retrieve the rooms (communities) that the user has joined
    joined_rooms = Room.objects.filter(participant=logged_user)
    
    # Retrieve the recent messages for the joined rooms
    recent_messages = Message.objects.filter(room__in=joined_rooms)


    
    # Filter rooms based on the selected topic
    if topic_name and topic_name != 'all':
        rooms = rooms.filter(topic__name__icontains=topic_name)

    topics = Topic.objects.all()
    room_count = rooms.count()
        

    recent_activity = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    
    return render(request, "Community/community.html", {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'recent_activity': recent_activity,'recent_messages':recent_messages})


@login_required(login_url='')
def room(request, pk):
    room = Room.objects.get(id=pk)
    print(room.host)
    user_rooms = Room.objects.filter(participant=request.user)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participant.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participant.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants,'user_rooms':user_rooms}
    return render(request, 'Community/ChatRoom.html', context)



@login_required
def join_room(request, pk):
    room = Room.objects.get(id=pk)
    if request.user not in room.participant.all():
        # User is not joined, so add them to the participant list
        room.participant.add(request.user)
    return redirect('community')  # Redirect back to the community page


@login_required(login_url='login')
def createRoom(request):
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user  # Set the host user to the current logged-in user
            
            room.unique_id = uuid.uuid4().hex[:6]  # Generate a random 6-character unique ID

            # Access the uploaded image file through form.cleaned_data
            uploaded_image = form.cleaned_data['image']
            # Now, save the uploaded image file to your storage
            room.image = uploaded_image  # Assign the image file to the room object
            print(uploaded_image)
            room.save()  # Save the room object to persist the changes
            return redirect('community')  # Redirect to some URL after room creation
    else:
        form = RoomForm()
    return render(request, 'Community/createcommunity.html', {'form': form, 'topics': topics})


@login_required(login_url='login')
def join_room_by_id(request, unique_id):
    room = Room.objects.filter(unique_id=unique_id).first()
    if room:
        if request.user not in room.participant.all():
            room.participant.add(request.user)
        return redirect('room', pk=room.id)  # Redirect to the room page
    else:
        # Handle invalid unique IDs
        return HttpResponse("Room not found or expired.")   

@login_required(login_url='login')
def updateRoom(request, pk):
    # Retrieve the room object by its ID
    room = get_object_or_404(Room, id=pk)
    topics = Topic.objects.all()

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('community')  # Redirect to some URL after room update
   
    else:
        # If it's a GET request, initialize the form with existing room data
        form = RoomForm(instance=room)

    return render(request, 'Community/updatecommunity.html', {'form': form, 'room':room,'topics': topics})


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # print("hello")
    # print("------------")
    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        # print("hello")
        if request.user == room.host:
            room.delete()
            # print("hello")
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

@login_required(login_url='login')
def update_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    
    #  # Print the request method (e.g., GET or POST)
    # print("Request method:", request.method)

    # # Print the request body
    # print("Request body:", request.body)

    if request.method == "POST":
        
        json_data = json.loads(request.body.decode('utf-8'))
        
        # Extract the new message body directly
        new_message_body = json_data['new_message_body'].strip()  # Remove leading/trailing whitespace if needed

        # Update the message body with the new message body
        message.body = new_message_body
        message.save()
        return JsonResponse({'success': True})  # Respond with a JSON success message
    

    return JsonResponse({'error': 'Invalid request'}) 



    
