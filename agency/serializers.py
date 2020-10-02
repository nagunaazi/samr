from .models import *
from master.models import EducationMaster
from rest_framework import serializers
from datetime import datetime
from drf_base64.fields import Base64FileField
# from drf_extra_fields.fields import Base64FileField

class TeamMasterSerializer(serializers.ModelSerializer):
	

	class Meta:
		model = TeamMaster
		fields = '__all__'











class AgencyRequestReasonSerializer(serializers.ModelSerializer):


	#ag_req_id = AgencyRequestMasterSerializer(many=True)
	#ag_req_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestMaster.objects.all())

	class Meta:
		model = AgencyRequestReason
		fields = ('reason','ag_code','ag_copies','ag_reason',)

	# def create(self, validated_data):
	# 	return AgencyRequestReason.objects.create(**validated_data)












class AgencyRequestSurveyVillageSerializer(serializers.ModelSerializer):

	#survey_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestSurvey.objects.all())#AgencyRequestSurveySerializer(many=True)

	class Meta:
		model = AgencyRequestSurveyVillage
		fields = ('village_name','village_copies',)
		# fields = '__all__'

	def create(self, validated_data):
		return AgencyRequestSurveyVillage.objects.create(**validated_data)






class AgencyRequestSurveyTargetSerializer(serializers.ModelSerializer):

	#survey_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestSurvey.objects.all())
	class Meta:
		model = AgencyRequestSurveyTarget
		# fields = '__all__'
		fields = ('agency_name',
'agecy_code',
'cur_copies',
'month_one',
'month_two',
'month_three',
)


	def create(self, validated_data):

		return AgencyRequestSurveyTarget.objects.create(**validated_data)







class Agency_ChildSerializer(serializers.ModelSerializer):

	# kybp_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestKYBP.objects.all())
	child_education = serializers.PrimaryKeyRelatedField(queryset=EducationMaster.objects.all())

	class Meta:
		model = Agency_Child
		# fields = '__all__'
		fields = ('child_name',
'child_DOB',
'child_education',
'child_gender',
)


	def create(self, validated_data):
		child_education = validated_data.pop('child_education')
		return Agency_Child.objects.create(child_education=child_education,**validated_data)


class Agency_OtherNewsPaperSerializer(serializers.ModelSerializer):

	# kybp_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestKYBP.objects.all())
	

	class Meta:
		model = Agency_OtherNewsPaper
		fields = ('newspaper_id',)
		# fields = '__all__'

	def create(self, validated_data):

		return Agency_OtherNewsPaper.objects.create(**validated_data)








class CirReqEditionSerializer(serializers.ModelSerializer):

	# cirreq_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestCIRReq.objects.all())
	edition_id = serializers.PrimaryKeyRelatedField(queryset=EditionMaster.objects.all())
	

	class Meta:
		model = CirReqEdition
		# fields = '__all__'
		fields = ('edition_id',
'edition_copies',

)

	def create(self, validated_data):
		edition_id = validated_data.pop('edition_id')
		return CirReqEdition.objects.create(edition_id=edition_id,**validated_data)





class CirReqDroppingSerializer(serializers.ModelSerializer):

	# cirreq_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestCIRReq.objects.all())
	dropping_id = serializers.PrimaryKeyRelatedField(queryset=DroppingPointMaster.objects.all())
	route_id = serializers.PrimaryKeyRelatedField(queryset=RouteMaster.objects.all())
	

	class Meta:
		model = CirReqDropping
		# fields = '__all__'
		fields = ('dropping_id',
'route_id',
'contact_no',
'sub_agent_code',
'sub_agent_name',
'sub_agent_contact_no',
'sub_agent_copies',
'self_copies',
)

	def create(self, validated_data):
		dropping_id = validated_data.pop('dropping_id')
		route_id = validated_data.pop('route_id')
		return CirReqDropping.objects.create(route_id=route_id,dropping_id=dropping_id,**validated_data)





