from django.db import models
from datetime import datetime
from master.models import EducationMaster

# Create your models here.


class StateMaster(models.Model):
	state_id = models.AutoField(primary_key=True)
	state_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	state_bscode = models.TextField(max_length=50, blank=False, null=False)
	state_sapcode = models.CharField(max_length=10, blank=False, null=False,default='0')
	state_name = models.TextField(max_length=250, blank=False, null=False)
	state_language  = models.TextField(max_length=50, blank=False, null=False, default='EN')
	state_area_in_km = models.PositiveIntegerField(default=0,blank=True, null=True)
	state_population = models.TextField(max_length=255, blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.state_code)


	class Meta:
	    db_table = "AgencyStateMaster"



class UnitMaster(models.Model):
	unit_id = models.AutoField(primary_key=True)
	state_id = models.ForeignKey(to="StateMaster", to_field="state_id", on_delete=models.PROTECT, null=False)
	unit_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	unit_name = models.TextField(max_length=250, blank=False, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.unit_code)


	class Meta:
	    db_table = "UnitMaster"









class CityMaster(models.Model):   #May used for District also
	city_id = models.AutoField(primary_key=True)
	state_id = models.ForeignKey(to="StateMaster", to_field="state_id", on_delete=models.PROTECT, null=False)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	city_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	city_name = models.TextField(max_length=250, blank=False, null=False)
	city_area_in_km = models.PositiveIntegerField(default=0,blank=True, null=True)
	city_population = models.TextField(max_length=255, blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.city_code)


	class Meta:
	    db_table = "CityMaster"









class LocationMaster(models.Model):
	location_id = models.AutoField(primary_key=True)
	city_id = models.ForeignKey(to="CityMaster", to_field="city_id", on_delete=models.PROTECT, null=False)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	location_code = models.TextField(max_length=50, blank=False, null=False)
	location_name = models.TextField(max_length=250, blank=False, null=False)
	location_area_in_km = models.PositiveIntegerField(default=0,blank=True, null=True)
	location_population = models.TextField(max_length=255, blank=True, null=True)
	city_upc = models.TextField(max_length=50, blank=False, null=False,default="City") #City/UPC
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.location_code)


	class Meta:
	    db_table = "LocationMaster"





class TownMaster(models.Model):
	town_id = models.AutoField(primary_key=True)
	city_id = models.ForeignKey(to="CityMaster", to_field="city_id", on_delete=models.PROTECT, null=False)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	town_code = models.TextField(max_length=50, blank=False, null=False)
	town_name = models.TextField(max_length=250, blank=False, null=False)
	town_area_in_km = models.PositiveIntegerField(default=0,blank=True, null=True)
	town_population = models.TextField(max_length=255, blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.town_code)


	class Meta:
	    db_table = "TownMaster"



class PlantMaster(models.Model):
	plant_id = models.AutoField(primary_key=True)
	plant_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	plant_name = models.TextField(max_length=250, blank=False, null=False)
	state_id = models.ForeignKey(to="StateMaster", to_field="state_id", on_delete=models.PROTECT, null=False)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	plant_location_lat = models.TextField(max_length=250, blank=True, null=True)
	plant_location_long = models.TextField(max_length=250, blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.plant_code)


	class Meta:
	    db_table = "PlantMaster"


