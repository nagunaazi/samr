from django.db import models
from datetime import datetime
from agency.models import *

# Create your models here.
class ZVT_PORTAL_CIR(models.Model):
    zvt_portal_cir_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    vbeln = models.CharField(max_length=30,null=True,blank=True)
    posnr = models.CharField(max_length=18,null=True,blank=True)
    gjahr = models.CharField(max_length=12,null=True,blank=True)
    monat = models.CharField(max_length=6,null=True,blank=True)
    vkorg = models.CharField(max_length=12,null=True,blank=True)
    vtweg = models.CharField(max_length=6,null=True,blank=True)   # CA= Cash else Credit
    spart = models.CharField(max_length=6,null=True,blank=True)
    pstyv = models.CharField(max_length=12,null=True,blank=True)
    sold_to_party = models.CharField(max_length=30,null=True,blank=True)
    ship_to_party = models.CharField(max_length=30,null=True,blank=True)
    ord_date = models.CharField(max_length=24,null=True,blank=True)
    vgbel = models.CharField(max_length=30,null=True,blank=True)
    bezei = models.CharField(max_length=120,null=True,blank=True)
    drerz = models.CharField(max_length=24,null=True,blank=True)
    pva = models.CharField(max_length=24,null=True,blank=True)
    matnr = models.CharField(max_length=54,null=True,blank=True)
    pub_name = models.CharField(max_length=120,null=True,blank=True)
    soff_name = models.CharField(max_length=75,null=True,blank=True)
    cg_name = models.CharField(max_length=60,null=True,blank=True)
    sdist_name = models.CharField(max_length=60,null=True,blank=True)
    edition_name = models.CharField(max_length=150,null=True,blank=True)
    cust_name = models.CharField(max_length=90,null=True,blank=True)
    city_name = models.CharField(max_length=75,null=True,blank=True)
    vkgrp = models.CharField(max_length=9,null=True,blank=True)
    sgrp_name = models.CharField(max_length=75,null=True,blank=True)
    vkbur = models.CharField(max_length=12,null=True,blank=True)
    kdgrp = models.CharField(max_length=6,null=True,blank=True)
    bzirk = models.CharField(max_length=18,null=True,blank=True)
    rate = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    disc_perc = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    discount = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    gross_copy = models.IntegerField(null=True,blank=True) #PO
    free_copy = models.IntegerField(null=True,blank=True)
    paid_copy = models.IntegerField(null=True,blank=True)
    zlao = models.IntegerField(null=True,blank=True)
    zcoo = models.IntegerField(null=True,blank=True)
    gross_value = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)   
    net_value = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    route = models.CharField(max_length=18,null=True,blank=True)
    ord_date_f = models.DateTimeField(blank=True, null=True)
    # create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    #PO = gross_copy
    #NPS = paid_copy + zcoo
    #Unsolld = PO-NPS
    #Sampling = free_copy
    def __str__(self):
        return str(self.zvt_portal_cir_id)

   
    def statename(self):
        UM = UnitMaster.objects.filter(unit_code=self.vkorg,status=1).first()
        if UM:
            return UM.state_id.state_name
        else:
            return ''


    def editionname(self):
        UM = EditionMaster.objects.filter(edition_code=self.pva,status=1).first()
        if UM:
            return UM.edition_name
        else:
            return ''

    def mainjj(self):
        UM = EditionMaster.objects.filter(edition_code=self.pva,status=1).first()
        if UM:
            if UM.publication_id.publication_code =="JJ":
                return 'JJ'
            elif UM.publication_id.publication_code in ('DB','DM','DV'):
                return 'MAIN'
            else:
                return ''
        else:
            return ''


    class Meta:
        db_table = "ZVT_PORTAL_CIR"




class ZVT_SMRD_OTS(models.Model):
    zvt_smrd_ots_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    partner = models.CharField(max_length=51,null=True,blank=True)
    out_std =  models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    asd =  models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    erfdate = models.CharField(max_length=24,null=True,blank=True)
    erftime = models.CharField(max_length=18,null=True,blank=True)
    vkorg = models.CharField(max_length=12,null=True,blank=True)
    
    
    def __str__(self):
        return str(self.zvt_smrd_ots_id)


    class Meta:
        db_table = "ZVT_SMRD_OTS"


