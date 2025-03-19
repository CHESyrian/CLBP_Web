from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from CC_Package.functions import Prepare_Balance
from Mechanisms_Department.models import Repair_Requests
from .models import Main_Balance, SubBalances, SubBalance_Items, Exchange_Orders
from datetime import datetime as dt
from numpy import zeros


@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_request', raise_exception=True)
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
def Requests_Aggrement_Page(request):
    current_year = dt.now().year
    reqs_for_agg = Repair_Requests.objects.filter(Status='بانتظار الموافقة', Year=str(current_year))
    Context = {
        'Requests' : reqs_for_agg
    }
    return render(request, 'Fin_Dep/requests_aggrement.html', Context)

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.add_main_balance', raise_exception=True)
def Set_Main_Balance_Page(request):
    return render(request, 'Fin_Dep/set_main_balance.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.add_main_balance', raise_exception=True)
def Setting_Main_Balance(request):
    if request.method == "POST":
        Bal_Year     = request.POST.get('Bal_Year')
        Bal_Volume   = request.POST.get('Bal_Volume')
        Bal_Duration = request.POST.get('Bal_Duration')
        if not Main_Balance.objects.filter(pk=Bal_Year).exists():
            Main_Balance.objects.create(
                Year     = Bal_Year,
                Volume   = Bal_Volume,
                Duration = Bal_Duration
            )
            return HttpResponseRedirect(reverse('Fin_Dep'))
    else:
        return HttpResponseRedirect(reverse('Set_Main_Balance'))

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.add_subbalances', raise_exception=True)
def Set_SubBalance_Page(request):
    main_balance_year = dt.now().year
    Context = {
        'Year' : main_balance_year
    }
    return render(request, 'Fin_Dep/set_sub_balances.html', Context)

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.add_subbalances', raise_exception=True)
def Setting_SubBalance(request):
    if request.method == "POST":
        SubBal_Account  = request.POST.getlist('SubBal_Account')
        SubBal_Year     = request.POST.getlist('SubBal_Year')
        SubBal_Volume   = request.POST.getlist('SubBal_Volume')
        SubBal_Duration = request.POST.getlist('SubBal_Duration')
        # Checking on SubBalance_ID and Main_Balance.
        SubBalance_IDs = []
        for i in range(len(SubBal_Account)):
            SubBalance_ID = SubBal_Account[i] + "_" + str(SubBal_Year[i])
            SubBalance_IDs.append(SubBalance_ID)
            if not Main_Balance.objects.filter(pk=SubBal_Year[i]).exists() or SubBalances.objects.filter(pk=SubBalance_ID).exists():
                json_resp = {
                    'Status'  : False,
                    'Message' : f'<< {SubBal_Account[i]} || {SubBal_Year[i]} >>   الرجاء التأكد من اسم الحساب و السنة'
                }
                return JsonResponse(json_resp)
        for i in range(len(SubBal_Account)):
            MainBalance_Obj = Main_Balance.objects.get(pk=SubBal_Year[i])
            SubBalances.objects.create(
                SubBalance_ID = SubBalance_IDs[i],
                Account       = SubBal_Account[i],
                Year          = MainBalance_Obj,
                Volume        = SubBal_Volume[i],
                Duration      = SubBal_Duration[i]
            )
        json_resp = {
            'Status'  : True,
            'Message' : 'تم الحفظ'
        }
        return  JsonResponse(json_resp)
    else:
        return HttpResponseRedirect(reverse('Set_SubBalance'))

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.add_subbalance_items', raise_exception=True)
def Set_SubBalance_Item_Page(request):
    main_balance_year = dt.now().year
    accounts_values   = SubBalances.objects.filter(Year=main_balance_year).values_list('Account')
    Context = {
        'Year'     : main_balance_year,
        'Accounts' : set([x[0] for x in accounts_values])
    }
    return render(request, 'Fin_Dep/set_sub_balance_items.html', Context)

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.add_subbalance_items', raise_exception=True)
def Setting_SubBalance_Item(request):
    if request.method == "POST":
        SubBalItm_Account  = request.POST.getlist('SubBalItm_Account')
        SubBalItm_Year     = request.POST.getlist('SubBalItm_Year')
        SubBalItm_Item     = request.POST.getlist('SubBalItm_Item')
        SubBalItm_Volume   = request.POST.getlist('SubBalItm_Volume')
        SubBalItm_Duration = request.POST.getlist('SubBalItm_Duration')
        # Checking on SubBalance_ID and Main_Balance.
        SubBalance_IDs    = []
        SubBalanceItm_IDs = []
        for i in range(len(SubBalItm_Account)):
            SubBalance_ID    = SubBalItm_Account[i] + "_" + str(SubBalItm_Year[i])
            SubBalanceItm_ID = SubBalItm_Account[i] + "_" + SubBalItm_Item[i] + "_" + str(SubBalItm_Year[i])
            SubBalance_IDs.append(SubBalance_ID)
            SubBalanceItm_IDs.append(SubBalanceItm_ID)
            if not Main_Balance.objects.filter(pk=SubBalItm_Year[i]).exists() \
            or not SubBalances.objects.filter(pk=SubBalance_ID).exists() \
            or SubBalance_Items.objects.filter(pk=SubBalanceItm_ID).exists():
                json_resp = {
                    'Status'  : False,
                    'Message' : f'<< {SubBalItm_Account[i]} || {SubBalItm_Item[i]}  ||  {SubBalItm_Year[i]} >>   الرجاء التأكد من اسم الحساب و اسم البند و السنة'
                }
                return JsonResponse(json_resp)
        for i in range(len(SubBalItm_Account)):
            MainBalance_Obj = Main_Balance.objects.get(pk=SubBalItm_Year[i])
            SubBalance_Obj  = SubBalances.objects.get(pk=SubBalance_IDs[i])
            SubBalance_Items.objects.create(
                SubBalanceItem_ID = SubBalanceItm_IDs[i],
                Account           = SubBalance_Obj,
                Item              = SubBalItm_Item[i],
                Year              = MainBalance_Obj,
                Volume            = SubBalItm_Volume[i],
                Duration          = SubBalItm_Duration[i]
            )
        json_resp = {
            'Status'  : True,
            'Message' : 'تم الحفظ'
        }
        return  JsonResponse(json_resp)
    else:
        return HttpResponseRedirect(reverse('Set_SubBalance'))

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.view_main_balance', raise_exception=True)
@permission_required('financial_department.view_subbalances', raise_exception=True)
@permission_required('financial_department.view_subbalance_items', raise_exception=True)
@permission_required('mechanisms_department.view_repair_request', raise_exception=True)
@permission_required('mechanisms_department.view_statements', raise_exception=True)
def View_Balances_Page(request):
    return render(request, 'Fin_Dep/view_balances.html')

