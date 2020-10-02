from django.contrib import admin
from .models import  RegLog, UserLogs,PaymentLog
# Register your models here.


class RegLogAdmin(admin.ModelAdmin):
    list_display = ('reg_log_id','PARTNER','adalias','user_name','mobile_no','reg_datetime','reg_device_id','platform')
    search_fields = ('PARTNER','adalias','user_name','mobile_no')
    list_filter   = ('PARTNER','adalias','user_name','mobile_no')

class UserLogsAdmin(admin.ModelAdmin):
    list_display = ('user_log_id','log_key','username','log_action','log_date','log_host','log_ip','browser_type','platform')
    search_fields = ('username','log_key','log_action','log_date')
    list_filter   = ('username','log_key','log_action','log_date')

class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('PaymentLog_id','username','Payment_Amount','Payment_Request','Payment_Response','Payment_date','Payment_diviceID','Payment_Status','SAPPOST_status','SAPPOST_date','SAP_Request','SAP_Response')
    search_fields = ('username','Payment_Status')
    list_filter   = ('username','Payment_date','Payment_Status')


admin.site.register(RegLog,RegLogAdmin)
admin.site.register(UserLogs,UserLogsAdmin)
admin.site.register(PaymentLog,PaymentLogAdmin)