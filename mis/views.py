from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from agency.models import StateMaster,UnitMaster,CityMaster
# Create your views here.
from django.db.models import Count
from django.core import serializers
import json


def mis_report(request):
    context=dict()
    states=StateMaster.objects.filter().order_by('pk')[:10]
    context['states']=states
    units = UnitMaster.objects.filter().order_by('pk')[:6]
    context['units'] = units

    cities = CityMaster.objects.filter().order_by('pk')[:6]
    context['cities'] = cities

    return render(request,'mis/mis-report.html',context=context)





def filter_report(request):
    context=dict()
    mystate = []
    mycity = []
    state = StateMaster.objects.get(state_code="MP")
    units = UnitMaster.objects.filter(state_id=state)[:10]
    context['units'] = units
    if request.is_ajax():
        stateId = json.loads(request.GET.get('stateId', ''))
        if stateId:
            for sid in stateId:
                id =int(sid['id'])
                state =StateMaster.objects.get(pk=id)
                mystate.append(state.pk)
            print(mystate)
            units = UnitMaster.objects.filter(pk__in=mystate)
            context['units']=units


    return render(request,'mis/filter-report.html',context)