from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout

User = get_user_model()

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')
    else:
        return redirect('index')  # fallback


@login_required
def editprofile(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'editprofile.html', {'user': user})

@login_required
def profile(request):
    user = request.user  
    return render(request, 'profile.html', {'user': user})

@login_required
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            print("user logged in")
            return redirect('/')
        else:
            print("invalid credentials")
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def register(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    password1 = request.POST['password']
    password2 = request.POST['confirm_password']
    email = request.POST['email']
    user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
    user.save()

    print("user created")
    return redirect('/')
  else:  
    return render(request, "register.html")