class RouteMaster(models.Model):
	route_id = models.AutoField(primary_key=True)
	route_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	route_name = models.TextField(max_length=250, blank=False, null=False)
	plant_id = models.ForeignKey(to="PlantMaster", to_field="plant_id", on_delete=models.PROTECT, null=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	city_upc = models.TextField(max_length=50, blank=True, null=True,default="City") #City/UPC
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
		return str(self.route_code)


	class Meta:
	    db_table = "RouteMaster"


class DroppingPointMaster(models.Model):
	dropping_id = models.AutoField(primary_key=True)
	#route_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	dropping_name = models.TextField(max_length=250, blank=False, null=False)
	route_id = models.ForeignKey(to="RouteMaster", to_field="route_id", on_delete=models.PROTECT, null=True)
	dropping_location_lat = models.TextField(max_length=250, blank=True, null=True)
	dropping_location_long = models.TextField(max_length=250, blank=True, null=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	city_upc = models.TextField(max_length=50, blank=True, null=True,default="City") #City/UPC
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.dropping_name)


	class Meta:
	    db_table = "DroppingPointMaster"



class PublicationMaster(models.Model):
	publication_id = models.AutoField(primary_key=True)
	publication_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	publication_name = models.TextField(max_length=250, blank=False, null=False)
	publication_language  = models.TextField(max_length=50, blank=False, null=False, default='EN')
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.publication_code)

	class Meta:
	    db_table = "PublicationMaster"


class EditionMaster(models.Model):
	edition_id = models.AutoField(primary_key=True)
	publication_id = models.ForeignKey(to="PublicationMaster", to_field="publication_id", on_delete=models.PROTECT, null=False)
	plant_id = models.ForeignKey(to="PlantMaster", to_field="plant_id", on_delete=models.PROTECT, null=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	edition_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	edition_name = models.TextField(max_length=250, blank=False, null=False)
	edition_language  = models.TextField(max_length=50, blank=False, null=False, default='EN')
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.edition_code)

	class Meta:
	    db_table = "EditionMaster"


class NewspaperMaster(models.Model):
	newspaper_id = models.AutoField(primary_key=True)
	newspaper_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	newspaper_name = models.TextField(max_length=250, blank=False, null=False)
	newspaper_language  = models.TextField(max_length=50, blank=False, null=False, default='EN')
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.newspaper_code)

	class Meta:
	    db_table = "NewspaperMaster"

class DesignationMaster(models.Model):
	designation_id = models.AutoField(primary_key=True)
	#designation_code = models.CharField(max_length=50, blank=False, null=False,unique=True)
	designation_name = models.CharField(max_length=250, blank=False, null=False,unique=True)
	#newspaper_language  = models.TextField(max_length=50, blank=False, null=False, default='EN')
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.designation_name)

	class Meta:
	    db_table = "DesignationMaster"


class DepartmentMaster(models.Model):
	department_id = models.AutoField(primary_key=True)
	department_name = models.CharField(max_length=250, blank=False, null=False,unique=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.department_name)

	class Meta:
	    db_table = "DepartmentMaster"


class AddressProofMaster(models.Model):
	addressproof_id = models.AutoField(primary_key=True)
	addressproof_name = models.CharField(max_length=250, blank=False, null=False,unique=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.addressproof_name)

	class Meta:
	    db_table = "AddressProofMaster"



class CommissionMaster(models.Model):
	commission_id = models.AutoField(primary_key=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=False)
	commission_per = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	commission_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	valid_from = models.DateTimeField(default=datetime.now,blank=False, null=False)
	valid_to = models.DateTimeField(default=datetime.now,blank=False, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.commission_per)

	class Meta:
	    db_table = "CommissionMaster"




class RealtionMaster(models.Model):
	relation_id = models.AutoField(primary_key=True)
	relation = models.CharField(max_length=250, blank=False, null=False,unique=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.relation)

	class Meta:
	    db_table = "RealtionMaster"


class MaritialStatusMaster(models.Model):
	maritial_id = models.AutoField(primary_key=True)
	maritial_status = models.CharField(max_length=250, blank=False, null=False,unique=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.maritial_status)

	class Meta:
	    db_table = "MaritialStatusMaster"


#####Agency Request Process####

