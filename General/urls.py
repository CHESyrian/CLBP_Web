from django.urls import path
from . import views


urlpatterns = [
    path('permissions/', views.Permissions_Page, name='Permissions_Page'),
    path('save_permissions/', views.Save_Permissions, name='Save_Permissions'),
]
