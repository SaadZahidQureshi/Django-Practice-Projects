from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='signin_user')
def index(request):
    return render(request, 'index.html')


def profile(request):
    return render(request, 'profile.html')

def search(request):
    return render(request, 'search.html')

def settings(request):
    user_profile= Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            bio =user_profile.bio
            location =user_profile.location

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio =user_profile.bio
            location =user_profile.location

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            

    return render(request, 'setting.html', {'user_profile':user_profile})

def signup_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 =request.POST['password']
        password2 =request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup_user')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup_user')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                user_login = auth.authenticate(username=username, password=password1)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                id_user = user_model.id
                new_profile = Profile.objects.create(user=user, id_user=id_user)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password not matching..')    
            return redirect('signup_user')
    return render(request, 'signup_user.html')

def signin_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('signin_user')
    return render(request, 'signin_user.html')

@login_required(login_url='signin_user')
def logout_user(request):
    auth.logout(request)
    return redirect('signin_user')