class AgencyRequestMaster(models.Model):
	ag_req_id = models.AutoField(primary_key=True)
	state_id = models.ForeignKey(to="StateMaster", to_field="state_id", on_delete=models.PROTECT, null=False)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=False)
	city_id = models.ForeignKey(to="CityMaster", to_field="city_id", on_delete=models.PROTECT, null=False)
	location_id = models.ForeignKey(to="LocationMaster", to_field="location_id", on_delete=models.PROTECT, null=False)
	town_id = models.ForeignKey(to="TownMaster", to_field="town_id", on_delete=models.PROTECT, null=False)
	pincode = models.TextField(max_length=10, blank=False, null=False)
	population = models.TextField(max_length=255, blank=True, null=True)
	tot_copies = models.PositiveIntegerField(default=0,blank=False, null=False)
	main_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	jj_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	city_upc = models.TextField(max_length=50, blank=False, null=False,default="City") #City/UPC
	reason = models.TextField(max_length=50, blank=False, null=False,default="Replacement")
	proposed_count = models.PositiveSmallIntegerField(default=0, blank=False, null=False)


	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.ag_req_id)

	class Meta:
	    db_table = "AgencyRequestMaster"



class AgencyRequestReason(models.Model):
	reason_id = models.AutoField(primary_key=True)
	ag_req_id = models.ForeignKey(to="AgencyRequestMaster", to_field="ag_req_id", related_name='AgencyRequestReason_set',on_delete=models.PROTECT, null=False)
	reason = models.TextField(max_length=50, blank=False, null=False,default="Replacement")
	ag_code = models.TextField(max_length=50, blank=False, null=False)
	ag_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	ag_reason = models.TextField(max_length=250, blank=True, null=True)

	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.ag_req_reason_id)

	class Meta:
	    db_table = "AgencyRequestReason"



class AgencyRequestAGDetail(models.Model):
	ag_detail_id = models.AutoField(primary_key=True)
	ag_req_id = models.ForeignKey(to="AgencyRequestMaster", to_field="ag_req_id",related_name='AgencyRequestAGDetail_set', on_delete=models.PROTECT, null=False)
	agenct_name = models.TextField(max_length=250, blank=False, null=False)
	agency_name = models.TextField(max_length=250, blank=False, null=False)
	cluster_id = models.ForeignKey(to="ClusterMaster", to_field="cluster_id", on_delete=models.PROTECT, blank=True, null=True)
	salesdist_id = models.ForeignKey(to="SalesDistMaster", to_field="salesdist_id", on_delete=models.PROTECT, blank=True, null=True)
	salesoff_id = models.ForeignKey(to="SalesOffMaster", to_field="salesoff_id", on_delete=models.PROTECT, blank=True, null=True)
	price_group_id = models.ForeignKey(to="PriceGroupMaster", to_field="price_group_id", on_delete=models.PROTECT, blank=True, null=True)
	custgrp = models.CharField(max_length=20,blank=True, null=True)
	final_status = models.PositiveSmallIntegerField(default=0, blank=True, null=True) #0=pending 1=final selection out of all
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.ag_detail_id)

	class Meta:
	    db_table = "AgencyRequestAGDetail"


class AgencyRequestSurvey(models.Model):
	survey_id = models.AutoField(primary_key=True)
	ag_detail_id = models.ForeignKey(to="AgencyRequestAGDetail", to_field="ag_detail_id", related_name='AgencyRequestSurvey_set',on_delete=models.PROTECT, null=False)
	tot_copies = models.PositiveIntegerField(default=0,blank=False, null=False)
	cash_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	subagenct_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	vendor_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	railway_copies =models.PositiveIntegerField(default=0,blank=True, null=True)
	self_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	UOH_meeting_flag = models.PositiveSmallIntegerField(default=0, blank=True, null=True) #0=No 1=Yes
	UOH_meeting_mode = models.TextField(max_length=20, blank=True, null=True)
	uoh_meeting_remark = models.TextField(max_length=250, blank=False, null=False)
	SOH_meeting_flag = models.PositiveSmallIntegerField(default=0, blank=True, null=True) #0=No 1=Yes
	SOH_meeting_mode = models.TextField(max_length=20, blank=True, null=True)
	SOH_meeting_remark = models.TextField(max_length=250, blank=False, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.survey_id)

	class Meta:
	    db_table = "AgencyRequestSurvey"