class CirReqChequeSerializer(serializers.ModelSerializer):

	#cirreq_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestCIRReq.objects.all())
	# dropping_id = serializers.PrimaryKeyRelatedField(queryset=DroppingPointMaster.objects.all())
	# route_id = serializers.PrimaryKeyRelatedField(queryset=RouteMaster.objects.all())
	

	class Meta:
		model = CirReqCheque
		#fields = '__all__'
		fields = ('cheque_mode',
'cheque_number',
'cheque_date',
'cheque_amt',
'cheque_bank',
)

	def create(self, validated_data):

		return CirReqCheque.objects.create(**validated_data)


# Final For POST
class AgencyRequestCIRReqSerializer(serializers.ModelSerializer):

	# ag_detail_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestAGDetail.objects.all())
	CirReqEdition_set = CirReqEditionSerializer(many=True)
	CirReqDropping_set = CirReqDroppingSerializer(many=True)
	CirReqCheque_set = CirReqChequeSerializer(many=True)

	class Meta:
		model = AgencyRequestCIRReq
		# fields = '__all__'
		fields = ('edition_count',
'start_date',
'commission_per',
'commission_amt',
'asd_as_per_norms',
'asd_collected',
'cheque_count',
'asd_mode',
'asd_days',
'dropping_count',
'executive_code',
'executive_name',
'UOH_code',
'UOH_name',
'SOH_code',
'SOH_name',
'creation_comments','CirReqEdition_set','CirReqDropping_set','CirReqCheque_set',
)

	def create(self, validated_data):
		CirReqEdition_validated_data = validated_data.pop('CirReqEdition_set')
		CirReqDropping_validated_data = validated_data.pop('CirReqDropping_set')
		CirReqCheque_validated_data = validated_data.pop('CirReqCheque_set')

		AGRCIRR = AgencyRequestCIRReq.objects.create(**validated_data)

		CirReqEdition_set_serializer = self.fields['CirReqEdition_set']
		for each in CirReqEdition_validated_data:
			each['cirreq_id'] = AGRCIRR
			#each['reason'] = validated_data.pop('reason')
		AG_CirReqEdition = CirReqEdition_set_serializer.create(CirReqEdition_validated_data)

		CirReqDropping_set_serializer = self.fields['CirReqDropping_set']
		for each in CirReqDropping_validated_data:
			each['cirreq_id'] = AGRCIRR
			#each['reason'] = validated_data.pop('reason')
		AG_CirReqDropping = CirReqDropping_set_serializer.create(CirReqDropping_validated_data)

		CirReqCheque_set_serializer = self.fields['CirReqCheque_set']
		for each in CirReqCheque_validated_data:
			each['cirreq_id'] = AGRCIRR
			#each['reason'] = validated_data.pop('reason')
		AG_CirReqCheque = CirReqCheque_set_serializer.create(CirReqCheque_validated_data)



		return AGRCIRR


