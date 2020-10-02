from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse, request
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.urls import reverse
from django.contrib.auth import authenticate, login
from config.utils import create_log
from django import forms
from master.models import UserMaster, UserMasterDetails
from config.models import IncidentMaster, IncidentCommentDetail, IncidentFeedbackDetail, IncidentStatusTypeMaster, IncidentCategoryMaster
from logs.models import RegLog, UserLogs, PaymentLog
import sys
from config.models import ServerMaster, SmsManager, SmsLog, ContactUs, Hint
import random
import requests
from master.models import EducationMaster, AccessTypeMaster, UserTypeMaster
from django.contrib.auth.models import auth
from config.views import GETSAP_Dashboard, GETSAP_Dashboard_DBUser, Last_Bill_Month, Last_Seven_Days_Copy, Last_Six_Month_Bill, GETSAP_NoOfCopies, get_outstanding, GETSAP_EditionList, GETSAP_Bill_Month, GETSAP_Ledger,GETSAP_BP_CRM,GETSAP_DBUser_Copies_Count,GETSAP_DBUser_Outstanding_Count,GETSAP_DBUser_Billing_Count,SAP_Profile_POST,GETIncident_Count_Dashboard
from django.contrib import messages
import datetime
import re
from datetime import date, timedelta
from django.core import serializers
import math
import pprint
from django.db import connection
import csv
from django.db.models import Count
from django.urls import resolve
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView


# class ExampleView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, format=None):
#         content = {
#             'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#             'auth': unicode(request.auth),  # None
#         }
#         return Response(content)





def login(request):
    context = {
    'msg':'Error',

    }

    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            userm = UserMaster.objects.filter(username=username)
            usermqq = UserMaster.objects.get(username=username)
            userdetail = UserMasterDetails.objects.filter(usermaster=usermqq)
            data = runSql("select id,access_type_id,mobile_no from usermasterdetails where usermaster_id = "+str(request.user.id))
            request.session['usermasterdetails'] = data[0]
            ul = user_log(request, username, 'Login', 'Login Done') 
            return HttpResponseRedirect(reverse('dash'))
        else:
            error = {
            'msg_error':'!! User  ID or Password is Not Correct !!'
            }
            return render(request,"login.html", error)

    return render(request,"login.html", context)



def signup(request):
    context = {
        'msg':'',


        }

    if request.method == 'POST':
        try:
            data = {}
            
            if request.method == 'POST':
                data = {'Verified': True,
                        'BpCode': request.POST['user'], 'Password': request.POST['password'], 'device_id': 'WEB'}
            if data['Verified'] == True:
                # is_bp = 0
                # is_adalias = 0
                # res = getSAPUserDetail(request, 'PRD')
                # if res:
                #     sapuser = res.server_username  # "DBITMGT"
                #     sappassword = res.server_password  # "Dbitmgt1$"
                #     sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_VERIFY_SRV/AGNconfSet?$format=json&$filter=(Partner eq '%s')" % (
                #         res.server_host, data['BpCode'])
                #     auth_values = (sapuser, sappassword)
                #     response = requests.get(sapurl, auth=auth_values)
                #     appdata = response.json()

                #     if response.status_code == 200:
                #         results = appdata['d']
                #         if len(results) > 0:
                #             fresult = results['results'][0]
                #             mobile_no = fresult["Mobile"]
                #             email = fresult['Email'] if fresult['Email'] else fresult['Partner'] + "@gmail.com"
                #             type = fresult['Type']
                #             partner = fresult['Partner']
                #             request_sent_flag = fresult['ReqsentFlag']
                #             first_name = fresult['Name1']
                #             last_name = fresult['Name2']
                #             active_flag = fresult['ActiveFlag']
                #             device_id = fresult['Deviceid']
                #             device_type = ''

                Usr_reg_sap = GETSAP_REG_DATA(request, data['BpCode'])
                ul = user_log(request, data['BpCode'],
                            'SignUp', 'User Activation Done')
            # sent_otp = mobileotp(request,Usr_reg_sap.Mobile)
                if Usr_reg_sap[0]:

                    fresult = Usr_reg_sap[1]["results"][0]
                    mobile_no = fresult["Mobile"]
                    # fresult['Email'] if fresult['Email'] else
                    email = fresult['Partner'] + "@gmail.com"
                    utype = fresult['Type']
                    partner = fresult['Partner']
                    request_sent_flag = fresult['ReqsentFlag']
                    first_name = fresult['Name1']
                    last_name = fresult['Name2']
                    active_flag = fresult['ActiveFlag']
                    device_id = data['device_id']  # fresult['Deviceid']
                    device_type = ''

                    if utype != '' and utype != None:
                        access_type = AccessTypeMaster.objects.filter(
                            access_type=utype).first()
                    else:
                        access_type = AccessTypeMaster.objects.filter(
                            access_type='AG').first()
                    if utype == 'AG':
                        user_type = UserTypeMaster.objects.filter(
                            user_type='EU').first()
                    else:
                        user_type = UserTypeMaster.objects.filter(
                            user_type='DB').first()

                    uu = UserMaster.objects.filter(
                        username=partner).count()
                    if uu > 0:
                        return JsonResponse({'reply': "user already exist"})
                    else:
                        
                        rs = SAPPOSTROCHAT(partner, device_id, 'X')
                        
                        dct = {
                            "UserMasterDetails": {
                                '_access_type': access_type,
                                '_user_type': user_type,
                                '_mobile': mobile_no,
                            }
                        }
                        res = UserMaster.objects.create_user(first_name=first_name, last_name=last_name,
                                                            email=email,
                                                            username=partner, password=data['Password'], **dct)

                        ul = user_log(request, partner, 'SignUp',
                                    'User Creation Done')
                        if isinstance(res, dict):
                            if res.get('error'):
                                return JsonResponse({"ERROR: ": res.get('error', "Can't create user profile")})
                        reg_log_details = RegLog(PARTNER=partner, adalias=partner,
                                                mobile_no=mobile_no,
                                                reg_device_id=device_id, platform=device_type)
                        reg_log_details.save()
                        create_log({'username': partner, 'log_action': '', 'log_host': '',
                                    'log-ip': '', 'browser_type': '', 'platform': device_type})
                messages.info(request,'Your Account activation request submit successfully, Thanks.!')
                return redirect('/')
            else:
                return JsonResponse({'reply': "Please enter valid OTP"})
        except Exception as e:
            return JsonResponse({"reply: ": str(e)})
    return render(request,"signup.html", context)


def signup_data(request):
    context = {
        'msg':'',


        }

    if request.method == 'POST':
        BPCODE = request.POST['user_id']
        BPMOBILE_NO = request.POST['number_agent']
        uu = UserMaster.objects.filter(username=BPCODE).count()
        if uu > 0:
            return JsonResponse({'data': None, 'reply': "user already exist"})
        else:
            Usr_reg_sap = GETSAP_REG_DATA(request, BPCODE)

        # sent_otp = mobileotp(request,Usr_reg_sap.Mobile)
        if Usr_reg_sap[0]:

            rr = Usr_reg_sap[1]
            if rr['results'][0]['ReqsentFlag'] == 'X':

                if rr['results'][0]['Mobile'] == BPMOBILE_NO:
                    sent_opt = mobileotp(request, rr['results'][0]['Mobile'])
                    return HttpResponse(sent_opt)
                else:
                    ul = user_log(request, BPCODE, 'SignUp','Mobile Number is not matched:'+BPMOBILE_NO)
                    return JsonResponse({'data': None, 'reply': "Mobile Number is not matched."})
            else:
                ul = user_log(request, BPCODE, 'SignUp','You are not authorized to use this application:'+BPMOBILE_NO)
                return JsonResponse({'data': None, 'reply': "!! You are not authorized to use this application !!"})

        else:
            user_veri = GETSAP_USER_MOBILE_VARIFY(request, BPCODE, BPMOBILE_NO)
            if user_veri[0]:
                rr1 = user_veri[1]
                sent_opt = mobileotp(request, BPMOBILE_NO)
                ul = user_log(request, BPCODE, 'SignUp','OPT Sent to:'+BPMOBILE_NO)
                return HttpResponse(sent_opt)
            else:
                ul = user_log(request, BPCODE, 'SignUp',str(user_veri[1])+BPMOBILE_NO)
                return JsonResponse({'data': None, 'reply': user_veri[1]})


    return render(request,"signup_data.html", context)


