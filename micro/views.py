from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username):
            return render(request, 'register.html', {'error': 'This username has already been registered,try another one'})
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return HttpResponseRedirect('/index')


def log_in(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'invalid username or password'})


def log_out(request):
    logout(request)
    return redirect('index')