from django.urls import path
from . import views


urlpatterns = [
    path('req_for_Aggrement/', views.Requests_Aggrement_Page, name='Req_Aggrement'),
    path('set_main_balance/', views.Set_Main_Balance_Page, name='Set_Main_Balance'),
    path('setting_main_balance/', views.Setting_Main_Balance, name='Setting_Main_Balance'),
    path('set_sub_balance/', views.Set_SubBalance_Page, name='Set_SubBalance'),
    path('setting_sub_balance/', views.Setting_SubBalance, name='Setting_SubBalance'),
    path('set_sub_balance_item/', views.Set_SubBalance_Item_Page, name='Set_SubBalance_Item'),
    path('setting_sub_balance_item/', views.Setting_SubBalance_Item, name='Setting_SubBalance_Item'),
    path('view_balances/', views.View_Balances_Page, name='View_Balances'),
    path('view_balances/repair_balance/', views.View_Repair_Balance_Page, name='View_Repair_Balance'),
## AJAX URLs
    path('giveAggrement/<str:repreq_id>/', views.giveAggrement, name='Give_Aggrement'),
    path('checkMainBalance/<str:year>/', views.checkMainBalance, name='Check_MainBalance'),
]
