from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User

# Create your views here.

from django.contrib.auth.models import User
from .models import Profile

def user_register(request):
    if request.method == "POST":
        # Retrieve form data from request.POST
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        about = request.POST.get('about')  # Get about from form
        image = request.FILES.get('image')  # Get image from form

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
        user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
        user.save()

        # Create profile for the user
        profile = Profile.objects.create(user=user,about=about)
        profile.save()

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
    context = {
        "user":user,
    }
    return render(request,'Account/profile.html',context)


def user_profile_update(request):
    if request.method == 'POST':
        # Get the submitted data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        bio = request.POST.get('bio')
        
        # Update the user's profile information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()
        
        # Update the bio in the user's profile (assuming you have a related profile model)
        user.profile.about = bio
        user.profile.save()
        
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')  # Redirect to the user's profile page
    else:
        return render(request, 'Account/profile.html')
    

def update_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')
        confirm_password = request.POST.get('confirmPassword')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('change_password')  # Redirect back to the password change page

        # Check if the old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, 'Incorrect old password.')
            return redirect('change_password')  # Redirect back to the password change page

        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()

        # Update the session to prevent the user from being logged out
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was successfully updated!')
        return redirect('profile')  # Redirect to the profile page or any other desired page
    else:
        return render(request, 'Account/profile.html')