class AgencyRequestSurveyVillage(models.Model):
	survey_village_id = models.AutoField(primary_key=True)
	survey_id = models.ForeignKey(related_name='AgencyRequestSurveyVillage_set',to="AgencyRequestSurvey", to_field="survey_id", on_delete=models.PROTECT, null=False)
	village_name = models.TextField(max_length=20, blank=False, null=False)
	village_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.survey_village_id)

	class Meta:
	    db_table = "AgencyRequestSurveyVillage"


class AgencyRequestSurveyTarget(models.Model):
	survey_target_id = models.AutoField(primary_key=True)
	survey_id = models.ForeignKey(related_name='AgencyRequestSurveyTarget_set',to="AgencyRequestSurvey", to_field="survey_id", on_delete=models.PROTECT, null=False)
	agency_name = models.TextField(max_length=250, blank=False, null=False)
	agecy_code = models.TextField(max_length=20, blank=True, null=True)
	cur_copies = models.PositiveIntegerField(default=0,blank=True, null=True)
	month_one = models.PositiveIntegerField(default=0,blank=True, null=True)
	month_two = models.PositiveIntegerField(default=0,blank=True, null=True)
	month_three = models.PositiveIntegerField(default=0,blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)


	def __str__(self):
	    return str(self.survey_target_id)

	class Meta:
	    db_table = "AgencyRequestSurveyTarget"



