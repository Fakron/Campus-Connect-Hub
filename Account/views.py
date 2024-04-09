from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm,UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.

def user_register(request):
    if request.method == "POST":
        # Retrieve form data from request.POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'Account/register.html')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return render(request, 'Account/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return render(request, 'Account/register.html')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Render registration form with success message
        messages.success(request, f'Account Successfully Created for {username}! Login Now')
        return render(request, 'Account/register.html')

    else:
        # If request method is not POST, render the registration form
        return render(request, 'Account/register.html')



def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Login successful.')
            return redirect('home')
        else:
            messages.error(request,'Invalid Login Credentials.')

    return render(request,'Account/login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):

    user = request.user
    # image = user.profile.image.url
    # if user.profile.image.url 
    
    return render(request,'Account/profile.html')


def user_profile_update(request):

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f'Account updated successfully')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    context = {
        
        'user_form' : user_form,
        'profile_form':profile_form,

        }

    return render(request,'Account/editprofile.html',context)