def forgotpwd_get_otp(request):
    try:
        BPMOBILE_NO = request.POST['number_agent']
        ud = UserMasterDetails.objects.get(mobile_no=BPMOBILE_NO)
        uu = UserMaster.objects.get(username=ud.usermaster)
        if uu:
            sent_opt = mobileotp_FPWD(request, BPMOBILE_NO, uu.username)
            return HttpResponse(sent_opt)
        else:
            ul = user_log(request, BPMOBILE_NO, 'ForgotPwd',
                          'Mobile Number is not matched:'+BPMOBILE_NO)
            return JsonResponse({'data': None, 'reply': "Mobile Number is not matched."})

    except UserMaster.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "Mobile Number Not Found"})
    except UserMasterDetails.DoesNotExist as ex:
        return JsonResponse({'data': None, 'reply': "Mobile Number Not Found"})


def forgotpwd(request):
    try:
        context = {
        'msg':'',


        }
        data = {}
        if request.method == 'POST':

            data = {'Verified': True, 'BpCode': request.POST['user'],
                    'Password': request.POST['password'], 'device_id': 'WEB'}
            if data['Verified'] == True:
                uu = UserMaster.objects.get(username=data['BpCode'])
                if uu:
                    #uu.password = request_data['Password']
                    uu.set_password(data['Password'])
                    uu.save()
                    ul = user_log(
                        request, data['BpCode'], 'UpdatePWD', 'Update Password Done')
                    messages.info(request,'Your Passowrd is Update Successfully.')
                    return redirect('/')
            else:
                return JsonResponse({'reply': "Please enter valid OTP"})
        return render(request,"forgot-password.html", context)
    except Exception as e:
        return JsonResponse({"reply: ": str(e)})


def logout(request):
    try:
        del request.session['usermasterdetails']
    except:
        pass

    auth.logout(request)
    return redirect('/')


def mobileotp_FPWD(request, mbileno, bpcode):
    # if 'userdata' not in request.session:
    #     return HttpResponseRedirect(reverse(''))
    try:
        # mbileno = str(request.GET.get('mbileno', None))
        mbileno = "91" + mbileno
        optval = str(random.randint(1000, 9999))
        # smshost = None
        smsurl = ""
        try:
            smshost = SmsManager.objects.get(sms_for='signup', sms_status='1')
            request.session["mobileOTP"] = optval
            smsval = smshost.sms_body_first + " " + optval + " ." + \
                smshost.sms_body_second + smshost.sms_body_third
            smsurl = "%s&to=%s&text=%s%s" % (
                smshost.sms_host, mbileno, smsval, smshost.sms_from)
        except ServerMaster.DoesNotExist as EX:
            data = {'data': None, 'reply':  str(EX)}
            return JsonResponse(data)
        # return HttpResponse("<script>alert('hi')</script>")
        except Exception as ex:
            # return HttpResponse("<script>alert('hi')</script>")
            data = {'data': None, 'reply':  str(EX)}
            return JsonResponse(data)
        response = requests.get(smsurl)
        smsresponse = response.json()
        smslogobj = SmsLog()
        smslogobj.sms_body = smsval
        smslogobj.sms_from_page = "SignUp Page"
        smslogobj.sms_response = smsresponse
        # smslogobj.sms_send_on
        smslogobj.sms_to = mbileno
        smslogobj.save()

        data = {
            'mobileotpsent': 'T',
            'mobileno': mbileno,
            'otp': optval,
            'Bp_code': bpcode,

        }
        return JsonResponse({'data': data, 'reply': ''})
    except Exception as ex:
        # return HttpResponse(str(ex))
        {'data': None, 'reply':  str(EX)}
        return JsonResponse({'data': data})




