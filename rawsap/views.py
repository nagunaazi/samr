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


from .serializers import *


# test comment
class ZVT_PORTAL_CIRViewSet(viewsets.ModelViewSet):
	
	queryset = ZVT_PORTAL_CIR.objects.all()
	serializer_class = ZVT_PORTAL_CIRSerializer_List
	http_method_names = ['get']
	filter_backends = (DjangoFilterBackend,OrderingFilter,)
	ordering_fields = '__all__'

	
	def get_queryset(self):
		queryset = ZVT_PORTAL_CIR.objects.all()

		ord_date = self.request.query_params.get('ord_date', None)
		vkorg = self.request.query_params.get('vkorg', None)
		vkgrp = self.request.query_params.get('vkgrp', None)
		pstyv = self.request.query_params.get('pstyv', None)
		
		
		if ord_date is not None:
			queryset = queryset.filter(ord_date=ord_date)

		if vkorg is not None:
			queryset = queryset.filter(vkorg=vkorg)

		if vkgrp is not None:
			queryset = queryset.filter(vkgrp=vkgrp)

		if pstyv is not None:
			queryset = queryset.filter(pstyv=pstyv)
		
		return queryset


	def create(self, request):
		return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)