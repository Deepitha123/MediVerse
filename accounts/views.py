from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
import cv2
import numpy as np
import base64
from io import BytesIO
from matplotlib import pyplot as plt
from django.shortcuts import render
from Deepskin.deepskin import wound_segmentation, evaluate_PWAT_score

def wound_analysis(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        img_array = np.frombuffer(image_file.read(), np.uint8)
        bgr = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

        wound_mask = wound_segmentation(rgb)
        pwat_score = evaluate_PWAT_score(rgb, wound_mask)

        if pwat_score <= 4:
            wound_type = "Mild / No wound"
        elif pwat_score <= 8:
            wound_type = "Moderate wound"
        elif pwat_score <= 12:
            wound_type = "Severe wound"
        else:
            wound_type = "Very Severe / Chronic wound"

        # Encode images to base64 for HTML display
        def encode_img(img):
            buffer = BytesIO()
            plt.imsave(buffer, img)
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode()

        original_image = encode_img(rgb)
        wound_mask_img = encode_img(wound_mask)

        return render(request, 'wound_analysis.html', {
            'pwat_score': round(pwat_score, 2),
            'wound_type': wound_type,
            'original_image': original_image,
            'wound_mask': wound_mask_img
        })
    return render(request, 'wound_analysis.html')


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
    if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please try another.")
            return render(request, 'register.html')  # Show error on the same page
    user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
    user.save()

    print("user created")
    return redirect('login')
  else:  
    return render(request, "register.html")
  

def health_status(request):
    return render(request, 'health_status.html')

def lifestyle_recommendations(request):
    return render(request, 'lifestyle_recommendations.html')