def dash(request):
    context = {
        'msg':'',
        

        }
    if request.user.is_authenticated:
        BPCODE = request.user.username

        dash = None
        lastmonth_year = ""
        lastmonth_year_Bill_Amt = ""
        YTDData = ""
        MTDData = ""
        HintCount = ""
        Open_count = 0
        Closed_Count = 0

        try:
            IC = GETIncident_Count_Dashboard(BPCODE)

            IC = json.loads(IC.content)
            Open_count = IC['Open_count']
            Closed_Count = IC['Closed_Count']

            try:
                userm = UserMaster.objects.get(username=BPCODE)
            except UserMaster.DoesNotExist as ex:
                userm = None
                dash_f = GETSAP_Dashboard(request, BPCODE)
                if dash_f[0]:
                    dash = dash_f[1]
                    del dash['__metadata']

                ll = Last_Bill_Month(request, BPCODE)
                ll_j = json.loads(ll.content)
                lastmonth_year = ll_j['lastmonth_year']
                lastmonth_year_Bill_Amt = ll_j['lastmonth_year_Bill_Amt']
                
                ytd = Last_Seven_Days_Copy(request, BPCODE)
                YTDData = json.loads(ytd.content)

                mtd = Last_Six_Month_Bill(request, BPCODE)
                MTDData = json.loads(mtd.content)


            cu = Hint.objects.filter(Hint_Status=1).count()
            HintCount = str(cu)

            if userm:
                # user_type = UserTypeMaster.objects.get(
                #     user_type='EU')
                try:
                    ud = UserMasterDetails.objects.get(usermaster=userm)
                except UserMasterDetails.DoesNotExist as ex:
                    ud = None
                    dash_f = GETSAP_Dashboard(request, BPCODE)
                    if dash_f[0]:
                        dash = dash_f[1]
                        del dash['__metadata']



                if ud:
                    if ud.user_type.user_type == "EU":
                        dash_f = GETSAP_Dashboard(request, BPCODE)
                        if dash_f[0]:
                            dash = dash_f[1]
                            del dash['__metadata']

                    else:
                        dash_f = GETSAP_Dashboard_DBUser(request, BPCODE)
                        if dash_f[0]:
                            dash = dash_f[1]

                            del dash['__metadata']
                            dash_new = {"Partner": BPCODE,
                                        "GrossCopy": dash['PaidCopy'],
                                        "FreeCopy": "",
                                        "PaidCopy": dash['PaidCopy'],
                                        "Zlao": "",
                                        "Zcoo": "",
                                        "OutStd": round(float(float(dash['OutStd'])/100000),2),
                                        "Asd": round(float(float(dash['Asd'])/100000),2)}
                            lastmonth_year_Bill_Amt = round(float(float(dash['Billing'])/100000),2)
                            dash = dash_new
                    ll = Last_Bill_Month(request, BPCODE)
                    ll_j = json.loads(ll.content)
                    lastmonth_year = ll_j['lastmonth_year']
                    if ud.user_type.user_type == "EU":
                        lastmonth_year_Bill_Amt = ll_j['lastmonth_year_Bill_Amt']
                    # else:
                    #     lastmonth_year_Bill_Amt = dash['Billing']


                    ytd = Last_Seven_Days_Copy(request, BPCODE)
                    YTDData = json.loads(ytd.content)

                    mtd = Last_Six_Month_Bill(request, BPCODE)
                    MTDData = json.loads(mtd.content)

                # else:
                #     dash_f = GETSAP_Dashboard(request, BPCODE)


            chart_val = []
            chart_date = []
            for val in MTDData['MTDdata']:
                chart_val.append(val['SoldCopies'])
                x = datetime.datetime(int(val['Gjahr']), int(val['Monat']), 1)
                chart_date.append(x.strftime("%b %Y"))

            lastmonth_year_Bill_Amt = math.ceil(float(lastmonth_year_Bill_Amt))
            dash['OutStd'] = math.ceil(float(dash['OutStd']))
            dash['Asd'] = math.ceil(float(dash['Asd']))
            
            ul = user_log(request, BPCODE, 'Dashboard', 'Dashboard Open')
            context = {'data': dash, 'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt, 'YTDData': YTDData, 'MTDData': MTDData, 'HintCount': HintCount, 'reply': 'User Dashboard Data', 'chart_val':chart_val, 'chart_date':chart_date , "Open_count": Open_count, "Closed_Count": Closed_Count}
            return render(request,"index.html", context)

        except Exception as e:
            ul = user_log(request, BPCODE, 'Dashboard','Dashboard Open with Error')
            context = {'data': None, 'lastmonth_year': lastmonth_year, 'lastmonth_year_Bill_Amt': lastmonth_year_Bill_Amt, 'YTDData': YTDData, 'MTDData': MTDData, 'HintCount': HintCount, "Open_count": Open_count, "Closed_Count": Closed_Count, 'reply': str(e)}
            return render(request,"index.html", context)
    else:
        return redirect('/')


def copies(request):
    if request.user.is_authenticated:
        BPCODE = request.user.username
        try:
            if request.method == 'POST':
                AgType = request.POST['AgType']
                fromdt = request.POST['fromdt']
                todt = request.POST['todt']
                edi = request.POST['edi']
                BPCODE = int(request.POST['BPCODE'])
            else:
                AgType = 'AG'
                fromdt = ''
                todt = ''
                edi = ''
                try:
                    BPCODE = request.GET['s']
                    loc = request.GET['v']
                    path_url = request.META.get('HTTP_REFERER')
                    her = request.session['url_copy']
                    her.append({'name':loc, 'url': path_url})
                    request.session['url_copy'] = her
                    i = 0
                    for h in her:
                        i = i+1
                        if h['name'] == loc:
                            del her[i:len(her)]
                            break

                except Exception as e:
                    BPCODE = request.user.username
                        
            Outstanding = ""
            if AgType == 'AG':
                AgType = 'MA'
            

            dash_f = GETSAP_NoOfCopies(request, BPCODE, AgType, fromdt, todt, edi)
            dash = []
            if dash_f[0]:
                dash = dash_f[1]
            # del dash['__metadata']
                for num in dash['results']:
                    del num['__metadata']
            
            Outstanding = get_outstanding(BPCODE)
            ul = user_log(request, BPCODE, 'Copies', 'Copies Open')
            lis_res = EditionList_data(request,BPCODE)
            items = []
            # pprint.pprint(dash['results'][0])
            i = 0
            for da in dash['results']:
                try:
                    date = datetime.datetime.fromtimestamp(int(da['OrdDate'])).strftime('%Y-%m-%d')
                    try:
                        prev_one_c = int(dash['results'][i-1]['GrossCopy'])
                        if prev_one_c > int(da['GrossCopy']):
                            v1 = {'title':int(da['GrossCopy']), 'start':date, 'textColor': '#ed2324'}
                        else:
                            v1 = {'title':int(da['GrossCopy']), 'start':date}
                    except Exception as e:
                        v1 = {'title':int(da['GrossCopy']), 'start':date}

                    items.append(v1)
                    i = i+1
                except Exception as e:
                    pass

            try:
                lis_res = lis_res['data']['results']
            except Exception as e:
                lis_res = []
                
            res = {'data': items, 'lis_res':lis_res, 'Outstanding': Outstanding, 'reply': 'Number of Copies'}
            
            if request.method == 'POST':
                return JsonResponse({'data':res['data']})
            else:
                return render(request,"copies.html", res)

        except Exception as e:
            ul = user_log(request, BPCODE, 'Copies', 'Copies Open with Error')
            res = {'data': [], 'Outstanding': Outstanding, 'reply': 'Number of Copies'}
            return render(request,"copies.html", res)

    else:
        return redirect('/')


def billing(request):
    if request.user.is_authenticated:
        try:
            try:
                BPCODE = request.GET['s']
            except Exception as e:
                BPCODE = request.user.username
            Outstanding = ""
            usercrm_f = GETSAP_Bill_Month(request, BPCODE)
            usercrm = None
            if usercrm_f[0]:
                usercrm = usercrm_f[1]

            Outstanding = get_outstanding(BPCODE)
            ul = user_log(request, BPCODE, 'Bill_Month',
                        'Show Bill Monthly Report')
            
            for us in usercrm['results']:
                s = us['Gjahr']+'-'+us['Monat']+'-01'
                date = datetime.datetime.strptime(s, "%Y-%m-%d").date()
                date = date.strftime('%b-%Y') 
                us['date'] = date
                us['OpenBal'] =  math.ceil(float(us['OpenBal']))
                us['Payment'] =  math.ceil(float(us['Payment']))
                us['CreditAmount'] =  math.ceil(float(us['CreditAmount']))
                us['NetBilling'] =  math.ceil(float(us['NetBilling'])) 
                us['CloseBal'] =  math.ceil(float(us['CloseBal']))
                
            data = {'data': usercrm, 'Outstanding': Outstanding, 'reply': 'Bill Monthly Report'}
            return render(request,"billing.html", data)

        except Exception as e:
            ul = user_log(request, BPCODE, 'Bill_Month',
                        'Show Bill Monthly Report with Error')
            data = {'data': [], 'Outstanding': Outstanding, 'reply': str(e)}
            return render(request,"billing.html", data)
    else:
        return redirect('/')



def ledger(request):
    if request.user.is_authenticated:
        try:
            try:
                BPCODE = request.GET['s']
            except Exception as e:
                BPCODE = request.user.username
            Outstanding = ""
            AgencyName = ""
            try:
                userm = UserMaster.objects.get(username=BPCODE)
                if userm:
                    AgencyName = userm.first_name
                else:
                    AgencyName = ""
            except UserMaster.DoesNotExist as ex:
                AgencyName = ""
            
            trantype = "*"
            if request.method == 'POST':
                fromdt = request.POST['fromdt']
                todt = request.POST['todt']
                BPCODE = request.POST['BPCODE']
            else:
                fromdt = date.today() - timedelta(days=95)
                fromdt = fromdt.strftime('%Y')
                fromdt = fromdt+"-04-01"
                todt = date.today()

            if not trantype:

                trantype = '*'

            dash_f = GETSAP_Ledger(request, BPCODE, fromdt, todt, trantype)
            dash = []
            if dash_f[0]:
                dash = dash_f[1]
            # del dash['__metadata']
                # for num in dash['results']:
                #     del num['__metadata']
            
            for da in dash['results'][0]['TRNSet']:
                da['Budat'] = datetime.datetime.fromtimestamp(int(da['Budat'])).strftime('%d-%b-%Y')
               #etime.fromtimestamp(int(da['Budat'])).strftime('%d%m%Y')})
                
                
            ul = user_log(request, BPCODE, 'Ledger',
                        'Show Ledger Data for Start Date: ' + str(fromdt) + ' End Date:' + str(todt))
            data = {'data': dash, 'AgencyName': AgencyName, 'reply': 'Ledger Data'}
            if request.method == 'POST':
                return JsonResponse({'data':dash['results'][0]['TRNSet']})
            else:
                return render(request,"ledger.html", data)
        except Exception as e:
            ul = user_log(request, BPCODE, 'Ledger',
                        'Show Ledger Data for Start Date: '+ str(fromdt) + ' End Date:' + str(todt))
            data = {'data': [], 'AgencyName': AgencyName, 'reply': str(e)}
            return render(request,"ledger.html", data)
    else:
        return redirect('/')



def EditionList_data(request,BPCODE):
    try:

        dash_f = GETSAP_EditionList(request, BPCODE)
        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            #del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']
                del num['SoldToParty']
                for num1 in num['NavSubagentSet']['results']:
                    del num1['__metadata']
                for num2 in num['NavEdtnSet']['results']:
                    del num2['__metadata']

        return {'data': dash, 'reply': 'Edition and Sub Agent List'}

    except Exception as e:
        return {'data': None, 'reply': str(e)}



def userprofile(request):
    if request.user.is_authenticated:
        BPCODE = request.user.username
        try:
            userm = UserMaster.objects.filter(username=BPCODE)
            usermqq = UserMaster.objects.get(username=BPCODE)
            # EducationMaster.objects.filter(status='1')
            EducationList = ['Primary', 'Secondary',
                            'Sr. Secondary', 'Graduation', 'Post Graduation']
            userdetail = UserMasterDetails.objects.filter(usermaster=usermqq)
            usercrm_f = GETSAP_BP_CRM(request, BPCODE)
            usercrm = None
            if usercrm_f[0]:
                usercrm = usercrm_f[1]
            ul = user_log(request, BPCODE, 'Profile', 'Show User Profile')

            data = {'data': {'usermaster': serializers.serialize('python', userm), 'userdetail': serializers.serialize('python', userdetail), 'usercrm': usercrm, 'EducationList': EducationList}, 'isedit': True, 'reply': 'User Profile'}
            if data['data']['usercrm']:
                if data['data']['usercrm']['results'][0]['Dob']:
                    data['data']['usercrm']['results'][0]['Dob'] = datetime.datetime.fromtimestamp(int(data['data']['usercrm']['results'][0]['Dob'])).strftime('%d-%b-%Y')

                if data['data']['usercrm']['results'][0]['WIFESet'][0]['Dob']:
                    data['data']['usercrm']['results'][0]['WIFESet'][0]['Dob'] = datetime.datetime.fromtimestamp(int(data['data']['usercrm']['results'][0]['WIFESet'][0]['Dob'])).strftime('%d-%b-%Y')

                if data['data']['usercrm']['results'][0]['MarrAnni']:
                    data['data']['usercrm']['results'][0]['MarrAnni'] = datetime.datetime.fromtimestamp(int(data['data']['usercrm']['results'][0]['MarrAnni'])).strftime('%d-%b-%Y')

                if len(data['data']['usercrm']['results'][0]['KIDSet']) > 0:
                    for kid in data['data']['usercrm']['results'][0]['KIDSet']:
                        kid['Dob'] = datetime.datetime.fromtimestamp(int(kid['Dob'])).strftime('%d-%b-%Y')

                if len(data['data']['usercrm']['results'][0]['SISSet']) > 0:
                    for sis in data['data']['usercrm']['results'][0]['SISSet']:
                        sis['Dob'] = datetime.datetime.fromtimestamp(int(sis['Dob'])).strftime('%d-%b-%Y')

                if len(data['data']['usercrm']['results'][0]['BROSet']) > 0:
                    for bro in data['data']['usercrm']['results'][0]['BROSet']:
                        bro['Dob'] = datetime.datetime.fromtimestamp(int(bro['Dob'])).strftime('%d-%b-%Y')

                if data['data']['usercrm']['results'][0]['FATSet']:
                    data['data']['usercrm']['results'][0]['FATSet'][0]['Dob'] = datetime.datetime.fromtimestamp(int(data['data']['usercrm']['results'][0]['FATSet'][0]['Dob'])).strftime('%d-%b-%Y')

                if data['data']['usercrm']['results'][0]['MOTSet']:
                    data['data']['usercrm']['results'][0]['MOTSet'][0]['Dob'] = datetime.datetime.fromtimestamp(int(data['data']['usercrm']['results'][0]['MOTSet'][0]['Dob'])).strftime('%d-%b-%Y')

            return render(request,"profile.html", data)

        except Exception as e:
            ul = user_log(request, BPCODE, 'Profile',
                        'Show User Profile with Error')
            data = {'data': None, 'isedit': True, 'reply': str(e)}
            return render(request,"profile.html", data)
    else:
        return redirect('/')
	

def profile_update_data(request):
    request_data = json.loads(request.POST['data'])
    post_body = {
        "BpCode": "",
        "BpMob1": "",
        "BpGndr": "",
        "BpEmail": "",
        "MarrAnvi": None,
        "WorkingWithDb": None,
        "Dob": None,
        "MaritalStatus": "",
        "State": "",
        "City": "",
        "Pincode": "",
        "Unit": "",
        "Addr": "",
        "Religion": "",
        "NoChild": "",
        "PolicyNo": "",
        "Aadhar": "",
        "Pan": "",
        "SpName": "",
        "SpDob": None,
        "MotName": "",
        "MotDob": None,
        "FatName": "",
        "FatDob": None,
        "Bro1Name": "",
        "Bro1Dob": None,
        "Bro2Name": "",
        "Bro2Dob": None,
        "Sis1Name": "",
        "Sis1Dob": None,
        "Sis2Name": "",
        "Sis2Dob": None,
        "Kid1Name": "",
        "Kid1Dob": None,
        "Kid1Edu": "",
        "Kid1Gndr": "",
        "Kid2Name": "",
        "Kid2Dob": None,
        "Kid2Edu": "",
        "Kid2Gndr": "",
        "Kid3Name": "",
        "Kid3Dob": None,
        "Kid3Edu": "",
        "Kid3Gndr": "",
        "Kid4Name": "",
        "Kid4Dob": None,
        "Kid4Edu": "",
        "Kid4Gndr": "",
        "Kid5Name": "",
        "Kid5Dob": None,
        "Kid5Edu": "",
        "Kid5Gndr": "",
    }

    try:
        if request.method == 'POST':
            req_usercrm = request_data
            if req_usercrm:
                post_body['BpCode'] = req_usercrm['BpCode']
                post_body['BpMob1'] = req_usercrm['Mobile1']
                # if req_usercrm['Gender'] == "Male"
                # post_body['BpGndr'] = req_usercrm['Gender']
                # post_body['BpEmail'] = req_usercrm['Email']
                if req_usercrm['MarrAnni'] != "":
                    post_body['MarrAnvi'] = "/Date(" + \
                        req_usercrm['MarrAnni']+")/"

                # if req_usercrm['WorkingWithDb'] != "":
                #     post_body['WorkingWithDb'] = "/Date(" + \
                #         req_usercrm['WorkingWithDb']+")/"

                if req_usercrm['Dob'] != "":
                    post_body['Dob'] = "/Date("+req_usercrm['Dob']+")/"

                post_body['MaritalStatus'] = req_usercrm['MaritalStatus']
                post_body['State'] = req_usercrm['State']
                # post_body['City'] = req_usercrm['City']
                post_body['Pincode'] = req_usercrm['Pincode']
                post_body['Unit'] = req_usercrm['Unit']
                post_body['Addr'] = req_usercrm['Addr']
                # post_body['Religion'] = req_usercrm['Religion']
                post_body['NoChild'] = req_usercrm['NoChild']
                # post_body['PolicyNo'] = req_usercrm['PolicyNo']
                post_body['Aadhar'] = req_usercrm['Aadhar']
                post_body['Pan'] = req_usercrm['Pan']

                post_body['SpName'] = req_usercrm['WIFESet'][0]['Name']
                if req_usercrm['WIFESet'][0]['Dob'] != "":
                    post_body['SpDob'] = "/Date(" + \
                        req_usercrm['WIFESet'][0]['Dob']+")/"

                post_body['MotName'] = req_usercrm['MOTSet'][0]['Name']
                if req_usercrm['MOTSet'][0]['Dob'] != "":
                    post_body['MotDob'] = "/Date(" + \
                        req_usercrm['MOTSet'][0]['Dob']+")/"

                post_body['FatName'] = ""
                post_body['FatDob'] = None

                post_body['Bro1Name'] = req_usercrm['BROSet'][0]['Name']
                if req_usercrm['BROSet'][0]['Dob'] != "":
                    post_body['Bro1Dob'] = "/Date(" + \
                        req_usercrm['BROSet'][0]['Dob']+")/"

                post_body['Bro2Name'] = req_usercrm['BROSet'][1]['Name']
                if req_usercrm['BROSet'][1]['Dob'] != "":
                    post_body['Bro2Dob'] = "/Date(" + \
                        req_usercrm['BROSet'][1]['Dob']+")/"

                post_body['Sis1Name'] = req_usercrm['SISSet'][1]['Name']
                if req_usercrm['SISSet'][1]['Dob'] != "":
                    post_body['Sis1Dob'] = "/Date(" + \
                        req_usercrm['SISSet'][1]['Dob']+")/"

                post_body['Sis2Name'] = req_usercrm['SISSet'][1]['Name']
                if req_usercrm['SISSet'][1]['Dob'] != "":
                    post_body['Sis2Dob'] = "/Date(" + \
                        req_usercrm['SISSet'][1]['Dob']+")/"

                if len(req_usercrm['KIDSet']) > 0:

                    post_body['Kid1Name'] = req_usercrm['KIDSet'][0]['Name']
                    if req_usercrm['KIDSet'][0]['Dob'] != "":
                        post_body['Kid1Dob'] = "/Date(" + \
                            req_usercrm['KIDSet'][0]['Dob']+")/"
                    post_body['Kid1Edu'] = req_usercrm['KIDSet'][0]['Education']
                    post_body['Kid1Gndr'] = req_usercrm['KIDSet'][0]['Gender']
                if len(req_usercrm['KIDSet']) > 1:

                    post_body['Kid2Name'] = req_usercrm['KIDSet'][1]['Name']
                    if req_usercrm['KIDSet'][1]['Dob'] != "":
                        post_body['Kid2Dob'] = "/Date(" + \
                            req_usercrm['KIDSet'][1]['Dob']+")/"
                    post_body['Kid2Edu'] = req_usercrm['KIDSet'][1]['Education']
                    post_body['Kid2Gndr'] = req_usercrm['KIDSet'][1]['Gender']

                if len(req_usercrm['KIDSet']) > 2:
                    post_body['Kid3Name'] = req_usercrm['KIDSet'][2]['Name']
                    if req_usercrm['KIDSet'][2]['Dob'] != "":
                        post_body['Kid3Dob'] = "/Date(" + \
                            req_usercrm['KIDSet'][2]['Dob']+")/"
                    post_body['Kid3Edu'] = req_usercrm['KIDSet'][2]['Education']
                    post_body['Kid3Gndr'] = req_usercrm['KIDSet'][2]['Gender']

                if len(req_usercrm['KIDSet']) > 3:
                    post_body['Kid4Name'] = req_usercrm['KIDSet'][3]['Name']
                    if req_usercrm['KIDSet'][3]['Dob'] != "":
                        post_body['Kid4Dob'] = "/Date(" + \
                            req_usercrm['KIDSet'][3]['Dob']+")/"
                    post_body['Kid4Edu'] = req_usercrm['KIDSet'][3]['Education']
                    post_body['Kid4Gndr'] = req_usercrm['KIDSet'][3]['Gender']
                if len(req_usercrm['KIDSet']) > 4:
                    post_body['Kid5Name'] = req_usercrm['KIDSet'][4]['Name']
                    if req_usercrm['KIDSet'][4]['Dob'] != "":
                        post_body['Kid5Dob'] = "/Date(" + \
                            req_usercrm['KIDSet'][4]['Dob']+")/"
                    post_body['Kid5Edu'] = req_usercrm['KIDSet'][4]['Education']
                    post_body['Kid5Gndr'] = req_usercrm['KIDSet'][4]['Gender']
                request.session['post_body'] = post_body
                pprint.pprint(post_body)
                ss = SAP_Profile_POST(request, post_body)
                if ss[0]:
                    ul = user_log(
                        request, post_body['BpCode'], 'Profile', 'Profile update request sent')
                    return JsonResponse({'data': post_body, 'status_code' : 1  , 'reply': 'Profile update request sent succesfully.'})
                else:
                    ul = user_log(
                        request, post_body['BpCode'], 'Profile', 'Profile update request with Error')
                    return JsonResponse({'data': post_body, 'status_code' : 0, 'reply': 'Error on Profile Update'})

    except Exception as e:
        return JsonResponse({'data': [], 'status_code' : 0, 'reply': str(e)})


def order_list(request):
    if request.user.is_authenticated:
        BPCODE = request.user.username
        usermasterdetails = request.session['usermasterdetails']
        try:
            try:
                try:
                    Search_Key = request.GET['s'] if request.GET['s'] else '*'
                except Exception as e:
                    Search_Key = '*'

                try:
                    Search_Key2 = request.GET['s2'] if request.GET['s2'] else '*'
                except Exception as e:
                    Search_Key2 = '*'

                try:
                    Search_Key3 = request.GET['s3'] if request.GET['s3'] else '*'
                except Exception as e:
                    Search_Key3 = '*'

                try:
                    Search_Key4 = request.GET['s4'] if request.GET['s4'] else '*'
                except Exception as e:
                    Search_Key4 = '*'

                try:
                    Search_Key5 = request.GET['s5'] if request.GET['s5'] else '*'
                except Exception as e:
                    Search_Key5 = '*'

                loc = request.GET['v']
                path_url = request.META.get('HTTP_REFERER')

                
                her = request.session['url_copy']
                her.append({'name':loc, 'url': path_url})
                request.session['url_copy'] = her
                i = 0
                for h in her:
                    i = i+1
                    if h['name'] == loc:
                        del her[i:len(her)]
                        break

                if loc == 'State List':
                    GrpBy = 'P'
                if loc == 'Credit/Cash':
                    GrpBy = 'L'
                if loc == 'Sales Org(City)':
                    GrpBy = 'G'
                if loc == 'Unit List':
                    GrpBy = 'G'
                if loc == 'Sales Group':
                    GrpBy = 'D'
                if loc == 'Sales District':
                    GrpBy = 'N'
            except Exception as e:
                s_key = '*'
                if usermasterdetails['access_type_id'] in ['UI','SH','CO']:
                    Search_Key = s_key
                    GrpBy = 'S'
                    request.session['url_copy'] = []


                if usermasterdetails['access_type_id'] in ['CE','UE','UH']:
                    Search_Key = s_key
                    GrpBy = 'L'
                    request.session['url_copy'] = []
                
                if usermasterdetails['access_type_id'] in ['EX']:
                    Search_Key = s_key
                    GrpBy = 'N'
                    request.session['url_copy'] = []


            fromdt = date.today()
            todt = date.today()
            ul = user_log(request, BPCODE, 'Copies', 'Copies Open with Group and Key:'+GrpBy + " " + Search_Key)
            if Search_Key == '*':
                dash_f = GETSAP_DBUser_Copies_Count(
                    request, BPCODE, GrpBy, fromdt, todt)
            else:
                dash_f = GETSAP_DBUser_Copies_Count(
                    request, BPCODE, GrpBy, fromdt, todt,Search_Key,Search_Key2,Search_Key3,Search_Key4,Search_Key5)

            dash = None
            if dash_f[0]:
                dash = dash_f[1]
                #del dash['__metadata']
                for num in dash['results']:
                    del num['__metadata']

                    # for num1 in num['NavSubagentSet']['results']:
                    #     del num1['__metadata']
                    # for num2 in num['NavEdtnSet']['results']:
                    #     del num2['__metadata']
            list_data = []
            if GrpBy == 'S':
                page = "State List"
                for res in dash['results']:
                    set_v = {'name' : res['State'], 'val': res['PaidCopy'], 'id' : res['State']}
                    list_data.append(set_v)
            
            if GrpBy == 'P':
                page = "Credit/Cash"
                for res in dash['results']:
                    set_v = {'name' : res['Dch'], 'val': res['PaidCopy'], 'id' : res['Vtweg']}
                    list_data.append(set_v)
            
            if GrpBy == 'L':
                try:
                    Search_Key2 = request.GET['s2']
                except Exception as e:
                    Search_Key2 = '*'

                s2 = Search_Key2
                if s2 == 'CA':
                    page = "Sales Org(City)"

                elif s2 == 'DA':
                    page = "Sales Org(City)"
                else:
                    page = "Unit List"
                
                for res in dash['results']:
                    set_v = {'name' : res['Location'], 'val': res['PaidCopy'], 'id' : res['Vkorg']}
                    list_data.append(set_v)
            
            if GrpBy == 'G':
                page = "Sales Group"
                for res in dash['results']:
                    set_v = {'name' : res['Sgrp'], 'val': res['PaidCopy'], 'id' : res['Vkgrp']}
                    list_data.append(set_v)

            if GrpBy == 'D':
                page = "Sales District"
                for res in dash['results']:
                    set_v = {'name' : res['SdistName'], 'val': res['PaidCopy'], 'id' : res['Bzirk']}
                    list_data.append(set_v)

            if GrpBy == 'N':
                page = "Agent List"
                for res in dash['results']:
                    set_v = {'name' : res['CustName'], 'val': res['PaidCopy'], 'id' : res['Partner']}
                    list_data.append(set_v)

            #pprint.pprint(list_data)
            
            data = {'data': list_data, 'page':page ,'reply': 'DBUser_Copies_Count'} 
            return render(request,"order_list.html", data)

        except Exception as e:
           data = {'data': [], 'reply': str(e)}
           return render(request,"order_list.html", data)
    else:
        return redirect('/')


def order_list_outstanding(request):
    if request.user.is_authenticated:
        BPCODE = request.user.username
        usermasterdetails = request.session['usermasterdetails']
        try:
            try:
                Search_Key = request.GET['s']
                loc = request.GET['v']
                if loc == 'States':
                    GrpBy = 'C'
                if loc == 'Unit':
                    GrpBy = 'A'
            except Exception as e:
                s_key = '*'
                if usermasterdetails['access_type_id'] in ['UI','SH','CO']:
                    Search_Key = s_key
                    GrpBy = 'S'
                
                if usermasterdetails['access_type_id'] in ['CE','UE','UH']:
                    Search_Key = s_key
                    GrpBy = 'C'
                
                if usermasterdetails['access_type_id'] in ['EX']:
                    Search_Key = s_key
                    GrpBy = 'A'

            ul = user_log(request, BPCODE, 'Outstanding', 'Outstanding Open with Group and Key:'+GrpBy + " " + Search_Key)
            # if Search_Key == '*':
            dash_f = GETSAP_DBUser_Outstanding_Count(request, BPCODE, GrpBy, Search_Key)

            dash = None
            if dash_f[0]:
                dash = dash_f[1]
                #del dash['__metadata']
                for num in dash['results']:
                    del num['__metadata']
                    
                    # for num1 in num['NavSubagentSet']['results']:
                    #     del num1['__metadata']
                    # for num2 in num['NavEdtnSet']['results']:
                    #     del num2['__metadata']

            list_data = []
            if GrpBy == 'S':
                page = "States"
                for res in dash['results']:
                    set_v = {'name' : res['State'], 'val': math.ceil(float(res['OutStd'])), 'id' : ''}
                    list_data.append(set_v)
            
            if GrpBy == 'C':
                page = "Unit"
                for res in dash['results']:
                    set_v = {'name' : res['Location'], 'val': math.ceil(float(res['OutStd'])), 'id' : ''}
                    list_data.append(set_v)
            
            if GrpBy == 'A':
                page = "Agent"
                for res in dash['results']:
                    set_v = {'name' : res['CustName'], 'val': math.ceil(float(res['OutStd'])), 'id' : res['SoldToParty']}
                    list_data.append(set_v)

            data = {'data': list_data, 'page':page ,'reply': 'DBUser_Outstanding_Count'} 
            return render(request,"order_list_outstanding.html", data)

        except Exception as e:
            data = {'data': [], 'reply': str(e)}
            return render(request,"order_list_outstanding.html", data)
    else:
        return redirect('/')


def order_list_billing(request):
    if request.user.is_authenticated:
        BPCODE = request.user.username
        usermasterdetails = request.session['usermasterdetails']
        try:
            try:
                Search_Key = request.GET['s']
                loc = request.GET['v']
                if loc == 'States':
                    GrpBy = 'C'
                if loc == 'Unit':
                    GrpBy = 'A'
            except Exception as e:
                s_key = '*'
                if usermasterdetails['access_type_id'] in ['UI','SH','CO']:
                    Search_Key = s_key
                    GrpBy = 'S'
                
                if usermasterdetails['access_type_id'] in ['CE','UE','UH']:
                    Search_Key = s_key
                    GrpBy = 'C'
                
                if usermasterdetails['access_type_id'] in ['EX']:
                    Search_Key = s_key
                    GrpBy = 'A'

            
            today = date.today()
            first = today.replace(day=1)
            lastdate = first - datetime.timedelta(days=1)
            firstdate = lastdate.replace(day=1)
            fromdt = firstdate
            todt = lastdate

            ul = user_log(request, BPCODE, 'Billing', 'Billing Open with Group and Key:'+GrpBy + " " + Search_Key)
            # if Search_Key == '*':
            dash_f = GETSAP_DBUser_Billing_Count(request, BPCODE, GrpBy, fromdt, todt,Search_Key)

            dash = None
            if dash_f[0]:
                dash = dash_f[1]
                #del dash['__metadata']
                for num in dash['results']:
                    del num['__metadata']

                    # for num1 in num['NavSubagentSet']['results']:
                    #     del num1['__metadata']
                    # for num2 in num['NavEdtnSet']['results']:
                    #     del num2['__metadata']

            list_data = []
            if GrpBy == 'S':
                page = "States"
                for res in dash['results']:
                    set_v = {'name' : res['State'], 'val': math.ceil(float(res['Billing'])), 'id' : ''}
                    list_data.append(set_v)
            
            if GrpBy == 'C':
                page = "Unit"
                for res in dash['results']:
                    set_v = {'name' : res['Location'], 'val': math.ceil(float(res['Billing'])), 'id' : ''}
                    list_data.append(set_v)
            
            if GrpBy == 'A':
                page = "Agent"
                for res in dash['results']:
                    set_v = {'name' : res['CustName'], 'val': math.ceil(float(res['Billing'])), 'id' : res['SoldToParty']}
                    list_data.append(set_v)


            data = {'data': list_data, 'page':page ,'reply': 'DBUser_Billing_Count'} 
            return render(request,"order_list_billing.html", data)

        except Exception as e:
           data = {'data': [], 'reply': str(e)}
           return render(request,"order_list_billing.html", data)
    else:
        return redirect('/')

def basic_name(request, name):
    p = {"name" : name}
    return HttpResponse(json.dumps(p))


def user_log(request, userid, logkey, log_action):
    try:

        ul = UserLogs()
        # userid request.session["userdata"]["Username"]
        ul.username = userid
        ul.log_key = logkey
        ul.log_action = log_action

        # try:
        #     ip = get_client_ip(request)
        # except Exception as ex:
        #     ip = " On Mobile/Tablet"

        # ul.log_ip = ip

        # try:
        #     ul.log_host = request.META['HTTP_HOST']
        # except Exception as ex:
        #     ul.log_host = " On Mobile/Tablet"

        # try:
        #     ul.platform = request.META['HTTP_USER_AGENT']
        # except Exception as ex:
        #     ul.platform = " On Mobile/Tablet"

        # try:
        #     ul.browser_type = request.META['PATH_INFO']
        # except Exception as ex:
        #     ul.browser_type = " On Mobile/Tablet"

        ul.save()
        return (True, 'Log Saved')
    except Exception as ex:
        ul = UserLogs()
        ul.userid = userid
        ul.log_key = logkey
        ul.log_action = "Error on: " + log_action + " " + str(ex)
        ul.save()
        return (False, str(ex))


def GETSAP_REG_DATA(request, BPCODE):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_VERIFY_SRV/AGNconfSet?$format=json&$filter=(Partner eq '%s')" % (
                    res.server_host, BPCODE)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "User not exist in SAP PRC system!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


