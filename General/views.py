from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
def Permissions_Page(request):
    Users     = User.objects.values()
    UserNames = [x['username'] for x in Users]
    Context   = {'UserNames' : UserNames}
    return render(request, 'General/permissions_page.html', Context)

def Save_Permissions(request):
    if request.method == "POST":
        mech_perms = request.POST.getlist('Mech_Perms')
        return HttpResponse('PERMISSIONS')
