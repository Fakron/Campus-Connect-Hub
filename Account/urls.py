from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   #User Authentication
   path('login',views.user_login,name="login"),
   path('register',views.user_register,name="register"),

   #profile
   path('profile',views.user_profile,name="profile"),
   path('profile/update',views.user_profile_update,name="editprofile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
