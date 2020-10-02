from django.db import models
from master.models import AccessTypeMaster,UserMaster

# Create your models here.

class NotificationLog(models.Model):
    Nitification_Id = models.AutoField(primary_key=True)
    usermaster = models.ForeignKey(to=UserMaster, on_delete=models.PROTECT, null=True)
    Notification_Category =  models.TextField(max_length=50, blank=True, null=True) #models.ForeignKey(to=NotificationCategoryMaster, on_delete=models.PROTECT, null=False)
    State = models.TextField(max_length=50, blank=True, null=True)
    Notification_Leng = models.TextField(max_length=50, blank=True, null=True, default='EN')
    SalseOrg =  models.TextField(max_length=50, blank=True, null=True)
    BP_Code = models.TextField(max_length=30, blank=True, null=True)
    Notification_Title = models.TextField(max_length=255, blank=True, null=True)
    Screen_Name = models.TextField(max_length=255, blank=True, null=True)
    Notification_To = models.TextField(max_length=5000, blank=True, null=True)
    Notification_body = models.TextField(max_length=5000, blank=True, null=True)
    Sent_Status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Sent_On = models.DateTimeField(blank=True, null=True)
    Read_Status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Read_On = models.DateTimeField(blank=True, null=True)
    googleapis_Request_Body = models.TextField(max_length=5000, blank=True, null=True)
    googleapis_Response_Code = models.TextField(max_length=50, blank=True, null=True)
    googleapis_Response_Body = models.TextField(max_length=5000, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    class Meta:
        db_table = 'NotificationLog'

    def __str__(self):
        return str(self.Nitification_Id)



class NotificationCategoryMaster(models.Model):
    NotiCat_Id = models.AutoField(primary_key=True)
    # NotiCat_Code = models.TextField(max_length=50, blank=False, null=False)
    NotiCat_Text = models.CharField(max_length=50, blank=False, null=False,unique=True)
    NotiCat_Screen = models.CharField(max_length=50, blank=False, null=False, default='Dashboard')
    
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    class Meta:
        db_table = 'NotificationCategoryMaster'

    def __str__(self):
        return self.NotiCat_Text



class SalesOrgMaster(models.Model):
    SalesOrg_Id = models.AutoField(primary_key=True)
    State_Code = models.TextField(max_length=50, blank=False, null=False)
    SalesOrg_Code = models.TextField(max_length=50, blank=False, null=False)
    SalesOrg_Text = models.TextField(max_length=250, blank=True, null=True)
    
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    class Meta:
        db_table = 'SalesOrgMaster'

    def __str__(self):
        return self.SalesOrg_Code





class StateMaster(models.Model):
    State_Id = models.AutoField(primary_key=True)
    State_Code = models.TextField(max_length=50, blank=False, null=False)
    State_Text = models.TextField(max_length=250, blank=False, null=False)
    State_Leng = models.TextField(max_length=50, blank=False, null=False, default='EN')
    
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    class Meta:
        db_table = 'StateMaster'

    def __str__(self):
        return self.State_Code



class TockenUser(models.Model):
    Tocken_id = models.AutoField(primary_key=True)
    usermaster = models.ForeignKey(to=UserMaster, on_delete=models.PROTECT, null=False)
    Tocken_code = models.CharField(max_length=255, blank=False, null=False)
    device_id = models.CharField(max_length=100, blank=True, null=True)
    Notification_Leng = models.CharField(max_length=100, blank=True, null=True,default='EN')
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)
    

    def __str__(self):
        return str(self.Tocken_id)

    
    class Meta:
        db_table = "TockenUser"

















class BankList(models.Model):
    Bank_id = models.AutoField(primary_key=True)
    Bank_Name = models.CharField(max_length=255, blank=False, null=False,unique=True)
    Bank_Type = models.CharField(max_length=30, blank=True, null=True)
    Bank_URL = models.CharField(max_length=255, blank=False, null=False)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)
    

    def __str__(self):
        return str(self.Bank_Name)

    
    class Meta:
        db_table = "BankList"



