class AgencyRequestKYBPSerializer(serializers.ModelSerializer):

	#ag_detail_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestAGDetail.objects.all())  #AgencyRequestAGDetailSerializer(many=True)
	resi_city = serializers.PrimaryKeyRelatedField(queryset=CityMaster.objects.all())
	resi_state = serializers.PrimaryKeyRelatedField(queryset=StateMaster.objects.all())

	busi_city = serializers.PrimaryKeyRelatedField(queryset=CityMaster.objects.all())
	busi_state = serializers.PrimaryKeyRelatedField(queryset=StateMaster.objects.all())

	ag_maritial_id = serializers.PrimaryKeyRelatedField(queryset=MaritialStatusMaster.objects.all())
	
	db_dept = serializers.PrimaryKeyRelatedField(queryset=DepartmentMaster.objects.all())

	db_desig = serializers.PrimaryKeyRelatedField(queryset=DesignationMaster.objects.all())
	db_relation = serializers.PrimaryKeyRelatedField(queryset=RealtionMaster.objects.all())
	db_city = serializers.PrimaryKeyRelatedField(queryset=CityMaster.objects.all())
	add_proof_type = serializers.PrimaryKeyRelatedField(queryset=AddressProofMaster.objects.all())


	Agency_Child_set = Agency_ChildSerializer(many=True)
	Agency_OtherNewsPaper_set = Agency_OtherNewsPaperSerializer(many=True)

	pan_copy = Base64FileField(allow_null=True,required=False)
	add_proof_copy = Base64FileField(allow_null=True,required=False)
	bank_copy = Base64FileField(allow_null=True,required=False)
	



	class Meta:
		model = AgencyRequestKYBP
		# fields = '__all__'
		fields = ('ag_gender',
			'ag_title',
'first_name',
'middle_name',
'last_name',
'agency_name',
'resi_houseno',
'resi_building',
'resi_street',
'resi_city',
'resi_state',
'resi_pincode',
'resi_mono',
'resi_watsup',
'resi_email',
'busi_houseno',
'busi_building',
'busi_street',
'busi_city',
'busi_state',
'busi_pincode',
'busi_mono',
'busi_watsup',
'busi_email',
'ag_religion',
'ag_dob',
'ag_maritial_id',
'spouse_name',
'spouse_dob',
'ag_marrige_ani',
'no_of_children',
'father_name',
'father_dob',
'mother_name',
'mother_dob',
'brother_name',
'brother_dob',
'sister_name',
'sister_dob',
'nominee_name',
'nominee_relation',
'other_nespaper_count',
'bank_holder_name',
'bank_acc_no',
'bank_name_branch',
'bank_address',
'bank_IFSC',
'GSTIN',
'ag_db_relative',
'db_gender',
'db_fullname',
'db_empid',
'db_dept',
'db_desig',
'db_relation',
'db_city',
'pan_no',
'pan_copy',
'add_proof_type',
'add_proof_no',
'add_proof_copy',
'bank_copy_type',
'bank_copy','Agency_Child_set','Agency_OtherNewsPaper_set',
)

	def create(self, validated_data):
		
		resi_city = validated_data.pop('resi_city')#serializers.PrimaryKeyRelatedField(queryset=CityMaster.objects.all())
		resi_state = validated_data.pop('resi_state')#serializers.PrimaryKeyRelatedField(queryset=StateMaster.objects.all())

		busi_city = validated_data.pop('busi_city')#serializers.PrimaryKeyRelatedField(queryset=CityMaster.objects.all())
		busi_state = validated_data.pop('busi_state')#serializers.PrimaryKeyRelatedField(queryset=StateMaster.objects.all())

		ag_maritial_id = validated_data.pop('ag_maritial_id')#serializers.PrimaryKeyRelatedField(queryset=MaritialStatusMaster.objects.all())
		
		db_dept = validated_data.pop('db_dept')#serializers.PrimaryKeyRelatedField(queryset=DepartmentMaster.objects.all())

		db_desig = validated_data.pop('db_desig')#serializers.PrimaryKeyRelatedField(queryset=DesignationMaster.objects.all())
		db_relation = validated_data.pop('db_relation')#serializers.PrimaryKeyRelatedField(queryset=RealtionMaster.objects.all())
		db_city = validated_data.pop('db_city')#serializers.PrimaryKeyRelatedField(queryset=CityMaster.objects.all())
		add_proof_type = validated_data.pop('add_proof_type')#serializers.PrimaryKeyRelatedField(queryset=AddressProofMaster.objects.all())

		Agency_Child_validated_data = validated_data.pop('Agency_Child_set')
		Agency_OtherNewsPaper_validated_data = validated_data.pop('Agency_OtherNewsPaper_set')

		AGKYBP = AgencyRequestKYBP.objects.create(add_proof_type=add_proof_type,db_city=db_city,db_relation=db_relation,db_desig=db_desig,db_dept=db_dept,ag_maritial_id=ag_maritial_id,busi_state=busi_state,busi_city=busi_city,resi_city=resi_city,resi_state=resi_state,**validated_data)


		Agency_Child_set_serializer = self.fields['Agency_Child_set']
		for each in Agency_Child_validated_data:
			each['kybp_id'] = AGKYBP
			#each['reason'] = validated_data.pop('reason')
		AG_Agency_Child = Agency_Child_set_serializer.create(Agency_Child_validated_data)

		Agency_OtherNewsPaper_set_serializer = self.fields['Agency_OtherNewsPaper_set']
		for each in Agency_OtherNewsPaper_validated_data:
			each['kybp_id'] = AGKYBP
			#each['reason'] = validated_data.pop('reason')
		AG_Agency_OtherNewsPaper = Agency_OtherNewsPaper_set_serializer.create(Agency_OtherNewsPaper_validated_data)




		return AGKYBP














