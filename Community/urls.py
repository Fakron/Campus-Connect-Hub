from django.urls import path
from . import views

urlpatterns = [
    path("",views.community,name="community"),
    path('room/<str:pk>',views.room,name="room"),
    
    path('create-room',views.createRoom,name="create-room"),
    path('update-room/<str:pk>',views.updateRoom,name="update-room"),
    path('join-room/<str:pk>/', views.join_room, name='join-room'),
    path('delete-room/<str:pk>',views.deleteRoom,name="delete-room"),
    path('delete-message/<str:pk>',views.deleteMessage,name="delete-message"),
    path('update_message/<str:pk>/', views.update_message, name='update_message'),
    path('delete_message/<str:pk>/', views.deleteMessage, name='delete_message'),
    path('leave-room/<str:pk>',views.leave_room,name="leave-room"),
    path('join/<str:unique_id>/', views.join_room_by_id, name='join_room_by_id'),
    
]