class BillConfirmation(models.Model):
    BillConfirmation_id = models.AutoField(primary_key=True)
    Bill_Period = models.CharField(max_length=30, blank=True, null=True)
    Bill_No = models.CharField(max_length=30, blank=True, null=True)
    BP_Code = models.CharField(max_length=30, blank=True, null=True)
    Confirm_Status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    Confirm_Remark = models.TextField(max_length=255, blank=True, null=True)
    Confirm_By = models.CharField(max_length=255, blank=True, null=True)
    Device_On = models.CharField(max_length=255, blank=True, null=True)
    Confirm_On = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Bill_Amount = models.CharField(max_length=255, blank=True, null=True)
    Bill_copies = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return str(self.BillConfirmation_id)

    
    class Meta:
        db_table = "BillConfirmation"




class BankTransactionPRD(models.Model):
    Transaction_ID = models.AutoField(primary_key=True)
    Transaction_Bank = models.CharField(max_length=50, blank=False, null=False,default="IDBI BANK")
    pan  = models.CharField(max_length=16, blank=False, null=False)
    van = models.CharField(max_length=16, blank=False, null=False)
    tranAmt = models.CharField(max_length=20, blank=False, null=False)
    trandate = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    Rem_name = models.CharField(max_length=100, blank=False, null=False)
    Rem_name_rbi = models.CharField(max_length=100, blank=True, null=True)
    utr = models.CharField(max_length=35, blank=False, null=False,unique=True)
    mode = models.CharField(max_length=15, blank=False, null=False)
    Sender_receiver_info = models.CharField(max_length=200, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)
    RemitterAcctNo = models.CharField(max_length=35, blank=True, null=True)
    Response_To_Bank  = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Bank_Response_Json = models.TextField(max_length=5000, blank=True, null=True)

    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    get_from_bank_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Post_To_SAP  = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Post_To_SAP_on = models.DateTimeField(blank=True, null=True)
    SAP_sent_Json = models.TextField(max_length=5000, blank=True, null=True)
    SAP_response_Json = models.TextField(max_length=5000, blank=True, null=True)

   

    def __str__(self):
        return str(self.Transaction_ID)

    
    class Meta:
        db_table = "BankTransactionPRD"


















class BankTransaction(models.Model):
    Transaction_ID = models.AutoField(primary_key=True)
    Transaction_Bank = models.CharField(max_length=50, blank=False, null=False,default="IDBI BANK")
    pan  = models.CharField(max_length=16, blank=False, null=False)
    van = models.CharField(max_length=16, blank=False, null=False)
    tranAmt = models.CharField(max_length=20, blank=False, null=False)
    trandate = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    Rem_name = models.CharField(max_length=100, blank=False, null=False)
    Rem_name_rbi = models.CharField(max_length=100, blank=True, null=True)
    utr = models.CharField(max_length=35, blank=False, null=False,unique=True)
    mode = models.CharField(max_length=15, blank=False, null=False)
    Sender_receiver_info = models.CharField(max_length=200, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)
    RemitterAcctNo = models.CharField(max_length=35, blank=True, null=True)
    Response_To_Bank  = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Bank_Response_Json = models.TextField(max_length=5000, blank=True, null=True)

    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    get_from_bank_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Post_To_SAP  = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    Post_To_SAP_on = models.DateTimeField(blank=True, null=True)
    SAP_sent_Json = models.TextField(max_length=5000, blank=True, null=True)
    SAP_response_Json = models.TextField(max_length=5000, blank=True, null=True)

   

    def __str__(self):
        return str(self.Transaction_ID)

    
    class Meta:
        db_table = "BankTransaction"














