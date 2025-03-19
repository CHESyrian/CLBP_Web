from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/log_in/')
def Home_Page(request):
    return render(request, 'base.html')