class ZVT_PORTAL_INVHD(models.Model):
    zvt_portal_invhd_id = models.AutoField(primary_key=True)
    mandt =  models.CharField(max_length=9,null=True,blank=True)
    vbeln =  models.CharField(max_length=30,null=True,blank=True)
    fkdat =  models.CharField(max_length=24,null=True,blank=True)
    kunnr =  models.CharField(max_length=30,null=True,blank=True)
    bukrs =  models.CharField(max_length=12,null=True,blank=True)
    sname =  models.CharField(max_length=105,null=True,blank=True)
    ablad =  models.CharField(max_length=75,null=True,blank=True)
    mon =  models.IntegerField(null=True,blank=True)
    quan =  models.DecimalField(max_digits=13, decimal_places=3,null=True,blank=True)
    rate =  models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    discnt =  models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    vrkme =  models.CharField(max_length=9,null=True,blank=True)
    cuuky =  models.CharField(max_length=15,null=True,blank=True)
    sparty =  models.CharField(max_length=3,null=True,blank=True)
    last_m_amt =  models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    last_m_amt2 =  models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    open_bal =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    gl_tran =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    close_bal =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    balance =  models.DecimalField(max_digits=23, decimal_places=4,null=True,blank=True)
    credit_amount =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    debit_amount =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    collection_amount =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    magzine_amount =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    net_amount =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    old_bal =  models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    asd =  models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    asd_flag =  models.CharField(max_length=3,null=True,blank=True)

    
    
    def __str__(self):
        return str(self.zvt_portal_invhd_id)


    class Meta:
        db_table = "ZVT_PORTAL_INVHD"








class ZVT_PORTAL_BILL(models.Model):
    zvt_portal_bill_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    bill_no = models.CharField(max_length=30,null=True,blank=True)
    fkdat = models.CharField(max_length=24,null=True,blank=True)
    sold_to_pty = models.CharField(max_length=30,null=True,blank=True)
    type = models.CharField(max_length=30,null=True,blank=True)
    belnr = models.CharField(max_length=30,null=True,blank=True)
    fi_doc = models.CharField(max_length=48,null=True,blank=True)
    bzirk = models.CharField(max_length=18,null=True,blank=True)
    bill_to_pty = models.CharField(max_length=30,null=True,blank=True)
    agent_id = models.CharField(max_length=30,null=True,blank=True)
    cust_name = models.CharField(max_length=105,null=True,blank=True)
    city_name = models.CharField(max_length=150,null=True,blank=True)
    barea = models.CharField(max_length=12,null=True,blank=True)
    pstyv = models.CharField(max_length=12,null=True,blank=True)
    aufnr = models.CharField(max_length=36,null=True,blank=True)
    edition = models.CharField(max_length=150,null=True,blank=True)
    vkgrp = models.CharField(max_length=9,null=True,blank=True)
    gross = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    free_copies = models.IntegerField(null=True,blank=True)
    sold_copies = models.IntegerField(null=True,blank=True)
    discper = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    gross_amount = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    discount = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    net_billing = models.DecimalField(max_digits=11, decimal_places=2,null=True,blank=True)
    diff_value = models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    net_value = models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    cnt = models.IntegerField(null=True,blank=True)
    kvgr3 = models.CharField(max_length=9,null=True,blank=True)
    monat = models.CharField(max_length=6,null=True,blank=True)
    gjahr = models.CharField(max_length=12,null=True,blank=True)
    vkorg = models.CharField(max_length=12,null=True,blank=True)

   
    
    def __str__(self):
        return str(self.zvt_portal_bill_id)


    class Meta:
        db_table = "ZVT_PORTAL_BILL"