def getSAPUserDetail(request, server_text_val):

    ss = ServerMaster.objects.get(server_text=server_text_val, server_status=1)
    return ss

def mobileotp(request, mbileno):
    # if 'userdata' not in request.session:
    #     return HttpResponseRedirect(reverse(''))
    try:
        # mbileno = str(request.GET.get('mbileno', None))
        mbileno = "91" + mbileno
        optval = str(random.randint(1000, 9999))
        # smshost = None
        smsurl = ""
        try:
            smshost = SmsManager.objects.get(sms_for='signup', sms_status='1')
            request.session["mobileOTP"] = optval
            smsval = smshost.sms_body_first + " " + optval + " ." + \
                smshost.sms_body_second + smshost.sms_body_third
            smsurl = "%s&to=%s&text=%s%s" % (
                smshost.sms_host, mbileno, smsval, smshost.sms_from)
        except ServerMaster.DoesNotExist as EX:
            data = {'data': None, 'reply':  str(EX)}
            return JsonResponse(data)
        # return HttpResponse("<script>alert('hi')</script>")
        except Exception as ex:
            # return HttpResponse("<script>alert('hi')</script>")
            data = {'data': None, 'reply':  str(EX)}
            return JsonResponse(data)
        response = requests.get(smsurl)
        smsresponse = response.json()
        smslogobj = SmsLog()
        smslogobj.sms_body = smsval
        smslogobj.sms_from_page = "SignUp Page"
        smslogobj.sms_response = smsresponse
        # smslogobj.sms_send_on
        smslogobj.sms_to = mbileno
        smslogobj.save()

        data = {
            'mobileotpsent': 'T',
            'mobileno': mbileno,
            'otp': optval,
        }
        return JsonResponse({'data': data, 'reply': ''})
    except Exception as ex:
        # return HttpResponse(str(ex))
        {'data': None, 'reply':  str(EX)}
        return JsonResponse({'data': data})


