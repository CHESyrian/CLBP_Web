from django.urls import path
from . import views


urlpatterns = [
    path('log_in/', views.Login_Page, name='Login_Page'),
    path('logging_in/', views.LoggingIn, name='LoggingIn'),
    path('logging_out/', views.LoggingOut, name='LoggingOut'),
    path('settings/', views.Settings, name='Settings'),
]
