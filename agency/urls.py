from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls


router = DefaultRouter()
router.register('agrequest',AgencyRequestViewSet,basename='agrequest')

router.register('AgencyRequestReason',AgencyRequestReasonViewSet,basename='AgencyRequestReason')
router.register('AgencyRequestAGDetail',AgencyRequestAGDetailViewSet,basename='AgencyRequestAGDetail')

router.register('AgencyRequestSurvey',AgencyRequestSurveyViewSet,basename='AgencyRequestSurvey')
router.register('AgencyRequestSurveyVillage',AgencyRequestSurveyVillageViewSet,basename='AgencyRequestSurveyVillage')
router.register('AgencyRequestSurveyTarget',AgencyRequestSurveyTargetViewSet,basename='AgencyRequestSurveyTarget')


router.register('AgencyRequestKYBP',AgencyRequestKYBPViewSet,basename='AgencyRequestKYBP')
router.register('Agency_Child',Agency_ChildViewSet,basename='Agency_Child')
router.register('Agency_OtherNewsPaper',Agency_OtherNewsPaperViewSet,basename='Agency_OtherNewsPaper')


router.register('AgencyRequestCIRReq',AgencyRequestCIRReqViewSet,basename='AgencyRequestCIRReq')
router.register('CirReqEdition',CirReqEditionViewSet,basename='CirReqEdition')
router.register('CirReqDropping',CirReqDroppingViewSet,basename='CirReqDropping')
router.register('CirReqCheque',CirReqChequeViewSet,basename='CirReqCheque')

router.register('TeamMaster',TeamViewSet,basename='TeamMaster')




urlpatterns = [
    path('getEducation/<str:bpcode>',getEducation,name="getEducation"),
    path('getState/<str:bpcode>', getState, name="getState"),
    
    path('getUnit/<str:bpcode>',getUnit,name="getUnit"),
    path('getUnit/<str:bpcode>/<int:state_id>',getUnit,name="getUnit"),
    path('getUnit/<str:bpcode>/<str:state_code>',getUnit,name="getUnit"),
# getcity 
    path('getCity/<str:bpcode>',getCity,name="getCity"),
    path('getCity/<str:bpcode>/<int:state_id>',getCity,name="getCity"),
    path('getCity/<str:bpcode>/<str:state_code>',getCity,name="getCity"),

# getlocation
    path('getLocation/<str:bpcode>',getLocation,name="getLocation"),
    path('getLocationCity/<str:bpcode>/<int:city_id>',getLocation,name="getLocation"),
    path('getLocationCity/<str:bpcode>/<str:city_code>',getLocation,name="getLocation"),
    path('getLocationUnit/<str:bpcode>/<int:unit_id>',getLocation,name="getLocation"),
    path('getLocationUnit/<str:bpcode>/<str:unit_code>',getLocation,name="getLocation"),


# getTown
    path('getTown/<str:bpcode>',getTown,name="getTown"),
    path('getTownCity/<str:bpcode>/<int:city_id>',getTown,name="getTown"),
    path('getTownCity/<str:bpcode>/<str:city_code>',getTown,name="getTown"),
    path('getTownUnit/<str:bpcode>/<int:unit_id>',getTown,name="getTown"),
    path('getTownUnit/<str:bpcode>/<str:unit_code>',getTown,name="getTown"),

# getPlant
    path('getPlant/<str:bpcode>',getTown,name="getPlant"),
    path('getPlantState/<str:bpcode>/<int:state_id>',getPlant,name="getPlant"),
    path('getPlantState/<str:bpcode>/<str:state_code>',getPlant,name="getPlant"),
    path('getPlantUnit/<str:bpcode>/<int:unit_id>',getPlant,name="getPlant"),
    path('getPlantUnit/<str:bpcode>/<str:unit_code>',getPlant,name="getPlant"),


# getRoute
    path('getRoute/<str:bpcode>',getRoute,name="getRoute"),
    path('getRoutePlant/<str:bpcode>/<int:plant_id>',getRoute,name="getRoute"),
    path('getRoutePlant/<str:bpcode>/<str:plant_code>',getRoute,name="getRoute"),
    path('getRouteUnit/<str:bpcode>/<int:unit_id>',getRoute,name="getRoute"),
    path('getRouteUnit/<str:bpcode>/<str:unit_code>',getRoute,name="getRoute"),

# getDroppingPoint
    path('getDroppingPoint/<str:bpcode>',getDroppingPoint,name="getDroppingPoint"),
    path('getDroppingPoint/<str:bpcode>/<int:route_id>',getDroppingPoint,name="getDroppingPoint"),
    path('getDroppingPoint/<str:bpcode>/<str:route_code>',getDroppingPoint,name="getDroppingPoint"),


    path('getPublication/<str:bpcode>', getPublication, name="getPublication"),

# getEdition
    path('getEdition/<str:bpcode>',getEdition,name="getEdition"),
    path('getEdition/<str:bpcode>/<int:publication_id>',getEdition,name="getEdition"),
    path('getEdition/<str:bpcode>/<str:publication_code>',getEdition,name="getEdition"),

# getNewsPaper
    path('getNewsPaper/<str:bpcode>', getNewsPaper, name="getNewsPaper"),
# Designation Master
    path('getDesignation/<str:bpcode>', getDesignation, name="getDesignation"),


# Department Master
    path('getDepartment/<str:bpcode>', getDepartment, name="getDepartment"),


#AddressProof Master
    path('getAddressProof/<str:bpcode>', getAddressProof, name="getAddressProof"),

#CommissionMaster 
    path('getCommission/<str:bpcode>', getCommission, name="getCommission"),
    path('getCommission/<str:bpcode>/<int:unit_id>',getCommission,name="getCommission"),
    path('getCommission/<str:bpcode>/<str:unit_code>',getCommission,name="getCommission"),


#Realtion Master
    path('getRealtion/<str:bpcode>', getRealtion, name="getRealtion"),

#Maritial Status Master
    path('getMaritialStatus/<str:bpcode>', getMaritialStatus, name="getMaritialStatus"),

#ASD
    path('getASD/<str:bpcode>/<int:unitid>/<str:salesoff>/<str:salesgrp>',getASD,name="getASD"),



#Custer
    path('getCluster/<str:bpcode>',getCluster,name="getCluster"),
    path('getCluster/<str:bpcode>/<int:unit_id>',getCluster,name="getCluster"),
    path('getCluster/<str:bpcode>/<str:unit_code>',getCluster,name="getCluster"),

#SalesDist
    path('getSalesDist/<str:bpcode>',getSalesDist,name="getSalesDist"),
    path('getSalesDist/<str:bpcode>/<int:unit_id>',getSalesDist,name="getSalesDist"),
    path('getSalesDist/<str:bpcode>/<str:unit_code>',getSalesDist,name="getSalesDist"),

#SelesOff

    path('getSalesOff/<str:bpcode>',getSalesOff,name="getSalesOff"),
    path('getSalesOff/<str:bpcode>/<int:unit_id>',getSalesOff,name="getSalesOff"),
    path('getSalesOff/<str:bpcode>/<str:unit_code>',getSalesOff,name="getSalesOff"),


    path('getlast7daysavg/<str:bpcode>/<str:agcode>',getlast7daysavg,name="getlast7daysavg"),

    path('getPricegrp/<str:bpcode>/<int:copies>/<int:unit_id>',getPricegrp,name="getPricegrp"),
    path('getPricegrp/<str:bpcode>/<int:copies>/<str:unit_code>',getPricegrp,name="getPricegrp"),


]
urlpatterns += router.urls