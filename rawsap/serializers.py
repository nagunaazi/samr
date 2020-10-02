from .models import *
from rest_framework import serializers
from datetime import datetime


class ZVT_PORTAL_CIRSerializer_List(serializers.ModelSerializer):


	class Meta:
		model = ZVT_PORTAL_CIR
		fields = '__all__'