def GETSAP_USER_MOBILE_VARIFY(request, BPCODE, MOBILE_NO):
    try:
        try:

            res = getSAPUserDetail(request, 'PRD')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"
                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_AGENT_VRF_SRV/VRFSet?$format=json&$filter=(Partner eq '%s' and Mobile eq '%s')" % (
                    res.server_host, BPCODE, MOBILE_NO)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))

        auth_values = (sapuser, sappassword)
        response = requests.get(sapurl, auth=auth_values)
        appdata = response.json()
        flag = None
        fresult = None

        if response.status_code == 200:
            results = appdata['d']
            if len(results) > 0:
                fresult = results
                flag = True
            else:
                pass

            if flag:
                return (flag, fresult)
            else:
                return (flag, "User not exist in SAP PEC system!!")

        else:

            return (flag, "Agent Code or Mobile Number is invalid")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))

def SAPPOSTROCHAT(Partner=None, Deviceid=None, ActiveFlag=None):
    try:

        sapuser = ''
        sappassword = ''
        sapurl = ''

        try:

            res = ServerMaster.objects.get(
                server_text='PRD', server_status='1')
            if res:
                sapuser = res.server_username  # "DBITMGT"
                sappassword = res.server_password  # "Dbitmgt1$"

                sapurl = "http://%s/sap/opu/odata/SAP/ZVO_SMRD_AGENT_REGISTRATION_SRV/AGN_REGSet" % (
                    res.server_host)

            else:
                return (False, "Runtime Error on server Master: No configration found ")

        except ServerMaster.DoesNotExist as ex:
            return (False, "Runtime Error on server Master: " + str(ex))
        headers = {"content-type": "application/json",
                   "X-Requested-With": "X", "Accept": "application/json"}
        auth_values = (sapuser, sappassword)
        body_json = {
            "Partner": Partner,
            "ActiveFlag": ActiveFlag,
            "Deviceid": Deviceid
        }
        response = requests.post(
            sapurl, auth=auth_values, data=json.dumps(body_json), headers=headers)
        flag = None
        fresult = None
        # if response.status_code == 201:
        appdata = (response.json())['error']['message']
        # else:
        #appdata = {'msg':response.json()}

        if len(appdata) >= 1:
            if response.status_code == "201":
                fresult = appdata['value']
            # else:
                #results = appdata['d']
            # if fresult == "Message Send: Successfully":
                flag = True
            else:
                flag = False

            # if len(results) >0:
            #     fresult = results

            # else:
            #     pass

            if flag:

                return (flag, fresult)
            else:

                return (flag, fresult)

        else:

            return (flag, "No Response Get From SAP!!")
        # return results
    except Exception as ex:
        #  return HttpResponse("Runtime Error: " + str(ex))
        return (False, "Runtime Error: " + str(ex))


