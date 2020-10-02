import json

from django.http import request, HttpResponse, JsonResponse

from django.shortcuts import render
from django.core import serializers as srz
from django.http import HttpResponse
from django.contrib.auth.models import Permission, User
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status,viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import *
from config.views import user_log
from master.models import EducationMaster
from rawsap.models import *


from .serializers import *
from datetime import timedelta
from django.db.models import Sum


# Create your views here.


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getlast7daysavg(request,bpcode,agcode):
	data = None
	status = "Failed"
	msg = ""
	UM = None
	avg_copy = 0
	try:
		
		# if unitid:
		# 	UM = ZVT_PORTAL_CIR.objects.get(pk=unitid)
		


		SM_sum = ZVT_PORTAL_CIR.objects.filter(sold_to_party=agcode, ord_date_f__gte=datetime.now()+ timedelta(days=-7)).aggregate(Sum('gross_copy'))
		
		SM_first = ZVT_PORTAL_CIR.objects.filter(sold_to_party=agcode, ord_date_f__gte=datetime.now()+ timedelta(days=-7)).values('cust_name').distinct()
		SM_name = SM_first[0]['cust_name']
		#print(SM_first)
		if SM_sum['gross_copy__sum'] >0:
			avg_copy = SM_sum['gross_copy__sum']//7

		if SM_name:
			data ={'AGCODE':agcode,
					'AGNAME':SM_name,
					'AVGCOPY7Days': avg_copy}
			#data = SM #srz.serialize('python', SM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get last7daysavg')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get last7daysavg')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response













@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getASD(request,bpcode,unitid,salesoff,salesgrp):
	data = None
	status = "Failed"
	msg = ""
	UM = None
	try:
		
		if unitid:
			UM = UnitMaster.objects.get(pk=unitid)
		


		SM = ASDMaster.objects.filter(status=1, unit_id=UM,sales_office=salesoff,sales_group=salesgrp,from_date__lte=datetime.now(),to_date__gte=datetime.now())
		if SM:
			data = srz.serialize('python', SM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get ASD')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get ASD')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response


























