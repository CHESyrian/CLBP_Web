from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def Login_Page(request):
    if request.user.is_authenticated:
        return HttpResponse('Logged In')
    else:
        return render(request, 'Accounts/login_page.html')

def LoggingIn(request):
    if request.method == 'POST':
        UserName  = request.POST.get('Log_UserName_Input')
        Password  = request.POST.get('Log_Password_Input')
        User_Auth = authenticate(username=UserName, password=Password)
        if User_Auth is not None:
            login(request, User_Auth)
            return HttpResponseRedirect(reverse('Home_Page'))
        else:
            return HttpResponseRedirect(reverse('Login_Page'))
    else:
        return HttpResponse(request.method == 'POST')

@login_required(login_url='/accounts/log_in/')
def LoggingOut(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_Page'))

@login_required(login_url='/accounts/log_in/')
def Settings(request):
    return render(request, 'Accounts/settings_page.html')

@user_passes_test(lambda user : user.is_superuser)
def Permissions_Page(request):
    pass

@user_passes_test(lambda user : user.is_superuser)
def Give_Permissions(request, user):
    pass