def runSql(q):
    cursor = connection.cursor()
    cursor.execute(q)
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def csv_download(request):
    if request.user.is_authenticated:
        BPCODE = '10307'
        usermasterdetails = request.session['usermasterdetails']
        #try: 
        print(date.today())
        Search_Key = '*'
        GrpBy = 'A'
        fromdt = date.today()
        todt = date.today()
        ul = user_log(request, BPCODE, 'Copies', 'Copies Open with Group and Key:'+GrpBy + " " + Search_Key)
        if Search_Key == '*':
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt)
        else:
            dash_f = GETSAP_DBUser_Copies_Count(
                request, BPCODE, GrpBy, fromdt, todt,Search_Key)

        dash = None
        if dash_f[0]:
            dash = dash_f[1]
            #del dash['__metadata']
            for num in dash['results']:
                del num['__metadata']

                # for num1 in num['NavSubagentSet']['results']:
                #     del num1['__metadata']
                # for num2 in num['NavEdtnSet']['results']:
                #     del num2['__metadata']
        list_data = []
        pprint.pprint(dash)
        #for res in dash['results']:
            # set_v = {'name' : res['CustName'], 'val': res['PaidCopy'], 'id' : res['Partner']}
            # list_data.append(set_v)

            #pprint.pprint(list_data)
            
            

        # except Exception as e:
        #    print()
    else:
        return redirect('/')