class AgencyRequestKYBP(models.Model):
	gender_choice = (('M','Male'),('F','Female'),('O','Other'))
	title_choice = (('Ms','Ms'),('Mr','Mr'),('Mrs','Mrs'),('M/s','M/s'))
	kybp_id = models.AutoField(primary_key=True)
	ag_detail_id = models.ForeignKey(related_name='AgencyRequestKYBP_set',to="AgencyRequestAGDetail", to_field="ag_detail_id", on_delete=models.PROTECT, null=False)
	ag_gender = models.CharField(max_length=1, choices=gender_choice,default='M')
	ag_title = models.CharField(max_length=20, choices=title_choice,default='Mr')
	first_name = models.TextField(max_length=150, blank=False, null=False)
	middle_name = models.TextField(max_length=150, blank=True, null=True)
	last_name = models.TextField(max_length=150, blank=False, null=False)
	agency_name = models.TextField(max_length=150, blank=False, null=False)
	resi_houseno = models.TextField(max_length=150, blank=False, null=False)
	resi_building = models.TextField(max_length=150, blank=False, null=False)
	resi_street = models.TextField(max_length=150, blank=False, null=False)
	resi_city = models.ForeignKey(to="CityMaster", to_field="city_id",related_name='resi_city', on_delete=models.PROTECT, null=False)
	resi_state = models.ForeignKey(to="StateMaster", to_field="state_id",related_name='resi_state', on_delete=models.PROTECT, null=False)
	resi_pincode = models.TextField(max_length=10, blank=True, null=True)
	resi_mono = models.TextField(max_length=10, blank=True, null=True)
	resi_watsup = models.TextField(max_length=10, blank=True, null=True)
	resi_email = models.TextField(max_length=50, blank=True, null=True)
	busi_houseno = models.TextField(max_length=150, blank=False, null=False)
	busi_building = models.TextField(max_length=150, blank=False, null=False)
	busi_street = models.TextField(max_length=150, blank=False, null=False)
	busi_city = models.ForeignKey(to="CityMaster", to_field="city_id",related_name='busi_city', on_delete=models.PROTECT, null=False)
	busi_state = models.ForeignKey(to="StateMaster", to_field="state_id",related_name='busi_state', on_delete=models.PROTECT, null=False)
	busi_pincode = models.TextField(max_length=10, blank=True, null=True)
	busi_mono = models.TextField(max_length=10, blank=True, null=True)
	busi_watsup = models.TextField(max_length=10, blank=True, null=True)
	busi_email = models.TextField(max_length=50, blank=True, null=True)

	ag_religion = models.TextField(max_length=50, blank=False, null=False)
	ag_dob = models.DateTimeField(blank=True, null=True)

	ag_maritial_id = models.ForeignKey(to="MaritialStatusMaster", to_field="maritial_id", on_delete=models.PROTECT, null=False)
	spouse_name = models.TextField(max_length=50, blank=False, null=False)
	spouse_dob = models.DateTimeField(blank=True, null=True)
	ag_marrige_ani = models.DateTimeField(blank=True, null=True)
	no_of_children = models.PositiveIntegerField(default=0, blank=False, null=False)
	father_name = models.TextField(max_length=150, blank=False, null=False)
	father_dob = models.DateTimeField(blank=True, null=True)
	mother_name = models.TextField(max_length=150, blank=False, null=False)
	mother_dob = models.DateTimeField(blank=True, null=True)
	brother_name = models.TextField(max_length=150, blank=False, null=False)
	brother_dob = models.DateTimeField(blank=True, null=True)
	sister_name = models.TextField(max_length=150, blank=False, null=False)
	sister_dob =models.DateTimeField(blank=True, null=True)
	nominee_name = models.TextField(max_length=150, blank=False, null=False)
	nominee_relation = models.TextField(max_length=150, blank=False, null=False)
	other_nespaper_count = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
	bank_holder_name = models.TextField(max_length=150, blank=False, null=False)
	bank_acc_no = models.TextField(max_length=150, blank=False, null=False)
	bank_name_branch = models.TextField(max_length=250, blank=False, null=False)
	bank_address = models.TextField(max_length=250, blank=False, null=False)
	bank_IFSC = models.TextField(max_length=150, blank=False, null=False)
	GSTIN = models.TextField(max_length=150, blank=False, null=False)
	ag_db_relative = models.PositiveSmallIntegerField(default=0, blank=True, null=True) #0=No 1=Yes
	db_gender = models.CharField(max_length=1, choices=gender_choice,default='M')
	db_fullname = models.TextField(max_length=150, blank=False, null=False)
	db_empid = models.TextField(max_length=150, blank=False, null=False)
	db_dept = models.ForeignKey(to="DepartmentMaster", to_field="department_id", on_delete=models.PROTECT, null=False)
	db_desig = models.ForeignKey(to="DesignationMaster", to_field="designation_id", on_delete=models.PROTECT, null=False)
	db_relation = models.ForeignKey(to="RealtionMaster", to_field="relation_id", on_delete=models.PROTECT, null=False)
	db_city = models.ForeignKey(to="CityMaster", to_field="city_id",related_name='db_city', on_delete=models.PROTECT, null=False)
	pan_no = models.TextField(max_length=10, blank=False, null=False)
	pan_copy = models.FileField(upload_to='PAN_Attach/',verbose_name='PAN Card Attachment',blank=True, null=True)
	add_proof_type = models.ForeignKey(to="AddressProofMaster", to_field="addressproof_id", on_delete=models.PROTECT, null=False)
	add_proof_no = models.TextField(max_length=50, blank=False, null=False)
	add_proof_copy = models.FileField(upload_to='ADDRESS_Attach/',verbose_name='Address Proof Attachment',blank=True, null=True)
	bank_copy_type = models.TextField(max_length=50, blank=False, null=False)
	bank_copy = models.FileField(upload_to='BANK_Attach/',verbose_name='Bank Proff Attachment',blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
	    return str(self.kybp_id)

	class Meta:
	    db_table = "AgencyRequestKYBP"



class Agency_Child(models.Model):
	gender_choice = (('M','Male'),('F','Female'),('O','Other'))
	ag_child_id = models.AutoField(primary_key=True)
	kybp_id = models.ForeignKey(related_name='Agency_Child_set',to="AgencyRequestKYBP", to_field="kybp_id", on_delete=models.PROTECT, null=False)
	child_name = models.TextField(max_length=150, blank=False, null=False)
	child_DOB = models.DateTimeField(blank=True, null=True)
	child_education = models.ForeignKey(to="master.EducationMaster", to_field="Education_code", on_delete=models.PROTECT, null=False)
	child_gender = models.CharField(max_length=1, choices=gender_choice,default='M')
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) #1=Pending 2=Approved 3=Reject 4=Hold 0=Delete
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)
	def __str__(self):
	    return str(self.ag_child_id)

	class Meta:
	    db_table = "Agency_Child"



