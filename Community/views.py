from django.shortcuts import render,redirect
from . models import Room
from . forms import RoomForm
# Create your views here.


# rooms = [
#     {'id':1, 'name':'lets Learn python'},
#     {'id':2, 'name':'lets Learn C'},
#     {'id':3, 'name':'lets Learn Java'},
# ]


def community(request):
    rooms = Room.objects.all()
    return render(request,"Community/community.html",{'rooms':rooms})

# rooms = Room.objects.all()

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    
    return render(request,'Community/room.html',context)



def createRoom(request):
    form = RoomForm
    
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('community')
        # else:
        #     form = RoomForm()
        
    context = {'form':form}
    return render(request,'Community/room_form.html',context)


def updateRoom(request,pk):
    
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('community')
    context = {'form':form}
    
    return render(request,'Community/room_form.html',context)


def deleteRoom(request,pk):
    
    room = Room.objects.get(id=pk)
    
    if request.method == "POST":
        room.delete()
        return redirect('community')
    return render(request,'Community/delete.html',{'obj':room})
    
    