def grievance(request):
    if request.user.is_authenticated:
        try:
            BPCODE = request.user.username
            try:
                Search_Key = request.GET['s']
            except Exception as e:
                Search_Key = '*'

            try:
                GrpBy = request.GET['g']
            except Exception as e:
                GrpBy = 'S'
            
            inci_count = []

            dash_f = GETSAP_DBUser_Outstanding_Count(
                request, BPCODE, GrpBy, Search_Key)
            Open_count = 0
            Closed_Count = 0
            dash = None
            if dash_f[0]:
                dash = dash_f[1]
                #del dash['__metadata']
                for num in dash['results']:
                    del num['__metadata']
                    inci_data = {'InHouse_Code': BPCODE, 'State': '', 'Vkorg': '', 'SoldToParty': '',
                                'Location': '', 'CustName': '', 'Open_Count': '', 'Closed_Count': ''}
                    Incident_Status_open = IncidentStatusTypeMaster.objects.get(
                        pk=2)
                    Incident_Status_close = IncidentStatusTypeMaster.objects.get(
                        pk=3)
                    if GrpBy == 'S':
                        inci_data['name'] = num['State']
                        inci_data['id'] = num['State']
                        group_next = 'C'
                        page = 'State List'
                        Open_count = IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_open, status=1, Incident_STATE=num['State']).count()
                        Closed_Count = IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_close, status=1, Incident_STATE=num['State']).count()
                    if GrpBy == 'C':
                        group_next = 'A'
                        inci_data['name'] = num['Location']
                        inci_data['id'] = num['Vkorg']
                        page = 'City List'
                        Open_count = IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_open, status=1, Incident_VKORG=num['Vkorg']).count()
                        Closed_Count = IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_close, status=1, Incident_VKORG=num['Vkorg']).count()

                    if GrpBy == 'A':
                        group_next = ''
                        inci_data['name'] = num['CustName']
                        inci_data['id'] = num['SoldToParty']
                        page = 'Agent List'
                        Open_count = IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_open, status=1, Incident_BP_CODE=num['SoldToParty']).count()
                        Closed_Count = IncidentMaster.objects.filter(
                            Incident_Status=Incident_Status_close, status=1, Incident_BP_CODE=num['SoldToParty']).count()

                    inci_data['Open_Count'] = Open_count
                    inci_data['Closed_Count'] = Closed_Count
                    if Open_count == 0 and Closed_Count == 0:
                        pass
                    else:
                        inci_count.append(inci_data)

            data = {'data': {'results': inci_count},'group_next':group_next, 'page':page,'reply': 'GETIncident_Count'}
            # pprint.pprint(data)
            return render(request,"grievance.html", data)

        except Exception as e:
            return render(request,"grievance.html", data)
    else:
        return redirect('/')


