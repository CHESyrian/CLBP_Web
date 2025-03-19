from builtins import eval, int, list, str, type
from django.db.models import Sum
from CC_Adminstration.settings import DATABASES
from General.models import Site_Dictionary
from Mechanisms_Department.models import Repair_Requests, Mechanisms_Repairs, Statements, Receipts
from Financial_Department.models import Exchange_Orders, SubBalance_Items
from pandas import DataFrame, read_sql
from numpy import zeros
import sqlite3
from datetime import datetime as dt


# Convert Numbers to Thousand Format
def thousand_groubing(value):
    return f'{value:,}'

# Translation using Site Dictionsry
## From Code to Name
def getName(code):
    if type(code) is str:
        name = Site_Dictionary.objects.get(Code=code).Name
        return name
    elif type(code) is list:
        #cn_dict = {}
        cn_list = []
        for x in code:
            N = Site_Dictionary.objects.get(Code=x).Name
            cn_list.append(N)
        return cn_list
    else:
        raise f"getName got one arg String or List, it got arg as {type(code)}"

## From Name to Code
def getCode(name):
    if type(name) is str:
        code = Site_Dictionary.objects.get(Name=name).Code
        return code
    elif type(name) is list:
        #cn_dict = {}
        cn_list = []
        for x in name:
            C = Site_Dictionary.objects.get(Name=x).Code
            cn_list.append(C)
        return cn_list
    else:
        raise f"getCode got one arg as String or List, it got arg as {type(code)}"

# Refresh Balances Data After Every Operation.
def RefreshBalances():
    ReqCost_Objs = Mechanisms_Repairs.objects.values('Request_ID', 'Cost')\
                                             .order_by('Request_ID')\
                                             .annotate(Total_Cost=Sum('Cost'))
    for Obj in ReqCost_Objs:
        # Get Object
        RepReq_Obj = Repair_Requests.objects.get(pk=Obj['Request_ID'])
        #Edit Object
        RepReq_Obj.Real_Cost = Obj['Total_Cost']
        # Save Object
        RepReq_Obj.save()
    # Read Data from Table and Processe it using Pandas
    DB    = DATABASES['default']['NAME']
    con   = sqlite3.connect(DB)
    table = Repair_Requests.objects.model._meta.db_table
    query = f"""SELECT * FROM {table}"""
    df    = read_sql(query, con)

# Read Data From Table and Return Pandas DataFrame
def DataFrame_from_Table(Data_Model, Filter=None, Keyword=None, Year='All'):
    # Set the Connect SQLIte
    DB  = DATABASES['default']['NAME']
    con = sqlite3.connect(DB)
    if type(Data_Model) is str:
        d_model = eval(Data_Model)
    else:
        d_model = Data_Model
    # Get Table Name from Model
    table = d_model.objects.model._meta.db_table
    # Get Data Without Filter for All Years
    if (Filter == None) and (Keyword == None) and (Year == 'All'):
        query_1 = f"""SELECT * FROM '{table}'"""
    # Get Data Without Filter for Specific Year
    elif (Filter == None) and (Keyword == None) and (Year != 'All'):
        query_1 = f"""SELECT * FROM '{table}' WHERE Year='{Year}'"""
        query_2 = f"""SELECT * FROM '{table}' WHERE Year_id='{Year}'"""
    # Get Data With Filter for All Years
    elif (Filter != None) and (Keyword != None) and (Year == 'All'):
        query_1 = f"""SELECT * FROM '{table}' WHERE {Filter}='{Keyword}'"""
    else:
        query_1 = f"""SELECT * FROM '{table}' WHERE {Filter}='{Keyword}' AND Year='{Year}'"""
        query_2 = f"""SELECT * FROM '{table}' WHERE {Filter}='{Keyword}' AND Year_id='{Year}'"""
    # Read the Data from Table
    try:
        df = read_sql(query_1, con)
    except:
        df = read_sql(query_2, con)
    # Change Columns Names
    df_columns  = list(df.columns)
    new_columns = getName(df_columns)
    df.columns  = new_columns
    # Close the Connection
    con.close()
    return df

