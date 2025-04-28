from pyexpat.errors import messages
import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from . import forms
from .models import Business, UserProfile
# Create your views here.

def generate_code():
    test_code  = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    if Business.objects.filter(code=test_code).exists():
        return generate_code()
    return test_code

def sign_up(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']

            if role == 'EMPLOYER':
                business_code = generate_code()
                business = Business.objects.create(owner = user, name='Your name', code=business_code)
                user_profile = UserProfile.objects.create(user=user, role=role, business=business)
                user_profile.save()

            elif role == 'EMPLOYEE':
                business_code = form.cleaned_data['business_code']
                if not Business.objects.filter(code=business_code).exists():
                    messages.error(request, "Invalid business code.")
                    return render(request, 'registration/sign_up.html', {"form": form})
                business = Business.objects.get(code=business_code)
                UserProfile.objects.create(user=user, role=role, business=business)

            login(request, user)
            return redirect('/home')
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

