from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from . import forms
# Create your views here.

def sign_up(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = forms.RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})