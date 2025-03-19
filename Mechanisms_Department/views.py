from builtins import Exception, int, len, range, str, sum
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from CC_Package.functions import DataFrame_from_Table, getName
from .models import Mechanism_Data, Repair_Requests, Mechanisms_Repairs, Drivers, Parts_and_Repaires, Stores, Receipts, Statements
from datetime import datetime as dt


# Perms -> [app name].[action].[model name]
# Actios [add, change, delete, view]
# Repairs Requests Functions (Views)...

## ENTERING DATA
@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.add_repair_request', raise_exception=True)
def Add_Repair_Request_Page(request):
    MechsID       = Mechanism_Data.objects.values_list('MechanismID', flat=True)
    Drivers_Name  = Drivers.objects.values_list('Driver_Name', flat=True)
    Stores_Name   = Stores.objects.values_list('Store_Name', flat=True)
    Repairs       = Parts_and_Repaires.objects.values_list('Name')
    Context = {
        'MechsID' : list(MechsID),
        'Drivers' : list(Drivers_Name),
        'Stores'  : list(Stores_Name),
        'Repairs' : list(Repairs)
    }
    return render(request, 'Mech_Dep/add_repreq.html', Context)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.add_repair_request', raise_exception=True)
def Adding_Repair_Request(request):
    if request.method == "POST":
        try:
            # Request Details
            Mech_ID         = request.POST.get('Mech_ID')
            Req_No          = request.POST.get('Req_No')
            Req_Date        = request.POST.get('Req_Date')
            Y, M, D         = Req_Date.split('-')
            Kilometers      = request.POST.get('Kilometers')
            Driver_Name     = request.POST.get('Driver_Name')
            Approval        = request.POST.get('Approval')
            Rep_Type        = request.POST.get('Rep_Type')
            Expected_Cost   = request.POST.get('Expected_Cost')
            Req_Status      = request.POST.get('RepReq_Status')
            # Get Objectss
            Mech_Obj   = Mechanism_Data.objects.get(pk=Mech_ID)
            # Repairs Details
            Repairs         = request.POST.getlist('Repairs')
            Quantity        = request.POST.getlist('Quantity')
            Type            = request.POST.getlist('Type')
            Cost            = request.POST.getlist('Cost')
            Stores_Names    = request.POST.getlist('Store_Name')
            Receipt_No      = request.POST.getlist('Receipt_No')
            Repairs_Details = [Repairs, Quantity, Type, Cost, Stores_Names, Receipt_No]
            # Check Driver & Stores if exists
            if not Drivers.objects.filter(Driver_Name=Driver_Name).exists():
                Drivers.objects.create(
                    Driver_Name  = Driver_Name,
                    Mechanism_No = Mech_Obj,
                    Disposal     = Mech_Obj.Disposal
                )
            for store_name in Stores_Names:
                if not Stores.objects.filter(Store_Name=store_name).exists():
                    Stores.objects.create(Store_Name=store_name)
            # Create Repair Request Object
            Mech_Model = Mech_Obj.Brand + " " + Mech_Obj.Model
            Real_Cost  = sum([int(x) for x in Cost])
            RepReq_Obj = Repair_Requests.objects.create(
                    Request_ID     = Req_No + "_" + Req_Date.split('-')[0],
                    Request_No     = Req_No,
                    Request_Date   = Req_Date,
                    Year           = Y,
                    Month          = M,
                    Day            = D,
                    Mechanism_No   = Mech_Obj,
                    KiloMeters     = Kilometers,
                    Ownership      = Mech_Obj.Ownership,
                    Disposal       = Mech_Obj.Disposal,
                    Model          = Mech_Model ,
                    Expected_Cost  = Expected_Cost,
                    Approval       = Approval,
                    Driver         = Driver_Name,
                    Real_Cost      = Real_Cost,
                    Repair_Type    = Rep_Type,
                    Status         = Req_Status
                )
            # Get Request Obj
            Req_ID  = Req_No + "_" + Req_Date.split('-')[0]
            Req_Obj = Repair_Requests.objects.get(pk=Req_ID)
            # Split Repairs Details for Saving
            bulk_list = []
            for n in range(len(Repairs)):
                try:
                    PCount = int(Quantity[n])
                except:
                    PCount = 1
                bulk_list.append(Mechanisms_Repairs(
                            Request_ID   = Req_Obj,
                            Part_Repair  = Repairs[n],
                            Part_Count   = PCount,
                            Part_Type    = Type[n],
                            Cost         = Cost[n],
                            Receipt_No   = Receipt_No[n],
                            Store        = Stores_Names[n],
                            Mechanism_No = Mech_ID,
                            Request_Date = Req_Date,
                            KiloMeters   = Kilometers,
                            Year         = Y,
                            Month        = M,
                            Day          = D
                        )
                    )
            # Create Mechaism Repairs Object
            MechReps_Obj = Mechanisms_Repairs.objects.bulk_create(bulk_list)
            # Create Parts and Repairs if not exists
            PartsReps_List = []
            for Rep in Repairs:
                if not Parts_and_Repaires.objects.filter(Name=Rep).exists():
                    PartsReps_List.append(Parts_and_Repaires(Name=Rep))
            Parts_and_Repaires.objects.bulk_create(PartsReps_List)
            json_resp = {
                'Status'  : True,
                'Message' : 'تم الحفظ'
            }
            return JsonResponse(json_resp)

        except Exception as Err:
            json_resp = {
                'Status'  : False,
                'Message' : str(Err)
            }
            return JsonResponse(json_resp)

    else:
        return HttpResponseRedirect(reverse('Add_Rep_Req'))

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
def Edit_Repair_Request_Page(request):
    return render(request, 'Mech_Dep/edit_repreq.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
def Editing_Repair_Request(request):
    if request.method == "POST":
        # Get Editing Information from POST
        RepReq_No    = request.POST.get('RepReq_No')
        RepReq_Year  = request.POST.get('RepReq_Year')
        RepReq_ID    = RepReq_No + "_" + RepReq_Year
        Editing_Type = request.POST.get('Editing_Type')
        # Do Editing Under Conditions
        try:
            if Editing_Type == "getRepairRequestData":
                # Get Repair Request Data from POST
                Mech_ID       = request.POST.get('Mech_ID')
                RepReq_Date   = request.POST.get('Req_Date')
                Kilometers    = request.POST.get('Kilometers')
                Driver_Name   = request.POST.get('Driver_Name')
                Approval      = request.POST.get('Approval')
                Repair_Type   = request.POST.get('Rep_Type')
                Expected_Cost = request.POST.get('Expected_Cost')
                # Get Mechanism Data as Object
                Mech_Obj       = Mechanism_Data.objects.get(pk=Mech_ID)
                Mech_Ownership = Mech_Obj.Ownership
                Mech_Desposal  = Mech_Obj.Disposal
                Mech_Model     = Mech_Obj.Brand + " " + Mech_Obj.Model
                # Editing Repair Request with New Data
                RepReq_Obj = Repair_Requests.objects.get(pk=RepReq_ID)
                RepReq_Obj.Request_ID     = RepReq_ID
                RepReq_Obj.Request_No     = RepReq_No
                RepReq_Obj.Request_Date   = RepReq_Date
                RepReq_Obj.Mechanism_No   = Mech_Obj
                RepReq_Obj.Mech_KMCount   = Kilometers
                RepReq_Obj.Mech_Ownership = Mech_Ownership
                RepReq_Obj.Mech_Disposal  = Mech_Desposal
                RepReq_Obj.Mech_Model     = Mech_Model
                RepReq_Obj.Expected_Cost  = Expected_Cost
                RepReq_Obj.Approval       = Approval
                RepReq_Obj.Driver         = Driver_Name
                RepReq_Obj.Repair_Type    = Repair_Type
                RepReq_Obj.save()
                # Return Json Response
                json_resp = {
                    'Status'  : True,
                    'Message' : 'تم حفظ التعديلات'
                }
                return JsonResponse(json_resp)

            elif Editing_Type == "getRepairsDetails":
                # Get Values from Request 'POST' as Lists.
                Repairs_IDs = request.POST.getlist('Repair_ID')
                Repairs     = request.POST.getlist('Repairs')
                Part_Count  = request.POST.getlist('Quantity')
                Part_Type   = request.POST.getlist('Type')
                Rep_Cost    = request.POST.getlist('Cost')
                Receipt_No  = request.POST.getlist('Receipt_No')
                Store_Name  = request.POST.getlist('Store_Name')
                # Get Repair Request Object.
                RepReq_Obj = Repair_Requests.objects.get(pk=RepReq_ID)
                # Make Editing for each Element or Creating it if New_ID.
                for i in range(len(Repairs_IDs)):
                    if Repairs_IDs[i] == "New_ID":
                        # Creating New Record in Mechanism Repairs Table and Saving it.
                        Mechanisms_Repairs.objects.create(
                            Request_ID  = RepReq_Obj,
                            Part_Repair = Repairs[i],
                            Part_Count  = int(Part_Count[i]),
                            Part_Type   = Part_Type[i],
                            Cost        = int(Rep_Cost[i]),
                            Receipt_No  = Receipt_No[i],
                            Store       = Store_Name[i]
                        )
                    else:
                        # Get Repair Details Object.
                        MechReps_Obj = Mechanisms_Repairs.objects.get(pk=Repairs_IDs[i])
                        # Editing Mechanism Repairs Object in New Values.
                        MechReps_Obj.Part_Repair = Repairs[i]
                        MechReps_Obj.Part_Count  = int(Part_Count[i])
                        MechReps_Obj.Part_Type   = Part_Type[i]
                        MechReps_Obj.Cost        = int(Rep_Cost[i])
                        MechReps_Obj.Receipt_No  = Receipt_No[i]
                        MechReps_Obj.Store       = Store_Name[i]
                        # Saving Repair Details Object with New Values
                        MechReps_Obj.save()
                    # Redirect to Edit Page
                json_resp = {
                    'Status'  : True,
                    'Message' : 'تم حفظ التعديلات'
                }
                return JsonResponse(json_resp)
        except Exception as Err:
            json_resp = {
                'Status'  : False,
                'Message' : str(Err)
            }
    else:
        return HttpResponseRedirect(reverse('Editing_RepReq'))

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.delete_mechanisms_repairs', raise_exception=True)
def Deleting_Mechanisms_Repairs(request, rep_id):
    try:
        MechRep_Obj = Mechanisms_Repairs.objects.get(pk=rep_id)
        MechRep_Obj.delete()
        json_resp = {
            'Status'  : True,
            'Message' : 'تم الحذف'
        }
        return JsonResponse(json_resp)
    except Exception as Err:
        json_resp = {
            'Status'  : False,
            'Message' : str(Err)
        }
        return  JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
def Add_Receipts_Page(request):
    return render(request, 'Mech_Dep/add_receipt.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
@permission_required('mechanisms_department.add_receipts', raise_exception=True)
def Adding_Receipts(request):
    if request.method == "POST":
        # Get Repair Request Data from POST
        RepReq_No       = request.POST.get('RepReq_No')
        RepReq_Year     = request.POST.get('Year')
        RepReq_ID       = RepReq_No + "_" + RepReq_Year
        A_Receipt_No    = request.POST.getlist('A_Receipt_No')
        A_Receipt_Date  = request.POST.getlist('A_Receipt_Date')
        A_Receipt_Value = request.POST.getlist('A_Receipt_Value')
        A_Stores_Names  = request.POST.getlist('A_Store_Name')
        Repairs_IDs     = request.POST.getlist('Repair_ID')
        Quantities      = request.POST.getlist('Quantity')
        Types           = request.POST.getlist('Type')
        Costs           = request.POST.getlist('Cost')
        Receipts_NOs    = request.POST.getlist('Receipt_No')
        Stores_Names    = request.POST.getlist('Store_Name')
        # Get RepairRequest Object and Check on Approval == Receipt Value
        RepReq_Obj   = Repair_Requests.objects.get(pk=RepReq_ID)
        Sum_Receipts = sum([int(x) for x in A_Receipt_Value])
        Sum_Costs    = sum([int(y) for y in Costs])
        Approval     = int(RepReq_Obj.Approval)
        if RepReq_Obj.Status == 'بانتظار الموافقة':
            json_resp = {
                'Status'  : False,
                'Message' : 'ان الطلب المرتبط بالفاتورة لم تتم الموافقة عليه بعد, الرجاء التأكد من الحالة.'
            }
            return JsonResponse(json_resp)
        if Sum_Receipts != Sum_Costs:
            json_resp = {
                'Status'  : False,
                'Message' : 'مجموع كلف الاصلاحات غير مطابق لمجموع قيم الفواتير' + '\n\n\n' +  f'{Sum_Costs}!={Sum_Receipts}'
            }
            return JsonResponse(json_resp)
        if (Sum_Receipts > Approval):
            json_resp = {
                'Status'  : False,
                'Message' : 'مجموع الفواتير اكبر من قيمة الموافقة' + '\n\n\n' +  f'{Approval}<{Sum_Receipts}'
            }
            return JsonResponse(json_resp)
        # Edit Repairs with New Values
        for i in range(len(Repairs_IDs)):
            Repair_Obj            = Mechanisms_Repairs.objects.get(pk=Repairs_IDs[i])
            Repair_Obj.Part_Count = Quantities[i]
            Repair_Obj.Part_Type  = Types[i]
            Repair_Obj.Cost       = Costs[i]
            Repair_Obj.Receipt_No = Receipts_NOs[i]
            Repair_Obj.Store      = Stores_Names[i]
            Repair_Obj.save()
        # Create New Receipts and Save it.
        for i in range(len(A_Receipt_No)):
            Receipt_ID = A_Receipt_No[i] + "_" + RepReq_ID
            Receipts.objects.create(
                Receipt_ID    = Receipt_ID,
                Receipt_No    = A_Receipt_No[i],
                Request_ID    = RepReq_Obj,
                Receipt_Value = A_Receipt_Value[i],
                Store_Name    = A_Stores_Names[i],
                Receipt_Date  = A_Receipt_Date[i]
            )
        # Change Repair Request Status
        RepReq_Obj.Status = 'تم التنفيذ'
        RepReq_Obj.save()
        # ِAdd New Store to Table Stores
        for store in Stores_Names:
            if not Stores.objects.filter(Store_Name=store).exists():
                Stores.objects.create(Store_Name=store)
        # Back to Add Receipt Page
        json_resp = {
            'Status'  : True,
            'Message' : 'تم الحفظ'
        }
        return JsonResponse(json_resp)
    else:
        return HttpResponseRedirect(reverse('Add_Receipts'))

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
def Change_Repair_Request_Status(request):
    return render(request, 'Mech_Dep/change_repreq_status.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
def Changing_Repair_Request_Status(request):
    if request.method == "POST":
        RepReq_No   = request.POST.get('RepReq_No')
        RepReq_Year = dt.now().year
        RepReq_ID   = RepReq_No + "_" + str(RepReq_Year)
        New_Status  = request.POST.get('RepReq_Status')
        try:
            if Repair_Requests.objects.filter(pk=RepReq_ID).exists():
                # Cheange & Save Repir Request Status
                RepReq_Obj        = Repair_Requests.objects.get(pk=RepReq_ID)
                RepReq_Obj.Status = New_Status
                RepReq_Obj.save()
                json_resp = {
                    'Status'  : True,
                    'Message' : 'تم الحفظ'
                }
                return JsonResponse(json_resp)
            else:
                json_resp = {
                    'Status'  : False,
                    'Message' : 'رقم الطلب غير موجود,الرجاء التأكد من الرقم'
                }
                return JsonResponse(json_resp)
        except Exception as Err:
            json_resp = {
                'Status'  : False,
                'Message' : str(Err)
            }
            return JsonResponse(json_resp)
    else:
        return HttpResponseRedirect(reverse('Change_RepReq_Status'))

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.add_statements', raise_exception=True)
def Add_Statement(request):
    return render(request, 'Mech_Dep/add_statement.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.add_statements', raise_exception=True)
def Adding_Statement(request):
    if request.method == "POST":
        # Get Statement Data from POST
        Statement_No    = request.POST.get('Statement_No')
        Statement_Year  = request.POST.get('Statement_Year')
        Statement_Value = request.POST.get('Statement_Value')
        SubBalance      = request.POST.get('SubBalance')
        Statement_Type  = request.POST.get('Statement_Type')
        RepReqs_NOs     = request.POST.getlist('RepReq_No')
        # Create Statement ID
        Statement_ID = Statement_No + "_" + Statement_Year + "_" + SubBalance + "_" + Statement_Type
        print(Statement_ID)
        # Create Statement
        Statements.objects.create(
            Statement_ID    = Statement_ID,
            Statement_No    = Statement_No,
            Statement_Type  = Statement_Type,
            Requests_No     = RepReqs_NOs,
            SubBalance      = SubBalance,
            Year            = Statement_Year,
            Statement_Value = Statement_Value
        )
        # Get Statement Object
        Statement_Obj = Statements.objects.get(pk=Statement_ID)
        # Save Statement in each Repair Request Record
        for repreq_no in RepReqs_NOs:
            repreq_id  = repreq_no + "_" + Statement_Year
            repreq_obj = Repair_Requests.objects.get(pk=repreq_id)
            repreq_obj.Statement = Statement_Obj.Statement_ID
            repreq_obj.save()
        return HttpResponseRedirect(reverse('Add_Statement'))
    else:
        return HttpResponseRedirect(reverse('Add_Statement'))

@login_required(login_url='/accounts/log_in/')
def Enter_Data_Page(request):
    return render(request, 'Mech_Dep/enter_data.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.add_drivers', raise_exception=True)
@permission_required('mechanisms_department.edit_drivers', raise_exception=True)
def Entering_Drivers(request):
    json_resp = {
        'Status'  : True, 
        'Message' : 'تم الحفظ'
    }
    return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.add_stores', raise_exception=True)
@permission_required('mechanisms_department.edit_stores', raise_exception=True)
def Entering_Stores(request):
    json_resp = {
        'Status'  : True, 
        'Message' : 'تم الحفظ'
    }
    return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.add_parts_and_repairs', raise_exception=True)
@permission_required('mechanisms_department.edit_parts_and_repairs', raise_exception=True)
def Entering_PartsRepairs(request):
    json_resp = {
        'Status'  : True, 
        'Message' : 'تم الحفظ'
    }
    return JsonResponse(json_resp)

## VIEWING DATA
@login_required(login_url='/accounts/log_in/')
def View_Data_Page(request):
    return render(request, 'Mech_Dep/view_data.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_requests', raise_exception=True)
def View_Repair_Requests(request):
    df      = DataFrame_from_Table(Repair_Requests)
    html_df = df.to_html(classes="Data-Table hover", table_id="RepReqs-Table", border=0.5)
    Context = {
        'Page_Title' : 'استعراض طلبات الاصلاح',
        'DataFrame'  : html_df
    }
    return render(request, 'General/view_data_table.html', Context)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_mechanisms_repairs', raise_exception=True)
def View_Mechanisms_Repairs(request):
    df      = DataFrame_from_Table(Mechanisms_Repairs)
    html_df = df.to_html(classes="Data-Table hover", table_id="MechsReps-Table", border=0.5)
    Context = {
        'Page_Title' : 'استعراض طلبات الاصلاح',
        'DataFrame'  : html_df
    }
    return render(request, 'General/view_data_table.html', Context)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_receipts', raise_exception=True)
@permission_required('mechanisms_department.view_statements', raise_exception=True)
def View_Data_Table(request, table):
    df = DataFrame_from_Table(table)
    html_df = df.to_html(classes="Data-Table hover", table_id=f"{table}-Table", border=0.5)
    Context = {
        'Page_Title' : 'استعراض البيانات',
        'DataFrame'  : html_df
    }
    return render(request, 'General/view_data_table.html', Context)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_requests', raise_exception=True)
@permission_required('mechanisms_department.view_mechanisms_repairs', raise_exception=True)
def View_Data_Filtering_Page(request):
    return render(request, 'Mech_Dep/view_data_filtering.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_requests', raise_exception=True)
@permission_required('mechanisms_department.view_mechanisms_repairs', raise_exception=True)
def View_Data_Filtering(request, Table, Filter, Keyword, Year):
    df      = DataFrame_from_Table(Table, Filter, Keyword, Year)
    html_df = df.to_html(classes="Data-Table hover", border=0.5)
    Context = {
        'Page_Title' : f'{Table} filtering by {Filter} - {Keyword} during {Year}',
        'DataFrame'  : html_df
    }
    return render(request, 'General/view_data_table.html', Context)

# Functions for Ajax Requests
@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_drivers', raise_exception=True)
def getDriversNames(request):
    drivers_names = Drivers.objects.values_list('Driver_Name')
    json_resp = {
        'Data' : drivers_names
    }
    return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in')
@permission_required('mechanisms_department.view_stores', raise_exception=True)
def getStoresNames(request):
    stores_names = Stores.objects.values_list('Store_Name')
    json_resp = {
        'Data' : stores_names
    }
    return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_mechanism_data', raise_exception=True)
def getMechanismsIDs(request):
    mechs_ids = Mechanism_Data.objects.values_list('MechanismID')
    json_resp = {
        'Data' : mechs_ids
    }
    return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_parts_and_repairs', raise_exception=True)
def getPartsRepairsNames(request):
    parts_repairs_names = Parts_and_Repaires.objects.values_list('Name')
    json_resp = {
        'Data' : parts_repairs_names
    }
    return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_mechanism_data', raise_exception=True)
def getMechData(request, mech_id):
    try:
        mech_data = Mechanism_Data.objects.get(pk=mech_id)
        mech_owsh = mech_data.Ownership
        mech_disp = mech_data.Disposal
        mech_brnd = mech_data.Brand
        mech_modl = mech_data.Model
        json_resp = {
            'Status'     : True,
            'Ownership'  : mech_owsh,
            'Disposal'   : mech_disp,
            'Model'      : f'{mech_brnd} - {mech_modl}',
        }
        return JsonResponse(json_resp)
    except Exception as Err:
        mech_id_check = Mechanism_Data.objects.filter(pk=mech_id).exists()
        if not mech_id_check:
            json_resp = {
                'Status'  : False,
                'Message' : 'عذرا,الآلية غير موجودة.الرجاء التأكد من الرقم',
            }
            return JsonResponse(json_resp)
        else:
            json_resp = {
                'Status'  : False,
                'Message' : str(Err)
            }
            return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_requests', raise_exception=True)
def getRepairRequestData(request, repreq_id):
    try:
        repreq_obj = Repair_Requests.objects.get(pk=repreq_id)
        repreq_data = {
            'Mech_ID'       : repreq_obj.Mechanism_No.MechanismID,
            'Ownership'     : repreq_obj.Mech_Ownership,
            'Disposal'      : repreq_obj.Mech_Disposal,
            'Model'         : repreq_obj.Mech_Model,
            'Req_No'        : repreq_obj.Request_No,
            'Req_Date'      : repreq_obj.Request_Date.strftime('%Y-%m-%d'),
            'Kilometers'    : repreq_obj.Mech_KMCount,
            'Approval'      : repreq_obj.Approval,
            'Real_Cost'     : repreq_obj.Real_Cost,
            'Expected_Cost' : repreq_obj.Expected_Cost,
            'Repir_Type'    : repreq_obj.Repair_Type,
            'Driver_Name'   : repreq_obj.Driver,
        }
        json_resp = {
            'Status' : True,
            'Data'   : repreq_data
        }
        return JsonResponse(json_resp)
    except Exception as Err:
        repreq_check = Repair_Requests.objects.filter(pk=repreq_id).exists()
        if not repreq_check:
            json_resp = {
                'Status'  : False,
                'Message' : 'عذرا,الطلب غير موجود.الرجاء ادخال رقم طلب صحيح'
            }
            return JsonResponse(json_resp)
        else:
            json_resp = {
                'Ststus'  : False,
                'Message' : str(Err)
            }
            return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_mechanisms_repairs', raise_exception=True)
def getRepairsDetails(request, repreq_id):
    try:
        repreq_obj       = Repair_Requests.objects.get(pk=repreq_id)
        req_status       = repreq_obj.Status
        rep_details_objs = Mechanisms_Repairs.objects.filter(Request_ID=repreq_obj).values()
        rep_details_list = [x for x in rep_details_objs]
        json_resp = {
            'Status'        : True,
            'RepReq_Status' : req_status,
            'Data'          : rep_details_list
        }
        return JsonResponse(json_resp)
    except Exception as Err:
        repreq_check = Repair_Requests.objects.filter(pk=repreq_id).exists()
        if not repreq_check:
            json_resp = {
                'Status'  : False,
                'Message' : 'عذرا, رقم الطلب غير موجود.الرجاء التأكد من رقم الطلب و السنة',
            }
            return JsonResponse(json_resp)
        else:
            json_resp = {
                'Status'  : False,
                'Message' : Err
            }
            return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_requests', raise_exception=True)
def checkRepairRequestID(request, repreq_id):
    if Repair_Requests.objects.filter(pk=repreq_id).exists():
        json_resp = {
            'Status'  : False,
            'Message' : f'رقم الطلب هذا موجود مسبقا,الرجاء التأكد من الرقم او التاريخ {repreq_id}'
        }
    else:
        json_resp = {
            'Status'  : True,
            'Message' : ''
        }
    return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_requests', raise_exception=True)
@permission_required('mechanisms_department.view_mechanisms_repairs', raise_exception=True)
def getTableColumns(request, table):
    try:
        Table     = eval(table)
        columns   = Table._meta.fields
        codes     = [f.get_attname() for f in columns]
        names     = getName(codes)
        json_resp = {
            'Status' : True,
            'Data'   : {
                'Names' : names,
                'Codes' : codes
            }
        }
        return JsonResponse(json_resp)
    except Exception as Err:
        json_resp = {
            'Status'  : False,
            'Message' : str(Err)
        }
        return JsonResponse(json_resp)

@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_requests', raise_exception=True)
@permission_required('mechanisms_department.view_mechanisms_repairs', raise_exception=True)
def getColumnValues(request, table, column):
    try:
        Table = eval(table)
        values = Table.objects.values_list(column, flat=True).distinct()
        values = list(values)
        json_resp = {
            'Status' : True,
            'Data'   : values
        }
        return JsonResponse(json_resp)
    except Exception as Err:
        json_resp = {
            'Status'  : False,
            'Message' : str(Err)
        }
        return JsonResponse(json_resp)