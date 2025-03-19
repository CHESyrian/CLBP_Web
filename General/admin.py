from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


# Create Class ImportExport Admin
## Resources Models


## Aaadmin Models
class SiteDictionaryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class UserPermissionsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass

# Register Models
admin.site.register(Site_Dictionary, SiteDictionaryAdmin)
admin.site.register(User_Permissions, UserPermissionsAdmin)