class Agency_OtherNewsPaper(models.Model):
	ag_othernewspaper_id = models.AutoField(primary_key=True)
	kybp_id = models.ForeignKey(related_name='Agency_OtherNewsPaper_set',to="AgencyRequestKYBP", to_field="kybp_id", on_delete=models.PROTECT, null=False)
	newspaper_id = models.ForeignKey(to="NewspaperMaster", to_field="newspaper_id", on_delete=models.PROTECT, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) 
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)
	def __str__(self):
	    return str(self.ag_child_id)

	class Meta:
	    db_table = "Agency_OtherNewsPaper"





class AgencyRequestCIRReq(models.Model):
	cirreq_id = models.AutoField(primary_key=True)
	ag_detail_id = models.ForeignKey(related_name='AgencyRequestCIRReq_set',to="AgencyRequestAGDetail", to_field="ag_detail_id", on_delete=models.PROTECT, null=False)
	edition_count = models.PositiveIntegerField(default=0, blank=True, null=True)
	start_date = models.DateTimeField(blank=True, null=True)
	commission_per = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	commission_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	asd_as_per_norms = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	asd_collected =  models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	cheque_count = models.PositiveIntegerField(default=0, blank=True, null=True)
	asd_mode = models.CharField(max_length=20,blank=True, null=True)
	asd_days = models.CharField(max_length=20,blank=True, null=True)
	dropping_count = models.PositiveIntegerField(default=0, blank=True, null=True)
	executive_code = models.TextField(max_length=20, blank=False, null=False)
	executive_name = models.TextField(max_length=150, blank=False, null=False)
	UOH_code = models.TextField(max_length=20, blank=False, null=False)
	UOH_name =  models.TextField(max_length=150, blank=False, null=False)
	SOH_code = models.TextField(max_length=20, blank=False, null=False)
	SOH_name = models.TextField(max_length=150, blank=False, null=False)
	creation_comments = models.TextField(max_length=1000, blank=False, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) 
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)
	def __str__(self):
	    return str(self.cirreq_id)

	class Meta:
	    db_table = "AgencyRequestCIRReq"


class CirReqEdition(models.Model):
	cirreqedition_id = models.AutoField(primary_key=True)
	cirreq_id = models.ForeignKey(related_name='CirReqEdition_set',to="AgencyRequestCIRReq", to_field="cirreq_id", on_delete=models.PROTECT, null=False)
	edition_id = models.ForeignKey(to="EditionMaster", to_field="edition_id", on_delete=models.PROTECT, null=False)
	edition_copies = models.PositiveIntegerField(default=0, blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) 
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)
	def __str__(self):
	    return str(self.cirreqedition_id)

	class Meta:
	    db_table = "CirReqEdition" 


class CirReqDropping(models.Model):
	cirreqdropping_id = models.AutoField(primary_key=True)
	cirreq_id = models.ForeignKey(related_name='CirReqDropping_set',to="AgencyRequestCIRReq", to_field="cirreq_id", on_delete=models.PROTECT, null=False)
	dropping_id = models.ForeignKey(to="DroppingPointMaster", to_field="dropping_id", on_delete=models.PROTECT, null=False)
	route_id = models.ForeignKey(to="RouteMaster", to_field="route_id", on_delete=models.PROTECT, null=False)
	contact_no = models.CharField(max_length=20,blank=True, null=True)
	sub_agent_code = models.CharField(max_length=20,blank=True, null=True)
	sub_agent_name = models.CharField(max_length=150,blank=True, null=True)
	sub_agent_contact_no = models.CharField(max_length=20,blank=True, null=True)
	sub_agent_copies = models.PositiveIntegerField(default=0, blank=True, null=True) 
	self_copies = models.PositiveIntegerField(default=0, blank=True, null=True) 
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) 
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)
	def __str__(self):
	    return str(self.cirreqdropping_id)

	class Meta:
	    db_table = "CirReqDropping" 
	 

