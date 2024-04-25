from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
   #User Authentication
   path('login',views.user_login,name="login"),
   path('register',views.user_register,name="register"),
   path('logout',views.user_logout,name="logout"),

   #profile
   path('profile',views.user_profile,name="profile"),
   path('profile/update',views.user_profile_update,name="editprofile"),
   path('profile/password/update/', views.update_password, name='update_password'),
   
   

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
