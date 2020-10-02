from django.contrib import admin
from .models import TockenUser,BankList,BankTransactionPRD,BillConfirmation,BankTransaction,EmailBodyMaster,IncidentCommentDetail,IncidentFeedbackDetail,IncidentMaster,IncidentStatusTypeMaster,IncidentCategoryMaster,Hint,ContactUs,ServerMaster,SmsManager,SmsLog
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin


from .resources import BankListResource



class TockenUserAdmin(admin.ModelAdmin):
   list_display = ('Tocken_id','usermaster','device_id','Tocken_code','Notification_Leng','status','create_date','update_date','create_user','update_user')
   search_fields = ('Tocken_code','device_id','device_id')
   list_filter   = ('usermaster','device_id')

admin.site.register(TockenUser,TockenUserAdmin)




class BankListAdmin(ImportExportModelAdmin):
   list_display = ('Bank_id','Bank_Name','Bank_Type','Bank_URL','status','create_date','update_date','create_user','update_user')
   search_fields = ('Bank_Name','Bank_URL')
   list_filter   = ('Bank_Name','Bank_URL','status')
   resource_class = BankListResource

admin.site.register(BankList,BankListAdmin)






class BillConfirmationAdmin(admin.ModelAdmin):
   list_display = ('BillConfirmation_id','Bill_Period','Bill_No','BP_Code','Confirm_Status','Confirm_Remark','Bill_Amount','Bill_copies','Confirm_By','Device_On','Confirm_On')
   search_fields = ('BillConfirmation_id','Bill_Period','Bill_No','BP_Code')
   list_filter   = ('Bill_Period','BP_Code','Bill_No')

admin.site.register(BillConfirmation,BillConfirmationAdmin)









class BankTransactionAdmin(admin.ModelAdmin):
   list_display = ('Transaction_ID','Transaction_Bank','pan','van','tranAmt','trandate','Rem_name','Rem_name_rbi','utr','mode','Sender_receiver_info','ifsc','RemitterAcctNo','Response_To_Bank','Bank_Response_Json','status','create_date','update_date','create_user','update_user','get_from_bank_on','Post_To_SAP','Post_To_SAP_on','SAP_sent_Json','SAP_response_Json')
   search_fields = ('Transaction_ID','van','utr')
   list_filter   = ('van','utr','create_date')

admin.site.register(BankTransaction,BankTransactionAdmin)

class BankTransactionPRDAdmin(admin.ModelAdmin):
   list_display = ('Transaction_ID','Transaction_Bank','pan','van','tranAmt','trandate','Rem_name','Rem_name_rbi','utr','mode','Sender_receiver_info','ifsc','RemitterAcctNo','Response_To_Bank','Bank_Response_Json','status','create_date','update_date','create_user','update_user','get_from_bank_on','Post_To_SAP','Post_To_SAP_on','SAP_sent_Json','SAP_response_Json')
   search_fields = ('Transaction_ID','van','utr')
   list_filter   = ('van','utr','create_date')

admin.site.register(BankTransactionPRD,BankTransactionPRDAdmin)


class IncidentMasterAdmin(admin.ModelAdmin):
   list_display = ('Incident_Number',
    'Incident_Cat',
    'Incident_Status',
    'Incident_Text',
    'Incident_VKORG',
    'Incident_STATE',
    'Incident_BP_CODE',
    'Incident_Last_Feedback',
    'Incident_Last_Feedback_By',
    'Incident_Last_Feedback_On',
    'Incident_Last_Comment',
    'Incident_Last_Comment_By',
    'Incident_Last_Comment_On',
    'Incident_Last_assigned_to_code',
    'Incident_Last_assigned_to_Name',
    'Incident_Last_assigned_to_Level',
    'Incident_Last_assigned_on',
    'status',
    'create_date',
    'update_date',
    'create_user',
    'update_user')
   search_fields = ('Incident_Number','Incident_BP_CODE')
   list_filter   = ('Incident_STATE','Incident_VKORG','Incident_BP_CODE','create_date')



class IncidentCommentDetailAdmin(admin.ModelAdmin):
   list_display = ('IncidentComment_Number',
    'Incident_Number',
    'IncidentComment_Text',
    'Incident_Status',
    'IncidentComment_By',
    'IncidentComment_By_Name',
    'IncidentComment_By_Level',
    'IncidentComment_On',
    'status',
    'create_date',
    'update_date',
    'create_user',
    'update_user')
   search_fields = ('Incident_Number','IncidentComment_By')
   list_filter   = ('Incident_Number','IncidentComment_By','IncidentComment_By_Level','create_date','IncidentComment_On')

class IncidentFeedbackDetailAdmin(admin.ModelAdmin):
   list_display = ('IncidentFeedback_Number',
    'Incident_Number',
    'IncidentFeedback_Rating',
    'IncidentFeedback_Text',
    'IncidentFeedback_By',
    'IncidentFeedback_On',
    'status',
    'create_date',
    'update_date',
    'create_user',
    'update_user')
   search_fields = ('Incident_Number','IncidentFeedback_By')
   list_filter   = ('Incident_Number','IncidentFeedback_By','IncidentFeedback_On','create_date')




admin.site.register(ServerMaster)
admin.site.register(SmsManager)
admin.site.register(SmsLog)
admin.site.register(ContactUs)
admin.site.register(Hint)
admin.site.register(IncidentCategoryMaster)
admin.site.register(IncidentStatusTypeMaster)

admin.site.register(IncidentMaster,IncidentMasterAdmin)
admin.site.register(IncidentFeedbackDetail,IncidentFeedbackDetailAdmin)
admin.site.register(IncidentCommentDetail,IncidentCommentDetailAdmin)

admin.site.register(EmailBodyMaster)