class EmailBodyMaster(models.Model):
    EmailBody_Number = models.AutoField(primary_key=True)
    EmailBody_For = models.CharField(max_length=30, blank=True, null=True)
    EmailBody_Len = models.CharField(max_length=2, blank=True, null=True,default="EN")
    EmailBody_Subject = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Header = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Line1 = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Line2 = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Line3 = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Line4 = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Line5 = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Line6 = models.TextField(max_length=255, blank=True, null=True)
    EmailBody_Bottom = models.TextField(max_length=255, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return str(self.IncidentFeedback_Number)

    
    class Meta:
        db_table = "EmailBodyMaster"













class IncidentFeedbackDetail(models.Model):
    IncidentFeedback_Number = models.AutoField(primary_key=True)
    Incident_Number = models.ForeignKey(to="IncidentMaster", to_field="Incident_Number", on_delete=models.PROTECT, null=False)
    IncidentFeedback_Rating = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    IncidentFeedback_Text = models.TextField(max_length=255, blank=True, null=True)
    IncidentFeedback_By = models.CharField(max_length=30, blank=True, null=True)
    IncidentFeedback_On = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return str(self.IncidentFeedback_Number)

    
    class Meta:
        db_table = "IncidentFeedbackDetail"










class IncidentCommentDetail(models.Model):
    IncidentComment_Number = models.AutoField(primary_key=True)
    Incident_Number = models.ForeignKey(to="IncidentMaster", to_field="Incident_Number", on_delete=models.PROTECT, null=False)
    IncidentComment_Text = models.TextField(max_length=255, blank=True, null=True)
    Incident_Status = models.ForeignKey(default=2,to="IncidentStatusTypeMaster", to_field="IncidentStatus_id", on_delete=models.PROTECT, null=False)
    IncidentComment_By = models.CharField(max_length=30, blank=True, null=True)
    IncidentComment_By_Name = models.CharField(max_length=150, blank=True, null=True)
    IncidentComment_By_Level = models.ForeignKey(to="master.AccessTypeMaster", to_field="access_type", on_delete=models.PROTECT, null=True)#models.CharField(max_length=150, blank=True, null=True)
    IncidentComment_On = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return str(self.IncidentComment_Number)

    
    class Meta:
        db_table = "IncidentCommentDetail"



class IncidentMaster(models.Model):
    Incident_Number = models.AutoField(primary_key=True)
    Incident_Cat = models.ForeignKey(to="IncidentCategoryMaster", to_field="IncidentCategory_id", on_delete=models.PROTECT, null=False)
    Incident_Status = models.ForeignKey(default=2,to="IncidentStatusTypeMaster", to_field="IncidentStatus_id", on_delete=models.PROTECT, null=False)
    Incident_Text = models.TextField(max_length=255, blank=False, null=False)
    Incident_VKORG = models.CharField(max_length=10, blank=True, null=True)
    Incident_STATE = models.CharField(max_length=10, blank=True, null=True)
    Incident_BP_CODE  = models.CharField(max_length=30, blank=False, null=False)
    Incident_Last_Feedback = models.TextField(max_length=255, blank=True, null=True)
    Incident_Last_Feedback_By = models.CharField(max_length=30, blank=True, null=True)
    Incident_Last_Feedback_On = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    Incident_Last_Comment = models.TextField(max_length=255, blank=True, null=True)
    Incident_Last_Comment_By = models.CharField(max_length=30, blank=True, null=True)
    Incident_Last_Comment_On = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    Incident_Last_assigned_to_code = models.CharField(max_length=30, blank=True, null=True)
    Incident_Last_assigned_to_Name = models.CharField(max_length=50, blank=True, null=True)
    Incident_Last_assigned_to_Level = models.CharField(max_length=30, blank=True, null=True)
    Incident_Last_assigned_on = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return str(self.Incident_Number)

    def getallcomments(self):
        try:
            com = IncidentCommentDetail.objects.filter(Incident_Number=self,status=1)
        except IncidentCommentDetail.DoesNotExist as ex:
            com = None
        return com

    def getallfeedback(self):
        try:
            com = IncidentFeedbackDetail.objects.filter(Incident_Number=self,status=1)
        except IncidentFeedbackDetail.DoesNotExist as ex:
            com = None
        return com

    
    class Meta:
        db_table = "IncidentMaster"














class IncidentStatusTypeMasterManager(models.Manager):
    def get_by_natural_key(self, IncidentStatus_Text):
        return self.get(IncidentStatus_Text=IncidentStatus_Text)





class IncidentStatusTypeMaster(models.Model):
    IncidentStatus_id = models.AutoField(primary_key=True)
    IncidentStatus_Srno = models.IntegerField(default=1, blank=True, null=True)
    IncidentStatus_Text = models.TextField(max_length=255, blank=False, null=False)
    IncidentStatus_Status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)

    objects = IncidentStatusTypeMasterManager()
    class Meta:
        db_table = 'IncidentStatusTypeMaster'

    def __str__(self):
        return self.IncidentStatus_Text

    def natural_key(self):
        return (self.IncidentStatus_Text)



