from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import authenticate, login as auth_login 
# Create your views here.

def register(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        faculty= request.POST['faculty']
        user = User.objects.create_user(username=username, password=password, email=email)
        Profile.objects.create(user=user, faculty=faculty)
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user) 
            return redirect(f'/home/{user.id}/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')
@login_required
def home(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(user=user)
        return render(request, 'home.html', {'user': user, 'profile': profile})
    except:
        return render(request, 'home.html', {'error': 'User not found'})
    
def logout_view(request):
    logout(request)
    return redirect('login')