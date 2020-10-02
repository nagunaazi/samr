from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, User, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.backends import django

from .managers import CustomUserManager

date_format = '%Y-%m-%d %H:%M:%S'



class EducationMaster(models.Model):
    Education_code = models.AutoField(primary_key=True)
    Education_text = models.CharField(max_length=100, blank=False, null=False)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return self.Education_text

    
    class Meta:
        db_table = "EducationMaster"





class UserMaster(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    adalias = models.PositiveSmallIntegerField(default=0) # for internal users
    bpcode = models.PositiveSmallIntegerField(default=1) # for end user
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    username = models.CharField(unique=True,max_length=30, default='test')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = 'UserMaster'

    def __str__(self):
        return self.username


class UserMasterDetails(models.Model):
    usermaster = models.ForeignKey(to=UserMaster, on_delete=models.PROTECT, null=True)
    access_type = models.ForeignKey(to="AccessTypeMaster", to_field="access_type", on_delete=models.PROTECT, null=True)
    user_type = models.ForeignKey(to="UserTypeMaster", to_field="user_type", on_delete=models.PROTECT)
    from_date = models.DateField(default=datetime.now, blank=True, null=True)
    to_date = models.DateField(default=datetime.strptime('9999-12-31 00:00:00', date_format), blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=50, null=True,default='test')
    update_user = models.CharField(max_length=50, null=True,default='test')
    last_login_on = models.DateTimeField(blank=True, null=True)
    mobile_no = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'UserMasterDetails'

    def __str__(self):
        return self.mobile_no

@receiver(post_save, sender=UserMaster)
def create_user_master_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserMasterDetails.objects.create(usermaster=instance,
                                             access_type=instance._access_type,
                                             user_type = instance._user_type,
                                             mobile_no=instance._mobile)
        except AttributeError as e:
            access_type = AccessTypeMaster.objects.filter(access_type='AG').first()
            user_type = UserTypeMaster.objects.filter(user_type='EU').first()
            UserMasterDetails.objects.create(usermaster=instance,
                                             access_type=access_type,
                                             user_type = user_type,
                                             mobile_no= '1234567890')


class UserTypeMaster(models.Model):
    usertype_code = models.AutoField(primary_key=True)
    usertype_text = models.CharField(max_length=100, blank=False, null=False)
    user_type = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return self.usertype_text

    def userlist(self):
        return UserMaster.objects.filter(user_type=self.user_type, status='1')

    class Meta:
        db_table = "UserTypeMaster"

class AccessTypeMaster(models.Model):
    accesstype_code = models.AutoField(primary_key=True)
    accesstype_text = models.CharField(max_length=100, blank=False, null=False)
    access_type = models.CharField(max_length=20, blank=False, null=False, unique=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return self.accesstype_text

    def userlist(self):
        return UserMaster.objects.filter(access_type=self.access_type, status='1')

    class Meta:
        db_table = "AccessTypeMaster"