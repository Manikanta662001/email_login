from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
from django.core.mail import send_mail


from app.models import *







def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UD=UserForm(request.POST)
        PD=ProfileForm(request.POST,request.FILES)
        if UD.is_valid() and PD.is_valid():
            pw=UD.cleaned_data['password']
            USO=UD.save(commit=False)
            USO.set_password(pw)
            USO.save()

            PFO=PD.save(commit=False)
            PFO.user=USO
            PFO.save()

            send_mail(
                'user registration',
                'user registerd successfully',
                'gundlurimanikanta142@gmail.com',
                [USO.email],
                fail_silently=False
            )



            return HttpResponse('registration is successful')



    return render(request,'registration.html',d)



def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))

    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
@login_required
def profile_info(request):
    username=request.session.get('username')
    USD=User.objects.get(username=username)
    PFD=Profile.objects.get(user=USD)
    d={'USD':USD,'PFD':PFD}


    return render(request,'profile_info.html',d)
@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session.get('username')
        npw=request.POST['npw']
        UO=User.objects.get(username=username)
        UO.set_password(npw)
        UO.save()
        return HttpResponseRedirect(reverse('user_login'))
    return render(request,'change_password.html')


def reset_password(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['npw']
        LUSO=User.objects.filter(username=username)
        if LUSO:
            LUSO[0].set_password(password)
            LUSO[0].save()
        else:
            return HttpResponse('username is not available')
    return render(request,'reset_password.html')













































