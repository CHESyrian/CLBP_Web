from django.urls import path
from . import views


urlpatterns = [
## Add/Edit/Delete DATA URLs
    path('add_rep_req/', views.Add_Repair_Request_Page, name='Add_Rep_Req'),
    path('adding_repreq/', views.Adding_Repair_Request, name='Adding_Rep_Req'),
    path('edit_repreq/', views.Edit_Repair_Request_Page, name='Edit_Rep_Req'),
    path('editing_repreq/', views.Editing_Repair_Request, name='Editing_RepReq'),
    path('deleting_mechrep/<int:rep_id>/', views.Deleting_Mechanisms_Repairs, name='Del_Mech_Repair'),
    path('add_receipts/', views.Add_Receipts_Page, name='Add_Receipts'),
    path('adding_receipts/', views.Adding_Receipts, name='Adding_Receipt'),
    path('add_statement/', views.Add_Statement, name='Add_Statement'),
    path('adding_statement/', views.Adding_Statement, name='Adding_Statement'),
    path('change_repreq_status/', views.Change_Repair_Request_Status, name='Change_RepReq_Status'),
    path('changing_repreq_status/', views.Changing_Repair_Request_Status, name='Changing_RepReq_Status'),
    path('enter_data/', views.Enter_Data_Page, name='Enter_Data'),
    path('enter_data/entering_drivers/', views.Entering_Drivers, name='Entering_Drivers'),
    path('enter_data/entering_stores/', views.Entering_Stores, name='Entering_Stores'),
    path('enter_data/entering_parts_repairs/', views.Entering_PartsRepairs, name='Entering_PartsRepairs'),

## View DATA YRLs
    path('view_data/', views.View_Data_Page, name='View_Data'),
    path('view_data/repair_requests/', views.View_Repair_Requests, name='View_RepReqs'),
    path('view_data/mechanisms_repairs/', views.View_Mechanisms_Repairs, name='View_MechsReps'),
    path('view_data/specific_table/<str:table>/', views.View_Data_Table, name='View_Data_Table'),
    path('view_data/data_filtering/',views.View_Data_Filtering_Page, name='View_Data_Filtering_Page'),
    path('view_data/data_filtering/<str:Table>/<str:Filter>/<str:Keyword>/<str:Year>/', views.View_Data_Filtering, name='View_Data_Filtering'),
## AJAX URLs
    path('getMechData/<str:mech_id>/', views.getMechData, name='Get_Mech_Data'),
    path('getRepairRequestData/<str:repreq_id>/', views.getRepairRequestData, name='Get_RepReq_Data'),
    path('getRepairsDetails/<str:repreq_id>/', views.getRepairsDetails, name='Get_Repairs_Details'),
    path('getRepairsDetailsD/<str:repreq_id>/', views.getRepairsDetails, name='Get_Repairs_Details'),
    path('checkRepairRequestID/<str:repreq_id>/', views.checkRepairRequestID, name='Chaeck_RepReq_ID'),
    path('getTableColumns/<str:table>/', views.getTableColumns, name='Get_Table_Columns'),
    path('getColumnValues/<str:table>/<str:column>/', views.getColumnValues, name='Get_Column_Values'),
]