# Get Balance by Ownership Function..
def Get_Balance_by_Ownership(Ownership):
    
    try:
        # Get Main Data & Tables
        year        = dt.now().year
        df_repreq   = DataFrame_from_Table(Data_Model=Repair_Requests, Year=year)
        df_exchords = DataFrame_from_Table(Data_Model=Exchange_Orders, Year=year)
        bal_item_1  = SubBalance_Items.objects.get(Account=f'{Ownership}_{year}', Item='اصلاح الآليات - صيانة دورية')
        bal_item_2  = SubBalance_Items.objects.get(Account=f'{Ownership}_{year}', Item='اصلاح الآليات - صيانة طارئة')
        # Create DataFrames for Balances
        Data = DataFrame(
                data=zeros((3, 7)),
                index=['الصيانة الدورية', 'الصيانة الطارئة', 'الرصيد الاجمالي'], 
                columns=['الرصيد الاساسي', 'المصروفات', 'الرصيد المتاح', 'اعتمادات محجوزة تم تنفيذها', \
                         'اعتمادات محجوزة قيد التنفيذ', 'الرصيد بعد صرف الاعتمادات', 'طلبات بانتظار الموافقة'],
                dtype='int64'
            )
        # Get Values from Tables
        # المصروفات
        c1 = df_exchords[(df_exchords['معرف - السنة'] == str(year)) & (df_exchords['معرف - الميزانية الفرعية'] == Ownership) & (df_exchords['معرف - بند الميزانية الفرعية']  == 'اصلاح الآليات - صيانة دورية')]['قيمة أمر الصرف'].sum()
        c2 = df_exchords[(df_exchords['معرف - السنة'] == str(year)) & (df_exchords['معرف - الميزانية الفرعية'] == Ownership) & (df_exchords['معرف - بند الميزانية الفرعية']  == 'اصلاح الآليات - صيانة طارئة')]['قيمة أمر الصرف'].sum()
        c3 = c1 + c2
        ## اعتمادات محجوزة تم تنفيذها
        x1 = df_repreq[(df_repreq['العائدية'] == Ownership) & (df_repreq['الحالة'] == 'تم التنفيذ') & ( df_repreq['نوع الاصلاح'] == 'صيانة دورية')]['التكلفة النهائية'].sum()
        x2 = df_repreq[(df_repreq['العائدية'] == Ownership) & (df_repreq['الحالة'] == 'تم التنفيذ') & ( df_repreq['نوع الاصلاح'] == 'صيانة طارئة')]['التكلفة النهائية'].sum()
        x3 = x1 + x2
        ## اعتمادات محجوزة قيد التنفيذ
        y1 = df_repreq[(df_repreq['العائدية'] == Ownership) & (df_repreq['الحالة'] == 'قيد التنفيذ') & ( df_repreq['نوع الاصلاح'] == 'صيانة دورية')]['الموافقة'].sum()
        y2 = df_repreq[(df_repreq['العائدية'] == Ownership) & (df_repreq['الحالة'] == 'قيد التنفيذ') & ( df_repreq['نوع الاصلاح'] == 'صيانة طارئة')]['الموافقة'].sum()
        y3 = y1 + y2
        ## طلبات بانتظار الموافقة
        z1 = df_repreq[(df_repreq['العائدية'] == Ownership) & (df_repreq['الحالة'] == 'بانتظار الموافقة') & ( df_repreq['نوع الاصلاح'] == 'صيانة دورية')]['التكلفة التقديرية'].sum()
        z2 = df_repreq[(df_repreq['العائدية'] == Ownership) & (df_repreq['الحالة'] == 'بانتظار الموافقة') & ( df_repreq['نوع الاصلاح'] == 'صيانة طارئة')]['التكلفة التقديرية'].sum()
        z3 = z1 + z2
        # Fill DataFrame
        Data['الرصيد الاساسي']            = [int(bal_item_1.Volume), int(bal_item_2.Volume), int(bal_item_1.Volume) + int(bal_item_2.Volume)]
        Data['المصروفات']                = [c1, c2, c3]
        Data['الرصيد المتاح']              = Data['الرصيد الاساسي'] - Data['المصروفات']
        Data['اعتمادات محجوزة تم تنفيذها'] = [x1, x2, x3]
        Data['اعتمادات محجوزة قيد التنفيذ'] = [y1, y2, y3]
        Data['الرصيد بعد صرف الاعتمادات'] = Data['الرصيد المتاح']  - (Data['اعتمادات محجوزة تم تنفيذها']  + Data['اعتمادات محجوزة قيد التنفيذ'])
        Data['طلبات بانتظار الموافقة']     = [z1, z2, z3]

        return Data
    except :
        Data = DataFrame(
                data=zeros((3, 7)),
                index=['الصيانة الدورية', 'الصيانة الطارئة', 'الرصيد الاجمالي'], 
                columns=['الرصيد الاساسي', 'المصروفات', 'الرصيد المتاح', 'اعتمادات محجوزة تم تنفيذها', \
                         'اعتمادات محجوزة قيد التنفيذ', 'الرصيد بعد صرف الاعتمادات', 'طلبات بانتظار الموافقة'],
            )
        Data['الرصيد الاساسي']                = ['غير متوفر', 'غير متوفر', 'غير متوفر']
        Data['المصروفات']                    = ['غير متوفر', 'غير متوفر', 'غير متوفر']
        Data['الرصيد المتاح']                = ['غير متوفر', 'غير متوفر', 'غير متوفر']
        Data['اعتمادات محجوزة تم تنفيذها']  = ['غير متوفر', 'غير متوفر', 'غير متوفر']
        Data['اعتمادات محجوزة قيد التنفيذ'] = ['غير متوفر', 'غير متوفر', 'غير متوفر']
        Data['الرصيد بعد صرف الاعتمادات']    = ['غير متوفر', 'غير متوفر', 'غير متوفر']
        Data['طلبات بانتظار الموافقة']      = ['غير متوفر', 'غير متوفر', 'غير متوفر']

        return Data

# Prepare Total Balance.
def Prepare_Balance(request):
    Data_1 = Get_Balance_by_Ownership('القيادة المركزية')
    Data_2 = Get_Balance_by_Ownership('الجبهة الوطنية التقدمية')
    Data_3 = Get_Balance_by_Ownership('مكتب الاتصال القومي')
    Data_4 = Get_Balance_by_Ownership('كتائب البعث')
    Data_5 = Get_Balance_by_Ownership('لجنة الرقابة و التفتيش الحزبية')
    # Convert DataFrame Numbers to Thousand Format
    Ds     = [Data_1, Data_2, Data_3, Data_4, Data_5]
    for D in Ds:
        for col in D.columns:
            D[col] = D[col].map(thousand_groubing)
    # Convert DataFrames to HTML.
    html_1  = Data_1.to_html(classes='balance-table')
    html_2  = Data_2.to_html(classes='balance-table')
    html_3  = Data_3.to_html(classes='balance-table')
    html_4  = Data_4.to_html(classes='balance-table')
    html_5  = Data_5.to_html(classes='balance-table')
    Context = {
        'Data_1' : html_1,
        'Data_2' : html_2,
        'Data_3' : html_3,
        'Data_4' : html_4,
        'Data_5' : html_5
    }

    return Context