class ZVT_DATA_ACCOUNT(models.Model):
    zvt_data_account_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    bukrs = models.CharField(max_length=12,null=True,blank=True)
    belnr = models.CharField(max_length=30,null=True,blank=True)
    gjahr = models.CharField(max_length=12,null=True,blank=True)
    monat = models.CharField(max_length=6,null=True,blank=True)
    xblnr = models.CharField(max_length=48,null=True,blank=True)
    blart = models.CharField(max_length=6,null=True,blank=True)
    umskz = models.CharField(max_length=3,null=True,blank=True)
    gsber = models.CharField(max_length=12,null=True,blank=True)
    cpudt = models.CharField(max_length=24,null=True,blank=True)
    budat = models.CharField(max_length=24,null=True,blank=True)
    xref1 = models.CharField(max_length=36,null=True,blank=True)
    dmshb = models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    konto = models.CharField(max_length=48,null=True,blank=True)
    name1 = models.CharField(max_length=90,null=True,blank=True)
    bktxt = models.CharField(max_length=75,null=True,blank=True)
    cash = models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    cheque = models.DecimalField(max_digits=13, decimal_places=2,null=True,blank=True)
    kvgr3 = models.CharField(max_length=9,null=True,blank=True)
    kunnr = models.CharField(max_length=30,null=True,blank=True)
    copies = models.IntegerField(null=True,blank=True)
    bezei = models.CharField(max_length=120,null=True,blank=True)

    
    def __str__(self):
        return str(self.zvt_data_account_id)


    class Meta:
        db_table = "ZVT_DATA_ACCOUNT"




class ZVT_PORTAL_REG(models.Model):
    zvt_portal_reg_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    partner = models.CharField(max_length=30,null=True,blank=True)
    vkorg = models.CharField(max_length=12,null=True,blank=True)
    vkbur = models.CharField(max_length=12,null=True,blank=True)
    vkgrp = models.CharField(max_length=9,null=True,blank=True)
    name1 = models.CharField(max_length=90,null=True,blank=True)
    name2 = models.CharField(max_length=90,null=True,blank=True)
    kdgrp = models.CharField(max_length=6,null=True,blank=True)
    city1 = models.CharField(max_length=120,null=True,blank=True)
    mobile = models.CharField(max_length=90,null=True,blank=True)
    email = models.CharField(max_length=723,null=True,blank=True)
    reqsent_flag = models.CharField(max_length=3,null=True,blank=True)
    request_send = models.CharField(max_length=24,null=True,blank=True)
    req_user = models.CharField(max_length=36,null=True,blank=True)
    active_flag = models.CharField(max_length=3,null=True,blank=True)
    active_date = models.CharField(max_length=24,null=True,blank=True)
    deviceid = models.CharField(max_length=300,null=True,blank=True)
    type = models.CharField(max_length=6,null=True,blank=True)
    request_time = models.CharField(max_length=18,null=True,blank=True)
    active_time = models.CharField(max_length=18,null=True,blank=True)
    parent_flag = models.CharField(max_length=3,null=True,blank=True)
    parent = models.CharField(max_length=30,null=True,blank=True)
    vtweg = models.CharField(max_length=6,null=True,blank=True)
    bzirk = models.CharField(max_length=18,null=True,blank=True)


    
    def __str__(self):
        return str(self.zvt_portal_reg_id)


    class Meta:
        db_table = "ZVT_PORTAL_REG"



class ZVT_PORTAL_REGIH(models.Model):
    zvt_portal_regih_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    vkorg = models.CharField(max_length=12,null=True,blank=True)
    state = models.CharField(max_length=6,null=True,blank=True)
    type = models.CharField(max_length=6,null=True,blank=True)
    adid = models.CharField(max_length=30,null=True,blank=True)
    name = models.CharField(max_length=150,null=True,blank=True)
    mobile = models.CharField(max_length=90,null=True,blank=True)
    email = models.CharField(max_length=723,null=True,blank=True)

    
    def __str__(self):
        return str(self.zvt_portal_regih_id)


    class Meta:
        db_table = "ZVT_PORTAL_REGIH"





class ZVT_PORTAL_EXBP(models.Model):
    zvt_portal_exbp_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    vkorg = models.CharField(max_length=12,null=True,blank=True)
    state = models.CharField(max_length=6,null=True,blank=True)
    partner = models.CharField(max_length=30,null=True,blank=True)
    adid = models.CharField(max_length=30,null=True,blank=True)
    type = models.CharField(max_length=6,null=True,blank=True)
    location = models.CharField(max_length=150,null=True,blank=True)


    
    def __str__(self):
        return str(self.zvt_portal_exbp_id)


    class Meta:
        db_table = "ZVT_PORTAL_EXBP"