class AgencyRequestSurveySerializer(serializers.ModelSerializer):

	#ag_detail_id = AgencyRequestAGDetailSerializer(many=True)
	AgencyRequestSurveyVillage_set = AgencyRequestSurveyVillageSerializer(many=True)
	AgencyRequestSurveyTarget_set = AgencyRequestSurveyTargetSerializer(many=True)

	class Meta:
		model = AgencyRequestSurvey
		# fields = '__all__'
		fields = ('tot_copies',
'cash_copies',
'subagenct_copies',
'vendor_copies',
'railway_copies',
'self_copies',
'UOH_meeting_flag',
'UOH_meeting_mode',
'uoh_meeting_remark',
'SOH_meeting_flag',
'SOH_meeting_mode',
'SOH_meeting_remark','AgencyRequestSurveyVillage_set','AgencyRequestSurveyTarget_set',
)


	def create(self, validated_data):
		AgencyRequestSurveyVillage_validated_data = validated_data.pop('AgencyRequestSurveyVillage_set')
		AgencyRequestSurveyTarget_validated_data = validated_data.pop('AgencyRequestSurveyTarget_set')


		ARS = AgencyRequestSurvey.objects.create(**validated_data)


		AgencyRequestSurveyVillage_set_serializer = self.fields['AgencyRequestSurveyVillage_set']
		for each in AgencyRequestSurveyVillage_validated_data:
			each['survey_id'] = ARS
			#each['reason'] = validated_data.pop('reason')
		AG_AgencyRequestSurveyVillage = AgencyRequestSurveyVillage_set_serializer.create(AgencyRequestSurveyVillage_validated_data)
		


		AgencyRequestSurveyTarget_set_serializer = self.fields['AgencyRequestSurveyTarget_set']
		for each in AgencyRequestSurveyTarget_validated_data:
			each['survey_id'] = ARS
			#each['reason'] = validated_data.pop('reason')
		AG_AgencyRequestSurveyTarget = AgencyRequestSurveyTarget_set_serializer.create(AgencyRequestSurveyTarget_validated_data)
		


		return ARS







class AgencyRequestAGDetailSerializer(serializers.ModelSerializer):

	#ag_req_id = serializers.PrimaryKeyRelatedField(queryset=AgencyRequestMaster.objects.all())
	
	cluster_id = serializers.PrimaryKeyRelatedField(queryset=ClusterMaster.objects.all())
	salesdist_id = serializers.PrimaryKeyRelatedField(queryset=SalesDistMaster.objects.all())
	salesoff_id = serializers.PrimaryKeyRelatedField(queryset=SalesOffMaster.objects.all())
	price_group_id = serializers.PrimaryKeyRelatedField(queryset=PriceGroupMaster.objects.all())

	AgencyRequestSurvey_set = AgencyRequestSurveySerializer(many=True)
	AgencyRequestKYBP_set = AgencyRequestKYBPSerializer(many=True)
	AgencyRequestCIRReq_set = AgencyRequestCIRReqSerializer(many=True)


	class Meta:
		model = AgencyRequestAGDetail
		fields = ('agenct_name','agency_name','cluster_id','salesdist_id','salesoff_id','price_group_id','custgrp','final_status','AgencyRequestSurvey_set','AgencyRequestKYBP_set','AgencyRequestCIRReq_set',)
		# fields = '__all__'

	def create(self, validated_data):
		AgencyRequestSurvey_validated_data = validated_data.pop('AgencyRequestSurvey_set')
		AgencyRequestKYBP_validated_data = validated_data.pop('AgencyRequestKYBP_set')
		AgencyRequestCIRReq_validated_data = validated_data.pop('AgencyRequestCIRReq_set')
		final_status = validated_data.pop('final_status')
		final_status = 0 
		ARAGD = AgencyRequestAGDetail.objects.create(final_status=final_status,**validated_data)
		

		AgencyRequestSurvey_set_serializer = self.fields['AgencyRequestSurvey_set']
		for each in AgencyRequestSurvey_validated_data:
			each['ag_detail_id'] = ARAGD
			#each['reason'] = validated_data.pop('reason')
		AG_AgencyRequestSurvey = AgencyRequestSurvey_set_serializer.create(AgencyRequestSurvey_validated_data)
		

		AgencyRequestKYBP_set_serializer = self.fields['AgencyRequestKYBP_set']
		for each in AgencyRequestKYBP_validated_data:
			each['ag_detail_id'] = ARAGD
			#each['reason'] = validated_data.pop('reason')
		AG_AgencyRequestKYBP = AgencyRequestKYBP_set_serializer.create(AgencyRequestKYBP_validated_data)
		

		AgencyRequestCIRReq_set_serializer = self.fields['AgencyRequestCIRReq_set']
		for each in AgencyRequestCIRReq_validated_data:
			each['ag_detail_id'] = ARAGD
			#each['reason'] = validated_data.pop('reason')
		AG_AgencyRequestCIRReq = AgencyRequestCIRReq_set_serializer.create(AgencyRequestCIRReq_validated_data)
		


		return ARAGD






