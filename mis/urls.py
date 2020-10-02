from django.urls import path
from . import views
urlpatterns = [
    path('',views.mis_report, name='misreport'),
    path('getUnit/',views.filter_report, name='getUnit'),

]