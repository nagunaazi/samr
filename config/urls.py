from django.urls import path
from .views import WebAPI_Get_SAP_PATH,User_Reg

urlpatterns = [
    path('WebAPI_Get_SAP_PATH/<str:client>', WebAPI_Get_SAP_PATH, name="WebAPI_Get_SAP_PATH"),
]