from django.urls import path
from . import views


urlpatterns = [
    path('mech_dep/', views.Mech_Dep, name='Mech_Dep'),
    path('fin_dep/', views.Fin_Dep, name='Fin_Dep'),
]