@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getEducation(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		SM = EducationMaster.objects.filter(status=1)
		if SM:
			data = srz.serialize('python', SM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Education List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Education List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response












@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getState(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		SM = StateMaster.objects.filter(status=1)
		if SM:
			data = srz.serialize('python', SM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get State List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get State List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getUnit(request,bpcode,state_id=None,state_code=None):
	data = None
	status = "Failed"
	msg = ""
	try:
		SM = None
		if state_id:
			SM = StateMaster.objects.get(pk=state_id)
		if state_code:
			SM = StateMaster.objects.get(state_code=state_code)

		if SM:
			UM = UnitMaster.objects.filter(status=1,state_id=SM)
		else:
			UM = UnitMaster.objects.filter(status=1)


		if UM:
			data = srz.serialize('python', UM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Unit List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Unit List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getCity(request, bpcode,state_id=None,state_code=None):
	data = None
	status = "Failed"
	msg= ""
	try:
		SM = None
		if state_id:
			SM = StateMaster.objects.get(pk=state_id)
		if state_code:
			SM = StateMaster.objects.get(state_code=state_code)

		if SM:
			CM = CityMaster.objects.filter(status=1, state_id=SM)
		else:
			CM = CityMaster.objects.filter(status=1)

		if CM:
			data = srz.serialize('python',CM, use_natural_foreign_keys=True, use_natural_primary_keys=True )
			status= "Success"
		else:
			msg= "No Data Found"

		ul = user_log(request, bpcode, 'Agency Request', 'Get City List')

	except Exception as e:
		ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get City List')
		msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response




@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getLocation(request,bpcode,city_id=None, city_code=None, unit_id=None, unit_code=None):
	data, status, msg = None, "Failed", ""
	try:
		CM = None
		UM = None
		
		if city_id:
			CM = CityMaster.objects.get(pk=city_id)
		if city_code:
			CM = CityMaster.objects.get(city_code=city_code)
		
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code= unit_code)
		
		if CM:
			LM = LocationMaster.objects.filter(status=1, city_id= CM)
		elif UM:
			LM = LocationMaster.objects.filter(status=1,unit_id=UM)
		else:
			LM = LocationMaster.objects.filter(status=1)


		if LM:
			data = srz.serialize('python', LM)
			status = "Success"
		else:
			
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Location List')

	except Exception as e:
		ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Location List')
		msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response




@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getTown(request,bpcode,city_id=None, city_code=None, unit_id=None, unit_code=None):
	data, status, msg = None, "Failed", ""
	try:
		CM = None
		UM = None
		
		if city_id:
			CM = CityMaster.objects.get(pk=city_id)
		if city_code:
			CM = CityMaster.objects.get(city_code=city_code)
		
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code= unit_code)
		
		if CM:
			TM = TownMaster.objects.filter(status=1, city_id= CM)
		elif UM:
			TM = TownMaster.objects.filter(status=1,unit_id=UM)
		else:
			TM = TownMaster.objects.filter(status=1)


		if TM:
			data = srz.serialize('python', TM)
			status = "Success"
		else:
			
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Town List')

	except Exception as e:
		ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Town List')
		msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response






@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getPlant(request,bpcode,state_id=None, state_code=None, unit_id=None, unit_code=None):
	data, status, msg = None, "Failed", ""
	try:
		SM = None
		UM = None
		
		if state_id:
			SM = StateMaster.objects.get(pk=state_id)
		if state_code:
			SM = StateMaster.objects.get(state_code=state_code)
		
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code= unit_code)
		
		if SM:
			PM = PlantMaster.objects.filter(status=1, state_id= SM)
		elif UM:
			PM = PlantMaster.objects.filter(status=1,unit_id=UM)
		else:
			PM = PlantMaster.objects.filter(status=1)


		if PM:
			data = srz.serialize('python', PM)
			status = "Success"
		else:
			
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Plant List')

	except Exception as e:
		ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Plant List')
		msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response




@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getRoute(request,bpcode,plant_id=None, plant_code=None, unit_id=None, unit_code=None):
	data, status, msg = None, "Failed", ""
	try:
		PM = None
		UM = None
		
		if plant_id:
			PM = PlantMaster.objects.get(pk=plant_id)
		if plant_code:
			PM = PlantMaster.objects.get(plant_code=plant_code)
		
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code= unit_code)
		
		if PM:
			RM = RouteMaster.objects.filter(status=1, state_id= PM)
		elif UM:
			RM = RouteMaster.objects.filter(status=1,unit_id=UM)
		else:
			RM = RouteMaster.objects.filter(status=1)


		if RM:
			data = srz.serialize('python', RM)
			status = "Success"
		else:
			
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Route List')

	except Exception as e:
		ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Route List')
		msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response





@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getDroppingPoint(request,bpcode,route_id=None,route_code=None):
	data = None
	status = "Failed"
	msg = ""
	try:
		RM = None
		if route_id:
			RM = RouteMaster.objects.get(pk=route_id)
		if route_code:
			RM = RouteMaster.objects.get(route_code=route_code)

		if RM:
			DPM = DroppingPointMaster.objects.filter(status=1,route_id=RM)
		else:
			DPM = DroppingPointMaster.objects.filter(status=1)


		if DPM:
			data = srz.serialize('python', DPM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Dropping Point List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Dropping Point List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getPublication(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		PM = PublicationMaster.objects.filter(status=1)
		if PM:
			data = srz.serialize('python', PM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Publication List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Publication List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getEdition(request,bpcode,publication_id=None,publication_code=None):
	data = None
	status = "Failed"
	msg = ""
	try:
		EM = None
		PM = None
		if publication_id:
			PM = PublicationMaster.objects.get(pk=publication_id)
		if publication_code:
			PM = PublicationMaster.objects.get(publication_code=publication_code)

		if PM:
			EM = EditionMaster.objects.filter(status=1,publication_id=PM)
		else:
			EM = EditionMaster.objects.filter(status=1)


		if EM:
			data = srz.serialize('python', EM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Edition List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Edition List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getNewsPaper(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		NP = NewspaperMaster.objects.filter(status=1)
		if NP:
			data = srz.serialize('python', NP, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Newspaper List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Newspaper List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getDesignation(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		DM = DesignationMaster.objects.filter(status=1)
		if DM:
			data = srz.serialize('python', DM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get DesignationMaster List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get DesignationMaster List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getDepartment(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		DM = DepartmentMaster.objects.filter(status=1)
		if DM:
			data = srz.serialize('python', DM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get DepartmentMaster List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get DepartmentMaster List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getAddressProof(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		APM = AddressProofMaster.objects.filter(status=1)
		if APM:
			data = srz.serialize('python', APM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get AddressProof Master List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get AddressProof Master List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response




@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getCommission(request,bpcode,unit_id=None,unit_code=None):
	data = None
	status = "Failed"
	msg = ""
	try:
		UM = None
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code=unit_code)

		if UM:
			CM = CommissionMaster.objects.filter(status=1,unit_id=UM)
		else:
			CM = CommissionMaster.objects.filter(status=1)


		if CM:
			data = srz.serialize('python', CM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Unit List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Unit List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response





@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getRealtion(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		RM = RealtionMaster.objects.filter(status=1)
		if RM:
			data = srz.serialize('python', RM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Realtion Master  List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Realtion Master  List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getMaritialStatus(request,bpcode):
	data = None
	status = "Failed"
	msg = ""
	try:
		MSM = MaritialStatusMaster.objects.filter(status=1)
		if MSM:
			data = srz.serialize('python', MSM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Maritial Status Master  List')
		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Maritial Status Master  List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response




class AgencyRequestAGDetailViewSet(viewsets.ModelViewSet):
	queryset = AgencyRequestAGDetail.objects.all()
	serializer_class = AgencyRequestAGDetailSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'





class AgencyRequestReasonViewSet(viewsets.ModelViewSet):
	queryset = AgencyRequestReason.objects.all()
	serializer_class = AgencyRequestReasonSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'

		



	# def create(self,request):

	# 	serializer = self.get_serializer(data=request.data)
	# 	serializer.is_valid(raise_exception=True)
	# 	self.perform_create(serializer)
	# 	headers = self.get_success_headers(serializer.data)
		
	# 	return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
	# def perform_create(self, serializer):
	# 	serializer.save(owner=self.request.user)





class AgencyRequestViewSet(viewsets.ModelViewSet):
	
	queryset = AgencyRequestMaster.objects.all()
	serializer_class = AgencyRequestMasterSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'

	
	# def get_serializer_class(self):
	# 	if self.action == 'retrive':
	# 	 	if hasattr(self,serializer_class):
	# 	 		return self.serializer_class

	# 	return super().get_serializer_class()

	
	def get_queryset(self):
		queryset = AgencyRequestMaster.objects.all()

		state_id = self.request.query_params.get('state_id', None)
		unit_id = self.request.query_params.get('unit_id', None)
		city_id = self.request.query_params.get('city_id', None)
		location_id = self.request.query_params.get('location_id', None)
		town_id = self.request.query_params.get('town_id', None)
		if state_id is not None:
			queryset = queryset.filter(state_id=state_id)

		if unit_id is not None:
			queryset = queryset.filter(unit_id=unit_id)

		if city_id is not None:
			queryset = queryset.filter(city_id=city_id)

		if location_id is not None:
			queryset = queryset.filter(location_id=location_id)

		if town_id is not None:
			queryset = queryset.filter(town_id=town_id)

		return queryset


	
	# def create(self,request):
	# 	#print("Hi2")
	# 	message = request.data.pop('message_type')

	# 	if message == 'NewRequest':

	# 		data = request.data.pop('data')
	# 		ag_header = data.pop('ag_header')


	# 		serializer = self.get_serializer(data=ag_header)
	# 		serializer.is_valid(raise_exception=True)
	# 		self.perform_create(serializer)
	# 		headers = self.get_success_headers(serializer.data)
			
	# 		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



	# 		# ag_header = AgencyRequestMaster.objects.create(**ag_header)

	# 		# return Response(status=status.HTTP_201_CREATED)



	# def perform_create(self, serializer):
	# 	serializer.save()




# @api_view(['POST'])
# @authentication_classes([BasicAuthentication])
# def saveAgencyRequest(request):

class AgencyRequestSurveyViewSet(viewsets.ModelViewSet):
	
	queryset = AgencyRequestSurvey.objects.all()
	serializer_class = AgencyRequestSurveySerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'



class AgencyRequestSurveyVillageViewSet(viewsets.ModelViewSet):
	
	queryset = AgencyRequestSurveyVillage.objects.all()
	serializer_class = AgencyRequestSurveyVillageSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'




class AgencyRequestSurveyTargetViewSet(viewsets.ModelViewSet):
	
	queryset = AgencyRequestSurveyTarget.objects.all()
	serializer_class = AgencyRequestSurveyTargetSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'



class AgencyRequestKYBPViewSet(viewsets.ModelViewSet):
	
	queryset = AgencyRequestKYBP.objects.all()
	serializer_class = AgencyRequestKYBPSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'

class Agency_ChildViewSet(viewsets.ModelViewSet):
	
	queryset = Agency_Child.objects.all()
	serializer_class = Agency_ChildSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'


class Agency_OtherNewsPaperViewSet(viewsets.ModelViewSet):
	
	queryset = Agency_OtherNewsPaper.objects.all()
	serializer_class = Agency_OtherNewsPaperSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'



class AgencyRequestCIRReqViewSet(viewsets.ModelViewSet):
	
	queryset = AgencyRequestCIRReq.objects.all()
	serializer_class = AgencyRequestCIRReqSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'


class CirReqEditionViewSet(viewsets.ModelViewSet):
	
	queryset = CirReqEdition.objects.all()
	serializer_class = CirReqEditionSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'


class CirReqDroppingViewSet(viewsets.ModelViewSet):
	
	queryset = CirReqDropping.objects.all()
	serializer_class = CirReqDroppingSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'


class CirReqChequeViewSet(viewsets.ModelViewSet):
	
	queryset = CirReqCheque.objects.all()
	serializer_class = CirReqChequeSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'




class TeamViewSet(viewsets.ModelViewSet):
	
	queryset = TeamMaster.objects.all()
	serializer_class = TeamMasterSerializer
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'

	
	def get_queryset(self):
		queryset = TeamMaster.objects.all()

		state_id = self.request.query_params.get('state_id', None)
		state_code = self.request.query_params.get('state_code', None)
		unit_id = self.request.query_params.get('unit_id', None)
		unit_code = self.request.query_params.get('unit_code', None)

		access_type = self.request.query_params.get('access_type', None)
		
		if state_id is not None:
			queryset = queryset.filter(state_id=state_id)
		
		# SM = None
		if state_code is not None:
			SM = StateMaster.objects.get(state_code=state_code)
			queryset = queryset.filter(state_id=SM)

		if unit_id is not None:
			queryset = queryset.filter(unit_id=unit_id)
		
		if unit_code is not None:
			UM = UnitMaster.objects.get(unit_code=unit_code,status=1)
			queryset = queryset.filter(unit_id=UM)


		if access_type is not None:
			queryset = queryset.filter(access_type=access_type)

		
			


		return queryset

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getCluster(request,bpcode,unit_id=None,unit_code=None):
	data = None
	status = "Failed"
	msg = ""
	UM = None
	try:
		SM = None
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code=unit_code)


		if UM:
			CM = ClusterMaster.objects.filter(status=1,unit_id=UM)

		


		if CM:
			data = srz.serialize('python', CM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Cluster List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Cluster List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response




@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getSalesDist(request,bpcode,unit_id=None,unit_code=None):
	data = None
	status = "Failed"
	msg = ""
	UM = None
	try:
		SM = None
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code=unit_code)


		if UM:
			CM = SalesDistMaster.objects.filter(status=1,unit_id=UM)

		


		if CM:
			data = srz.serialize('python', CM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Sales Dist List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Sales Dist List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response




@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getSalesOff(request,bpcode,unit_id=None,unit_code=None):
	data = None
	status = "Failed"
	msg = ""
	UM = None
	try:
		SM = None
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code=unit_code)


		if UM:
			CM = SalesOffMaster.objects.filter(status=1,unit_id=UM)

		


		if CM:
			data = srz.serialize('python', CM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Sales Off List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Sales Off List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response



@api_view(['GET'])
@authentication_classes([BasicAuthentication])
def getPricegrp(request,bpcode,copies,unit_id=None,unit_code=None):
	data = None
	status = "Failed"
	msg = ""
	UM = None
	try:
		SM = None
		if unit_id:
			UM = UnitMaster.objects.get(pk=unit_id)
		if unit_code:
			UM = UnitMaster.objects.get(unit_code=unit_code)


		if UM:
			CM = PriceGroupMaster.objects.filter(status=1,unit_id=UM,min_copy_limit__lte=copies, max_copy_limit__gte=copies,from_date__lte=datetime.now(),to_date__gte=datetime.now())

		


		if CM:
			data = srz.serialize('python', CM, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			status = "Success"
		else:
			#status = "Success"
			msg = "No Data Found"
		
		ul = user_log(request, bpcode, 'Agency Request', 'Get Price grp List')

		# response['Cache-Control'] = f'max-age={60*60*24}'
	except Exception as e:
	    ul = user_log(request, bpcode, 'Agency Request', 'Error on : Get Price grp List')
	    msg = str(e)

	response = JsonResponse({'data':data,'status':status,'msg':msg})
	return response

