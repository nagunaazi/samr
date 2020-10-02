from django.contrib import admin
# from .models import UserMaster, UserTypeMaster, AccessTypeMaster
from .models import EducationMaster,UserTypeMaster, AccessTypeMaster, UserMaster, UserMasterDetails
from django.contrib.auth.admin import UserAdmin


class UserMasterAdmin(admin.ModelAdmin):
   list_display = ('username','first_name','last_name','adalias','bpcode','email','is_staff','is_active','is_superuser','date_joined')
   search_fields = ('first_name','adalias','bpcode','username')
   list_filter   = ('first_name','adalias','bpcode','username')

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('usermaster','access_type','user_type','from_date','to_date','status','create_date','update_date','create_user','update_user','last_login_on','mobile_no')
    search_fields = ('usermaster','access_type','user_type','mobile_no')
    list_filter   = ('usermaster','access_type','user_type','mobile_no')
# Register your models here.
admin.site.register(UserMaster, UserMasterAdmin)
admin.site.register(UserMasterDetails,UserDetailsAdmin)
admin.site.register(UserTypeMaster)
admin.site.register(AccessTypeMaster)
admin.site.register(EducationMaster)