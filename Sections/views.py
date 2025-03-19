from django.shortcuts import render

# Create your views here.
def Mech_Dep(request):
    return render(request, 'Sections/mech_dep_page.html')


def Fin_Dep(request):
    return render(request, 'Sections/fin_dep_page.html')
