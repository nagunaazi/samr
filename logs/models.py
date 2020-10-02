from django.db import models

# Create your models here.



class PaymentLog(models.Model):
    PaymentLog_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    Payment_Amount = models.CharField(max_length=255, blank=True, null=True)
    Payment_Request = models.TextField(max_length=5000, blank=True, null=True)
    Payment_Response = models.TextField(max_length=5000, blank=True, null=True)
    Payment_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Payment_diviceID = models.CharField(max_length=50, blank=True, null=True)
    Payment_Status = models.CharField(max_length=50, null=True, blank=True)
    SAPPOST_status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    SAPPOST_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    SAP_Request = models.TextField(max_length=5000, blank=True, null=True)
    SAP_Response = models.TextField(max_length=5000, blank=True, null=True)
    
    class Meta:
        db_table = "PaymentLog"

    def __str__(self):
        if self.PaymentLog_id:
            return self.PaymentLog_id










class RegLog(models.Model):
    reg_log_id = models.AutoField(primary_key=True)
    PARTNER = models.CharField(max_length=100, blank=True, null=True)
    adalias = models.CharField(max_length=30)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    reg_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    reg_device_id = models.CharField(max_length=100, blank=True, null=True)
    platform = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'RegLog'

    def __str__(self):
        return self.PARTNER


class UserLogs(models.Model):
    user_log_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    log_key = models.CharField(max_length=50, blank=True, null=True)
    log_action = models.CharField(max_length=250, blank=False, null=False)
    log_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    log_host = models.CharField(max_length=50, blank=True, null=True)
    log_ip = models.CharField(max_length=50, blank=True, null=True)
    browser_type = models.CharField(max_length=50, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = "UserLog"

    def __str__(self):
        if self.username:
            return self.username