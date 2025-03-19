from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *

# Create Class ImportExport Admin
## Resources Models
class MechanismDataResource(resources.ModelResource):
    class Meta:
        model = Mechanism_Data
        import_id_fields = ['MechanismID']


## Aaadmin Models
class MechanismDataAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = MechanismDataResource


class DriversAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class StoresAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class PartsAndRepairsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class RepairRequestsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class MechanismsRepairsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class StatementsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class ReceiptsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


# Register your models here.
admin.site.register(Mechanism_Data, MechanismDataAdmin)
admin.site.register(Repair_Requests, RepairRequestsAdmin)
admin.site.register(Mechanisms_Repairs, MechanismsRepairsAdmin)
admin.site.register(Parts_and_Repaires, PartsAndRepairsAdmin)
admin.site.register(Stores, StoresAdmin)
admin.site.register(Drivers, DriversAdmin)
admin.site.register(Statements, StatementsAdmin)
admin.site.register(Receipts, ReceiptsAdmin)
