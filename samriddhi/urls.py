"""samriddhi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from config.views import Notification_Read_ID,dashboard_data_IH,user_len,Notification_Read,Notification_List,send_noti,BillConfirm,GetAGChield,Update_PaymentStatus,Profile_Update,WebAPI_Get_SAP_PATH, User_Reg, Verify_OTP,dashboard_data,NoOfCopies_data,EditionList_data,GETIncident_Count,GETAgent_Hirarchy,GetIncidentComments,GetIncidentList,GetIncidentReportCATWISE,GetIncidentReport,CreateIncident,GetIncidentStatusType,GetIncidentCategory,SAPFIPOST,GetAGChield,Update_PaymentStatus,Profile_Update,WebAPI_Get_SAP_PATH, User_Reg, Verify_OTP,dashboard_data,NoOfCopies_data,EditionList_data


from rest_framework.authtoken import views
from config.views import send_push_notification,Bank_List,POSTIDBIUTRSAP,POST_BANK_TRID,POSTIDBIUTR,UpdateIncidentComment,UpdateFeedback,DBUser_Outstanding_Count_KEY,DBUser_Billing_Count_KEY,DBUser_Copies_Count_KEY,Update_PWD,User_Reg_Mob_Forgot,Get_Hint,User_Reg_Mob,Ledger_data,Last_Six_Month_Bill,Last_Seven_Days_Copy,Last_Bill_Month,GETBillPDF,Get_ContactUs,Bill_Month,user_login,User_Profile,DBUser_Copies_Count

from .views import login,forgotpwd,signup,dash,userprofile,signup_data,forgotpwd_get_otp,logout,copies,billing,ledger,order_list,order_list_outstanding,order_list_billing, profile_update_data,csv_download,grievance,grievance_details,grievance_cat_complete


urlpatterns = [
     
    path('', login, name='login'),
    path('admin/', admin.site.urls),
    path('signup',signup,name='signup'),
    path('logout',logout,name='logout'),
    path('signup_data',signup_data,name='signup_data'),
    path('forgotpwd/',forgotpwd,name='forgotpwd'),
    path('forgotpwd_get_otp',forgotpwd_get_otp,name='forgotpwd_get_otp'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dash/',dash,name='dash'),
    path('dash/userprofile/',userprofile,name='userprofile'),

    path('dash/number-copies/',copies,name='copies'),
    path('dash/billing/',billing,name='billing'),
    path('dash/ledger/',ledger,name='ledger'),
    path('dash/order_list_copy/',order_list,name='order_list'),
    path('dash/order_list_outstanding/',order_list_outstanding,name='order_list_outstanding'),
    path('dash/order_list_billing/',order_list_billing,name='order_list_billing'),
    path('dash/csv-download',csv_download,name='csv_download'),

    path('dash/userprofile-update/',profile_update_data,name='profile_update_data'),
    path('dash/grievance/',grievance,name='grievance'),
    path('dash/grievance-details/',grievance_details,name='grievance_details'),
    path('dash/grievance-cat-complete/',grievance_cat_complete,name='grievance_cat_complete'),
    # path('', include('master.urls')),


    
    #
    path('WebAPI_Get_SAP_PATH/<str:client>', WebAPI_Get_SAP_PATH, name="WebAPI_Get_SAP_PATH"),
    path('User_Reg/<str:BPCODE>', User_Reg, name="User_Reg"),
    path('User_Reg_Mob/<str:BPCODE>/<str:BPMOBILE_NO>', User_Reg_Mob, name="User_Reg_Mob"),
    path('User_Reg_Mob_Forgot/<str:BPMOBILE_NO>', User_Reg_Mob_Forgot, name="User_Reg_Mob_Forgot"),
    path('Verify', Verify_OTP, name="Verify_OTP"),
    path('Update_PWD', Update_PWD, name="Update_PWD"),
    path("api-auth/", include('rest_framework.urls')),
    path('user_login', user_login,name="user_login"),
    path('User_Profile/<str:BPCODE>', User_Profile, name="User_Profile"),
    path('dashboard_data/<str:BPCODE>', dashboard_data, name="dashboard_data"),
    path('NoOfCopies_data/<str:BPCODE>/<str:AgType>/<str:fromdt>/<str:todt>/<str:edi>', NoOfCopies_data, name="NoOfCopies_data"),
    path('EditionList_data/<str:BPCODE>', EditionList_data, name="EditionList_data"),
    path('DBUser_Copies_Count/<str:BPCODE>/<str:GrpBy>/<str:fromdt>/<str:todt>', DBUser_Copies_Count, name="DBUser_Copies_Count"),
    path('DBUser_Copies_Count_KEY/<str:BPCODE>/<str:GrpBy>/<str:fromdt>/<str:todt>/<str:Search_Key>', DBUser_Copies_Count_KEY, name="DBUser_Copies_Count_KEY"),
    path('DBUser_Copies_Count_KEY/<str:BPCODE>/<str:GrpBy>/<str:fromdt>/<str:todt>/<str:Search_Key>/<str:Search_Key2>', DBUser_Copies_Count_KEY, name="DBUser_Copies_Count_KEY2"),
    path('DBUser_Copies_Count_KEY/<str:BPCODE>/<str:GrpBy>/<str:fromdt>/<str:todt>/<str:Search_Key>/<str:Search_Key2>/<str:Search_Key3>', DBUser_Copies_Count_KEY, name="DBUser_Copies_Count_KEY3"),
    path('DBUser_Copies_Count_KEY/<str:BPCODE>/<str:GrpBy>/<str:fromdt>/<str:todt>/<str:Search_Key>/<str:Search_Key2>/<str:Search_Key3>/<str:Search_Key4>', DBUser_Copies_Count_KEY, name="DBUser_Copies_Count_KEY4"),
    path('DBUser_Copies_Count_KEY/<str:BPCODE>/<str:GrpBy>/<str:fromdt>/<str:todt>/<str:Search_Key>/<str:Search_Key2>/<str:Search_Key3>/<str:Search_Key4>/<str:Search_Key5>', DBUser_Copies_Count_KEY, name="DBUser_Copies_Count_KEY5"),
    path('Bill_Month/<str:BPCODE>', Bill_Month, name="Bill_Month"),
    path('Get_ContactUs/', Get_ContactUs, name='Get_ContactUs'),
    path('GETBillPDF/<str:Billno>',GETBillPDF,name="GETBillPDF"),
    path('Last_Bill_Month/<str:BPCODE>',Last_Bill_Month,name="Last_Bill_Month"),
    path('Last_Seven_Days_Copy/<str:BPCODE>',Last_Seven_Days_Copy,name="Last_Seven_Days_Copy"),
    path('Last_Six_Month_Bill/<str:BPCODE>',Last_Six_Month_Bill,name="Last_Six_Month_Bill"),
    path('Ledger_data/<str:BPCODE>/<str:fromdt>/<str:todt>/<str:trantype>', Ledger_data, name="Ledger_data"),

    path('Get_Hint/', Get_Hint, name='Get_Hint'),
    path('Get_Hint/<str:Lan>', Get_Hint, name='Get_Hint_Lan'),
    path('Profile_Update', Profile_Update, name="Profile_Update"),

    path('Update_PaymentStatus', Update_PaymentStatus, name="Update_PaymentStatus"),

    path('DBUser_Billing_Count_KEY/<str:BPCODE>/<str:GrpBy>/<str:fromdt>/<str:todt>/<str:Search_Key>', DBUser_Billing_Count_KEY, name="DBUser_Billing_Count_KEY"),
    path('DBUser_Outstanding_Count_KEY/<str:BPCODE>/<str:GrpBy>/<str:Search_Key>', DBUser_Outstanding_Count_KEY, name="DBUser_Outstanding_Count_KEY"),
    path('GetAGChield/<str:BPCODE>', GetAGChield, name="GetAGChield"),

    path('SAPFIPOST/<str:PaymentLog_id>', SAPFIPOST, name="SAPFIPOST"),


    path('GetIncidentCategory/', GetIncidentCategory, name='GetIncidentCategory'),
    path('GetIncidentStatusType/', GetIncidentStatusType, name='GetIncidentStatusType'),
    path('CreateIncident', CreateIncident,name="CreateIncident"),
    path('GetIncidentReport/<str:BPCODE>/<str:CATEGORY_CODE>', GetIncidentReport, name='GetIncidentReport'),
    path('GetIncidentReportCATWISE/<str:BPCODE>/<str:Status_CODE>', GetIncidentReportCATWISE, name='GetIncidentReportCATWISE'),
    path('GetIncidentList/<str:BPCODE>/<str:Status_CODE>/<str:CATEGORY_CODE>', GetIncidentList, name='GetIncidentList'),
    path('GetIncidentComments/<str:Incident_Number>', GetIncidentComments, name='GetIncidentComments'),

    path('UpdateFeedback', UpdateFeedback,name="UpdateFeedback"),
    path('UpdateIncidentComment', UpdateIncidentComment,name="UpdateIncidentComment"),
    path('GETAgent_Hirarchy/<str:BPCODE>', GETAgent_Hirarchy, name="GETAgent_Hirarchy"),


    path('GETIncident_Count/<str:BPCODE>/<str:GrpBy>/<str:Search_Key>', GETIncident_Count, name="GETIncident_Count"),
    path('POSTIDBIUTR', POSTIDBIUTR,name="POSTIDBIUTR"),
    path('BillConfirm', BillConfirm,name="BillConfirm"),
    path('POST_BANK_TRID/<str:Tr_ID>/<str:serverCode>', POST_BANK_TRID, name="POST_BANK_TRID"),
    path('POSTIDBIUTRSAP', POSTIDBIUTRSAP,name="POSTIDBIUTRSAP"),
    path('Bank_List/', Bank_List, name='Bank_List'),
    path('send_push_notification/', send_push_notification, name='send_push_notification'),

    path('send_noti/', send_noti, name='send_noti'),
    path('Notification_List/<str:BP_Code>', Notification_List, name='Notification_List'),
    path('Notification_Read/<str:BP_Code>', Notification_Read, name='Notification_Read'),
    path('user_len/', user_len, name='user_len'),

    path('dashboard_data_IH/<str:BPCODE>', dashboard_data_IH, name="dashboard_data_IH"),
    path('Notification_Read_ID/<str:Nitification_Id>', Notification_Read_ID, name='Notification_Read_ID'),

    # Agency request process
    path('agency/', include('agency.urls')),
    path('rawsap/', include('rawsap.urls')),
    path('misreport/', include('mis.urls')),
]
# urlpatterns += [
#     path('api-token-auth/', views.obtain_auth_token)
# ]