#Final AG_Request MAster

class AgencyRequestMasterSerializer(serializers.ModelSerializer):
	state_id = serializers.PrimaryKeyRelatedField(queryset=StateMaster.objects.all())
	unit_id = serializers.PrimaryKeyRelatedField(queryset=UnitMaster.objects.all())
	city_id = serializers.PrimaryKeyRelatedField(queryset=CityMaster.objects.all())
	location_id = serializers.PrimaryKeyRelatedField(queryset=LocationMaster.objects.all())
	town_id = serializers.PrimaryKeyRelatedField(queryset=TownMaster.objects.all())
	
	AgencyRequestReason_set = AgencyRequestReasonSerializer(many=True)
	AgencyRequestAGDetail_set = AgencyRequestAGDetailSerializer(many=True)
	#AgencyRequestReason_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)#serializers.StringRelatedField(many=True)




	class Meta:
		model = AgencyRequestMaster
		# fields = '__all__' 
		fields = ('ag_req_id','state_id','unit_id','city_id','location_id','town_id','pincode','population',
			'tot_copies','main_copies','jj_copies','city_upc','reason','proposed_count',
			'status','create_user','update_user','AgencyRequestReason_set','AgencyRequestAGDetail_set',)


	def create(self, validated_data):
		state_id = validated_data.pop('state_id')
		unit_id = validated_data.pop('unit_id')
		city_id = validated_data.pop('city_id')
		location_id = validated_data.pop('location_id')
		town_id = validated_data.pop('town_id')
		AgencyRequestReason_validated_data = validated_data.pop('AgencyRequestReason_set')
		AgencyRequestAGDetail_validated_data = validated_data.pop('AgencyRequestAGDetail_set')



		AG_Request_Mst = AgencyRequestMaster.objects.create(state_id=state_id,unit_id=unit_id,city_id=city_id,location_id=location_id,town_id=town_id,**validated_data)

		
		AgencyRequestReason_set_serializer = self.fields['AgencyRequestReason_set']
		for each in AgencyRequestReason_validated_data:
			each['ag_req_id'] = AG_Request_Mst
			each['reason'] = validated_data.pop('reason')
		AG_REQ_R = AgencyRequestReason_set_serializer.create(AgencyRequestReason_validated_data)


		AgencyRequestAGDetail_set_serializer = self.fields['AgencyRequestAGDetail_set']
		for each in AgencyRequestAGDetail_validated_data:
			each['ag_req_id'] = AG_Request_Mst
			#each['reason'] = validated_data.pop('reason')
		AG_AgencyRequestAGDetail = AgencyRequestAGDetail_set_serializer.create(AgencyRequestAGDetail_validated_data)


		return AG_Request_Mst