def grievance_details(request):
    if request.user.is_authenticated:
        Cat_Inci_List = []
        Cat_Inci_item = {'Incident_category_Code': '',
                        'Incident_category_Text': '', 'Total Incident': ''}
        BPCODE = request.GET['s']
        Status_CODE = request.GET['g']
        try:
            IncidentStatus = None
            if Status_CODE != '*':
                try:

                    IncidentStatus = IncidentStatusTypeMaster.objects.get(
                        pk=Status_CODE)

                except IncidentStatusTypeMaster.DoesNotExist as ex:
                    return JsonResponse({'data': None, 'reply': "No Status Code Found"})

            if Status_CODE == '*':
                Incident_data = IncidentMaster.objects.filter(status=1, Incident_BP_CODE=BPCODE).values(
                    'Incident_Cat').annotate(total=Count('Incident_Number')).order_by('Incident_Cat')
                #Incident_data = IncidentMaster.objects.annotate(total=Count('Incident_Number')).order_by('Incident_Cat')
            else:
                Incident_data = IncidentMaster.objects.filter(status=1, Incident_BP_CODE=BPCODE, Incident_Status=IncidentStatus).values(
                    'Incident_Cat').order_by('Incident_Cat').annotate(count=Count('Incident_Cat'))
                #Incident_data = IncidentMaster.objects.annotate(total=Count('Incident_Number')).order_by('Incident_Cat')

            if Incident_data:
                for inct in Incident_data:
                    cat_code = inct['Incident_Cat']
                    try:

                        IncidentCategory = IncidentCategoryMaster.objects.get(
                            pk=cat_code)
                        cat_text = IncidentCategory.IncidentCategory_Text

                    except IncidentCategoryMaster.DoesNotExist as ex:
                        cat_text = ""

                    Cat_Inci_item = {'BP_Code': BPCODE, 'Status_CODE': Status_CODE, 'Status_Text': IncidentStatus.IncidentStatus_Text,
                                    'Incident_category_Code': inct['Incident_Cat'], 'Incident_category_Text': cat_text, 'Total_Incident': inct['count']}
                    Cat_Inci_List.append(Cat_Inci_item)

                #Incident_data1 = json.dumps(list(Incident_data))
                data = {'data': Cat_Inci_List, 'reply': 'GetIncidentReportCATWISE'}
                pprint.pprint(data)
                return render(request,"grievance_details.html", data)
            else:
                data = {'data': None, 'reply': "No Incident Found"}
                return render(request,"grievance_details.html", data)
        except IncidentMaster.DoesNotExist as ex:
            data = {'data': None, 'reply': "No Incident Found"}
            return render(request,"grievance_details.html", data)

        except Exception as ex:
            data = {'data': None, 'reply': str(ex)}
            return render(request,"grievance_details.html", data)
    else:
        return redirect('/')


def grievance_cat_complete(request):
    if request.user.is_authenticated:
        try:
            IncidentCommentList = []
            IncidentFeedbackList = []
            IncidentStatus = None
            IncidentCategory = None
            BPCODE = request.POST['BPCODE']
            Status_CODE = request.POST['Status_CODE']
            CATEGORY_CODE = request.POST['CATEGORY_CODE']
            if Status_CODE != '*':
                try:

                    IncidentStatus = IncidentStatusTypeMaster.objects.get(
                        pk=Status_CODE)

                except IncidentStatusTypeMaster.DoesNotExist as ex:
                    return JsonResponse({'data': None, 'reply': "No Status Code Found"})

            if CATEGORY_CODE != '*':
                try:

                    IncidentCategory = IncidentCategoryMaster.objects.get(
                        pk=CATEGORY_CODE)

                except IncidentCategoryMaster.DoesNotExist as ex:
                    return JsonResponse({'data': None, 'reply': "No Category Code Found"})

            if Status_CODE == '*':
                if CATEGORY_CODE == '*':
                    Incident_data = IncidentMaster.objects.filter(
                        status=1, Incident_BP_CODE=BPCODE)
                else:
                    Incident_data = IncidentMaster.objects.filter(
                        status=1, Incident_BP_CODE=BPCODE, Incident_Cat=IncidentCategory)
            else:
                if CATEGORY_CODE == '*':
                    Incident_data = IncidentMaster.objects.filter(
                        status=1, Incident_BP_CODE=BPCODE, Incident_Status=IncidentStatus)
                else:
                    Incident_data = IncidentMaster.objects.filter(
                        status=1, Incident_BP_CODE=BPCODE, Incident_Status=IncidentStatus, Incident_Cat=IncidentCategory)

            if Incident_data:

                for incidata in Incident_data:
                    com = incidata.getallcomments()
                    if com:
                        for comdata in com:
                            com_jj = {'Incident_Number': incidata.Incident_Number, 'IncidentComment_Number': comdata.IncidentComment_Number,
                                    'IncidentComment_Text': comdata.IncidentComment_Text, 'IncidentComment_By': comdata.IncidentComment_By, 'IncidentComment_On': comdata.IncidentComment_On}
                            IncidentCommentList.append(com_jj)

                    fed = incidata.getallfeedback()
                    if fed:
                        for feddata in fed:
                            fed_jj = {'Incident_Number': incidata.Incident_Number, 'IncidentFeedback_Number': feddata.IncidentFeedback_Number, 'IncidentFeedback_Rating': feddata.IncidentFeedback_Rating,
                                    'IncidentFeedback_Text': feddata.IncidentFeedback_Text, 'IncidentFeedback_By': feddata.IncidentFeedback_By, 'IncidentFeedback_On': feddata.IncidentFeedback_On}
                            IncidentFeedbackList.append(fed_jj)

                return JsonResponse({'data': {'Incidentlist': serializers.serialize('python', Incident_data, use_natural_foreign_keys=True, use_natural_primary_keys=True), 'Comments': IncidentCommentList, 'Feedback': IncidentFeedbackList}, 'reply': 'GetIncidentList'})
            else:
                return JsonResponse({'data': None, 'reply': "No Incident Found"})

        except IncidentMaster.DoesNotExist as ex:
            return JsonResponse({'data': None, 'reply': "No Incident Found"})

        except Exception as ex:
            return JsonResponse({'data': None, 'reply': str(ex)})
    else:
        return redirect('/')

