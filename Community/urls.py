from django.urls import path
from . import views

urlpatterns = [
    path("",views.community,name="community"),
    path('room/<str:pk>',views.room,name="room"),
    
]