class IncidentCategoryMasterManager(models.Manager):
    def get_by_natural_key(self, IncidentCategory_Text):
        return self.get(IncidentCategory_Text=IncidentCategory_Text)



class IncidentCategoryMaster(models.Model):
    IncidentCategory_id = models.AutoField(primary_key=True)
    IncidentCategory_Srno = models.IntegerField(default=1, blank=True, null=True)
    IncidentCategory_Text = models.TextField(max_length=255, blank=False, null=False)
    
    IncidentCategory_Status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    
    objects = IncidentCategoryMasterManager()
    class Meta:
        db_table = 'IncidentCategory_Text'

    def __str__(self):
        return self.IncidentCategory_Text

    def natural_key(self):
        return (self.IncidentCategory_Text)



class Hint(models.Model):
    Hint_id = models.AutoField(primary_key=True)
    Hint_Srno = models.IntegerField(default=1, blank=True, null=True)
    Hint_Text = models.TextField(max_length=255, blank=False, null=False)
    Hint_Leng = models.TextField(max_length=2, blank=False, null=False,default='EN')
    Hint_Status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    
    class Meta:
        db_table = 'Hint'

    def __str__(self):
        return self.Hint_Text










class ContactUs(models.Model):
    ContactUs_id = models.AutoField(primary_key=True)
    ContactUs_Top = models.TextField(max_length=255, blank=False, null=False)
    ContactUs_Number = models.TextField(max_length=20, blank=False, null=False)
    ContactUs_EmailID = models.CharField(max_length=100, blank=True, null=True)
    ContactUs_Bottom = models.TextField(max_length=255, blank=False, null=False)
    ContactUs_Status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)

    class Meta:
        db_table = 'ContactUs'

    def __str__(self):
        return self.ContactUs_top








class ServerMaster(models.Model):
    server_id = models.AutoField(primary_key=True)
    server_text = models.TextField(max_length=50, blank=False, null=False)
    server_host = models.TextField(max_length=50, blank=False, null=False)
    server_username = models.CharField(max_length=255, blank=True, null=True)
    server_password = models.CharField(max_length=255, blank=True, null=True)
    server_status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)

    class Meta:
        db_table = 'ServerMaster'

    def __str__(self):
        return self.server_text


class SmsManager(models.Model):
    sms_for = models.CharField(max_length=20, unique=True, blank=False, null=False)
    sms_host = models.CharField(max_length=255,  blank=False, null=False)
    sms_user = models.CharField(max_length=30,  blank=False, null=False)
    sms_password = models.CharField(max_length=25,  blank=False, null=False)
    sms_body_first = models.CharField(max_length=255,  blank=False, null=False)
    sms_body_second = models.CharField(max_length=255,  blank=False, null=False)
    sms_body_third = models.CharField(max_length=255,  blank=False, null=False)
    sms_from = models.CharField(max_length=20, blank=False, null=False)
    sms_status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return self.sms_host

    class Meta:
        db_table = 'SmsManager'


class SmsLog(models.Model):
    sms_id = models.AutoField(primary_key=True)
    sms_from_page = models.CharField(max_length=20, blank=False, null=False)
    sms_body = models.CharField(max_length=255,  blank=False, null=False)
    sms_to = models.CharField(max_length=15,  blank=False, null=False)
    sms_response = models.CharField(max_length=255,  blank=False, null=False)
    sms_send_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.sms_body

    class Meta:
        db_table = 'SmsLog'
