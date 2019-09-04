import time
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .snap import snap, initial, get_position
from matplotlib import pyplot as plt
from matplotlib import image
from.models import Status


@login_required
def index(request):
    if request.method == 'GET':
        mmc = initial()
        mmc.setProperty('Cam', 'PixelType', '32bitRGB')
        sn = snap(mmc)
        src = sn['src']
        img = sn['array']
        dic = get_position(mmc)
        return render(request, 'index.html', {'src': src, 'mmc': mmc, 'X': dic['x'], 'Y': dic['y'], 'Z': dic['z'],
                                              'img':img})
    if request.method == 'POST':
        mmc= initial()
        x = float(request.POST.get('X'))
        y = float(request.POST.get('Y'))
        z = float(request.POST.get('Z'))
        mmc.setXYPosition(x, y)
        mmc.setPosition(z)
        mmc.snapImage()
        img = mmc.getImage()
        plt.imshow(img, cmap='gray')
        dic = get_position(mmc)
        sn = snap(mmc)
        src = sn['src']
        img = sn['array']

        return render(request, 'index.html', {'src': src, 'mmc': mmc, 'X': dic['x'], 'Y': dic['y'], 'Z': dic['z'],
                                              'img': img})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if len(username)<4 or len(password)<4 or len(email)<4:
            return render(request, 'register.html', {'error': 'username or password or email too short'})
        elif User.objects.filter(username=username):
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
        if len(username)<4 or len(password)<4 :
            return render(request, 'login.html', {'error': 'invaild input'})
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'invalid username or password'})


@login_required
def log_out(request):
    logout(request)
    return redirect('index')


@login_required
def sequential(request):
    if request.method=='GET':
        return render(request, 'sequential.html')
    if request.method=='POST':
        li = request.POST.get('position')
        li = li.strip(' ').split(' ')
        gap = int(request.POST.get('time'))
        repeat = int(request.POST.get('loop'))
        if repeat == 0:
            repeat = 1
        mmc = initial()
        i = 0
        while repeat:
            for pos in li:
                l_ = pos.split(',')
                x = int(l_[0])
                y = int(l_[1])
                mmc.setXYPosition(x,y)
                mmc.snapImage()
                pic = mmc.getImage()
                image.imsave(str(i)+'.png', pic)
                i += 1
            time.sleep(gap)
            repeat -= 1
        return render(request,'sequential.html',{'message': 'Success! images are saved'})


@login_required
def save_pic(request):
    if request.method=='POST':
        base64= request.POST.get('image')
        x=float(request.POST.get('x'))
        y=float(request.POST.get('y'))
        z=float(request.POST.get('z'))
        name = request.POST.get('status')
        status = Status.objects.filter(name=name).first()
        if not status:
            status = Status(name=name, pic=base64, x=x, y=y, z=z)
            status.save()
            return redirect('index')
        status.update(pic=base64,x=x,y=y,z=z)
        return redirect('index')


@login_required   
def comparison(request):
    if request.method=='GET':
        status1=Status.objects.filter(name="status1").first()
        status2=Status.objects.filter(name="status2").first()
        src1 = status1.pic
        src2 = status2.pic
        return render(request,'comparison.html',{'src1':src1,'src2':src2})


