class CirReqCheque(models.Model):
	cirreqcheque_id = models.AutoField(primary_key=True)
	cirreq_id = models.ForeignKey(related_name='CirReqCheque_set',to="AgencyRequestCIRReq", to_field="cirreq_id", on_delete=models.PROTECT, null=False)
	cheque_mode = models.CharField(max_length=150,blank=True, null=True)
	cheque_number = models.CharField(max_length=150,blank=True, null=True)
	cheque_date = models.DateTimeField(blank=True,null=True)
	cheque_amt = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	cheque_bank = models.CharField(max_length=150,blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True) 
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)
	def __str__(self):
	    return str(self.cirreqcheque_id)

	class Meta:
	    db_table = "CirReqCheque" 

class TeamMaster(models.Model):
    team_id = models.AutoField(primary_key=True)
    state_id = models.ForeignKey(to="StateMaster", to_field="state_id", on_delete=models.PROTECT, null=False)
    unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
    access_type = models.ForeignKey(to="master.AccessTypeMaster", to_field="access_type", on_delete=models.PROTECT, null=True)
    team_SAPcode = models.TextField(max_length=50, blank=False, null=False)
    team_name = models.TextField(max_length=250, blank=False, null=False)
    team_email = models.CharField(max_length=50,blank=True, null=True)
    team_mono = models.CharField(max_length=20,blank=True, null=True)
    status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_user = models.CharField(max_length=20,blank=True, null=True)
    update_user = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return str(self.team_id)

    class Meta:
        db_table = "TeamMaster"


class ASDMaster(models.Model):
	asd_id = models.AutoField(primary_key=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	publication_id = models.ForeignKey(to="PublicationMaster", to_field="publication_id", on_delete=models.PROTECT, null=False)
	sales_group = models.CharField(max_length=4, blank=False, null=False)
	sales_office = models.CharField(max_length=4, blank=False, null=False)
	asd = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
	from_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	to_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
		return str(self.asd_id)

	class Meta:
		db_table = "ASDMaster"











class PriceGroupMaster(models.Model):
	price_group_id = models.AutoField(primary_key=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	price_group = models.CharField(max_length=2,blank=True, null=True)
	min_copy_limit = models.IntegerField(blank=True, null=True)
	max_copy_limit = models.IntegerField(blank=True, null=True)
	comm_per = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	price_group_desc = models.CharField(max_length=100,blank=True, null=True)
	from_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	to_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
		return str(self.price_group_id)

	class Meta:
		db_table = "PriceGroupMaster"


class SalesOffMaster(models.Model):
	salesoff_id = models.AutoField(primary_key=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	sales_office = models.CharField(max_length=4, blank=False, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
		return str(self.salesoff_id)

	class Meta:
		db_table = "SalesOffMaster"


class SalesDistMaster(models.Model):
	salesdist_id = models.AutoField(primary_key=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	sales_dist_code = models.CharField(max_length=6, blank=False, null=False,unique=True)
	sales_dist_name = models.CharField(max_length=50, blank=False, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
		return str(self.salesdist_id)

	class Meta:
		db_table = "SalesDistMaster"





class ClusterMaster(models.Model):
	cluster_id = models.AutoField(primary_key=True)
	unit_id = models.ForeignKey(to="UnitMaster", to_field="unit_id", on_delete=models.PROTECT, null=True)
	cluster_code = models.CharField(max_length=4, blank=False, null=False,unique=True)
	cluster_name = models.CharField(max_length=50, blank=False, null=False)
	status = models.PositiveSmallIntegerField(default=1, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
	create_user = models.CharField(max_length=20,blank=True, null=True)
	update_user = models.CharField(max_length=20,blank=True, null=True)

	def __str__(self):
		return str(self.cluster_id)

	class Meta:
		db_table = "ClusterMaster"