class ZVT_SMRD_PROFILE(models.Model):
    zvt_smrd_profile_id = models.AutoField(primary_key=True)
    mandt = models.CharField(max_length=9,null=True,blank=True)
    bp_code = models.CharField(max_length=30,null=True,blank=True)
    marital_status = models.CharField(max_length=30,null=True,blank=True)
    state = models.CharField(max_length=105,null=True,blank=True)
    city = models.CharField(max_length=75,null=True,blank=True)
    pincode = models.CharField(max_length=30,null=True,blank=True)
    unit = models.CharField(max_length=120,null=True,blank=True)
    addr = models.CharField(max_length=360,null=True,blank=True)
    religion = models.CharField(max_length=45,null=True,blank=True)
    no_child = models.CharField(max_length=6,null=True,blank=True)
    policy_no = models.CharField(max_length=120,null=True,blank=True)
    aadhar = models.CharField(max_length=36,null=True,blank=True)
    pan = models.CharField(max_length=30,null=True,blank=True)
    working_with_db = models.CharField(max_length=24,null=True,blank=True)
    bp_mob1 = models.CharField(max_length=30,null=True,blank=True)
    bp_gndr = models.CharField(max_length=3,null=True,blank=True)
    dob = models.CharField(max_length=24,null=True,blank=True)
    marr_anvi = models.CharField(max_length=24,null=True,blank=True)
    bp_email = models.CharField(max_length=300,null=True,blank=True)
    mot_name = models.CharField(max_length=105,null=True,blank=True)
    mot_dob = models.CharField(max_length=24,null=True,blank=True)
    bro1_name = models.CharField(max_length=105,null=True,blank=True)
    bro1_dob = models.CharField(max_length=24,null=True,blank=True)
    bro2_name = models.CharField(max_length=105,null=True,blank=True)
    bro2_dob = models.CharField(max_length=24,null=True,blank=True)
    sis1_name = models.CharField(max_length=105,null=True,blank=True)
    sis1_dob = models.CharField(max_length=24,null=True,blank=True)
    sis2_name = models.CharField(max_length=105,null=True,blank=True)
    sis2_dob = models.CharField(max_length=24,null=True,blank=True)
    kid1_name = models.CharField(max_length=105,null=True,blank=True)
    kid1_gndr = models.CharField(max_length=3,null=True,blank=True)
    kid1_dob = models.CharField(max_length=24,null=True,blank=True)
    kid1_edu = models.CharField(max_length=60,null=True,blank=True)
    kid2_name = models.CharField(max_length=105,null=True,blank=True)
    kid2_gndr = models.CharField(max_length=3,null=True,blank=True)
    kid2_dob = models.CharField(max_length=24,null=True,blank=True)
    kid2_edu = models.CharField(max_length=60,null=True,blank=True)
    kid3_name = models.CharField(max_length=105,null=True,blank=True)
    kid3_gndr = models.CharField(max_length=3,null=True,blank=True)
    kid3_dob = models.CharField(max_length=24,null=True,blank=True)
    kid3_edu = models.CharField(max_length=60,null=True,blank=True)
    kid4_name = models.CharField(max_length=105,null=True,blank=True)
    kid4_gndr = models.CharField(max_length=3,null=True,blank=True)
    kid4_dob = models.CharField(max_length=24,null=True,blank=True)
    kid4_edu = models.CharField(max_length=60,null=True,blank=True)
    kid5_name = models.CharField(max_length=105,null=True,blank=True)
    kid5_gndr = models.CharField(max_length=3,null=True,blank=True)
    kid5_dob = models.CharField(max_length=24,null=True,blank=True)
    kid5_edu = models.CharField(max_length=60,null=True,blank=True)
    fat_name = models.CharField(max_length=105,null=True,blank=True)
    fat_dob = models.CharField(max_length=24,null=True,blank=True)
    sp_name = models.CharField(max_length=105,null=True,blank=True)
    sp_dob = models.CharField(max_length=24,null=True,blank=True)
    erdat = models.CharField(max_length=24,null=True,blank=True)
    upd_on = models.CharField(max_length=24,null=True,blank=True)
    upd_status = models.CharField(max_length=3,null=True,blank=True)
    upd_by = models.CharField(max_length=24,null=True,blank=True)


    
    def __str__(self):
        return str(self.zvt_smrd_profile_id)


    class Meta:
        db_table = "ZVT_SMRD_PROFILE"