@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.view_main_balance', raise_exception=True)
@permission_required('financial_department.view_subbalances', raise_exception=True)
@permission_required('financial_department.view_subbalance_items', raise_exception=True)
@permission_required('mechanisms_department.view_repair_request', raise_exception=True)
@permission_required('mechanisms_department.view_statements', raise_exception=True)
def View_Repair_Balance_Page(request):
    Context = Prepare_Balance(request)
    return render(request, 'Fin_Dep/view_repair_balance.html', Context)

# Functions for Ajax Requests
@login_required(login_url='/accounts/log_in/')
@permission_required('mechanisms_department.view_repair_request', raise_exception=True)
@permission_required('mechanisms_department.edit_repair_request', raise_exception=True)
def giveAggrement(request, repreq_id):
    if request.method == 'POST':
        repreq_obj          = Repair_Requests.objects.get(pk=repreq_id)
        Approval            = int(request.POST.get('Approval'))
        repreq_obj.Approval = Approval
        repreq_obj.Status   = 'قيد التنفيذ'
        repreq_obj.save()
        return JsonResponse({'Message' : 'تم الحفظ'})
    else:
        return JsonResponse({'Message' : request.method})


@login_required(login_url='/accounts/log_in/')
@permission_required('financial_department.view_main_balance', raise_exception=True)
def checkMainBalance(request, year):
    if Main_Balance.objects.filter(pk=year).exists():
        json_resp = {
            'Status'  : True,
            'Message' : ''
        }
        return JsonResponse(json_resp)
    else:
        json_resp = {
            'Status'  : False,
            'Message' : 'الميزانية الاساسية غير موجودة,الرجاء اعداد الميزانية او التأكد من حقل "السنة"'
        }
        return JsonResponse(json_resp)
