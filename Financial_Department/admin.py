from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


# Create Class ImportExport Admin
## Resources Models


## Aaadmin Models
class MainBalanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class SubBalancesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

class SubBalanceItemsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

class ExchangeOrdersAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Main_Balance, MainBalanceAdmin)
admin.site.register(SubBalances, SubBalancesAdmin)
admin.site.register(SubBalance_Items, SubBalanceItemsAdmin)
admin.site.register(Exchange_Orders, ExchangeOrdersAdmin)
